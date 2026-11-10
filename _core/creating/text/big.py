"""Многострочный read-only текст на базе виртуального списка."""
from __future__ import annotations

from .line import _TextLine
from ..listing.down import CoreListOfItemsDown
from ....easel.window import Window
from ....pfmath.markup import Point, Size
from ....font.ttf.font import Font


class _BigText(CoreListOfItemsDown):
    """
    Многострочный read-only текст.

    Каждая строка - отдельный _TextLine (register=False, read_only=True).
    Скролл, виртуальный диапазон и ползунок - унаследованы от
    CoreListOfItemsBase / CoreListOfItemsDown.
    """

    def __init__(
        self,
        page: Window,
        left_top: Point | tuple[int, int],
        width_height: Size | tuple[int, int],
        font: str | Font,
        text: str = "",
        size_px: int = 16,
        color: tuple[int, int, int] = (255, 255, 255),
        distance: int = 4,
        **kw,
    ) -> None:
        self._font = Font(font) if isinstance(font, str) else font
        self._size_px = size_px
        self._color = color

        items = self._make_lines(page, text)
        super().__init__(
            page, left_top, width_height,
            items=items, distance=distance, **kw,
        )

    # внутреннее
    def _make_lines(self, page: Window, text: str) -> list[_TextLine]:
        return [
            _TextLine(
                page, (0, 0), self._font, raw, self._size_px, self._color,
                register=False, read_only=True,
            )
            for raw in text.split("\n")
        ]

    # _TextLine хранит высоту в .img, а не в .height
    def _item_size(self, item: _TextLine) -> int:
        return item.img.height

    # публичный API
    def set_text(self, text: str) -> None:
        self.clear(is_update=False)
        self.items.extend(self._make_lines(self._page, text))
        self._rebuild_cache()

    def get_content(self) -> str:
        return "\n".join(it.text for it in self.items)

    @property
    def text(self) -> str:
        return self.get_content()