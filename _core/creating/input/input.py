import sdl2
from typing import Callable
from .core import InputTextCore
from ....easel.object import PfObject
from ....easel.window import Window
from ....widget.button import Button
from ....math.markup import Point, Size
from ....easel.event import KeyboardEvent, CommonEvent
from ....base.scrap import get_text_buffer, set_text_buffer
from ....base.logger import printError

class InputLine(PfObject):
    _log_txt_func: list[Callable]
    _log_delte_func: list[Callable]
    _log_click_func: list[Callable]
    _log_key_func: list[Callable]
    _log_index_func: list[Callable]

    active: bool = False # активен ли ввод
    index: int = -1
    text: InputTextCore

    def __init__(self, 
                page: Window,
                left_top: Point | tuple[int, int],
                width_height: Size | tuple[int, int],
                text: str='',
                color = (255,255,255),
                line_time: float = 1.0
                ) -> None:
        PfObject.__init__(page, left_top, width_height)
        self.text = InputTextCore(text)
        self.text.shift = len(self.text)+1
        self.color = color
        self.time = line_time

    def __bool__(self):
        return self.active

    # обработка клавиш
    def keyup(self, common: CommonEvent, key: KeyboardEvent):
        if key.keysym.sym == sdl2.SDLK_SPACE: # пробел
            for f in self._log_txt_func:
                f(self.text)
        elif key.keysym.sym == sdl2.SDLK_v and (key.keysym.mod & sdl2.KMOD_CTRL): # ctrl + v
            try:
                self.text.addText(get_text_buffer())
            except BufferError as e:
                printError(f"[{self}] [BufferError] {e}")
        elif key.keysym.sym == sdl2.SDLK_c and (key.keysym.mod & sdl2.KMOD_CTRL): # ctrl + c
            try:
                if self.text.selection:
                    set_text_buffer(self.text.get_selected_text())
                else:
                    set_text_buffer(self.text)
            except BufferError as e:
                printError(f"[{self}] [BufferError] Не удалось положить текст в буфер.")
            except Exception as e:
                printError(f"[{self}] [{type(e).__name__}] {e}")
                raise e
        elif key.keysym.sym == sdl2.SDLK_BACKSPACE: # удаление символа
            if self.text.backText():
                for f in self._log_delte_func:
                    f(self.text)
            else:
                printError(f"[{self}] [keyup] Ошибка при удаление символа")
        elif key.keysym.sym == sdl2.SDLK_LEFT: # влево
            self.text.ShiftLeft()
        elif key.keysym.sym == sdl2.SDLK_RIGHT:
            self.text.ShiftRight()
        else:
            
            

    # дикораторы
    def log_enter(self, func: Callable):
        """вызывается при нажании энтр fun(text)"""
        self._log_txt_func.append(func)
        return func
    def log_delte(self, func: Callable):
        """вызывается при нажатии кнопки удалить fun(text)"""
        self._log_delte_func.append(func)
        return func
    def log_key(self, func: Callable):
        """вызывается при нажатии на кнопку fun(text)"""
        self._log_key_func.append(func)
        return func
    def log_clik(self, func: Callable):
        """вызывается при нажатии fun(text)"""
        self._log_click_func.append(func)
        return func
    def log_index(self, func: Callable):
        """вызывается при смещении"""
        self._log_index_func.append(func)
        return func

