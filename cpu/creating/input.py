from ..._core.creating.input.input import _InputLine
from ...easel.draw import rect
from ...easel.surface import Surface

class InputLine(_InputLine):
    def draw(self, win: Surface):
        win.blit(self.img, (self.left, self.top))