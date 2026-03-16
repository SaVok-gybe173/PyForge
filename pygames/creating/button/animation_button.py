import pygame as pg
import os
import sys

try:
    from .animation import FrameAnimationButton
except ImportError:
    from animation import FrameAnimationButton
    
try:
    
    from image.tools import round_corners_alternative
except (ImportError, ModuleNotFoundError):
        
        imag_d = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # Добавляем 'root' в sys.path, если его там еще нет
        if imag_d not in sys.path:
            sys.path.insert(0, imag_d)
        from image.tools import round_corners_alternative
    
    
    
class Increase(FrameAnimationButton):
    def __init__(self, sped = 0.5, fps = 60, seze = 10, click_size = 0, efects_size = 5):
        if efects_size < seze:
            raise TypeError('efects_size < seze')
        self.efects_size =  efects_size
        self.sped = sped
        self.click_size = click_size or sped//2
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
    def update(self):
        if self.button.retention():
            if self.seze > self.i:
                self.x = self.x - (self.sped + self.conif)
                self.y = self.y - (self.sped + self.conif)
                
                self.height = self.height + (self.sped + self.conif)*2
                self.width = self.width + (self.sped + self.conif)*2
                
                self.i += self.sped + self.conif
        elif 0 < self.i:

            self.x = self.x + (self.sped + self.conif)
            self.y = self.y + (self.sped + self.conif)
            
            self.height = self.height - (self.sped + self.conif)*2
            self.width = self.width - (self.sped + self.conif)*2
            
            self.i -= self.sped + self.conif
        self.button.y = self.y
        self.button.x = self.x
        
        self.button.height = self.height
        self.button.width = self.width
    def __call__(self, button):
        super().__call__(button)
        
        self.x = button.x
        self.y = button.y
        self.width = button.width
        self.height = button.height

class Impuls(FrameAnimationButton):
    def __init__(self, sped: int | float = 0.5, fps:int = 60, shadow: int = 50, clic_shadow: int = 30, time_click: int | float = 0.1):
        self.conif = 1/fps
        self.sped = sped
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
        
    def update(self):
        
        if self.button.retention():
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
            self.activites += self.conif
        elif self.a_activites:
            self.a_activites = False
            self.susto = 0
            self.shadow_surface.fill(self.shadow)
            self._round_image()
            
    def draw(self, screen: pg.Surface):
        screen.blit(self.shadow_surface, (self.button.x, self.button.y))
        #pg.draw.circle(self.shadow_surface, (0,0,0), (50, 25), 20)
    def _round_image(self):
        self.shadow_surface = round_corners_alternative(self.shadow_surface, self.radius)
    def efects(self):
        self.a_activites = True
        self.activites = 0
        self.shadow_surface.fill((self.shadow[0], self.shadow[2], self.shadow[2], self.shadow[3]+self.clic_shadow))
        self._round_image()
    
class CollorsClick(FrameAnimationButton):
    def __init__(self, static_collor, retention_collor, click_collor, time_click: int | float = 0.1, fps: int = 60):
        self.static_collor = static_collor
        self.retention_collor = retention_collor
        self.click_collor = click_collor
        
        self._conif = 1/fps
        self.time_click = time_click
    def update(self):
        if self.activites < self.time_click:
            self.activites += self._conif
            self.button.collor_button = self.click_collor
        elif self.button.retention():
            self.button.collor_button = self.retention_collor
        else:
            self.button.collor_button = self.static_collor
    def efects(self):
        self.activites = 0
            