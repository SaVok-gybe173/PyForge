import pygame as pg
import os
import sys

from .animation import FrameAnimationButton
from ....cpu.creating.image.tools import round_corners_alternative

    
    
class Increase(FrameAnimationButton):
    def __init__(self, speed = 0.5, fps = 60, seze = 5, click_size = 0, efects_size = 10):
        self.efects_size =  efects_size
        self.speed = speed
        self.click_size = click_size or speed//2
        self.i = 0
        self.conif = 1/fps
        self.seze = seze
        
    def efects(self):
        if self.i >= self.efects_size:
            self.i -=  self.efects_size
            self.x += self.efects_size
            self.y += self.efects_size
            self.width -= self.efects_size*2
            self.height -= self.efects_size*2
        else:
            self.x += self.i
            self.y += self.i
            self.width -= self.i*2
            self.height -= self.i*2
            self.i = 0
    def update(self, dt):
        if self.button.collidepoint(pg.mouse.get_pos()):
            if self.seze > self.i:
                self.x = self.x - (self.speed + self.conif)
                self.y = self.y - (self.speed + self.conif)
                
                self.height = self.height + (self.speed + self.conif)*2
                self.width = self.width + (self.speed + self.conif)*2
                
                self.i += self.speed + self.conif
        elif 0 < self.i:

            self.x = self.x + (self.speed + self.conif)
            self.y = self.y + (self.speed + self.conif)
            
            self.height = self.height - (self.speed + self.conif)*2
            self.width = self.width - (self.speed + self.conif)*2
            
            self.i -= self.speed + self.conif
        self.button.left = self.y
        self.button.top = self.x
        
        self.button.height = self.height
        self.button.width = self.width
    def __call__(self, button):
        super().__call__(button)
        self.x = button.left
        self.y = button.top
        self.width_height = (button.width, button.height)

    def mousebuttondown(self, pos, button, touch):
        self.efects()

class Impuls(FrameAnimationButton):
    def __init__(self, speed: int | float = 0.5, shadow: int = 50, clic_shadow: int = 30, time_click: int | float = 0.1):
        self.speed = speed
        self.i = 0
        self.clic_shadow = clic_shadow
        self.shadow = (0,0,0, shadow)
        self.shadow_srov = (0,0,0,0)
        
        self.shadow_surface = None
        self.radius = 0
        self.susto = None
        
        self.time_click = time_click
        self.activites = 0
        self.a_activites = True
    def __call__(self, button):
        super().__call__(button)
        self.shadow_surface = pg.Surface((button.width, button.height), pg.SRCALPHA)
        
    def update(self, dt):
        
        if self.button.collidepoint(pg.mouse.get_pos()):
            if self.susto != 0:
                self.susto = 0
                self.shadow_surface.fill(self.shadow)
                self._round_image()
        else:
            if self.susto != 1:
                self.susto = 1
                self.shadow_surface.fill(self.shadow_srov)
                self._round_image()
        
        if self.activites < self.time_click and self.a_activites:
            self.activites += dt
        elif self.a_activites:
            self.a_activites = False
            self.susto = 0
            self.shadow_surface.fill(self.shadow)
            self._round_image()
            
    def draw(self, screen: pg.Surface):
        screen.blit(self.shadow_surface, (self.button.left, self.button.top))
        #pg.draw.circle(self.shadow_surface, (0,0,0), (50, 25), 20)
    def _round_image(self):
        self.shadow_surface = round_corners_alternative(self.shadow_surface, self.radius)
    def efects(self):
        self.a_activites = True
        self.activites = 0
        self.shadow_surface.fill((self.shadow[0], self.shadow[2], self.shadow[2], self.shadow[3]+self.clic_shadow))
        self._round_image()
    
class ImageClick(FrameAnimationButton):
    def __init__(self, retention_image: pg.Surface, click_image: pg.Surface, time_click: int | float = 0.15):
        self.retention_image = retention_image
        self.click_image = click_image
        self.activites = time_click
        self.time_click = time_click
    def update(self, dt):
        if self.activites < self.time_click:
            self.activites += dt
            self.button.img = self.click_image
        elif self.button.collidepoint(pg.mouse.get_pos()):
            self.button.img = self.retention_image
        else:
            self.button.img = self.static_image
    def __call__(self, button):
        self.static_image = button.img
        return super().__call__(button)
    def efects(self):
        self.activites = 0

    def mousebuttondown(self, pos, button, touch):
        if self.button.collidepoint(pos):
            self.activites = 0
            