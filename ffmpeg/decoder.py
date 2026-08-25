from collections import deque
from .path import get_ffmpeg, get_ffprobe
import subprocess
import threading
import numpy as np
import json
import queue
import pyaudio
import pygame


class MediaContainer:
    "умный контейнер"
    def __init__(self, filepath):
        self.filepath = filepath
        self.video_info = {}
        self.audio_info = {}
        self._probe()

    def _probe(self):
        # Получаем информацию через ffprobe
        cmd = [
            get_ffprobe(), "-v", "quiet", "-print_format", "json",
            "-show_streams", self.filepath
        ]
        result = subprocess.check_output(cmd)
        data = json.loads(result)
        for stream in data["streams"]:
            if stream["codec_type"] == "video":
                self.video_info = {
                    "width": int(stream["width"]),
                    "height": int(stream["height"]),
                    "fps": eval(stream["r_frame_rate"])  # может быть дробью
                }
            elif stream["codec_type"] == "audio":
                self.audio_info = {
                    "sample_rate": int(stream["sample_rate"]),
                    "channels": int(stream["channels"])
                }

class AudioMaster:
    "дирижёр времени"
    def __init__(self, sample_rate=44100, channels=2):
        self.sample_rate = sample_rate
        self.channels = channels
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.audio_time = 0.0  # текущая позиция в секундах
        self._lock = threading.Lock()
        self._running = False
        self._buffer = []
        self._chunk_size = 1024

    def start(self):
        self._running = True
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            output=True,
            frames_per_buffer=self._chunk_size,
            stream_callback=self._callback
        )
        self.stream.start_stream()

    def _callback(self, in_data, frame_count, time_info, status):
        # Здесь мы должны выдавать следующий кусок PCM-данных
        # и обновлять audio_time на длительность этого куска
        if not self._running:
            return (None, pyaudio.paComplete)
        # Если буфер пуст – выдаём тишину и не двигаем время
        if not self._buffer:
            data = np.zeros(frame_count * self.channels, dtype=np.int16).tobytes()
            return (data, pyaudio.paContinue)
        # Берём первый кусок из буфера
        chunk = self._buffer.pop(0)
        # Вычисляем длительность этого куска в секундах
        duration = len(chunk) / (self.sample_rate * self.channels * 2)  # 2 байта на сэмпл
        with self._lock:
            self.audio_time += duration
        return (chunk, pyaudio.paContinue)

    def feed_audio(self, pcm_bytes):
        # Добавляем PCM-данные в буфер (байты, s16le)
        self._buffer.append(pcm_bytes)

    def get_time(self):
        with self._lock:
            return self.audio_time

    def stop(self):
        self._running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

class VideoDecoder:
    "поставщик видеокадров"
    def __init__(self, filepath: str, fps: int | float, width: int, height: int):
        self.filepath = filepath
        self.fps = fps
        self.width = width
        self.height = height
        self.frame_duration = 1.0 / fps
        self._process = None
        self._frame_queue = queue.Queue(maxsize=30)  # храним (frame_index, numpy_array)
        self._running = False
        self._thread = None

    def start(self):
        cmd = [
            get_ffmpeg(), "-i", self.filepath,
            "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-vsync", "0", "-an", "-"
        ]
        self._process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)
        self._running = True
        self._thread = threading.Thread(target=self._reader)
        self._thread.start()

    def _reader(self):
        frame_size = self.width * self.height * 3
        frame_index = 0
        while self._running:
            raw = self._process.stdout.read(frame_size)
            if not raw:
                break
            frame = np.frombuffer(raw, dtype=np.uint8).reshape((self.height, self.width, 3))
            self._frame_queue.put((frame_index, frame))
            frame_index += 1

    def get_frame_at_time(self, time_sec):
        # Возвращает кадр, соответствующий времени time_sec, и его индекс
        # Если такого кадра нет, возвращает ближайший предыдущий, или None
        # Реализация: проверяем очередь, извлекаем все кадры, чей индекс * frame_duration <= time_sec
        # и запоминаем последний подходящий.
        latest = None
        while not self._frame_queue.empty():
            idx, frame = self._frame_queue.queue[0]  # смотрим без извлечения
            if idx * self.frame_duration <= time_sec:
                # Этот кадр уже должен быть показан, извлекаем его
                _, f = self._frame_queue.get()
                latest = f
            else:
                break
        return latest

    def stop(self):
        self._running = False
        if self._process:
            self._process.kill()
        if self._thread:
            self._thread.join()

class AudioDecoder:
    "альтернативный способ воспроизведения"
    def __init__(self, container, chunk_size=4096):
        self.container = container
        self.sample_rate = container.audio_info["sample_rate"]
        self.channels = container.audio_info["channels"]
        self.chunk_size = chunk_size
        self._process = None
        self._running = False
        self._thread = None

    def start(self):
        cmd = [
            get_ffmpeg(), "-i", self.container.filepath,
            "-f", "s16le", "-acodec", "pcm_s16le",
            "-ar", str(self.sample_rate), "-ac", str(self.channels),
            "-vn", "-"
        ]
        self._process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)
        self._running = True
        self._thread = threading.Thread(target=self._player_loop)
        self._thread.start()

    def _player_loop(self):
        # используем pygame.mixer (инициализирован заранее)
        pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=self.channels)
        while self._running:
            raw = self._process.stdout.read(self.chunk_size)
            if not raw:
                break
            sound = pygame.sndarray.make_sound(
                np.frombuffer(raw, dtype=np.int16).reshape(-1, self.channels)
            )
            sound.play()
            # ждём окончания воспроизведения этого чанка
            while pygame.mixer.get_busy():
                pygame.time.wait(10)

    def stop(self):
        self._running = False
        if self._process:
            self._process.kill()
        if self._thread:
            self._thread.join()

