from sdl2.surface import SDL_Surface, SDL_FreeSurface, SDL_BlitSurface, SDL_FillRect, SDL_CreateRGBSurface
from sdl2.pixels import SDL_MapRGB
from sdl2.rect import SDL_Rect
from sdl2.error import SDL_GetError

class Surface:
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

    @property
    def width(self):
        return self._surface.contents.w if self._surface else 0

    @property
    def height(self):
        return self._surface.contents.h if self._surface else 0

    def fill(self, color):
        r, g, b = color
        color_val = SDL_MapRGB(self._surface.contents.format, r, g, b)
        SDL_FillRect(self._surface, None, color_val)

    def blit(self, source, dest_pos):
        dst_rect = SDL_Rect(dest_pos[0], dest_pos[1], 0, 0)
        SDL_BlitSurface(source._surface, None, self._surface, dst_rect)

    def free(self):
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