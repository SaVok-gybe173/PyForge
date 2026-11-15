from .core import LayoutNode
from .constants import AUTO, CENTER

class Container(LayoutNode):
    """
    widget    - ваш виджет
    align     - как разместить виджет внутри (CENTER / TOP_LEFT / Align(fx,fy))
    resize    - что делать с размером виджета:
                "natural"  - оставить natural_size
                "fill"     - растянуть по обеим осям
                "fill_w"/"fill_h" - только по одной
                Size(...)  - точный размер
    padding   - внутренние отступы
    bgcolor   - залить прямоугольник (для фона/отладки)
    """
    def __init__(self, widget, size_w=AUTO, size_h=AUTO,
                 align=CENTER, resize="natural", padding=0, bgcolor=None):
        self.widget   = widget
        self.size_w, self.size_h = size_w, size_h
        self.align    = align
        self.resize   = resize
        self.padding  = padding
        self.bgcolor  = bgcolor
        self.rect     = None

    def measure(self, avail_w, avail_h):
        w = self.size_w.resolve(avail_w)
        h = self.size_h.resolve(avail_h)
        if w is None or h is None:
            nw, nh = self.widget.natural_size()
            if w is None: w = nw + 2 * self.padding
            if h is None: h = nh + 2 * self.padding
        return w, h

    def arrange(self, x, y, w, h):
        super().arrange(x, y, w, h)
        nw, nh = self.widget.natural_size()

        # размеры ребёнка
        if   self.resize in ("fill", "fill_w", "stretch"):
            cw = max(0, w - 2 * self.padding)
        elif isinstance(self.resize, tuple):
            cw = max(0, self.resize.resolve(w - 2 * self.padding))
        else:
            cw = nw

        if   self.resize in ("fill", "fill_h", "stretch"):
            ch = max(0, h - 2 * self.padding)
        elif isinstance(self.resize, tuple):
            ch = max(0, self.resize.resolve(h - 2 * self.padding))
        else:
            ch = nh

        # позиция через align
        cx, cy = self.align.place(
            x + self.padding, y + self.padding,
            w - 2 * self.padding, h - 2 * self.padding,
            cw, ch,
        )
        self.widget.set_rect(cx, cy, cw, ch)

    def draw(self, surf):
        if self.bgcolor is not None:
            surf.fill(self.rect, self.bgcolor)   # адаптируйте под API
        self.widget.draw(surf)

    def event(self, event):
        return self.widget.event(event)

    def update(self, dt):
        self.widget.update(dt)