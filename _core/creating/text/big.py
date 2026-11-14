"""Многострочный read-only текст на базе виртуального списка."""
from __future__ import annotations

from .line import _TextLine
from ..listing.down import CoreListOfItemsDown
from ....easel import Window, Surface, PfObjectIMG
from ....pfmath.markup import Point, Size
from ....font.ttf import Font, render_text
from ..listing._list_math import find_index_at

from dataclasses import dataclass

import sdl2

class _BigText(CoreListOfItemsDown):
    _sel_anchor = None | tuple[int, int]    # (line_idx, char_idx)
    _sel_cursor = None | tuple[int, int]    # (line_idx, char_idx)
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
    def _normalized_selection(self) -> None | tuple[int, int]: # нармальзация
        if self._sel_anchor is None or self._sel_cursor is None:
            return None
        a, c = self._sel_anchor, self._sel_cursor
        return (a, c) if a <= c else (c, a)

    def _hit_global(self, x, y):
        """Глобальные координаты (индекс строки, индекс символа).
        Если мышь выше/ниже viewport - попадаем в первую/последнюю строку.
        Если левее/правее строки - hit_test прижмёт к 0 или len(text)."""
        pos = (y - self._axis_offset()) + self.scroll_offset

        if pos < 0: return (0, 0)
        if pos >= self._total_length:
            last = len(self.items) - 1
            return (last, len(self.items[last].text))

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

    # публичный API
    def set_text(self, text: str) -> None:
        self.clear(is_update=False)
        self.items.extend(self._make_lines(text))
        self._rebuild_cache()

    def get_content(self) -> str:
        return "\n".join(it.text for it in self.items)

    @property
    def text(self) -> str:
        return self.get_content()

    # события

    def mousebuttondown(self, common, button):
        if button.button in (4, 5):
            return super().mousebuttondown(common, button)
        if button.button != sdl2.SDL_BUTTON_LEFT:
            return False

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
        super().keydown(common, key)
