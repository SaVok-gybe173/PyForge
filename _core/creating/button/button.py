from copy import copy
from typing import Callable
from .animation import FrameAnimationButton
from ....easel import Point, PfObjectIMG, Surface
from ....easel.event import Event, CommonEvent, MouseMotionEvent, MouseButtonEvent, MOUSEBUTTONDOWN, MouseWheelEvent
from sdl2.mouse import SDL_SYSTEM_CURSOR_HAND, SDL_SYSTEM_CURSOR_ARROW, SDL_CreateSystemCursor, SDL_SetCursor

class ButtonClick:
    LCM = 3
    PCM = 1
    NO_CLICK = 0
    SCR = 2
    FORWARD = 4
    BACK = 5
    
class _Button(PfObjectIMG):
    cursor_hand = SDL_SYSTEM_CURSOR_HAND # как выглядит мыш при наведение
    cursor_arrow = SDL_SYSTEM_CURSOR_ARROW # как выглядит мыш когда убираем мыш с кнопки

    def __init__(self, page, left_top: Point | tuple[int, int], image: Surface, *, is_click: Callable[[int], None] | None = None):
        """
        Кнопка может работать в ручном режиме и также в автоматическом.
        
        Аргументы:
            page - ссылка на главное окно
            left_top: list[int, int] - координаты
            image: Surface - изображение (размеры)
            is_click: Callable[[int], None] - ссылка на функцию, которая принимает тип клика ButtonClick
        """
        super().__init__(page, left_top, image)
        self._IsActiveSystemCursor = False # активный ли курсор
        self.is_click = (lambda _: None) if is_click is None else is_click


    def mousemotion(self, common: CommonEvent, motion: MouseMotionEvent):
        if self.rect.collidepoint(motion.x, motion.y):
            # для смены курсора
            self._IsActiveSystemCursor = True
            hand_cursor = SDL_CreateSystemCursor(self.cursor_hand)
            SDL_SetCursor(hand_cursor)
        else:
            if self._IsActiveSystemCursor:
                self.stop()

    def mousebuttondown(self, common: CommonEvent, button: MouseButtonEvent):
        if self.rect.collidepoint(button.x, button.y):
            self.is_click(button)

    def stop(self):
        """
        Сменяет тип мыши на self.cursor_arrow.
        """
        self._IsActiveSystemCursor = False
        hand_cursor = SDL_CreateSystemCursor(self.cursor_hand)
        SDL_SetCursor(hand_cursor)

    def click(self,event: Event, i: int) -> bool:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == i and self.rect.collidepoint(event.button.x, event.button.y):
                return True
        return False
    

    # Функции для отслеживания разных нажатий
    def lcm(self, event: Event) -> bool: return self.click(event, ButtonClick.PCM)
    def pcm(self, event: Event) -> bool: return self.click(event, ButtonClick.LCM)
    def scm(self, event: Event) -> bool: return self.click(event, ButtonClick.SCR)
    def forward(self, event: Event) -> bool: return self.click(event, ButtonClick.FORWARD)
    def back(self, event: Event) -> bool: return self.click(event, ButtonClick.BACK)
    
    def copy(self) -> "_Button":
        cop = copy(self)
        return cop

    def setIsClick(self, fun: Callable[[int], None]) -> Callable[[int], None]:
        """
        Функция которая принимает другую функцию что бы вызвать ее во время нажатия. 
        Эта функция принимает int флаг в ButtonClick.
        """
        self._IsActiveSystemCursor = fun
        return fun

class _AnimationButton(_Button):
    def __init__(self, page, left_top: list[int, int] | Point, image: Surface,  animation: FrameAnimationButton = FrameAnimationButton(), *, is_click: Callable[[int], None] | None = None):
        """
        Этот класс похож на Button, он она принимает также класс анимации.

        Аргументы:
            page - ссылка на главное окно
            left_top - координаты
            image: Surface - изображение (размеры)
            animation: FrameAnimationButton - класс анимации
            
            is_click: Callable[[int], None] - ссылка на функцию, которая принимает тип клика ButtonClick
        """
        super().__init__(page, left_top, image, is_click=is_click)
        self.animation = animation
        self.animation(self)
    
    def event(self, event):
        self.animation.event(event)
        return super().event(event)

    def draw(self, win):
        super().draw(win)
        self.animation.draw(win)
    
    def update(self, dt: float):
        self.animation.update(dt)

    def effect(self):
        self.animation.effect()

    def mousemotion(self, common: CommonEvent, motion: MouseMotionEvent):
        self.animation.mousemotion(common, motion)
        super().mousemotion(common, motion)
    
    def mousebuttondown(self, common: CommonEvent, wheel: MouseWheelEvent):
        super().mousebuttondown(common, wheel)
        self.animation.mousebuttondown(common, wheel)