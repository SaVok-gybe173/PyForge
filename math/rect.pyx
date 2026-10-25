# distutils: language = c
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True

from __future__ import annotations
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from .._core.game3D.rect cimport Rect3D

Coordinate = Tuple[int, int]
RectLike = Union["Rect", Tuple[int, int, int, int], Sequence[int]]


cdef class Rect:
    """
    Cython-реализация прямоугольника.

    Атрибуты:
        x: Координата X левого верхнего угла.
        y: Координата Y левого верхнего угла.
        w: Ширина прямоугольника.
        h: Высота прямоугольника.
    """

    # ВНИМАНИЕ: cdef-поля x/y/w/h объявлены в rect.pxd.
    # Здесь их повторно объявлять нельзя.


    def __init__(self, *args):
        """
        Инициализация прямоугольника.

        Поддерживаемые варианты:
            Rect()                              -> (0, 0, 0, 0)
            Rect(left, top, width, height)
            Rect((left, top), (width, height))
            Rect((left, top, width, height))
            Rect(other_rect)
            Rect(object_with_xywh_attributes)

        Raises:
            TypeError: Если аргументы не соответствуют ни одному формату.
        """
        cdef object arg, pos, size
        cdef Py_ssize_t n = len(args)

        if n == 0:
            self.x = self.y = self.w = self.h = 0
            return

        if n == 1:
            arg = args[0]
            if isinstance(arg, Rect):
                self.x = (<Rect>arg).x
                self.y = (<Rect>arg).y
                self.w = (<Rect>arg).w
                self.h = (<Rect>arg).h
                return
            if isinstance(arg, (tuple, list)):
                if len(arg) == 4:
                    self.x = int(arg[0])
                    self.y = int(arg[1])
                    self.w = int(arg[2])
                    self.h = int(arg[3])
                    return
                if len(arg) == 2:
                    pos, size = arg[0], arg[1]
                    self.x = int(pos[0])
                    self.y = int(pos[1])
                    self.w = int(size[0])
                    self.h = int(size[1])
                    return
            if (hasattr(arg, "x") and hasattr(arg, "y")
                    and hasattr(arg, "w") and hasattr(arg, "h")):
                self.x = int(arg.x)
                self.y = int(arg.y)
                self.w = int(arg.w)
                self.h = int(arg.h)
                return
            raise TypeError(f"Cannot create Rect from {arg!r}")

        if n == 2:
            pos, size = args[0], args[1]
            self.x = int(pos[0])
            self.y = int(pos[1])
            self.w = int(size[0])
            self.h = int(size[1])
            return

        if n == 4:
            self.x = int(args[0])
            self.y = int(args[1])
            self.w = int(args[2])
            self.h = int(args[3])
            return

        raise TypeError(f"Cannot create Rect from {args!r}")

    # Магические методы
    def __repr__(self):
        """Возвращает читаемое строковое представление прямоугольника."""
        return f"<Rect({self.x}, {self.y}, {self.w}, {self.h})>"

    def __iter__(self):
        """Позволяет распаковывать: x, y, w, h = rect."""
        yield self.x
        yield self.y
        yield self.w
        yield self.h

    def __len__(self):
        """Возвращает длину последовательности (всегда 4)."""
        return 4

    def __getitem__(self, index):
        """Поддерживает индексацию: rect[0] -> x, rect[3] -> h."""
        return (self.x, self.y, self.w, self.h)[index]

    def __eq__(self, other):
        """Сравнивает два прямоугольника по всем четырём полям."""
        cdef Rect r
        if isinstance(other, Rect):
            r = <Rect>other
            return (self.x == r.x and self.y == r.y
                    and self.w == r.w and self.h == r.h)
        if isinstance(other, (tuple, list)) and len(other) == 4:
            return (self.x, self.y, self.w, self.h) == tuple(other)
        return NotImplemented

    def __hash__(self):
        """Прямоугольники не хэшируются (изменяемая структура)."""
        raise TypeError(f"unhashable type: '{type(self).__name__}'")

    # Виртуальные атрибуты
    @property
    def top(self) -> int:
        """Верхняя граница прямоугольника (== y)."""
        return self.y

    @top.setter
    def top(self, value):
        self.y = int(value)

    @property
    def left(self) -> int:
        """Левая граница прямоугольника (== x)."""
        return self.x

    @left.setter
    def left(self, value):
        self.x = int(value)

    @property
    def bottom(self) -> int:
        """Нижняя граница прямоугольника (y + h)."""
        return self.y + self.h

    @bottom.setter
    def bottom(self, value):
        self.y = int(value) - self.h

    @property
    def right(self) -> int:
        """Правая граница прямоугольника (x + w)."""
        return self.x + self.w

    @right.setter
    def right(self, value):
        self.x = int(value) - self.w

    @property
    def centerx(self) -> int:
        """X-координата центра прямоугольника."""
        return self.x + (self.w >> 1)

    @centerx.setter
    def centerx(self, value):
        self.x = int(value) - (self.w >> 1)

    @property
    def centery(self) -> int:
        """Y-координата центра прямоугольника."""
        return self.y + (self.h >> 1)

    @centery.setter
    def centery(self, value):
        self.y = int(value) - (self.h >> 1)

    @property
    def center(self) -> Coordinate:
        """Координата центра прямоугольника (centerx, centery)."""
        return (self.x + (self.w >> 1), self.y + (self.h >> 1))

    @center.setter
    def center(self, value):
        self.x = int(value[0]) - (self.w >> 1)
        self.y = int(value[1]) - (self.h >> 1)

    @property
    def topleft(self) -> Coordinate:
        """Координата левого верхнего угла (x, y)."""
        return (self.x, self.y)

    @topleft.setter
    def topleft(self, value):
        self.x = int(value[0])
        self.y = int(value[1])

    @property
    def topright(self) -> Coordinate:
        """Координата правого верхнего угла (right, top)."""
        return (self.x + self.w, self.y)

    @topright.setter
    def topright(self, value):
        self.x = int(value[0]) - self.w
        self.y = int(value[1])

    @property
    def bottomleft(self) -> Coordinate:
        """Координата левого нижнего угла (left, bottom)."""
        return (self.x, self.y + self.h)

    @bottomleft.setter
    def bottomleft(self, value):
        self.x = int(value[0])
        self.y = int(value[1]) - self.h

    @property
    def bottomright(self) -> Coordinate:
        """Координата правого нижнего угла (right, bottom)."""
        return (self.x + self.w, self.y + self.h)

    @bottomright.setter
    def bottomright(self, value):
        self.x = int(value[0]) - self.w
        self.y = int(value[1]) - self.h

    @property
    def midtop(self) -> Coordinate:
        """Середина верхней стороны (centerx, top)."""
        return (self.x + (self.w >> 1), self.y)

    @midtop.setter
    def midtop(self, value):
        self.x = int(value[0]) - (self.w >> 1)
        self.y = int(value[1])

    @property
    def midleft(self) -> Coordinate:
        """Середина левой стороны (left, centery)."""
        return (self.x, self.y + (self.h >> 1))

    @midleft.setter
    def midleft(self, value):
        self.x = int(value[0])
        self.y = int(value[1]) - (self.h >> 1)

    @property
    def midbottom(self) -> Coordinate:
        """Середина нижней стороны (centerx, bottom)."""
        return (self.x + (self.w >> 1), self.y + self.h)

    @midbottom.setter
    def midbottom(self, value):
        self.x = int(value[0]) - (self.w >> 1)
        self.y = int(value[1]) - self.h

    @property
    def midright(self) -> Coordinate:
        """Середина правой стороны (right, centery)."""
        return (self.x + self.w, self.y + (self.h >> 1))

    @midright.setter
    def midright(self, value):
        self.x = int(value[0]) - self.w
        self.y = int(value[1]) - (self.h >> 1)

    @property
    def size(self) -> Coordinate:
        """Размер прямоугольника (w, h)."""
        return (self.w, self.h)

    @size.setter
    def size(self, value):
        self.w = int(value[0])
        self.h = int(value[1])

    @property
    def width(self) -> int:
        """Ширина прямоугольника (== w)."""
        return self.w

    @width.setter
    def width(self, value):
        self.w = int(value)

    @property
    def height(self) -> int:
        """Высота прямоугольника (== h)."""
        return self.h

    @height.setter
    def height(self, value):
        self.h = int(value)

    # Копирование
    def copy(self) -> Rect:
        """Возвращает новый прямоугольник с теми же позицией и размером."""
        return Rect(self.x, self.y, self.w, self.h)

    # Перемещение и изменение размера
    def move(self, int x, int y) -> Rect:
        """
        Возвращает новый прямоугольник, смещённый на (x, y).

        Args:
            x: Смещение по горизонтали.
            y: Смещение по вертикали.

        Returns:
            Новый экземпляр Rect.
        """
        return Rect(self.x + x, self.y + y, self.w, self.h)

    def move_ip(self, int x, int y) -> None:
        """
        Смещает прямоугольник на (x, y) на месте (in-place).

        Args:
            x: Смещение по горизонтали.
            y: Смещение по вертикали.
        """
        self.x += x
        self.y += y

    def inflate(self, int x, int y) -> Rect:
        """
        Возвращает новый прямоугольник, размер которого изменён на (x, y).

        Прямоугольник остаётся центрированным относительно текущего центра.
        Отрицательные значения уменьшают размер.

        Args:
            x: Изменение ширины.
            y: Изменение высоты.

        Returns:
            Новый экземпляр Rect.
        """
        return Rect(self.x - (x >> 1), self.y - (y >> 1),
                    self.w + x, self.h + y)

    def inflate_ip(self, int x, int y) -> None:
        """
        Изменяет размер прямоугольника на (x, y) на месте (in-place).

        Args:
            x: Изменение ширины.
            y: Изменение высоты.
        """
        self.x -= (x >> 1)
        self.y -= (y >> 1)
        self.w += x
        self.h += y

    def clamp(self, other) -> Rect:
        """
        Возвращает новый прямоугольник, перемещённый внутрь `other`.

        Если прямоугольник слишком велик, он центрируется внутри `other`,
        но его размер не меняется.

        Args:
            other: Прямоугольник, в который нужно поместиться.

        Returns:
            Новый экземпляр Rect.
        """
        cdef Rect result = Rect(self.x, self.y, self.w, self.h)
        result.clamp_ip(other)
        return result

    def clamp_ip(self, other) -> None:
        """
        Перемещает прямоугольник внутрь `other` на месте (in-place).

        Args:
            other: Прямоугольник, в который нужно поместиться.
        """
        cdef Rect o
        if isinstance(other, Rect):
            o = <Rect>other
        else:
            o = Rect(other)

        if self.w >= o.w:
            self.x = o.x + ((o.w - self.w) >> 1)
        elif self.x < o.x:
            self.x = o.x
        elif self.x + self.w > o.x + o.w:
            self.x = o.x + o.w - self.w

        if self.h >= o.h:
            self.y = o.y + ((o.h - self.h) >> 1)
        elif self.y < o.y:
            self.y = o.y
        elif self.y + self.h > o.y + o.h:
            self.y = o.y + o.h - self.h

    def clip(self, other) -> Rect:
        """
        Возвращает новый прямоугольник, обрезанный по границам `other`.

        Если прямоугольники не пересекаются, возвращается Rect нулевого размера.

        Args:
            other: Прямоугольник, по которому обрезается текущий.

        Returns:
            Новый экземпляр Rect.
        """
        cdef Rect o
        if isinstance(other, Rect):
            o = <Rect>other
        else:
            o = Rect(other)
        cdef int x1 = self.x if self.x > o.x else o.x
        cdef int y1 = self.y if self.y > o.y else o.y
        cdef int sx2 = self.x + self.w
        cdef int ox2 = o.x + o.w
        cdef int x2 = sx2 if sx2 < ox2 else ox2
        cdef int sy2 = self.y + self.h
        cdef int oy2 = o.y + o.h
        cdef int y2 = sy2 if sy2 < oy2 else oy2
        if x2 <= x1 or y2 <= y1:
            return Rect(self.x, self.y, 0, 0)
        return Rect(x1, y1, x2 - x1, y2 - y1)

    def fit(self, other) -> Rect:
        """
        Возвращает новый прямоугольник, масштабированный и перемещённый,
        чтобы вписаться в `other` с сохранением пропорций.

        Args:
            other: Целевой прямоугольник.

        Returns:
            Новый экземпляр Rect.
        """
        cdef Rect o
        if isinstance(other, Rect):
            o = <Rect>other
        else:
            o = Rect(other)
        if self.w <= 0 or self.h <= 0 or o.w <= 0 or o.h <= 0:
            return Rect(o.x, o.y, 0, 0)

        cdef double aspect_self = <double>self.w / <double>self.h
        cdef double aspect_other = <double>o.w / <double>o.h
        cdef int new_w, new_h

        if aspect_self > aspect_other:
            new_w = o.w
            new_h = <int>(o.w / aspect_self)
        else:
            new_h = o.h
            new_w = <int>(o.h * aspect_self)

        cdef int new_x = o.x + ((o.w - new_w) >> 1)
        cdef int new_y = o.y + ((o.h - new_h) >> 1)
        return Rect(new_x, new_y, new_w, new_h)

    def normalize(self) -> None:
        """
        Исправляет отрицательные значения ширины или высоты на месте (in-place).

        Меняет местами стороны, если размер отрицательный.
        """
        if self.w < 0:
            self.x += self.w
            self.w = -self.w
        if self.h < 0:
            self.y += self.h
            self.h = -self.h

    # Проверка коллизий
    def colliderect(self, other) -> bool:
        """
        Проверяет, пересекаются ли два прямоугольника.

        Прямоугольники с нулевой шириной или высотой никогда не пересекаются.

        Args:
            other: Другой прямоугольник.

        Returns:
            True, если прямоугольники пересекаются.
        """
        cdef Rect o
        if isinstance(other, Rect):
            o = <Rect>other
        else:
            o = Rect(other)
        if self.w <= 0 or self.h <= 0 or o.w <= 0 or o.h <= 0:
            return False
        return (self.x < o.x + o.w and o.x < self.x + self.w
                and self.y < o.y + o.h and o.y < self.y + self.h)

    def collidepoint(self, int x, int y) -> bool:
        """
        Проверяет, находится ли точка (x, y) внутри прямоугольника.

        Точки на правой или нижней границе не считаются внутри.

        Args:
            x: Координата X точки.
            y: Координата Y точки.

        Returns:
            True, если точка внутри.
        """
        return (self.x <= x < self.x + self.w
                and self.y <= y < self.y + self.h)

    def contains(self, other) -> bool:
        """
        Проверяет, полностью ли `other` находится внутри текущего прямоугольника.

        Args:
            other: Прямоугольник для проверки.

        Returns:
            True, если `other` полностью внутри.
        """
        cdef Rect o
        if isinstance(other, Rect):
            o = <Rect>other
        else:
            o = Rect(other)
        return (self.x <= o.x and self.y <= o.y
                and o.x + o.w <= self.x + self.w
                and o.y + o.h <= self.y + self.h)

    def collidelist(self, other_list) -> int:
        """
        Возвращает индекс первого пересекающегося прямоугольника из списка.

        Args:
            other_list: Последовательность прямоугольников.

        Returns:
            Индекс или -1, если пересечений нет.
        """
        cdef int i = 0
        for r in other_list:
            if self.colliderect(r):
                return i
            i += 1
        return -1

    def collidelistall(self, other_list) -> List[int]:
        """
        Возвращает список индексов всех пересекающихся прямоугольников.

        Args:
            other_list: Последовательность прямоугольников.

        Returns:
            Список индексов.
        """
        return [i for i, r in enumerate(other_list) if self.colliderect(r)]

    def collidedict(self, other_dict, rects_values: int = 0) -> Optional[Tuple[Any, Any]]:
        """
        Возвращает пару (ключ, значение) первого пересекающегося элемента словаря.

        Args:
            other_dict: Словарь с прямоугольниками.
            rects_values: 0 — прямоугольники в значениях, 1 — в ключах.

        Returns:
            Кортеж (ключ, значение) или None.
        """
        for key, value in other_dict.items():
            r = key if rects_values == 1 else value
            if self.colliderect(r):
                return (key, value)
        return None

    def collidedictall(self, other_dict, rects_values: int = 0) -> List[Tuple[Any, Any]]:
        """
        Возвращает список всех пересекающихся пар (ключ, значение).

        Args:
            other_dict: Словарь с прямоугольниками.
            rects_values: 0 — прямоугольники в значениях, 1 — в ключах.

        Returns:
            Список кортежей (ключ, значение).
        """
        return [(key, value) for key, value in other_dict.items()
                if self.colliderect(key if rects_values == 1 else value)]

    # Объединение и промежутки
    def union(self, other) -> Rect:
        """
        Возвращает новый прямоугольник, охватывающий оба прямоугольника.

        Args:
            other: Другой прямоугольник.

        Returns:
            Новый экземпляр Rect.
        """
        cdef Rect result = Rect(self.x, self.y, self.w, self.h)
        result.union_ip(other)
        return result

    def union_ip(self, other) -> None:
        """
        Расширяет текущий прямоугольник, чтобы охватить `other`, на месте.

        Args:
            other: Другой прямоугольник.
        """
        cdef Rect o
        if isinstance(other, Rect):
            o = <Rect>other
        else:
            o = Rect(other)
        cdef int x1 = self.x if self.x < o.x else o.x
        cdef int y1 = self.y if self.y < o.y else o.y
        cdef int sx2 = self.x + self.w
        cdef int ox2 = o.x + o.w
        cdef int x2 = sx2 if sx2 > ox2 else ox2
        cdef int sy2 = self.y + self.h
        cdef int oy2 = o.y + o.h
        cdef int y2 = sy2 if sy2 > oy2 else oy2
        self.x = x1
        self.y = y1
        self.w = x2 - x1
        self.h = y2 - y1

    def unionall(self, other_seq) -> Rect:
        """
        Возвращает новый прямоугольник — объединение с последовательностью.

        Args:
            other_seq: Последовательность прямоугольников.

        Returns:
            Новый экземпляр Rect.
        """
        cdef Rect result = Rect(self.x, self.y, self.w, self.h)
        result.unionall_ip(other_seq)
        return result

    def unionall_ip(self, other_seq) -> None:
        """
        Расширяет текущий прямоугольник, чтобы охватить последовательность.

        Args:
            other_seq: Последовательность прямоугольников.
        """
        for r in other_seq:
            self.union_ip(r)

    def gap(self, other) -> Rect:
        """
        Возвращает новый прямоугольник, представляющий промежуток между двумя
        прямоугольниками. Если прямоугольники пересекаются — Rect нулевого размера.

        Args:
            other: Другой прямоугольник.

        Returns:
            Новый экземпляр Rect.
        """
        cdef Rect o
        if isinstance(other, Rect):
            o = <Rect>other
        else:
            o = Rect(other)
        if self.colliderect(o):
            return Rect(self.x, self.y, 0, 0)

        cdef int gx, gw, gy, gh

        if self.x + self.w <= o.x:
            gx = self.x + self.w
            gw = o.x - gx
        elif o.x + o.w <= self.x:
            gx = o.x + o.w
            gw = self.x - gx
        else:
            gx = self.x
            gw = 0

        if self.y + self.h <= o.y:
            gy = self.y + self.h
            gh = o.y - gy
        elif o.y + o.h <= self.y:
            gy = o.y + o.h
            gh = self.y - gy
        else:
            gy = self.y
            gh = 0

        return Rect(gx, gy, gw, gh)

    # Мост в SDL2
    def to_sdl(self):
        """
        Возвращает эквивалентную структуру ``sdl2.SDL_Rect``.

        Требует установленного пакета ``PySDL2``. Полезно для передачи
        в C-функции SDL2 (SDL_RenderCopy, SDL_BlitSurface и т.п.).

        Returns:
            Экземпляр ``sdl2.SDL_Rect``.
        """
        import sdl2
        return sdl2.SDL_Rect(self.x, self.y, self.w, self.h)