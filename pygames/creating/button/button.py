import pygame as pg
try:
    from typing_extensions import (
        deprecated,  # added in 3.13
    )
except ModuleNotFoundError:
    def deprecated(message, *, category = None, stacklevel: int = 1):
        def wr(f):
            return f
        return wr

from copy import copy

try:
    from .animation import FrameAnimationButton
except ImportError:
    from animation import FrameAnimationButton
from PyForge.tools import PfObject

class ButtonClick:
    LCM = 3
    PCM = 1
    NO_CLICK = 0
    SCR = 2
    FORWARD = 4
    BACK = 5
    
class Button(PfObject):
    _event = None
    
    def __init__(self, left_top: list[int, int], image: pg.Surface, *, is_mask: bool = False, alpha: int = 0, is_clicking: bool = True):
        '''
        инцилизация!
        
        Аргументы:
            left_top: list[int, int] - кординаты
            image: pg.Surface - изображение (размеры)
            
            is_mask: bool - использовать маску для точной колизии
            alpha: int - прозрачность для маски
            is_clicking: bool - показывать облость нажатия
        '''
        self.set_mask(is_mask)
        self._rect = pg.Rect(left_top, image.get_size())
        self.collor_button = None
        self.image = image
        self.is_clicking = is_clicking
        self._is_clicking = False
    def update(self): pass
    def event(self, event):
        if self.is_clicking and event.type == pg.MOUSEMOTION:
            if self._rect.collidepoint(event.pos):
                self._is_clicking = True
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                self.clicking()
            else:
                if self._is_clicking:
                    self._is_clicking = False
                    pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, (self._rect.x, self._rect.y))

    def _click(self,event: pg.event.Event, i: int) -> bool:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == i and self._rect.collidepoint(event.pos):
                return True
        return False
    

    def lcm(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.PCM)
    def pcm(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.LCM)
    def scm(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.SCR)
    def forward(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.FORWARD)
    def back(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.BACK)
    
    def copy(self):
        cop = copy(self)
        cop._rect = pg.Rect(self._rect)
        return cop
    
    def move(self, left_top):
        self._rect = self._rect.move(*left_top)
    
    @property
    def width_height(self):
        return [self._rect.width, self._rect.height]
    @width_height.setter
    def width_height(self, width_height: list[int | float, int | float]):
        self._rect.width, self._rect.height = width_height[0], width_height[1]
        
    @property
    def width(self):
        return self._rect.width
    @width.setter
    def width(self, width: int | float):
        self._rect.width = width
        
    @property
    def height(self):
        return self._rect.height
    @height.setter
    def height(self, height: int | float):
        self._rect.height = height
        
    @property
    def x(self):
        return self._rect.x
    @x.setter
    def x(self, x: int | float):
        self._rect.x = x
        
    @property
    def y(self):
        return self._rect.y
    @y.setter
    def y(self, y: int | float):
        self._rect.y = y
        
    @deprecated("Функция перенагружает систему, лучше использовать стандарт")
    def retention(self):
        return self._rect.collidepoint(pg.mouse.get_pos())
    
    def set_mask(self, is_mask):
        self._is_mask = is_mask

    def clicking(self):
        pass
    def collidepoint(self, pos):
        return self._rect.collidepoint(pos)

class AnimationButton(Button):
    '''
        инцилизация!
        
        Аргументы:
            
            left_top - кординаты
            image: pg.Surface - изображение (размеры)
            
            animation: FrameAnimationButton - класс анимации
            is_mask: bool - использовать маску для точной колизии
            alpha: int - прозрачность для маски
            is_clicking: bool - показывать облость нажатия
        '''
    def __init__(self, left_top: list[int, int], image: pg.Surface,  animation: FrameAnimationButton = FrameAnimationButton(), *, is_mask: bool = False, alpha: int = 0, is_clicking: bool = True):
        super().__init__(left_top,image, is_mask=is_mask, alpha=alpha, is_clicking=is_clicking)
        self.animation = animation
        self.animation(self)
    def draw(self, screen: pg.Surface):
        super().draw(screen)
        self.animation.draw(screen)
    def event(self, event):
        self.animation.event(event)
        return super().event(event)
    def update(self):
        self.animation.update()
    def efects(self):
        self.animation.efects()

