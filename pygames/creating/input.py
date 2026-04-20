import pygame as pg
from functools import wraps
from typing import Callable
from PyForge.tools import PfObject

def set_txt_bufer(text_string):
    """
    Помещает заданную строку текста в буфер обмена.
    """
    if pg.scrap.get_init():
        pg.scrap.put(pg.SCRAP_TEXT, text_string.encode('cp1251'))
            
    else:
        raise TypeError("Буфер обмена не инициализирован, не удалось поместить текст.")

def ger_txt_bufer():
    if pg.scrap.get_init():
        clipboard_text_bytes = pg.scrap.get(pg.SCRAP_TEXT)
        if clipboard_text_bytes:
            try:
                return clipboard_text_bytes.decode('cp1251').replace('\x00', '')
            except UnicodeDecodeError: ...
        return "" 
            
    else:
        raise TypeError("Буфер обмена не инициализирован, не удалось поместить текст.")

class InputLine(PfObject):
    _log_txt_func: list 
    _log_delte_func: list
    active: bool = False # активен ли ввод

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
        self._left, self._top = left_top
        self.left_text, self.top_text = left_top
        self.surfase = surfase # фон
        self.color = color # цвет текста
        self.font = pg.font.Font(None, 32) if font is None else font # шрифт
        self.text = text # тест
     
        self._log_txt_func = [] #
        self._log_delte_func = [] #
        self._log_click_func = [] #
        self._log_key_func = []

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
    def clic_window(self, e):
        if e.type == pg.MOUSEBUTTONDOWN:
            return self.surfase.get_rect(left = self._left, top = self._top).collidepoint(e.pos)
        return False

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.clic_window(event):
                self.active = not self.active
            else:
                if self.line_aktiv:
                    self.text = self.text[:-1]
                self.active = self.line_aktiv = False
            for f in self._log_click_func:
                f(self.text)
                
        if event.type == pg.KEYDOWN:
            if self.active:
                if self.line_aktiv:
                    self._text = self._text[:-1]
                if event.key == pg.K_v and (pg.key.get_mods() & pg.KMOD_CTRL):
                    
                    self.text += ger_txt_bufer()
                    for f in self._log_key_func:
                        f(self.text)
                elif event.key == pg.K_c and (pg.key.get_mods() & pg.KMOD_CTRL):
                    set_txt_bufer(self.text)
                elif event.key == pg.K_RETURN:  
                    for f in self._log_txt_func:
                        f(self.text)
                elif event.key == pg.K_BACKSPACE:  
                    self.text = self.text[:-1]
                    for f in self._log_delte_func:
                        f(self.text)
                else:
                    self.text += event.unicode
                    for f in self._log_key_func:
                        f(self.text)
                if self.line_aktiv:
                    self.text += '|'
    
    def update(self):
        if self.active:
            if self.line_update:
                if self.line_time > self.line_out:
                    self.line_out += self.tik
                else:
                    self.line_out = 0
                    self.line_aktiv = not self.line_aktiv
                    if self.line_aktiv:
                        self.text += '|'
                    else:
                        self.text = self.text[:-1]
    def draw(self, screen: pg.Surface):
        screen.blit(self.surfase, (self._left, self._top))
        screen.blit(self.txt_surface, (self.left_text, self.top_text))
        
    # дикораторы
    def log_enter(self, func: Callable):
        """вызывается при нажании энтр"""
        self._log_txt_func.append(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(self.text)
        return wrapper
    def log_delte(self, func: Callable):
        """вызывается при нажатии кнопки удалить"""
        self._log_delte_func.append(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(self.text)
        return wrapper
    def log_key(self, func: Callable):
        """вызывается при нажатии на кнопку"""
        self._log_key_func.append(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(self.text)
        return wrapper
    def log_clik(self, func: Callable):
        self._log_click_func.append(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(self.text)
        return wrapper

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