from typing import overload
from sdl2.surface import SDL_Surface

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