class InputLine(PfObject):

    def __bool__(self):
        return bool(self.active)

    def __init__(self, left_top: list[int], surfase: pg.Surface , text: str='', color = (255,255,255), font: pg.font.Font = None, fps: int= 60, line_time: int | float = 1):
        '''
        командная строка HeartComandRend
        
        Args:
            left, top: int- кординаты
            surfase - задний фон (основа для ввода текста)
            text - изначальный текст
            color - цвет текста
            font - шрифт
        Другие аргументы:
            left_text, top_text = left, top - размещение текста
            active - активно ли окно для ввода
        '''
        self.button = Button(left_top, surfase)
        self.button.cursor_hand = pg.SYSTEM_CURSOR_IBEAM
        self.left_text, self.top_text = 0, 0
        self.surfase = surfase # фон
        self.color = color # цвет текста
        self.font = pg.font.Font(None, 32) if font is None else font # шрифт
        self.text = text # тест
     
        self._log_txt_func = [] #
        self._log_delte_func = [] #
        self._log_click_func = [] #
        self._log_key_func = []
        self._log_index_func = []

        self.line_update = True # обновление строки анимации
        self.line_time = line_time #
        self.line_out = 0 #
        self.line_aktiv = False #
        self.tik = 1/fps #

    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, t):
        self._text = t
        self.txt_surface = self.font.render(self._text, True, self.color).convert_alpha()

    def event(self, event):
        self.button.event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.button.collidepoint(event.pos):
                self.active = not self.active
                if self.line_aktiv:
                    self.del_index(self.index)
                    self.line_aktiv = False

            else:
                if self.line_aktiv:
                    self.del_index(self.index)
                self.active = self.line_aktiv = False
            for f in self._log_click_func:
                f(self.text)
                
        if event.type == pg.KEYDOWN:
            if self.active:
                if self.line_aktiv:
                    self.del_index(self.index)
                if event.key == pg.K_v and (pg.key.get_mods() & pg.KMOD_CTRL):
                    
                    self.add_index(ger_txt_bufer(), self.index)
                    for f in self._log_key_func:
                        f(self.text)
                elif event.key == pg.K_c and (pg.key.get_mods() & pg.KMOD_CTRL):
                    set_txt_bufer(self.text)
                elif event.key == pg.K_RETURN:  
                    for f in self._log_txt_func:
                        f(self.text)
                elif event.key == pg.K_BACKSPACE: 
                    if len(self.text)+self.index+1 > 0:
                        self.del_index(self.index)
                        for f in self._log_delte_func:
                            f(self.text)
                elif event.key == 1073741903:
                    self.index += 1
                    if self.index > -1:
                        self.index = -1
                    else:
                        self.line_out = 0
                        self.line_aktiv = True
                    for f in self._log_index_func:
                            f(self.index)
                elif event.key == 1073741904:
                    if len(self.text)+self.index+1 > 0:
                        self.index -= 1
                    self.line_out = 0
                    self.line_aktiv = True
                    for f in self._log_index_func:
                            f(self.index)
                else:
                    self.add_index(event.unicode, self.index)
                    for f in self._log_key_func:
                        f(self.text)
                if self.line_aktiv:
                    self.add_index('|', self.index)
    
    def update(self):
        self.button.update()
        if self.active:
            if self.line_update:
                if self.line_time > self.line_out:
                    self.line_out += self.tik
                else:
                    self.line_out = 0
                    self.line_aktiv = not self.line_aktiv
                    if self.line_aktiv:
                        self.add_index('|', self.index)
                    else:
                        self.del_index(self.index)
    
    def add_index(self, text, index: int):
        if index<0:
            index=len(self.text)+index+1
        self.text = self.text[:index] + text + self.text[index:]

    def del_index(self, index: int, lens=1):
        if index<0:
            index=len(self.text)+index+1
        self.text = self.text[:index-1] + self.text[index+lens-1:]

    def draw(self, screen: pg.Surface):
        sur = self.surfase.copy()
        sur.blit(self.txt_surface, (self.left_text, self.top_text))
        screen.blit(sur, (self.left, self.top))
        
    # дикораторы
    def log_enter(self, func: Callable):
        """вызывается при нажании энтр fun(text)"""
        self._log_txt_func.append(func)
        return func
    def log_delte(self, func: Callable):
        """вызывается при нажатии кнопки удалить fun(text)"""
        self._log_delte_func.append(func)
        return func
    def log_key(self, func: Callable):
        """вызывается при нажатии на кнопку fun(text)"""
        self._log_key_func.append(func)
        return func
    def log_clik(self, func: Callable):
        """вызывается при нажатии fun(text)"""
        self._log_click_func.append(func)
        return func
    def log_index(self, func: Callable):
        """вызывается при смещении"""
        self._log_index_func.append(func)
        return func
    
    @property
    def top(self):
        return self.button._rect.top
    @top.setter
    def top(self, top):
        self.button._rect.top = top

    @property
    def left(self):
        return self.button._rect.left
    @left.setter
    def left(self, left):
        self.button._rect.left = left


    
    @property
    @deprecated("устаревший метод")
    def _top(self):
        return self.button._rect.top
    @_top.setter
    @deprecated("устаревший метод")
    def _top(self, top):
        self.button._rect.top = top

    @property
    @deprecated("устаревший метод")
    def _left(self):
        return self.button._rect.left
    @_left.setter
    @deprecated("устаревший метод")
    def _left(self, left):
        self.button._rect.left = left

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((800, 600))
    font15 = pg.font.Font(pg.font.match_font('dejavusans'), 14)
    pg.scrap.init()
    clock = pg.time.Clock()
    i = InputLine(100,100, pg.Surface((200,30)), color=(42,233,84), font=font15)

    @i.log_enter
    def das(text):
        print(text)

    @i.log_delte
    def das(text):
        print("удалён символ")

    running = True
    while running:
        screen.fill((122,122, 122), )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            i.event(event)
        i.update()
        #print(i.text)
        i.draw(screen)
        clock.tick(60)
        pg.display.flip()
    pg.quit()