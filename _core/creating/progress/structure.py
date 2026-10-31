from ....easel.object import PfObject
from ....easel.window import Window
from .calculation_progress import ProgressBarCalc
from ....math.markup import Point, Size
from ....math.rect import Rect

class _ProgressBar(ProgressBarCalc, PfObject):
    def __init__(self, page: Window, left_top: tuple[int, int] | Point, width_height: tuple[int, int] | Size, color: tuple[int, int, int]):
        self.color = color
        self.rect = Rect(left_top,  (0, 0))
        PfObject.__init__(self, page, left_top, width_height)
        ProgressBarCalc.__init__(self)

    def update_progress(self):
        if self.width > self.height:
            self.rect = Rect(self.left_top,  (self.get_pixel(), self.height))
            
        return super().update_progress(self.width_height.pixel)