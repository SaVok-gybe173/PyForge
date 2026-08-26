from .path import get_ffmpeg
from .decoder import (MediaContainer,
                      AudioMaster, VideoDecoder)
from ..markup import Point, Size, isListType
import subprocess
import threading
import pygame

class Streamer:
    "для отправки в сеть"
    def __init__(self, container: MediaContainer, output_url: str):
        self.container = container
        self.output_url = output_url
        self._process = None

    def start_streaming(self):
        # Запускаем FFmpeg как приёмник данных из stdin
        cmd = [
            get_ffmpeg(), "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{self.container.video_info['width']}x{self.container.video_info['height']}",
            "-r", str(self.container.video_info["fps"]),
            "-i", "-",  # видео подаётся в stdin
            "-f", "s16le", "-ar", str(self.container.audio_info["sample_rate"]),
            "-ac", str(self.container.audio_info["channels"]),
            "-i", "-",  # аудио подаётся в stdin
            "-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency",
            "-c:a", "aac", "-f", "flv", self.output_url
        ]
        self._process = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    def write_frame(self, frame_bytes):
        # принимает байты RGB кадра
        if self._process and self._process.stdin:
            self._process.stdin.write(frame_bytes)

    def write_audio(self, audio_bytes):
        if self._process and self._process.stdin:
            self._process.stdin.write(audio_bytes)

    def close(self):
        if self._process:
            self._process.stdin.close()
            self._process.wait()

class Video:
    def __init__(self, container: MediaContainer,
                left_top: tuple[int, int] | Point,
                width_height: tuple[int, int] | Size | None = None):

        """
        Args:
            container (MediaContainer): Контейнер видео
            left_top (tuple[int, int] | Point): Позиция
            width_height (tuple[int, int] | Size | None): Размер
            
        Raise:
            ValueError: Если типы left_top и width_height не совподают
        """

        if (type(left_top) is Point): self.left_top = left_top
        else:
            print(left_top)
            if not isListType(left_top):
                raise ValueError()
            self.left_top = Point(*left_top)

        if width_height is None:
            self.width_height = Point(container.video_info["width"], container.video_info["height"])
        elif (type(width_height) is Point): self.width_height = width_height
        else:
            if width_height is None:
                width_height = container.video_info
            elif not isListType(width_height):
                raise ValueError()
            else:
                self.width_height = Point(*width_height)

        self.container = container
        self.surf = pygame.Surface(self.width_height.pixel)

        self.audio = AudioMaster(sample_rate=container.audio_info["sample_rate"],
                                channels=container.audio_info["channels"])

        self.video = VideoDecoder(
            container.filepath,
            fps=container.video_info["fps"],
            width=container.video_info["width"],   # исходная ширина
            height=container.video_info["height"]  # исходная высота
        )
        self.orig_size = (container.video_info["width"], container.video_info["height"])
        
        def audio_feeder():
            cmd_audio = [get_ffmpeg(), "-i", container.filepath,
                         "-f", "s16le", "-acodec", "pcm_s16le",
                         "-ar", str(container.audio_info["sample_rate"]),
                         "-ac", str(container.audio_info["channels"]),
                         "-vn", "-"]
            proc = subprocess.Popen(cmd_audio, stdout=subprocess.PIPE, bufsize=10**8)
            while True:
                data = proc.stdout.read(4096)
                if not data:
                    break
                self.audio.feed_audio(data)
            proc.wait()
        self.threading = threading.Thread(target=audio_feeder, daemon=True)
        self._paused = False
        self._finished = False

    def start(self):
        self.audio.start()
        self.video.start()
        self.threading.start()
        self._finished = False

    def pause(self):
        self.audio.set_pause(True)
        self._paused = True

    def resume(self):
        self.audio.set_pause(False)
        self._paused = False

    def toggle_pause(self):
        self.audio.toggle_pause()
        self._paused = not self._paused

    def seek(self, time_sec: float):
        """Перемотка на указанную секунду"""
        if time_sec < 0:
            time_sec = 0
        if time_sec > self.container.duration:
            time_sec = self.container.duration

        # Останавливаем текущее воспроизведение (не убивая потоки полностью)
        self.video.stop()
        # Перезапускаем видео-декодер с новым временем
        self.video.seek(time_sec)  # теперь у VideoDecoder есть seek
        
        # Перезапускаем аудио-фидер с новым смещением
        # Для этого надо остановить старый поток и создать новый
        # Пока упрощённо: просто останавливаем и пересоздаём
        self.audio.stop()
        self.audio = AudioMaster(sample_rate=self.container.audio_info["sample_rate"],
                                 channels=self.container.audio_info["channels"])
        self.audio.start()

        # Создаём новый поток для audio_feeder с параметром -ss
        def new_audio_feeder():
            cmd_audio = [get_ffmpeg(), "-ss", str(time_sec), "-i", self.container.filepath,
                         "-f", "s16le", "-acodec", "pcm_s16le",
                         "-ar", str(self.container.audio_info["sample_rate"]),
                         "-ac", str(self.container.audio_info["channels"]),
                         "-vn", "-"]
            proc = subprocess.Popen(cmd_audio, stdout=subprocess.PIPE, bufsize=10**8)
            while True:
                data = proc.stdout.read(4096)
                if not data:
                    break
                self.audio.feed_audio(data)
            proc.wait()
        
        self.threading = threading.Thread(target=new_audio_feeder, daemon=True)
        self.threading.start()

        # Сбрасываем флаги
        self._paused = False
        self._finished = False

    def set_volume(self, volume: float):
        self.audio.set_volume(volume)

    def get_current_time(self) -> float:
        return self.audio.get_time()

    def get_duration(self) -> float:
        return self.container.duration

    def is_paused(self) -> bool:
        return self._paused

    def is_finished(self) -> bool:
        """Проверяет, достигнут ли конец файла"""
        # Если время >= длительность и аудио уже не воспроизводится
        if self.get_current_time() >= self.get_duration():
            # дополнительно проверяем, что буфер аудио пуст и видео-очередь пуста
            if self.audio._buffer and len(self.audio._buffer) == 0:
                return True
        return False

    def update(self):
        """Обновление кадра – вызывается каждый тик главного цикла"""
        if self._finished:
            return
        current_time = self.audio.get_time()
        frame = self.video.get_frame_at_time(current_time)
        if frame is not None:
            self.surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        # Проверяем окончание
        if self.is_finished():
            self._finished = True
            # Можно вызвать коллбэк, если есть

    def stop(self):
        """Полная остановка и освобождение ресурсов"""
        self.video.stop()
        self.audio.stop()
        # Ждём завершения потока audio_feeder (опционально)
        # self.threading.join(timeout=1)

    def close(self):
        """Альтернативное имя для stop"""
        self.stop()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.left_top.pixel)
    
def main():
    video_file = r"ttr.mp4"
    container = MediaContainer(video_file)
    pygame.init()
    screen = pygame.display.set_mode((container.video_info["width"], container.video_info["height"]))

    v = Video(container)
    v.start()
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        v.update()
        v.draw(screen)
        pygame.display.flip()
        pygame.time.wait(60)

    v.stop()
    pygame.quit()

if __name__ == "__main__":
    main()