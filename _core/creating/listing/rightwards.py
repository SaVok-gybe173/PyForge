" Горизонтальный список"
from .structure import CoreListOfItemsBase
from ....pfmath.rect import Rect
from ....easel.draw import rect
from ....easel.surface import Surface

class CoreListOfItemsRightwards(CoreListOfItemsBase):
    """Список слева направо. Полоса прокрутки сверху, элементы смещены вниз."""

    def _item_size(self, item) -> int:
        return item.width

    def _view_length(self) -> int:
        return self.width

    def _axis_offset(self) -> int:
        return self.left

    def _mouse_axis(self) -> int:
        return self.page.mouse_pos[0]

    def _blit_item(self, screen: Surface, item, screen_pos): # смещение по Y, чтобы не наезжать на полосу сверху
        screen.blit(item.img, (screen_pos, self.top + self.size_streak))

    def _draw_thumb(self, screen: Surface, thumb_pos):
        rect(screen, self.color_streak, (self.left + thumb_pos, self.top, self._thumb_size, self.size_streak))

    def _item_global_pos(self, idx):
        return ( self._axis_offset() - self.scroll_offset + self._prefix[idx], self.top + self.size_streak )