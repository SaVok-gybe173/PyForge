# easel/surface.pxd
from libc.stdint cimport uint32_t, uint8_t

cdef class Surface:
    cdef public object _surface # PySDL2 SDL_Surface (ctypes pointer)
    cdef object        _fmt_ctype # ctypes POINTER(SDL_PixelFormat), cached
    cdef public bint   _owned
    cdef bint          _freed
    cdef uint32_t*     _px # прямой C-указатель на пиксели
    cdef int           _pitch_u32
    cdef int           _w, _h
    cdef uint32_t      _Rmask, _Gmask, _Bmask, _Amask
    cdef uint8_t       _Rshift, _Gshift, _Bshift, _Ashift

    cdef void _check(self) except *
    cpdef void fill(self, color)
    cpdef void blit(self, Surface source, tuple dest_pos)
    cpdef void blit_scaled(self, Surface src, dst_rect)
    cpdef void set_colorkey(self, color)
    cpdef void clear_colorkey(self)
    cpdef void set_alpha(self, alpha)
    cpdef void set_blendmode(self, mode)
    cpdef int  get_blendmode(self)
    cpdef tuple get_at(self, pos)
    cpdef void set_at(self, pos, color)