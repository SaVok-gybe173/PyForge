from sdl2.surface import (
    SDL_Surface, SDL_BlitScaled, SDL_SetColorKey, SDL_SetSurfaceAlphaMod,
    SDL_FreeSurface, SDL_BlitSurface, SDL_FillRect, SDL_CreateRGBSurface,
    SDL_SetSurfaceBlendMode, SDL_GetSurfaceBlendMode,
    SDL_CreateRGBSurfaceWithFormat
)
from sdl2.pixels import SDL_MapRGB, SDL_GetRGBA, SDL_MapRGBA, SDL_PIXELFORMAT_RGBA32, SDL_PIXELFORMAT_RGB888
from sdl2.rect import SDL_Rect
from sdl2.stdinc import SDL_TRUE
from sdl2.error import SDL_GetError
from sdl2.ext import subsurface, PixelView
from ..base.logger import printInfo, printError
import ctypes

# Маски каналов для 32-битного RGBA (порядок байт: R G B A в little-endian).
_RMASK = 0x00FF0000
_GMASK = 0x0000FF00
_BMASK = 0x000000FF
_AMASK = 0xFF000000

# Флаги поверхности (аналог флагов в pygame при создании Surface)
SRCALPHA = 0x00010000  # поверхность использует альфа-смешивание
PREALLOC = 0x00000001  # поверхность использует предварительно выделенную память
RLEACCEL = 0x00000002  # RLE-ускорение для colorkey

# Режимы смешивания (аналог BLEND_* в pygame)
BLEND_NONE   = 0x00000000  # без смешивания (dst = src)
BLEND_ALPHA  = 0x00000001  # обычное альфа-смешивание (как BLEND_ALPHA)
BLEND_ADD    = 0x00000002  # аддитивное смешивание (как BLEND_ADD / BLEND_RGB_ADD)
BLEND_MOD    = 0x00000004  # мультипликативное смешивание (как BLEND_MULT / BLEND_RGB_MULT)

# Псевдонимы (чтобы было как в pygame)
BLEND_DEFAULT = BLEND_ALPHA
BLEND_MULT    = BLEND_MOD

