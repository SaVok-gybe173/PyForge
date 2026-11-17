from .core import MultiChildNode
from .constants import AUTO, ALIGN_START, ALIGN_CENTER, ALIGN_END, ALIGN_STRETCH


class Column(MultiChildNode):
    """
    Дети сверху вниз.

        spacing  - расстояние между детьми
        align_h  - выравнивание по ширине:
            ALIGN_START | ALIGN_CENTER | ALIGN_END | ALIGN_STRETCH
    """

    def __init__(self, page, children, size_w=AUTO, size_h=AUTO,
             spacing=0, align_h=ALIGN_CENTER, padding=0):
        super().__init__(page, children, size_w, size_h, padding)
        self.spacing = spacing
        self.align_h = align_h

    def measure(self, avail_w, avail_h):
        # Свои размеры: px (если >1), доля (если <=1), или AUTO (None)
        w = self.resolve(self.size_w, avail_w)
        h = self.resolve(self.size_h, avail_h)

        iw = (w - 2 * self.padding) if w is not None else avail_w
        ih = (h - 2 * self.padding) if h is not None else avail_h

        total_h, max_w = 2 * self.padding, 0
        for c in self.children:
            cw, ch = c.measure(iw, ih)
            total_h += ch
            if cw > max_w:
                max_w = cw

        total_h += self.spacing * max(0, len(self.children) - 1)

        if w is None: w = max_w + 2 * self.padding
        if h is None: h = total_h
        return w, h

    def arrange(self, x, y, w, h):
        super().arrange(x, y, w, h)

        ix, iy = x + self.padding, y + self.padding
        iw, ih = w - 2 * self.padding, h - 2 * self.padding

        sizes = [c.measure(iw, ih) for c in self.children]

        cy = iy
        for c, (cw, ch) in zip(self.children, sizes):
            if   self.align_h & ALIGN_STRETCH:
                cx, cw2 = ix, iw
            elif self.align_h & ALIGN_CENTER:
                cx, cw2 = ix + (iw - cw) / 2, cw
            elif self.align_h & ALIGN_END:
                cx, cw2 = ix + iw - cw, cw
            else:  # ALIGN_START
                cx, cw2 = ix, cw

            c.arrange(cx, cy, cw2, ch)
            cy += ch + self.spacing