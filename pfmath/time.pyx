# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False

import sdl2


cdef extern from *:
    """
    #if defined(_WIN32)
    #include <windows.h>
    static double __cy_clock_now(void) {
        static LARGE_INTEGER freq;
        static int init = 0;
        LARGE_INTEGER c;
        if (!init) { QueryPerformanceFrequency(&freq); init = 1; }
        QueryPerformanceCounter(&c);
        return (double)c.QuadPart / (double)freq.QuadPart;
    }
    #else
    #include <time.h>
    static double __cy_clock_now(void) {
        struct timespec ts;
        clock_gettime(CLOCK_MONOTONIC, &ts);
        return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
    }
    #endif
    """
    double __cy_clock_now() nogil


cdef class Clock:
    cdef:
        double _last_time
        double _last_raw_time

        # кольцевые буферы на 10 элементов (аналог deque(maxlen=10))
        double _frame_times[10]
        int    _frame_count
        int    _frame_head

        double _fps_buffer[10]
        int    _fps_count
        int    _fps_head

    def __cinit__(self):
        self._last_time     = __cy_clock_now()
        self._last_raw_time = 0.0
        self._frame_count   = 0
        self._frame_head    = 0
        self._fps_count     = 0
        self._fps_head      = 0

    cdef int _update(self, double framerate, bint busy_loop) except -1:
        cdef double now, raw, total, avg, fps
        cdef double target, remaining, end
        cdef int i

        now = __cy_clock_now()
        raw = now - self._last_time
        self._last_time     = now
        self._last_raw_time = raw

        self._frame_times[self._frame_head] = raw
        self._frame_head = (self._frame_head + 1) % 10
        if self._frame_count < 10:
            self._frame_count += 1

        total = 0.0
        for i in range(self._frame_count):
            total += self._frame_times[i]
        avg = total / self._frame_count
        fps = 1.0 / avg if avg > 0.0 else 0.0

        self._fps_buffer[self._fps_head] = fps
        self._fps_head = (self._fps_head + 1) % 10
        if self._fps_count < 10:
            self._fps_count += 1


        if framerate > 0.0:
            target    = 1.0 / framerate
            remaining = target - raw
            if remaining > 0.0:
                if busy_loop:

                    end = __cy_clock_now() + remaining
                    while __cy_clock_now() < end:
                        pass
                else:
                    sdl2.SDL_Delay(<unsigned int>(remaining * 1000.0))

        return <int>(raw * 1000.0)

    cpdef int tick(self, double framerate=0):
        """Обновляет часы и (опционально) ограничивает FPS через SDL_Delay."""
        return self._update(framerate, False)

    cpdef int tick_busy_loop(self, double framerate=0):
        """То же, что tick, но с активным ожиданием (точнее, но грузит CPU)."""
        return self._update(framerate, True)

    cpdef int get_time(self):
        """Время (мс) между двумя последними вызовами tick."""
        return <int>(self._last_raw_time * 1000.0)

    cpdef int get_rawtime(self):
        """Время (мс) последнего кадра без учёта искусственной задержки."""
        return <int>(self._last_raw_time * 1000.0)

    cpdef double get_fps(self):
        """Средний FPS по последним 10 вызовам tick."""
        cdef double total
        cdef int i

        if self._fps_count == 0:
            return 0.0
        total = 0.0
        for i in range(self._fps_count):
            total += self._fps_buffer[i]
        return total / self._fps_count

    cpdef void reset(self):
        """Сбрасывает внутренние счётчики."""
        self._last_time     = __cy_clock_now()
        self._last_raw_time = 0.0
        self._frame_count   = 0
        self._frame_head    = 0
        self._fps_count     = 0
        self._fps_head      = 0


cdef class StableClock(Clock):
    cdef:
        double _accumulator
        double _target_dt

    def __cinit__(self):
        self._accumulator = 0.0
        self._target_dt   = 0.0

    cpdef int tick(self, double framerate=0):
        cdef double now, raw, target, delay, end
        cdef int ms

        now = __cy_clock_now()
        raw = now - self._last_time
        self._last_time     = now
        self._last_raw_time = raw

        if framerate > 0.0:
            target = 1.0 / framerate
            if self._target_dt != target:
                self._target_dt   = target
                self._accumulator = 0.0

            self._accumulator += raw
            delay = self._target_dt - self._accumulator

            if delay > 0.002:  
                ms = <int>(delay * 1000.0)
                sdl2.SDL_Delay(<unsigned int>ms)
                self._accumulator += ms / 1000.0
            else:
                end = __cy_clock_now() + (delay if delay > 0.0 else 0.0)
                while __cy_clock_now() < end:
                    pass
                self._accumulator = 0.0

        return <int>(raw * 1000.0)