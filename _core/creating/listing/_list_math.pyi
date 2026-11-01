"""
Тип-стабы для _list_math (Cython-модуль + pure-Python fallback).
Все числовые параметры знаковые 64-битные (C `long long`).
Возвращаемые массивы `array.array('q')` (типизированный буфер, memoryview-friendly).
"""

from __future__ import annotations
from array import array
from typing import TypeAlias
Int64Array: TypeAlias = array[int] # array('q') — знаковые 64-битные целые.

# построение
def build_prefix(sizes: Int64Array, distance: int = 0) -> Int64Array: ...

def total_length(prefix: Int64Array, sizes: Int64Array) -> int: ...

# поиск
def find_visible_range(
    prefix: Int64Array,
    sizes: Int64Array,
    scroll_offset: int,
    view_length: int,
) -> tuple[int, int]:
    """
    Возвращает (start, end) включительно.
    Если ничего не видно — (n, n - 1), т.е. start > end.
    """
    ...

def find_index_at(
    prefix: Int64Array,
    sizes: Int64Array,
    content_pos: int,
) -> int:
    """
    Индекс элемента, содержащего content_pos, или -1
    (включая случай попадания в зазор между элементами).
    """
    ...

# ползунок
def scroll_metrics(
    total_length: int,
    view_length: int,
    min_thumb: int,
) -> tuple[int, int, int]:
    """
    Возвращает кортеж (max_scroll, thumb_size, thumb_travel).

    - max_scroll: максимальное смещение контента (>=0).
    - thumb_size: длина ползунка в пикселях (<=view_length).
    - thumb_travel: сколько пикселей может пройти ползунок (view_length - thumb_size).
    """

def thumb_from_scroll(
    scroll: int,
    max_scroll: int,
    thumb_travel: int,
) -> int: ...

def scroll_from_thumb(
    thumb: int,
    max_scroll: int,
    thumb_travel: int,
) -> int: ...

# утилиты
def clamp(v: int, lo: int, hi: int) -> int: ...
