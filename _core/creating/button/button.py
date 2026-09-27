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
from PyForge.easel import Point, PfObject

class ButtonClick:
    LCM = 3
    PCM = 1
    NO_CLICK = 0
    SCR = 2
    FORWARD = 4
    BACK = 5
    
class _Button(PfObject):
    _event = None
    
    cursor_hand = pg.SYSTEM_CURSOR_HAND
    cursor_arrow = pg.SYSTEM_CURSOR_ARROW

    def __init__(self, left_top: Point | tuple[int, int], image: pg.Surface, *, is_mask: bool = False, is_clicking: bool = True):
        '''
        инцилизация!
        
        Аргументы:
            left_top: list[int, int] - кординаты
            image: pg.Surface - изображение (размеры)
            
            is_mask: bool - использовать маску для точной колизии
            is_clicking: bool - показывать облость нажатия
        '''
        super().__init__(left_top, image.get_size())
        self.setMask(is_mask)
        self.collor_button = None
        self.image = image
        self.is_clicking = is_clicking
        self._is_clicking = False

    def event(self, event):
        if self.is_clicking and event.type == pg.MOUSEMOTION:
            if self.image.get_rect(left_top=self._left_top).collidepoint(event.pos):
                self._is_clicking = True
                pg.mouse.set_cursor(self.cursor_hand)
                self.clicking()
            else:
                if self._is_clicking:
                    self.stop()

    def stop(self):
        self._is_clicking = False
        pg.mouse.set_cursor(self.cursor_arrow)

    def _click(self,event: pg.event.Event, i: int) -> bool:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == i and self.image.get_rect(left_top=self._left_top).collidepoint(event.pos):
                return True
        return False
    

    def lcm(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.PCM)
    def pcm(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.LCM)
    def scm(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.SCR)
    def forward(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.FORWARD)
    def back(self, event: pg.event.Event) -> bool: return self._click(event, ButtonClick.BACK)
    
    def copy(self):
        cop = copy(self)
        return cop

    @deprecated("Функция перенагружает систему, лучше использовать collidepoint")
    def retention(self):
        return self.image.get_rect(left_top=self._left_top).collidepoint(pg.mouse.get_pos())
    
    def setMask(self, is_mask):
        self._is_mask = is_mask

    def clicking(self):
        pass
    def collidepoint(self, pos):
        return self.image.get_rect(left_top=self._left_top).collidepoint(pos)

class _AnimationButton(_Button):
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
    
    def event(self, event):
        self.animation.event(event)
        return super().event(event)
    def update(self):
        self.animation.update()
    def efects(self):
        self.animation.efects()

