from sdl2.surface import SDL_Surface, SDL_BlitScaled, SDL_SetColorKey,  SDL_SetSurfaceAlphaMod, SDL_FreeSurface, SDL_BlitSurface, SDL_FillRect, SDL_CreateRGBSurface
from sdl2.pixels import SDL_MapRGB, SDL_GetRGBA
from sdl2.rect import SDL_Rect
from sdl2.stdinc import SDL_TRUE
from sdl2.error import SDL_GetError
from sdl2.ext import subsurface, PixelView
import ctypes, sdl2

class Surface:
    _surface: SDL_Surface

    def __init__(self, sdl, owned=True):
        self._surface = None
        self._owned = owned
        self._freed = True

        if sdl is None:
            raise ValueError("SDL_Surface не может быть None")

        if isinstance(sdl, (tuple, list)):
            self._surface = SDL_CreateRGBSurface(
                0, sdl[0], sdl[1], 32,
                0, 0, 0, 0,
            )
        else:
            self._surface = sdl

        if self._surface is None:
            raise RuntimeError(f"Не удалось создать поверхность: {SDL_GetError()}")

        self._freed = False
        self._pixel_view = None    # ленивое создание

    @property
    def width(self):
        return self._surface.contents.w if self._surface else 0

    @property
    def height(self):
        return self._surface.contents.h if self._surface else 0

    def fill(self, color):
        color_val = SDL_MapRGB(self._surface.contents.format, *color)
        SDL_FillRect(self._surface, None, color_val)

    def blit(self, source, dest_pos: tuple[int, int]):
        dst_rect = SDL_Rect(dest_pos[0], dest_pos[1], 0, 0)
        SDL_BlitSurface(source._surface, None, self._surface, dst_rect)

    def free(self):
        self._pixel_view = None
        if self._owned and not self._freed and self._surface is not None:
            SDL_FreeSurface(self._surface)
            self._surface = None
            self._freed = True

    def __del__(self):
        try:
            self.free()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.free()

    def set_colorkey(self, color: tuple[int, int, int]) -> None:
        """
        Устанавливает цветовой ключ (цвет, который будет прозрачным). 
        Используйте SDL_SetColorKey
        """
        key = SDL_MapRGB(self._surface.contents.format, *color)
        SDL_SetColorKey(self._surface, SDL_TRUE, key)

    def set_alpha(self, alpha):
        """
        Устанавливает общую прозрачность поверхности (0–255). Используйте SDL_SetSurfaceAlphaMod.
        """
        SDL_SetSurfaceAlphaMod(self._surface, alpha)

    def blit_scaled(self, src: "Surface", dst_rect: SDL_Rect) -> None:
        """
        Копирование с масштабированием. Используйте SDL_BlitScaled.
        """
        SDL_BlitScaled(src._surface, None, self._surface, dst_rect)

    def _view(self):
        if self._pixel_view is None:
            self._pixel_view = PixelView(self._surface)
        return self._pixel_view

    def get_at(self, pos):
        pixel = self._view()[pos[1]][pos[0]]
        # Распаковка в (r, g, b, a)
        fmt = self._surface.contents.format
        r, g, b, a = (ctypes.c_uint8() for _ in range(4))
        sdl2.SDL_GetRGBA(pixel, fmt, ctypes.byref(r), ctypes.byref(g),
                         ctypes.byref(b), ctypes.byref(a))
        return (r.value, g.value, b.value, a.value)

    def set_at(self, pos, color):
        self._view()[pos[1]][pos[0]] = color

    def get_size(self) -> tuple[int, int]:
        return self.width, self.height