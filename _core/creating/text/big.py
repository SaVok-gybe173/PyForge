"""Многострочный read-only текст на базе виртуального списка."""
from __future__ import annotations

from .line import _TextLine
from ..listing.down import CoreListOfItemsDown
from ....easel import Window, Surface, PfObjectIMG
from ....pfmath.markup import Point, Size
from ....font.ttf import Font, render_text
from ..listing._list_math import find_index_at
from ....base.scrap import set_text_buffer
from ....base.logger import printError

from dataclasses import dataclass

import sdl2

class _BigText(CoreListOfItemsDown):
    _sel_anchor: None | tuple[int, int] = None   # (line_idx, char_idx)
    _sel_cursor: None | tuple[int, int] = None   # (line_idx, char_idx)
    _dragging = False


    items: list[_TextLine]

    """
    Многострочный read-only текст.

    Каждая строка - отдельный _TextLine (register=False, read_only=True).
    Скролл, виртуальный диапазон и ползунок - унаследованы от
    CoreListOfItemsBase / CoreListOfItemsDown.
    """

    def __init__(self, page, left_top, width_height, font,
                 text="", size_px=16, color=(255, 255, 255),
                 distance=4, **kw):
        self._font = Font(font) if isinstance(font, str) else font
        self._size_px = size_px
        self._color = color        
        super().__init__(page, left_top, width_height,
                         items=None, distance=distance, **kw)
        self.items.extend(self._make_lines(text))
        self._rebuild_cache()
        
    # выделение текста

    def _hit_global(self, x, y):
        """Глобальные координаты (индекс строки, индекс символа).
        Если мышь выше/ниже viewport - попадаем в первую/последнюю строку.
        Если левее/правее строки - hit_test прижмёт к 0 или len(text)."""
        pos = (y - self._axis_offset()) + self.scroll_offset

        if pos < 0: return (0, 0)
        if pos >= self._total_length:
            last = len(self.items) - 1
            try:
                return (last, len(self.items[last].text))
            except IndexError:
                return None
            
        line_idx = find_index_at(self._prefix, self._sizes, pos)
        if line_idx < 0 or line_idx >= len(self.items): return None

        line = self.items[line_idx]
        lx = x - line.left
        if lx < 0: lx = 0
        if lx > line.img.width: lx = line.img.width
        return (line_idx, line.core.hit_test(lx, line.layout[0], line.layout[1]))

    def _apply_selection(self):
        """Пройтись по видимым строкам и сказать каждой её кусок выделения."""
        if self._sel_anchor is None or self._sel_cursor is None: sel = None
        else:
            a, c = self._sel_anchor, self._sel_cursor
            sel = (a, c) if a <= c else (c, a)

        if self.visible_start > self.visible_end: return

        for i in range(self.visible_start, self.visible_end + 1):
            line = self.items[i]
            n = len(line.text)

            if sel is None:
                line.clear()
                continue

            (sl, sc), (el, ec) = sel
            if i < sl or i > el:line.clear()
            elif sl == el == i: line.selection(sc, ec)
            elif i == sl:       line.selection(sc, n)
            elif i == el:       line.selection(0, ec)
            else:               line.selection(0, n)

    # рендр текста
    def _make_lines(self, text):
        items = []
        for raw in text.split("\n"):
            if not raw:
                continue
            items.append(_TextLine(self.page, (0, 0), self._font, raw, self._size_px, self._color))
        return items

    # _TextLine хранит высоту в .img, а не в .height
    def _item_size(self, item: _TextLine) -> int:
        return item.img.height

    def _scroll_by(self, delta):
        super()._scroll_by(delta)
        self._apply_selection()


    # события

    def mousebuttondown(self, common, button):
        if button.button in (4, 5): return super().mousebuttondown(common, button)
        if button.button != sdl2.SDL_BUTTON_LEFT: return False
        hit = self._hit_global(button.x, button.y)
        if hit is None:
            return False

        self._sel_anchor = self._sel_cursor = hit
        self._dragging = True
        self._apply_selection()
        return True


    def mousemotion(self, common, motion):
        if not self._dragging:
            return False

        # Автоскролл: если мышь выше/ниже viewport
        vy = self.top
        vh = self.height
        if motion.y < vy: self._scroll_by(-15)
        elif motion.y > vy + vh: self._scroll_by(15)
        hit = self._hit_global(motion.x, motion.y)
        if hit is None:
            return False

        self._sel_cursor = hit
        self._apply_selection()
        return True
    
    def mousebuttonup(self, common, button):
        if button.button == sdl2.SDL_BUTTON_LEFT:
            self._dragging = False
        return False

    def keydown(self, common, key):
        if key.keysym.sym == sdl2.SDLK_c and (key.keysym.mod & sdl2.KMOD_CTRL):
            try:
                text = self.get_selected_text()
                if text:
                    set_text_buffer(text)
            except BufferError as e:
                printError(f"[{self}] [BufferError] Не удалось положить текст в буфер.")
            except Exception as e:
                printError(f"[{self}] [{type(e).__name__}] {e}")
        if key.keysym.sym == sdl2.SDLK_a and (key.keysym.mod & sdl2.KMOD_CTRL):
            self.select_all()

    # публичный API
    
    def set_text(self, text: str) -> None:
        self.clear(is_update=False)
        self.items.extend(self._make_lines(text))
        self._rebuild_cache()

    def add_text(self, text: str) -> None:
        _max_scroll, scroll_offset = self._max_scroll, self.scroll_offset
        self.items.extend(self._make_lines(text))
        self._rebuild_cache()
        if _max_scroll == scroll_offset:
            self.scroll_offset = self._max_scroll

    def get_content(self) -> str:
        return "\n".join(it.text for it in self.items)

    @property
    def text(self) -> str:
        return self.get_content()
    @text.setter
    def text(self, text: str) -> None:
        self.set_text(text)



    def clear_selection(self):
        """Снять выделение со всех строк."""
        self._sel_anchor = None
        self._sel_cursor = None
        self._dragging = False
        for line in self.items:
            line.set_external_selection(None, None)


    def has_selection(self) -> bool:
        """Есть ли непустое выделение."""
        if self._sel_anchor is None or self._sel_cursor is None: return False
        return self._sel_anchor != self._sel_cursor


    def get_selection(self) -> tuple[int, int] | None:
        """Вернуть ((start_line, start_char), (end_line, end_char)) в нормализованном порядке.
        None если выделения нет."""
        if self._sel_anchor is None or self._sel_cursor is None: return None
        a, c = self._sel_anchor, self._sel_cursor
        return (a, c) if a <= c else (c, a)

    def get_selected_text(self) -> str:
        select = self.get_selection()
        if select is None:
            return ''

        res = ''
        (sl, sc), (el, ec) = select
        for i in range(sl, el):
            res += self.items[i].core.get_selected_text() + '\n'
        res += self.items[el].core.get_selected_text()
        return res

    def select(self, start_line, start_char, end_line, end_char):
        """Программно задать выделение. Порядок не важен — нормализуется внутри."""
        if not self.items: return
        sl = max(0, min(start_line, len(self.items) - 1))
        el = max(0, min(end_line, len(self.items) - 1))
        self._sel_anchor = (sl, max(0, min(start_char, len(self.items[sl].text))))
        self._sel_cursor = (el, max(0, min(end_char, len(self.items[el].text))))
        self._apply_selection()


    def select_all(self):
        """Выделить весь текст."""
        if not self.items: return
        self._sel_anchor = (0, 0)
        self._sel_cursor = (len(self.items) - 1, len(self.items[-1].text))
        self._apply_selection()
