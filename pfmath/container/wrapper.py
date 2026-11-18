from .core import LayoutNode
from .constants import AUTO, CENTER, NATURAL, FILL_W, FILL_H
from ...easel.object import PfObject
from ...easel.surface import Surface
from ...easel.draw import rect

class Container(LayoutNode):
    def __init__(self, page, widget: PfObject, size_w=AUTO, size_h=AUTO,
             align=CENTER, resize=NATURAL, padding=0, bgcolor=None):
        """
        widget    - ваш виджет
        align     - как разместить виджет внутри (CENTER / TOP_LEFT / Align(fx,fy))
        resize - что делать с размером виджета:
            NATURAL  - оставить natural_size
            FILL     - растянуть по обеим осям
            FILL_W / FILL_H - только по одной
            tuple    - точный размер (rw, rh)
    
        padding   - внутренние отступы
        bgcolor   - залить прямоугольник (для фона/отладки)
        """
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
            if isinstance(self.widget, LayoutNode):
                nw, nh = self.widget.measure(
                    w - 2*self.padding if w is not None else avail_w,
                    h - 2*self.padding if h is not None else avail_h,
                )
            else:
                nw, nh = self.widget.width_height
            if w is None: w = nw + 2*self.padding
            if h is None: h = nh + 2*self.padding
        return w, h

    def arrange(self, x, y, w, h):
        super().arrange(x, y, w, h)
        if isinstance(self.resize, tuple):
            rw, rh = self.resize
            cw = max(0, self.resolve(rw, w - 2*self.padding))
            ch = max(0, self.resolve(rh, h - 2*self.padding))
        else:
            if isinstance(self.widget, LayoutNode):
                nw, nh = self.widget.measure(w - 2*self.padding, h - 2*self.padding)
            else:
                nw, nh = self.widget.width_height
            cw = max(0, w - 2*self.padding) if self.resize & FILL_W else nw
            ch = max(0, h - 2*self.padding) if self.resize & FILL_H else nh

        cx, cy = self.place(
            x + self.padding, y + self.padding,
            w - 2*self.padding, h - 2*self.padding,
            cw, ch,
        )
        if isinstance(self.widget, LayoutNode):
            self.widget.arrange(cx, cy, cw, ch)
        else:
            self.widget.left_top     = (cx, cy)
            self.widget.width_height = (cw, ch)


    def draw(self, surf: Surface):
        if self.bgcolor is not None:
            rect(surf, self.bgcolor, self.rect)
        self.widget.draw(surf)

    def event(self, event):
        return self.widget.event(event)

    def update(self, dt):
        self.widget.update(dt)