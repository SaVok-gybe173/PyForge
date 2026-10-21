from ...._core.creating.button import _Button, _AnimationButton
from ....easel import Surface
import pygame as pg

class Button(_Button):
    def draw(self, screen: Surface):
        screen.blit(self.img, (self.left, self.top))
        


class AnimationButton(_AnimationButton):
    def draw(self, screen: Surface):
        screen.blit(self.img, (self.left, self.top))
        self.animation.draw(screen)