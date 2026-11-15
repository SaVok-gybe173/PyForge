from .core import LayoutNode
from .constants import AUTO, CENTER
from ...easel.object import PfObject
from ...easel.surface import Surface
from ...easel.draw import rect

class Container(LayoutNode):
    """
    widget    - ваш виджет
    align     - как разместить виджет внутри (CENTER / TOP_LEFT / Align(fx,fy))
    resize    - что делать с размером виджета:
                "natural"  - оставить natural_size
                "fill"     - растянуть по обеим осям
                "fill_w"/"fill_h" - только по одной
                tuple  - точный размер
    padding   - внутренние отступы
    bgcolor   - залить прямоугольник (для фона/отладки)
    """
    def __init__(self, page, widget: PfObject, size_w=AUTO, size_h=AUTO,
                 align=CENTER, resize="natural", padding=0, bgcolor=None):
        super().__init__(page, (0, 0), (0, 0))
        self.widget   = widget
        self.size_w, self.size_h = size_w, size_h
        self.align    = align
        self.resize   = resize
        self.padding  = padding
        self.bgcolor  = bgcolor

    def measure(self, avail_w, avail_h):
        w = self.resolve(self.size_w, avail_w)
        h = self.resolve(self.size_h, avail_h)
        if w is None or h is None:
            nw, nh = self.widget.natural_size()
            if w is None: w = nw + 2 * self.padding
            if h is None: h = nh + 2 * self.padding
        return w, h

    def arrange(self, x, y, w, h):
        super().arrange(x, y, w, h)
        nw, nh = self.widget.width_height

        # размеры ребёнка
        if self.resize in ("fill", "fill_w", "stretch"):
            cw = max(0, w - 2 * self.padding)
        elif isinstance(self.resize, tuple):
            cw = max(0, self.resolve(self.resize, w - 2 * self.padding))
        else:
            cw = nw

        if   self.resize in ("fill", "fill_h", "stretch"):
            ch = max(0, h - 2 * self.padding)
        elif isinstance(self.resize, tuple):
            cw = max(0, self.resolve(self.resize[0], w - 2*self.padding))
        else:
            ch = nh

        # позиция через align
        cx, cy = self.place(
            x + self.padding, y + self.padding,
            w - 2 * self.padding, h - 2 * self.padding,
            cw, ch,
        )
        self.widget.left, self.widget.top = cx, cy
        self.widget.width, self.widget.height = cw, ch

    def draw(self, surf: Surface):
        if self.bgcolor is not None:
            rect(surf, self.bgcolor, self.rect)
        self.widget.draw(surf)

    def event(self, event):
        return self.widget.event(event)

    def update(self, dt):
        self.widget.update(dt)