import pygame as pg
from typing_extensions import (
    deprecated,  # added in 3.13
)

from copy import copy

try:
    from .animation import FrameAnimationButton
except ImportError:
    from animation import FrameAnimationButton

class ButtonClick:
    LCM = 3
    PCM = 1
    NO_CLICK = 0
    SCR = 2
    FORWARD = 4
    BACK = 5
    
class Button:
    _event = None
    
    def __init__(self, left_top: list[int, int], image: pg.Surface, *, is_mask: bool, alpha: int = 0):
        '''
        инцилизация!
        
        Аргументы:
            left_top: list[int, int] - кординаты
            image: pg.Surface - изображение (размеры)
            
            is_mask: bool - использовать маску для точной колизии
            alpha: int - прозрачность для маски
        '''
        self._is_mask = is_mask
        self._rect = pg.Rect(left_top, image.get_size())
        self.collor_button = None
        self.image = image

    def update(self): pass
    def event(self, event):pass

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, (self._rect.x, self._rect.y))

    def _click(self,event, i):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == i and self._rect.collidepoint(event.pos):
                return True 
        return False
    

    def lcm(self, event) -> bool: return self._click(event, ButtonClick.PCM)
    def pcm(self, event) -> bool: return self._click(event, ButtonClick.LCM)
    def scm(self, event) -> bool: return self._click(event, ButtonClick.SCR)
    def forward(self, event) -> bool: return self._click(event, ButtonClick.FORWARD)
    def back(self, event) -> bool: return self._click(event, ButtonClick.BACK)
    
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

class AnimationButton(Button):
    '''
        инцилизация!
        
        Аргументы:
            
            left_top - кординаты
            image: pg.Surface - изображение (размеры)
            
            animation: FrameAnimationButton - класс анимации
        '''
    def __init__(self, left_top: list[int, int], image: pg.Surface,  animation: FrameAnimationButton = FrameAnimationButton()):
        super().__init__(left_top,image)
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


if __name__ == '__main__':
    from animation_button import Increase, Impuls
    pg.init()
    screen = pg.display.set_mode((800, 600))
    screen.fill((25, 25, 25)) 

    clock = pg.time.Clock()
    s = AnimationButton(screen, (100, 100), (50, 50), animation = Increase(0.5, seze = 5), width_stroke_panel=1, border_radius=10, collor_button=(100,100,100))
    sa = AnimationButton(screen, (200, 200), (50, 50), animation = Impuls(0.5), width_stroke_panel=1, border_radius=10, collor_button=(100,100,100), accuracy = True)
    s.draw()
    clock = pg.time.Clock()
    pg.display.flip()


    running = True
    while running:
        screen.fill((25, 25, 25))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if s.lcm(event):
                s.efects()
                print('s')
            if sa.pcm(event):
                sa.efects()
                print('sa')
        sa.draw()
        s.draw()
        clock.tick(60)
        pg.display.flip()
    pg.quit()