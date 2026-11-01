" Горизонтальный список"
from .structure import CoreListOfItemsBase
from ....math.rect import Rect
from ....easel.draw import rect
from ....easel.surface import Surface

class CoreListOfItemsRightwards(CoreListOfItemsBase):
    """Список слева направо. Полоса прокрутки сверху, элементы смещены вниз."""

    def _item_size(self, item) -> int:
        return item.width

    def _view_length(self) -> int:
        return self.width_height.pixel[0]

    def _view_rect(self) -> Rect:
        x, y = self.left_top.pixel
        w, h = self.width_height.pixel
        return Rect(x, y, w, h)

    def _axis_offset(self) -> int:
        return self.left_top.pixel[0]

    def _mouse_axis(self) -> int:
        return self.page.mouse_pos[0]

    def _blit_item(self, screen: Surface, item, screen_pos): # смещение по Y, чтобы не наезжать на полосу сверху
        screen.blit(item.img, (screen_pos, self.left_top.pixel[1] + self.size_streak))

    def _draw_thumb(self, screen: Surface, thumb_pos):
        x, y = self.left_top.pixel
        w, h = self.width_height.pixel
        rect(screen, self.color_streak, (x + thumb_pos, y, self._thumb_size, self.size_streak))