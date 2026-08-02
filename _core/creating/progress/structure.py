from ....tools import PfObject
from .calculation_progress import ProgressBarCalc
from ....markup import Point, Size
from ....color import RGB
import pygame as pg

class _ProgressBar(ProgressBarCalc, PfObject):
    def __init__(self, left_top: tuple[int, int] | Point, width_height: tuple[int, int] | Size, color: tuple[int, int, int]):
        self.color = color
        
        super().__init__(left_top,  width_height)
    def update_progress(self):
        self.rect = pg.rect.Rect(self.left_top,  self.width_height)
        return super().update_progress()