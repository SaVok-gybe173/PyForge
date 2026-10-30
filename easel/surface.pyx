# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
# cython: nonecheck=False

from libc.stdint cimport uint32_t, uint8_t, uintptr_t
import ctypes
from ctypes import c_int, byref

import sdl2
import sdl2.surface as sdl2_surface
import sdl2.pixels  as sdl2_pixels
import sdl2.rect    as sdl2_rect

from ..base.logger import printInfo, printError


SRCALPHA      = 0x00010000
PREALLOC      = 0x00000001
RLEACCEL      = 0x00000002
BLEND_NONE    = 0x00000000
BLEND_ALPHA   = 0x00000001
BLEND_ADD     = 0x00000002
BLEND_MOD     = 0x00000004
BLEND_DEFAULT = BLEND_ALPHA
BLEND_MULT    = BLEND_MOD


cdef class Surface:
    cdef public object _surface      # PySDL2 SDL_Surface (ctypes pointer)
    cdef object    _fmt_ctype    # ctypes POINTER(SDL_PixelFormat), cached
    cdef public bint      _owned
    cdef bint      _freed
    cdef uint32_t* _px           # прямой C-указатель на пиксели
    cdef int       _pitch_u32
    cdef int       _w, _h
    cdef uint32_t  _Rmask, _Gmask, _Bmask, _Amask
    cdef uint8_t   _Rshift, _Gshift, _Bshift, _Ashift

    def __cinit__(self, *args, **kwargs):
        self._surface   = None
        self._fmt_ctype = None
        self._px        = NULL
        self._pitch_u32 = 0
        self._w = self._h = 0
        self._owned = True
        self._freed = True

    def __init__(self, sdl, owned=True, flags=SRCALPHA):
        self._owned = bool(owned)

        if sdl is None:
            raise ValueError("SDL_Surface не может быть None")

        if isinstance(sdl, (tuple, list)):
            w = int(sdl[0]); h = int(sdl[1])
            creation_flags = flags & ~SRCALPHA
            fmt_enum = (sdl2_pixels.SDL_PIXELFORMAT_RGBA32 if (flags & SRCALPHA)
                        else sdl2_pixels.SDL_PIXELFORMAT_RGB888)
            self._surface = sdl2_surface.SDL_CreateRGBSurfaceWithFormat(
                creation_flags, w, h, 32, fmt_enum)
            self._owned = True
        elif isinstance(sdl, Surface):
            self._surface = (<Surface>sdl)._surface
            self._owned = False
        else:
            self._surface = sdl          # PySDL2-объект

        if self._surface is None:
            raise RuntimeError(f"Не удалось создать поверхность: {sdl2.SDL_GetError().decode()}")

        # --- кэшируем всё, что нужно для быстрого пиксельного доступа ---
        self._freed = False
        cdef object cont = self._surface.contents
        self._w = cont.w
        self._h = cont.h
        self._pitch_u32 = cont.pitch // 4
        self._fmt_ctype = cont.format

        # сырой C-указатель на пиксели (одна ctypes-операция за всю жизнь объекта)
        cdef uintptr_t addr = 0
        if cont.pixels:
            addr = <uintptr_t>cont.pixels
        self._px = <uint32_t*>addr

        # маски/сдвиги каналов
        cdef object fmt = cont.format.contents
        self._Rmask  = fmt.Rmask
        self._Gmask  = fmt.Gmask
        self._Bmask  = fmt.Bmask
        self._Amask  = fmt.Amask
        self._Rshift = fmt.Rshift
        self._Gshift = fmt.Gshift
        self._Bshift = fmt.Bshift
        self._Ashift = fmt.Ashift

    # свойства
    @property
    def width(self):
        return self._w if not self._freed else 0

    @property
    def height(self):
        return self._h if not self._freed else 0

    def get_size(self):
        return (self.width, self.height)

    @property
    def has_alpha(self):
        if self._freed:
            return False
        if self._Amask:
            return True
        return bool(self._surface.contents.flags & SRCALPHA)

    @property
    def pointer(self):
        return ctypes.cast(self._surface, ctypes.c_void_p).value

    cdef inline void _check(self) except *:
        if self._freed or self._surface is None:
            raise RuntimeError("Surface освобождена")

    # рисование
    cpdef void fill(self, color):
        self._check()
        cdef uint32_t c
        if isinstance(color, (tuple, list)):
            if len(color) >= 4:
                c = sdl2_pixels.SDL_MapRGBA(self._fmt_ctype,
                    int(color[0]), int(color[1]), int(color[2]), int(color[3]))
            else:
                c = sdl2_pixels.SDL_MapRGB(self._fmt_ctype,
                    int(color[0]), int(color[1]), int(color[2]))
        else:
            c = <uint32_t>int(color)
        sdl2_surface.SDL_FillRect(self._surface, None, c)

    cpdef void blit(self, Surface source, tuple dest_pos):
        self._check()
        source._check()
        cdef object rect = sdl2_rect.SDL_Rect(
            int(dest_pos[0]), int(dest_pos[1]), 0, 0)
        sdl2_surface.SDL_BlitSurface(source._surface, None, self._surface, rect)

    cpdef void blit_scaled(self, Surface src, dst_rect):
        self._check()
        src._check()
        cdef object rect
        if isinstance(dst_rect, (tuple, list)):
            rect = sdl2_rect.SDL_Rect(
                int(dst_rect[0]), int(dst_rect[1]),
                int(dst_rect[2]), int(dst_rect[3]))
        else:
            rect = dst_rect
        sdl2_surface.SDL_BlitScaled(src._surface, None, self._surface, rect)

    # colorkey / alpha
    cpdef void set_colorkey(self, color):
        self._check()
        cdef uint32_t key
        if isinstance(color, (tuple, list)):
            if len(color) >= 4:
                key = sdl2_pixels.SDL_MapRGBA(self._fmt_ctype,
                    int(color[0]), int(color[1]), int(color[2]), int(color[3]))
            else:
                key = sdl2_pixels.SDL_MapRGB(self._fmt_ctype,
                    int(color[0]), int(color[1]), int(color[2]))
        else:
            key = <uint32_t>int(color)
        sdl2_surface.SDL_SetColorKey(self._surface, 1, key)

    cpdef void clear_colorkey(self):
        self._check()
        sdl2_surface.SDL_SetColorKey(self._surface, 0, 0)

    cpdef void set_alpha(self, alpha):
        self._check()
        sdl2_surface.SDL_SetSurfaceAlphaMod(self._surface, int(alpha))

    # blend modes
    cpdef void set_blendmode(self, mode):
        self._check()
        sdl2_surface.SDL_SetSurfaceBlendMode(self._surface, int(mode))

    cpdef int get_blendmode(self):
        self._check()
        cdef object m = c_int(0)
        sdl2_surface.SDL_GetSurfaceBlendMode(self._surface, byref(m))
        return m.value

    # пиксельный доступ (быстрый путь, без ctypes-разыменований)
    cpdef tuple get_at(self, pos):
        self._check()
        cdef int x = <int>pos[0]
        cdef int y = <int>pos[1]
        if x < 0 or x >= self._w or y < 0 or y >= self._h:
            raise IndexError("pixel index out of range")
        cdef uint32_t v = self._px[y * self._pitch_u32 + x]
        cdef uint8_t r = <uint8_t>((v & self._Rmask) >> self._Rshift)
        cdef uint8_t g = <uint8_t>((v & self._Gmask) >> self._Gshift)
        cdef uint8_t b = <uint8_t>((v & self._Bmask) >> self._Bshift)
        cdef uint8_t a
        if self._Amask:
            a = <uint8_t>((v & self._Amask) >> self._Ashift)
        else:
            a = 255
        return (r, g, b, a)

    cpdef void set_at(self, pos, color):
        self._check()
        cdef int x = <int>pos[0]
        cdef int y = <int>pos[1]
        if x < 0 or x >= self._w or y < 0 or y >= self._h:
            raise IndexError("pixel index out of range")

        cdef uint32_t v = 0
        if isinstance(color, (tuple, list)):
            v  = (<uint32_t>int(color[0]) << self._Rshift) & self._Rmask
            v |= (<uint32_t>int(color[1]) << self._Gshift) & self._Gmask
            v |= (<uint32_t>int(color[2]) << self._Bshift) & self._Bmask
            if self._Amask:
                if len(color) >= 4:
                    v |= (<uint32_t>int(color[3]) << self._Ashift) & self._Amask
                else:
                    v |= (<uint32_t>0xFF << self._Ashift) & self._Amask
        else:
            v = <uint32_t>int(color)
        self._px[y * self._pitch_u32 + x] = v

    # жизненный цикл
    def free(self):
        if self._owned and not self._freed and self._surface is not None:
            sdl2_surface.SDL_FreeSurface(self._surface)
        self._surface = None
        self._fmt_ctype = None
        self._px = NULL
        self._freed = True

    def __dealloc__(self):
        if self._owned and not self._freed and self._surface is not None:
            sdl2_surface.SDL_FreeSurface(self._surface)
            self._surface = None

    def __enter__(self):  return self
    def __exit__(self, *a): self.free()