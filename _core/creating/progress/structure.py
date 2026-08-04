from ....tools import PfObject
from .calculation_progress import ProgressBarCalc
from ....markup import Point, Size
from ....color import RGB
import pygame as pg

class _ProgressBar(ProgressBarCalc, PfObject):
    def __init__(self, left_top: tuple[int, int] | Point, width_height: tuple[int, int] | Size, color: tuple[int, int, int]):
        self.color = color
        self.rect = pg.rect.Rect(left_top,  (0, 0))
        super().__init__(left_top,  width_height)
    def update_progress(self):
        if self.width > self.height:
            self.rect = pg.rect.Rect(self.left_top,  (self.get_pixel(), self.height))
            
        return super().update_progress()