from typing import Final, overload
from sdl2.surface import SDL_Surface
from sdl2.rect import SDL_Rect

# Флаги поверхности (аналог флагов в pygame при создании Surface)
PREALLOC: Final[int]    # 0x00000001 Поверхность использует предварительно выделенную память.
RLEACCEL: Final[int]    # 0x00000002 RLE-ускорение для цветового ключа (colorkey).
SRCALPHA: Final[int]    # 0x00010000 Поверхность использует альфа-смешивание (включает Amask).


# Режимы смешивания (аналог pygame.BLEND_*)
BLEND_NONE: Final[int]      # 0x00000000 Без смешивания: dst = src.
BLEND_ALPHA: Final[int]     # 0x00000001 Обычное альфа-смешивание.
BLEND_ADD: Final[int]       # 0x00000002 Аддитивное смешивание (свечение).
BLEND_MOD: Final[int]       # 0x00000004 Мультипликативное смешивание (затемнение).
BLEND_DEFAULT: Final[int]   # BLEND_ALPHA Псевдоним режима по умолчанию.
BLEND_MULT: Final[int]      # BLEND_MOD Псевдоним мультипликативного режима (как в pygame).

class Surface:
    _surface: SDL_Surface

    @overload
    def __init__(self, sdl: SDL_Surface, owned: bool = ..., flags: int = ...): ...

    @overload
    def __init__(self, sdl: tuple[int, int], owned: bool = ..., flags: int = ...): ...

    @property
    def width(self) -> int: ...

    @property
    def height(self) -> int: ...

    @property
    def has_alpha(self) -> bool:
        """True, если у поверхности есть альфа-канал (Amask != 0)."""

    def get_size(self) -> tuple[int, int]:
        """Возвращает (width, height)."""

    # заливка/рисование
    def fill(self, color: tuple[int, int, int] | tuple[int, int, int, int]) -> None:
        """
        Заливает всю поверхность цветом (R, G, B) или (R, G, B, A).
        Для поверхности с альфа-каналом альфа из кортежа учитывается.
        """

    def blit(self, source_surface: "Surface", dest_pos: tuple[int, int]) -> None:
        """
        Копирует другую поверхность (source_surface) в позицию dest_pos (x, y).
        """

    def blit_scaled(self, src: "Surface", dst_rect: SDL_Rect) -> None:
        """
        Копирование с масштабированием. Используйте SDL_BlitScaled.
        """

    # цветовой ключ / альфа
    def set_colorkey(self, color: tuple[int, int, int] | tuple[int, int, int, int]) -> None:
        """
        Устанавливает цветовой ключ (цвет, который будет прозрачным).
        Используйте SDL_SetColorKey.
        """

    def clear_colorkey(self) -> None:
        """Снимает цветовой ключ (отключает прозрачность по цвету)."""

    def set_alpha(self, alpha: int) -> None:
        """
        Устанавливает общую прозрачность поверхности (0–255).
        Используйте SDL_SetSurfaceAlphaMod.
        """
    

    # режимы смешивания
    def set_blendmode(self, mode: int) -> None:
        """
        Устанавливает режим смешивания для blit:
        BLEND_NONE / BLEND_ALPHA / BLEND_ADD / BLEND_MOD.
        Используйте SDL_SetSurfaceBlendMode.
        """

    def get_blendmode(self) -> int:
        """Возвращает текущий режим смешивания (одна из констант BLEND_*)."""

    # пиксельный доступ
    def get_at(self, pos: tuple[int, int]) -> tuple[int, int, int, int]:
        """
        Прямой доступ к пикселям.
        Используйте sdl2.ext.PixelView — он позволяет читать и писать через view[y][x].
        Возвращает кортеж (R, G, B, A).
        """

    def set_at(
        self,
        pos: tuple[int, int],
        color: tuple[int, int, int] | tuple[int, int, int, int] | int,
    ) -> None:
        """
        Прямой доступ к пикселям.
        Принимает кортеж (R, G, B) / (R, G, B, A) либо уже смапленное значение (int).
        Используйте sdl2.ext.PixelView — он позволяет читать и писать через view[y][x].
        """

    #  жизненный цикл
    def free(self) -> None:
        """
        Явно освобождает память.
        """

    def __del__(self) -> None:
        """
        Автоматическая очистка при удалении объекта.
        """

    def __enter__(self) -> "Surface": ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...