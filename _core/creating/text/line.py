from .core import InputTextCore
from ....font.ttf.font import Font
from ....font.ttf.render import render_text
from ....pfmath.markup import Point, Size
from ....pfmath.rect import Rect
from ....easel.event import CommonEvent, MouseButtonEvent, MouseMotionEvent, KeyboardEvent
from ....easel.window import Window
from ....easel.object import PfObjectIMG
from ....easel.surface import Surface
from ....easel.draw import rect as draw_rect
from ....base.scrap import get_text_buffer, set_text_buffer
from ....base.logger import printError

import sdl2

class _TextLine(PfObjectIMG):
    font: Font # шрифт
    core: InputTextCore # ядро текста
    layout: tuple[list[float], list[float], list[int]] # тех инфа для выделения
    _min_y: int
    _size_px: int
    _color: tuple
    anchor: int = 0 # начальный символ
    idx: int = 0 # конечный символ
    dragging: bool = False # активно ли щас выделение
    selected_rect: Rect # область выделения
    _text_surf: Surface

    def __init__(self, page: Window, left_top: Point | tuple[int, int], 
                font: str | Font, text: str, size_px: int, color: tuple[int, int, int] = (255, 255, 255),
                highlighting: tuple[int, int, int, int] = (0x32, 0x97, 0xfd, 0x44)) -> None:
        """
        Одна редактируемая строка текста.

        Создаёт поверхность с отрендеренным текстом, вычисляет раскладку символов
        (для попадания курсора мышью и выделения) и регистрирует объект на `page`.
        Поддерживает ввод, удаление, перемещение курсора,
        выделение мышью/клавиатурой, копирование в буфер обмена.

        Args:
            page: Окно, на которой рисуется строка.
            left_top: Позиция левого верхнего угла строки в глобальных координатах.
            font: Путь к TTF-файлу или готовый объект `Font`.
            text: Начальный текст строки (может быть пустым).
            size_px: Размер шрифта в пикселях.
            color: Цвет текста RGB, по умолчанию белый `(255, 255, 255)`.
            highlighting: Цвет подсветки выделения RGBA. Альфа-канал
                применяется только на RGBA-поверхностях (см. `_fill_rect_blend`);
                по умолчанию — полупрозрачный синий `(0x32, 0x97, 0xfd, 0x44)`.

        Raises:
            ValueError: Если `font` — не `str` и не `Font`.

        Note:
            Для read-only использования (например, внутри `BigText`) строку нужно
            создавать с `read_only=True`, иначе она будет ловить клики и портить
            текст по Backspace/Delete. Также для элемента виртуального списка
            нужен `register=False`, чтобы строка не рисовалась дважды.
        """
        if isinstance(font, str): self.font = Font(font)
        elif isinstance(font, Font): self.font = font
        else: raise ValueError()
        self._size_px = size_px
        self._color = color
        self.core = InputTextCore(text)
        sur, self._min_y = render_text(self.font, text, size_px, color)
        super().__init__(page, left_top, sur)
        self._text_surf = self.img
        self.layout =   self.font.layout(text, size_px, 0)

        self.selected_rect = Rect(0, 0, 0, 0)
        self.highlighting = highlighting

    
    def updateMeta(self) -> None:
        """Обновления мета данных для выделения (если не обновлять то при выделении обьект может выдать ошибку)"""
        self.dragging = False
        self.layout = self.font.layout(self.text, self.size_px, 0)
        self.img, self._min_y = render_text(self.font, self.core.text, self.size_px, self._color)
        if not self._text_surf is None:
            del self._text_surf
        if self.img is None:
            self.width, self.height = 0, 0
        else:
            self.width, self.height = self.img.width, self.img.height
        self._text_surf = self.img

    # оболочка над GraphicsInputTextCore

    def addText(self, text: str) -> None:
        """Вставка с заменой выделения (если оно есть)."""
        self.core.addText(text)
        self.updateMeta()

    def backText(self) -> bool: # Backspace
        _is = self.core.backText()
        if _is:
            self.updateMeta()
        return _is

    def delText(self) -> bool: # удаление справа от курсора
        """Удалит символ или удали выделенную часть"""
        _is = self.core.delText()
        if _is:
            self.updateMeta()
        return _is

    # выделение текста
    def clear(self) -> None: # очистка выделения
        "clear_selection"
        self.core.clear_selection()
        self.selected_rect.x = self.selected_rect.y = self.selected_rect.w = self.selected_rect.h = 0
        del self.img
        self.img = self._text_surf

    def select_all(self) -> None:
        "Выделяет весь текст"
        self.core.select_all()
        self.updateMeta()

    def get_selected_text(self) -> None:
        "Возвращает выделенный текст"
        return self.core.get_selected_text()

    def delete_selection(self) -> None:
        "Удалить выделенный фрагмент курсор ставится на место выделения."
        self.core.delete_selection()
        self.updateMeta()

    def set_selection(self, anchor: int, cursor: int) -> None:
        "Установить выделение из двух индексов (для мыши). Если anchor == cursor - это каретка, выделение пустое."
        self.core.set_selection(anchor, cursor)
        self.updateMeta()

    # события
    def mousebuttondown(self, common: CommonEvent, button: MouseButtonEvent):
        if button.button == sdl2.SDL_BUTTON_LEFT:
            if self.rect.collidepoint(button.x, button.y):
                self.img = self._text_surf.copy()
                self.idx = self.anchor = self.core.hit_test(button.x-self.left, self.layout[0], self.layout[1])
                self.dragging = True
                self.core.set_selection(self.anchor, self.idx) # каретка, без выделения
            else: 
                self.clear()
            
        elif button.button == sdl2.SDL_BUTTON_RIGHT:
            self.clear()


    def selection(self, anchor: int, idx: int) -> None: # отрисовка выделения
        self.idx, self.anchor = idx, anchor
        self.core.set_selection(self.anchor, self.idx)
        
        start = min(self.anchor, self.idx)
        end = max(self.anchor, self.idx)

        x_start = self.layout[0][start] if start != len(self.core) else self.left+self.img.width
        x_end = self.layout[0][end] if end !=  len(self.core) else self.left+self.img.width

        self.selected_rect.left = x_start
        self.selected_rect.top = 0
        self.selected_rect.width = x_end - x_start
        self.selected_rect.height = self.img.height

        self.img = self._text_surf.copy()
        draw_rect(self.img, self.highlighting, self.selected_rect)

    def mousemotion(self, common: CommonEvent, motion: MouseMotionEvent):
        if self.dragging:
            if self.rect.collidepoint(motion.x, motion.y):
                self.selection(self.anchor, self.core.hit_test(motion.x-self.left, self.layout[0], self.layout[1]))
            
    def mousebuttonup(self, common: CommonEvent, button: MouseButtonEvent):
        if (button.button == sdl2.SDL_BUTTON_LEFT or button.button == sdl2.SDL_BUTTON_RIGHT) and self.dragging:
            self.dragging = False

    def keydown(self, common: CommonEvent, key: KeyboardEvent):
        if key.keysym.sym == sdl2.SDLK_c and (key.keysym.mod & sdl2.KMOD_CTRL):
            try:
                if self.core.selection:
                    set_text_buffer(self.core.get_selected_text())
            except BufferError as e:
                printError(f"[{self}] [BufferError] Не удалось положить текст в буфер.")
            except Exception as e:
                printError(f"[{self}] [{type(e).__name__}] {e}")
        if key.keysym.sym == sdl2.SDLK_a and (key.keysym.mod & sdl2.KMOD_CTRL):
            self.selection(0, len(self.core))

    # сеттеры и геттеры
    @property
    def text(self) -> str:
        return self.core.text
    @text.setter
    def text(self, text: str) -> None:
        self.core.text = text
        self.updateMeta()

    @property
    def size_px(self) -> int:
        return self._size_px
    @size_px.setter
    def size_px(self, size_px: int) -> None:
        self._size_px = size_px
        self.updateMeta()