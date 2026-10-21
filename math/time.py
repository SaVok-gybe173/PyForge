import time
from collections import deque

import sdl2


class Clock:
    """
    Аналог pygame.time.Clock для PySDL2.

    Методы:
        tick(framerate=0) -> int
        tick_busy_loop(framerate=0) -> int
        get_time() -> int
        get_rawtime() -> int
        get_fps() -> float
        reset() -> None
    """

    def __init__(self):
        self._last_time = time.perf_counter()
        self._last_raw_time = 0.0               # время с прошлого tick (без задержки)
        self._fps_buffer = deque(maxlen=10)     # для среднего FPS как в pygame
        self._frame_times = deque(maxlen=10)    # времена кадров

    def _update(self, framerate: float, busy_loop: bool) -> int:
        now = time.perf_counter()
        raw = now - self._last_time
        self._last_time = now

        # Сохраняем для get_fps (pygame считает по последним 10 кадрам)
        self._last_raw_time = raw
        self._frame_times.append(raw)

        avg = sum(self._frame_times) / len(self._frame_times)
        fps = 1.0 / avg if avg > 0 else 0.0
        self._fps_buffer.append(fps)

        if framerate > 0:
            target = 1.0 / framerate
            remaining = target - raw
            if remaining > 0:
                if busy_loop:
                    
                    end = time.perf_counter() + remaining
                    while time.perf_counter() < end:
                        pass
                else:
                    
                    sdl2.SDL_Delay(int(remaining * 1000))
        return int(raw * 1000)


    def tick(self, framerate: float = 0) -> int:
        """Обновляет часы и (опционально) ограничивает FPS через SDL_Delay."""
        return self._update(framerate, busy_loop=False)

    def tick_busy_loop(self, framerate: float = 0) -> int:
        """То же, что tick, но с активным ожиданием (точнее, но грузит CPU)."""
        return self._update(framerate, busy_loop=True)

    def get_time(self) -> int:
        """Время (мс) между двумя последними вызовами tick — включая задержку."""
        # В pygame get_time возвращает время последнего tick без ожидания,
        # фактически == get_rawtime. Оставляем для совместимости.
        return int(self._last_raw_time * 1000)

    def get_rawtime(self) -> int:
        """Время (мс) последнего кадра без учёта искусственной задержки."""
        return int(self._last_raw_time * 1000)

    def get_fps(self) -> float:
        """Средний FPS по последним 10 вызовам tick."""
        if not self._fps_buffer:
            return 0.0
        return sum(self._fps_buffer) / len(self._fps_buffer)

    def reset(self) -> None:
        """Сбрасывает внутренние счётчики."""
        self._last_time = time.perf_counter()
        self._last_raw_time = 0.0
        self._fps_buffer.clear()
        self._frame_times.clear()


class StableClock(Clock):
    def __init__(self):
        super().__init__()
        self._accumulator = 0.0
        self._target_dt = 0.0

    def tick(self, framerate: float = 0) -> int:
        now = time.perf_counter()
        raw = now - self._last_time
        self._last_time = now
        self._last_raw_time = raw

        if framerate > 0:
            if self._target_dt != 1.0 / framerate:
                self._target_dt = 1.0 / framerate
                self._accumulator = 0.0

            self._accumulator += raw
            delay = self._target_dt - self._accumulator

            if delay > 0.002:  # больше 2 мс — можно спать
                sdl2.SDL_Delay(int(delay * 1000))
                self._accumulator += int(delay * 1000) / 1000.0
            else:
                # остаток дожимаем busy-wait (меньше 2 мс)
                end = time.perf_counter() + max(0.0, delay)
                while time.perf_counter() < end:
                    pass
                self._accumulator = 0.0
        return int(raw * 1000)