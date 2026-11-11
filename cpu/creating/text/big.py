from ...._core.creating.text.big import _BigText
from ..listitng.list_of_items import ListOfItemsDown

class BigText(_BigText):
    def draw(self, win):
        ListOfItemsDown.draw(self, win)