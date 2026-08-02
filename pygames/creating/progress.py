from ..._core.creating.progress.structure import _ProgressBar
import pygame as pg

class ProgressBar(_ProgressBar):
    def draw(self, sceen):
        pg.draw.rect(sceen, self.color)