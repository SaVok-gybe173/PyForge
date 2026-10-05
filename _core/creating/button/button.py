from copy import copy
from typing import Callable
from .animation import FrameAnimationButton
from ....easel import Point, PfObjectIMG

import pygame as pg

class ButtonClick:
    LCM = 3
    PCM = 1
    NO_CLICK = 0
    SCR = 2
    FORWARD = 4
    BACK = 5
    
class _Button(PfObjectIMG):
    _event = None
    
    cursor_hand = pg.SYSTEM_CURSOR_HAND
    cursor_arrow = pg.SYSTEM_CURSOR_ARROW

    def __init__(self, left_top: Point | tuple[int, int], image: pg.Surface, *, is_mask: bool = False, mousebuttondown: Callable[[int], None] | None = None):
        '''
        Кнопка может работать в ручном режиме и также в автоматическом.
        
        Аргументы:
            left_top: list[int, int] - кординаты
            image: pg.Surface - изображение (размеры)
            
            is_mask: bool - использовать маску для точной колизии
        '''
        super().__init__(left_top, image)
        self.setMask(is_mask)
        self.collor_button = None
        self._is_mousemotion = False
        self._mousebuttondown = (lambda _: None) if mousebuttondown is None else mousebuttondown

    def mousemotion(self, pos, rel, buttons, touch):
        if self.rect.collidepoint(pos):
            self._is_mousemotion = True
            pg.mouse.set_cursor(self.cursor_hand)
        else:
            if self._is_mousemotion:
                self.stop()

    def mousebuttondown(self, pos, button, touch):
        if self.rect.collidepoint(pos):
            self._mousebuttondown(button)

    def stop(self):
        """
        Сменяет тип мыши на пасивный.
        """
        self._is_mousemotion = False
        pg.mouse.set_cursor(self.cursor_arrow)

    def click(self,event: pg.event.Event, i: int) -> bool:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == i and self.rect.collidepoint(event.pos):
                return True
        return False
    

    # Функции для отслежтвания разных нажатий
    def lcm(self, event: pg.event.Event) -> bool: return self.click(event, ButtonClick.PCM)
    def pcm(self, event: pg.event.Event) -> bool: return self.click(event, ButtonClick.LCM)
    def scm(self, event: pg.event.Event) -> bool: return self.click(event, ButtonClick.SCR)
    def forward(self, event: pg.event.Event) -> bool: return self.click(event, ButtonClick.FORWARD)
    def back(self, event: pg.event.Event) -> bool: return self.click(event, ButtonClick.BACK)
    
    def copy(self):
        cop = copy(self)
        return cop
    
    def setMask(self, is_mask):
        """
        Устанавливает маску.
        """
        self._is_mask = is_mask

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def setMousebuttondown(self, fun: Callable[[int], None]) -> Callable[[int], None]:
        """
        Функция которая принмает другую функцию что бы вызвать ее во премя нажатия. 
        Эта цункция принимает int флаг в ButtonClick.
        """
        self._mousebuttondown = fun
        return fun

class _AnimationButton(_Button):
    def __init__(self, left_top: list[int, int] | Point, image: pg.Surface,  animation: FrameAnimationButton = FrameAnimationButton(), *, is_mask: bool = False, mousebuttondown: Callable[[int], None] | None = None):
        """
        
        Аргументы:
            
            left_top - кординаты
            image: pg.Surface - изображение (размеры)
            animation: FrameAnimationButton - класс анимации
            
            is_mask: bool - использовать маску для точной колизии
 
        """
        super().__init__(left_top, image, is_mask=is_mask, mousebuttondown=mousebuttondown)
        self.animation = animation
        self.animation(self)
    
    def event(self, event):
        self.animation.event(event)
        return super().event(event)
    def update(self, dt: float):
        self.animation.update(dt)
    def efects(self):
        self.animation.efects()

    def mousemotion(self, pos, rel, buttons, touch):
        self.animation.mousemotion(pos, rel, buttons, touch)
        return super().mousemotion(pos, rel, buttons, touch)
    
    def mousebuttondown(self, pos, button, touch):
        self.animation.mousebuttondown(pos, button, touch)
        return super().mousebuttondown(pos, button, touch)