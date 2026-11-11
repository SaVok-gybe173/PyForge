from .structure import CoreListOfItemsBase
from ....pfmath.rect import Rect
from ....easel.draw import rect
from ....easel.surface import Surface
from ....easel.object import PfObjectIMG

class CoreListOfItemsDown(CoreListOfItemsBase):
    """Список сверху вниз. Полоса прокрутки справа."""

    def _item_size(self, item: PfObjectIMG) -> int:
        return item.height

    def _view_length(self) -> int:
        return self.width_height.pixel[1]

    def _view_rect(self) -> Rect:
        x, y = self.left_top.pixel
        w, h = self.width_height.pixel
        return Rect(x, y, w, h)

    def _axis_offset(self) -> int:
        return self.left_top.pixel[1]

    def _mouse_axis(self) -> int:
        return self.page.mouse_pos[1]

    def _blit_item(self, screen: Surface, item: PfObjectIMG, screen_pos: int) -> None:
        screen.blit(item.img, (self.left_top.pixel[0], screen_pos))

    def _draw_thumb(self, screen: Surface, thumb_pos: int) -> None:
        x, y = self.left_top.pixel
        w, h = self.width_height.pixel
        rect(screen, self.color_streak, (x + w - self.size_streak, y + thumb_pos, self.size_streak, self._thumb_size))
