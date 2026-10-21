from typing import overload
from sdl2.surface import SDL_Surface
from sdl2.rect import SDL_Rect

class Surface:
    _surface: SDL_Surface

    @overload
    def __init__(self, sdl: SDL_Surface): ...

    @overload
    def __init__(self, sdl: tuple[int, int]): ...

    @property
    def width(self) -> int: ...

    @property
    def height(self) -> int: ...

    def fill(self, color: tuple[int, int, int ]) -> None:
        """
        Заливает всю поверхность цветом (R, G, B).
        """

    def blit(self, source_surface: "Surface", dest_pos: tuple[int, int]) -> None:
        """
        Копирует другую поверхность (source_surface) в позицию dest_pos (x, y).
        """

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

    def set_colorkey(self, color: tuple[int, int, int]) -> None:
        """
        Устанавливает цветовой ключ (цвет, который будет прозрачным). 
        Используйте SDL_SetColorKey
        """

    def set_alpha(self, alpha: int) -> None:
        """
        Устанавливает общую прозрачность поверхности (0–255). Используйте SDL_SetSurfaceAlphaMod.
        """

    def blit_scaled(self, src: "Surface", dst_rect: SDL_Rect) -> None:
        """
        Копирование с масштабированием. Используйте SDL_BlitScaled.
        """

    def get_at(self, pos: tuple[int, int]) -> tuple[int, int, int, int]:
        """
        Прямой доступ к пикселям. 
        Используйте sdl2.ext.PixelView — он позволяет читать и писать через view[y][x].
        """

    def set_at(self, pos: tuple[int, int], color: tuple[int, int, int, int]) -> None:
        """
        Прямой доступ к пикселям. 
        Используйте sdl2.ext.PixelView — он позволяет читать и писать через view[y][x].
        """