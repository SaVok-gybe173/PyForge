from ....easel import Surface
from dataclasses import dataclass
from typing import Tuple, Any
from ...._core.creating.listing import CoreListOfItemsDown, CoreListOfItemsRightwards, CoreListOfItemsBase
from ...._core.creating.listing._list_math import thumb_from_scroll

class ListOfItemsBase(CoreListOfItemsBase):
    def draw(self, screen: Surface):
        """Рендерит только видимые элементы. Никаких промежуточных поверхностей."""
        if self.visible_start <= self.visible_end:
            old_clip = screen.get_clip()
            screen.set_clip(self._view_rect())
            try:
                offset = self._axis_offset() - self.scroll_offset
                prefix = self._prefix
                items = self.items
                for i in range(self.visible_start, self.visible_end + 1):
                    self._blit_item(screen, items[i], offset + prefix[i])
            finally:
                screen.set_clip(old_clip)

        if self._max_scroll > 0:
            thumb_pos = thumb_from_scroll(self.scroll_offset, self._max_scroll, self._thumb_travel,)
            self._draw_thumb(screen, thumb_pos)

class ListOfItemsDown(CoreListOfItemsDown):
    def draw(self, screen: Surface):
        ListOfItemsBase.draw(self, screen)

class ListOfItemsRightwards(CoreListOfItemsRightwards):
    def draw(self, screen: Surface):
        ListOfItemsBase.draw(self, screen)