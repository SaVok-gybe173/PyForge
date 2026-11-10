"""Многострочный read-only текст на базе виртуального списка."""
from __future__ import annotations

from .line import _TextLine
from ..listing.down import CoreListOfItemsDown
from ....easel import Window, Surface, PfObjectIMG
from ....pfmath.markup import Point, Size
from ....font.ttf import Font, render_text

from dataclasses import dataclass



class _BigText(CoreListOfItemsDown):
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

    def _make_lines(self, text):
        items = []
        for raw in text.split("\n"):
            if not raw:
                continue
            items.append(_TextLine(self.page, (0, 0), self._font, raw, self._size_px, self._color))
        return items

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