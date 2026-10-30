from ..._core.creating.progress.structure import _ProgressBar
import pygame as pg

class ProgressBar(_ProgressBar):
    def draw(self, scene):
        pg.draw.rect(scene, self.color, self.rect)