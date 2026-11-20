from .core import MultiChildNode
from .constants import AUTO, ALIGN_START, ALIGN_CENTER, ALIGN_END, ALIGN_STRETCH
from .wrapper import Container

class Row(MultiChildNode):
    def __init__(self, page, children: list[Container], size_w=AUTO, size_h=AUTO,
             spacing=0, align_v=ALIGN_CENTER, padding=0):
        """
        Дети слева направо.
    
            spacing  - расстояние между детьми
            align_v  - выравнивание по высоте:
                ALIGN_START | ALIGN_CENTER | ALIGN_END | ALIGN_STRETCH
        """
        super().__init__(page, children, size_w, size_h, padding)
        self.spacing = spacing
        self.align_v = align_v

    def measure(self, avail_w, avail_h):
        w = self.resolve(self.size_w, avail_w)
        h = self.resolve(self.size_h, avail_h)
        iw = (w - 2 * self.padding) if w is not None else avail_w
        ih = (h - 2 * self.padding) if h is not None else avail_h

        total_w, max_h = 2 * self.padding, 0
        for c in self.children:
            cw, ch = c.measure(iw, ih)
            total_w += cw
            if ch > max_h:
                max_h = ch
        total_w += self.spacing * max(0, len(self.children) - 1)

        if w is None: w = total_w
        if h is None: h = max_h + 2 * self.padding
        return w, h

    def arrange(self, x, y, w, h):
        super().arrange(x, y, w, h)
        ix, iy = x + self.padding, y + self.padding
        iw, ih = w - 2 * self.padding, h - 2 * self.padding
        sizes = [c.measure(iw, ih) for c in self.children]

        cx = ix
        for c, (cw, ch) in zip(self.children, sizes):
            if   self.align_v & ALIGN_STRETCH:
                cy, ch2 = iy, ih
            elif self.align_v & ALIGN_CENTER:
                cy, ch2 = iy + (ih - ch) / 2, ch
            elif self.align_v & ALIGN_END:
                cy, ch2 = iy + ih - ch, ch
            else:  # ALIGN_START
                cy, ch2 = iy, ch

            c.arrange(cx, cy, cw, ch2)
            cx += cw + self.spacing