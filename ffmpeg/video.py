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

        if (isinstance(left_top) is Point): self.left_top = left_top
        else:
            if not isListType(left_top):
                raise ValueError()
            self.left_top = Point(*left_top)

        if (isinstance(width_height) is Point): self.width_height = width_height
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

        self.video = VideoDecoder(container.filepath,
                                fps=container.video_info["fps"],
                                width=self.width_height.pixel[0],
                                height=self.width_height.pixel[1])
        
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


    def start(self):
        self.audio.start()
        self.video.start()
        self.threading.start()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, (0, 0))

    def update(self):
        current_time = self.audio.get_time()
        frame = self.video.get_frame_at_time(current_time)
        if frame is not None:
            print(1)
            self.surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    def stop(self):
        self.video.stop()
        self.audio.stop()

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