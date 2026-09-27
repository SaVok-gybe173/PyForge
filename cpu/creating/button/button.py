from ...._core.creating.button import _Button, _AnimationButton
import pygame as pg

class Button(_Button):
    def draw(self, screen: pg.Surface):
        print((self.left, self.top))
        screen.blit(self.image, (self.left, self.top))

class AnimationButton(_AnimationButton):
    def draw(self, screen: pg.Surface):
        screen.blit(self.image, (self.left, self.top))
        self.animation.draw(screen)