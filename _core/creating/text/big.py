"""Многострочный read-only текст на базе виртуального списка."""
from __future__ import annotations

from .line import _TextLine
from ..listing.down import CoreListOfItemsDown
from ....easel import Window, Surface, PfObjectIMG
from ....pfmath.markup import Point, Size
from ....font.ttf import Font, render_text

from dataclasses import dataclass

import sdl2

class _BigText(CoreListOfItemsDown):
    _sel_anchor = None | tuple[int, int]    # (line_idx, char_idx)
    _sel_cursor = None | tuple[int, int]    # (line_idx, char_idx)
    dragging = False

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
        if button.button == sdl2.SDL_BUTTON_LEFT:
            index = self.index()
            if not index is None:
                self._sel_anchor = (index, self.items[index].core.selectionX)
                super().mousebuttondown(common, button)
                self.dragging = True

    def mousemotion(self, common, motion):
        if self.dragging:
            super().mousemotion(common, motion)
    
    def mousebuttonup(self, common, button):
        super().mousebuttonup(common, button)

    def keydown(self, common, key):
        super().keydown(common, key)