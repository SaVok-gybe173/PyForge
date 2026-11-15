from ...easel.object import PfObject
from ...easel.surface import Surface
from .constants import AUTO, CENTER

class LayoutNode(PfObject):
    align: tuple[int, int]
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

    @staticmethod
    def resolve(value, available):
        """Превратить в пиксели, зная сколько места дали родители.
        Возвращает None, если размер AUTO (пусть решает родитель)."""
        if value is None: return None
        if value > 1: return value
        return available * value

    def place(self, px_, py_, pw, ph, cw, ch):
        """Где поставить ребёнка размера (cw, ch),
        внутри прямоугольника (px_, py_, pw, ph).
        Возвращает (x, y) левого верхнего угла ребёнка."""
        x = px_ + (pw - cw) * self.align[0]
        y = py_ + (ph - ch) * self.align[1]
        return x, y


class MultiChildNode(LayoutNode):
    """Общий предок Row/Column: несколько детей, проксирование вызовов."""

    def __init__(self, page, children: list[PfObject], size_w=AUTO, size_h=AUTO, padding=0):
        super().__init__(page, (0, 0), (0, 0))
        self.children = list(children)   # копия, чтобы не мутировать вход
        self.size_w   = size_w
        self.size_h   = size_h
        self.padding  = padding

    def draw(self, surf: Surface):
        for c in self.children:
            c.draw(surf)

    def update(self, dt):
        for c in self.children:
            c.update(dt)