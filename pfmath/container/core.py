from ...easel.object import PfObject
from .constants import AUTO

class LayoutNode(PfObject):
    # Размеры, которые запросил пользователь (px / frac / AUTO)
    size_w = AUTO
    size_h = AUTO

    def measure(self, avail_w, avail_h):
        """Сколько нужно места при доступном (avail_w, avail_h).
        не меняет self.rect и не двигает детей.
        Возвращает (w, h) - желаемый размер."""
        raise NotImplementedError

    def arrange(self, x, y, w, h):
        """Окончательный прямоугольник (x, y, w, h).
        Поставь self.rect и разложи детей рекурсивно.
        это единственное место, где вообще меняется rect."""
        self.left, self.top = x, y
        self.width, self.height = w, h