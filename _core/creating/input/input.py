import sdl2
from typing import Callable
from .core import InputTextCore
from ....easel.object import PfObject
from ....easel.window import Window
from ....widget.button import Button
from ....math.markup import Point, Size
from ....easel.event import TextInputEvent, KeyboardEvent, CommonEvent
from ....base.scrap import get_text_buffer, set_text_buffer
from ....base.logger import printError

class InputLine(PfObject):
    _log_txt_func: list[Callable]
    _log_removal_func: list[Callable]
    _log_key_func: list[Callable]
    _log_index_func: list[Callable]

    _active: bool = False   # активен ли ввод
    text: InputTextCore     # оболочка для работы с текстом

    def __init__(self, 
                page: Window,
                left_top: Point | tuple[int, int],
                width_height: Size | tuple[int, int],
                text: str='',
                color: tuple[int, int, int] = (255,255,255),
                ) -> None:
        """
        Ввод текста в окно разметом width_height
        Данный класс требует ручной активации и присваивание функций.
        
        Args:
            page (Window): ссылка на главное окно программы
            left_top (Point): расположение окна для ввода
            width_height (Size): размеры окна для ввода
            text (str): изначальный текст
            color (tuple[int, int, int]): цвет текста
        """
        
        super().__init__(page, left_top, width_height)
        self.text = InputTextCore(text)
        self.text.shift = len(self.text)+1
        self.color = color

    def __bool__(self):
        return self._active

    # обработка клавиш
    def keydown(self, common: CommonEvent, key: KeyboardEvent):
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

        elif key.keysym.sym == sdl2.SDLK_BACKSPACE: # удаление символа
            if self.text.backText():
                for f in self._log_removal_func:
                    f(self.text)
            else:
                printError(f"[{self}] [keyup] Ошибка при удаление символа")
        elif key.keysym.sym == sdl2.SDLK_LEFT: # влево
            self.text.ShiftLeft()
        elif key.keysym.sym == sdl2.SDLK_RIGHT:
            self.text.ShiftRight()

    def textinput(self, common: CommonEvent, text: TextInputEvent):
        self.text.addText(text.text)

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

