import sdl2
from typing import Callable
from ....easel.window import Window
from ....widget.button import Button
from ....pfmath.markup import Point, Size
from ....easel.event import TextInputEvent, KeyboardEvent, CommonEvent
from ....base.scrap import get_text_buffer, set_text_buffer
from ....base.logger import printError
from ..text.line import _TextLine
from ....font.ttf.font import Font

class _InputLine(_TextLine):
    _log_txt_func: list[Callable]
    _log_removal_func: list[Callable]
    _log_key_func: list[Callable]
    _log_index_func: list[Callable]

    _active: bool = False   # активен ли ввод

    def __init__(self, 
                page: Window,
                left_top: Point | tuple[int, int],
                length: int,
                font: str | Font, text: str, size_px: int, color: tuple[int, int, int] = (255, 255, 255),
                highlighting: tuple[int, int, int, int] = (0x32, 0x97, 0xfd, 0x44)
                ) -> None:
        """
        Ввод текста в окно разметом width_height
        Данный класс требует ручной активации и присваивание функций.
        
        Args:
            page (Window): ссылка на главное окно программы
            left_top (Point): расположение окна для ввода
            length (int): длина окна для ввода (высота зажаеться size_px через шрифт)
            text (str): изначальный текст
            color (tuple[int, int, int]): цвет текста
        """
        self.length = length
        super().__init__(page, left_top, font, text, size_px, color, highlighting)
        self.core.shift = len(self.text)+1
        self.color = color

        self._log_txt_func = []
        self._log_removal_func = []
        self._log_key_func = []
        self._log_index_func = []

    def __bool__(self):
        return self._active

    # обработка клавиш
    def keydown(self, common: CommonEvent, key: KeyboardEvent):
        if key.keysym.sym == (sdl2.SDLK_RETURN, sdl2.SDLK_KP_ENTER): # энтр
            for f in self._log_txt_func:
                f(self.text)
        elif key.keysym.mod & sdl2.KMOD_CTRL:
            if key.keysym.sym == sdl2.SDLK_v: # ctrl + v
                try:
                    self.addText(get_text_buffer())
                except BufferError as e:
                    printError(f"[{self}] [BufferError] {e}")
            else:
                super().keydown(common, key)

        elif key.keysym.sym == sdl2.SDLK_BACKSPACE: # удаление символа
            if self.backText():
                for f in self._log_removal_func:
                    f(self.core.text)
            else:
                printError(f"[{self}] [keyup] Ошибка при удаление символа")

        elif key.keysym.sym == sdl2.SDLK_DELETE:
            if self.delText():
                for f in self._log_removal_func:
                    f(self.core.text)
            else:
                printError(f"[{self}] [keyup] Ошибка при удаление символа")

        elif key.keysym.sym == sdl2.SDLK_LEFT: # влево
            self.core.ShiftLeft()
        elif key.keysym.sym == sdl2.SDLK_RIGHT:
            self.core.ShiftRight()

    def textinput(self, common: CommonEvent, text: TextInputEvent):
        self.addText(text.text.decode("utf-8"))

    # декораторы
    def log_enter(self, func: Callable):
        """вызывается при нажатии Enter fun(text)"""
        self._log_txt_func.append(func)
        return func
    def log_removal(self, func: Callable):
        """вызывается при нажатии кнопки удалить fun(text)"""
        self._log_removal_func.append(func)
        return func
    def log_key(self, func: Callable):
        """вызывается при нажатии на кнопку fun(text)"""
        self._log_key_func.append(func)
        return func
    def log_index(self, func: Callable):
        """вызывается при смещении"""
        self._log_index_func.append(func)
        return func


    @property
    def active(self) -> bool:
        return self._active
    @active.setter
    def active(self, active: bool) -> None:
        self._active = active
        if sdl2.SDL_IsTextInputActive():
            if not active:
                sdl2.SDL_StopTextInput()   
        else:
            if active:
                sdl2.SDL_StartTextInput()

    def on(self):
        self.active = True
    def off(self):
        self.active = False

