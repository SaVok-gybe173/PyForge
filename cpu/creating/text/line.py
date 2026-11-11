from ...._core.creating.text.line import _TextLine
from ....easel.draw import rect
from ....easel.surface import Surface

class TextLine(_TextLine):
    def draw(self, win: Surface):
        if self.core.selection:
            rect(win, self.highlighting, self.selected_rect)
        win.blit(self.img, (self.left, self.top))