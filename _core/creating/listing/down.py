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
        return self.height

    def _axis_offset(self) -> int:
        return self.top

    def _mouse_axis(self) -> int:
        return self.page.mouse_pos[1]

    def _blit_item(self, screen: Surface, item: PfObjectIMG, screen_pos: int) -> None:
        screen.blit(item.img, (self.left, screen_pos))

    def _draw_thumb(self, screen: Surface, thumb_pos: int) -> None:
        rect(screen, self.color_streak, (self.left + self.width - self.size_streak, self.top + thumb_pos, self.size_streak, self._thumb_size))

    def _item_global_pos(self, idx):
        return (self.left, self._axis_offset() - self.scroll_offset + self._prefix[idx] )