class Surface:
    _surface: SDL_Surface

    def __init__(self, sdl: SDL_Surface | tuple[int, int], owned: int = True, flags: int = SRCALPHA):
        """
        sdl    — SDL_Surface или (width, height) для создания новой.
        owned  — освобождать ли поверхность в free()/__del__.
        flags  — флаги поверхности (SRCALPHA, PREALLOC и т.д.).
                 Если SRCALPHA не указан — альфа-канал отключён,
                 и Amask будет 0.
        """
        printInfo(f"[{self}] sdl={sdl!r} flags=0x{flags:x}")
        self._surface = None
        self._owned = owned
        self._freed = True

        if sdl is None:
            printError(f"[{self}] SDL_Surface не может быть None")
            raise ValueError("SDL_Surface не может быть None")

        if isinstance(sdl, (tuple, list)):
            w, h = int(sdl[0]), int(sdl[1])

            # SRCALPHA в creation flags не передаём — он приватный
            creation_flags = flags & ~SRCALPHA

            if flags & SRCALPHA:
                pixel_format = SDL_PIXELFORMAT_RGBA32   # с альфа-каналом
            else:
                pixel_format = SDL_PIXELFORMAT_RGB888   # без альфы

            self._surface = SDL_CreateRGBSurfaceWithFormat(
                creation_flags, w, h, 32, pixel_format
            )
        else:
            self._surface = sdl

        if self._surface is None:
            printError(f"[{self}] Не удалось создать поверхность: {SDL_GetError()}")
            raise RuntimeError(f"Не удалось создать поверхность: {SDL_GetError()}")

        self._freed = False
        self._pixel_view = None  # ленивое создание
        if self._surface:
            f = self._surface.contents.format.contents
            printInfo(f"[{self}] created Amask=0x{f.Amask:08x} fmt=0x{f.format:08x}")

    #свойства
    @property
    def width(self) -> int:
        return self._surface.contents.w if self._surface else 0

    @property
    def height(self) -> int:
        return self._surface.contents.h if self._surface else 0

    def get_size(self) -> tuple[int, int]:
        return self.width, self.height

    @property
    def has_alpha(self) -> bool:
        if not self._surface:
            return False
        fmt = self._surface.contents.format
        if fmt and fmt.contents.Amask:
            return True
        return bool(self._surface.contents.flags & SRCALPHA)   # ← fallback

    # заливка/рисование
    def fill(self, color: tuple[int, int, int] | tuple[int, int, int, int]) -> None:
        """
        Залить всю поверхность. Принимает (r,g,b) или (r,g,b,a).
        Для поверхности с альфа-каналом альфа из кортежа учитывается.
        """
        fmt = self._surface.contents.format
        if len(color) >= 4:
            color_val = SDL_MapRGBA(fmt, int(color[0]), int(color[1]), int(color[2]), int(color[3]))
        else:
            color_val = SDL_MapRGB(fmt, int(color[0]), int(color[1]), int(color[2]))
        SDL_FillRect(self._surface, None, color_val)

    def blit(self, source: "Surface", dest_pos: tuple[int, int]) -> None:
        dst_rect = SDL_Rect(int(dest_pos[0]), int(dest_pos[1]), 0, 0)
        SDL_BlitSurface(source._surface, None, self._surface, dst_rect)

    def blit_scaled(self, src: "Surface", dst_rect: SDL_Rect) -> None:
        SDL_BlitScaled(src._surface, None, self._surface, dst_rect)

    # цветовой ключ / альфа
    def set_colorkey(self, color) -> None:
        """Цвет, который станет прозрачным при blit. (r,g,b[,a])."""
        fmt = self._surface.contents.format
        if len(color) >= 4:
            key = SDL_MapRGBA(fmt, int(color[0]), int(color[1]), int(color[2]), int(color[3]))
        else:
            key = SDL_MapRGB(fmt, int(color[0]), int(color[1]), int(color[2]))
        SDL_SetColorKey(self._surface, SDL_TRUE, key)

    def clear_colorkey(self) -> None:
        """Снять цветовой ключ."""
        SDL_SetColorKey(self._surface, 0, 0)

    def set_alpha(self, alpha: int) -> None:
        """Общая прозрачность поверхности 0–255."""
        SDL_SetSurfaceAlphaMod(self._surface, int(alpha))

    # режимы смешивания (как BLEND_* в pygame)
    def set_blendmode(self, mode: int) -> None:
        """
        Установить режим смешивания для blit.
        BLEND_NONE / BLEND_ALPHA / BLEND_ADD / BLEND_MOD.
        """
        SDL_SetSurfaceBlendMode(self._surface, mode)

    def get_blendmode(self) -> int:
        """Получить текущий режим смешивания."""
        mode = ctypes.c_int(0)
        SDL_GetSurfaceBlendMode(self._surface, ctypes.byref(mode))
        return int(mode.value)

    # пиксельный доступ
    def _view(self) -> PixelView:
        if self._pixel_view is None:
            self._pixel_view = PixelView(self._surface)
        return self._pixel_view

    def _pixels(self):
        """Указатель на пиксельные данные поверхности как массив uint32."""
        return ctypes.cast(self._surface.contents.pixels,
                           ctypes.POINTER(ctypes.c_uint32))

    def _pitch_u32(self) -> int:
        """Pitch в единицах uint32 (сколько пикселей в строке с учётом padding)."""
        return self._surface.contents.pitch // 4


    def get_at(self, pos):
        x, y = int(pos[0]), int(pos[1])
        value = self._pixels()[y * self._pitch_u32() + x]
        fmt = self._surface.contents.format
        r, g, b, a = (ctypes.c_uint8() for _ in range(4))
        SDL_GetRGBA(value, fmt,
                    ctypes.byref(r), ctypes.byref(g),
                    ctypes.byref(b), ctypes.byref(a))
        return (r.value, g.value, b.value, a.value)


    def set_at(self, pos, color) -> None:
        x, y = int(pos[0]), int(pos[1])
        fmt = self._surface.contents.format
        if isinstance(color, (tuple, list)):
            if len(color) >= 4:
                value = SDL_MapRGBA(fmt, int(color[0]), int(color[1]),
                                    int(color[2]), int(color[3]))
            else:
                value = SDL_MapRGB(fmt, int(color[0]), int(color[1]), int(color[2]))
        else:
            value = int(color)

        # Прямая запись в память поверхности — тем же способом, что и SDL_FillRect.
        self._pixels()[y * self._pitch_u32() + x] = value

    # жизненный цикл
    def free(self):
        printInfo(f"[{self}] Очистка объекта.")
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
