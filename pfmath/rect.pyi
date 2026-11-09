from __future__ import annotations
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

# Псевдонимы типов для удобства чтения
Coordinate = Tuple[int, int]
RectLike = Union["Rect", Tuple[int, int, int, int]]
RectSequence = Sequence[RectLike]


class Rect:
    """
    Класс для хранения и манипуляции прямоугольными областями.
    
    Атрибуты:
        x: Координата X левого верхнего угла.
        y: Координата Y левого верхнего угла.
        w: Ширина прямоугольника.
        h: Высота прямоугольника.
    """
    x: int
    y: int
    w: int
    h: int

    def __init__(
        self,
        *args: Union[
            Tuple[int, int, int, int],
            Tuple[Coordinate, Coordinate],
            RectLike,
        ],
    ) -> None:
        """
        Инициализация прямоугольника.
        
        Поддерживаемые варианты:
            Rect(left, top, width, height)
            Rect((left, top), (width, height))
            Rect(object_with_rect_attr)
            Rect(other_rect)
        
        Raises:
            TypeError: Если аргументы не соответствуют ни одному из форматов.
        """
        ...

    # Методы копирования и создания новых прямоугольников
    def copy(self) -> Rect:
        """
        Возвращает новый прямоугольник с теми же позицией и размером.
        
        Returns:
            Новый экземпляр Rect.
        """
        ...

    # Методы перемещения и изменения размера (возвращают новый Rect)
    def move(self, x: int, y: int) -> Rect:
        """
        Возвращает новый прямоугольник, смещённый на (x, y).
        
        Args:
            x: Смещение по горизонтали.
            y: Смещение по вертикали.
        
        Returns:
            Новый экземпляр Rect.
        """
        ...

    def move_ip(self, x: int, y: int) -> None:
        """
        Смещает прямоугольник на (x, y) на месте (in-place).
        
        Args:
            x: Смещение по горизонтали.
            y: Смещение по вертикали.
        """
        ...

    def inflate(self, x: int, y: int) -> Rect:
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
        ...

    def inflate_ip(self, x: int, y: int) -> None:
        """
        Изменяет размер прямоугольника на (x, y) на месте (in-place).
        
        Args:
            x: Изменение ширины.
            y: Изменение высоты.
        """
        ...

    def clamp(self, other: RectLike) -> Rect:
        """
        Возвращает новый прямоугольник, перемещённый внутрь `other`.
        
        Если прямоугольник слишком велик, чтобы поместиться, он центрируется
        внутри `other`, но его размер не меняется.
        
        Args:
            other: Прямоугольник, в который нужно поместиться.
        
        Returns:
            Новый экземпляр Rect.
        """
        ...

    def clamp_ip(self, other: RectLike) -> None:
        """
        Перемещает прямоугольник внутрь `other` на месте (in-place).
        
        Args:
            other: Прямоугольник, в который нужно поместиться.
        """
        ...

    def clip(self, other: RectLike) -> Rect:
        """
        Возвращает новый прямоугольник, обрезанный по границам `other`.
        
        Если прямоугольники не пересекаются, возвращается Rect нулевого размера.
        
        Args:
            other: Прямоугольник, по которому обрезается текущий.
        
        Returns:
            Новый экземпляр Rect.
        """
        ...

    def fit(self, other: RectLike) -> Rect:
        """
        Возвращает новый прямоугольник, масштабированный и перемещённый,
        чтобы вписаться в `other` с сохранением пропорций.
        
        Args:
            other: Целевой прямоугольник.
        
        Returns:
            Новый экземпляр Rect.
        """
        ...

    def normalize(self) -> None:
        """
        Исправляет отрицательные значения ширины или высоты на месте (in-place).
        
        Меняет местами стороны, если размер отрицательный.
        """
        ...

    # Методы проверки коллизий
    def colliderect(self, other: RectLike) -> bool:
        """
        Проверяет, пересекаются ли два прямоугольника.
        
        Args:
            other: Другой прямоугольник.
        
        Returns:
            True, если прямоугольники пересекаются.
        """
        ...

    def collidepoint(self, x: int, y: int) -> bool:
        """
        Проверяет, находится ли точка (x, y) внутри прямоугольника.
        
        Точки на правой или нижней границе не считаются внутри.
        
        Args:
            x: Координата X точки.
            y: Координата Y точки.
        
        Returns:
            True, если точка внутри.
        """
        ...

    def contains(self, other: RectLike) -> bool:
        """
        Проверяет, полностью ли `other` находится внутри текущего прямоугольника.
        
        Args:
            other: Прямоугольник для проверки.
        
        Returns:
            True, если `other` полностью внутри.
        """
        ...

    def collidelist(self, other_list: Sequence[RectLike]) -> int:
        """
        Возвращает индекс первого прямоугольника из списка, пересекающегося с текущим.
        
        Args:
            other_list: Последовательность прямоугольников.
        
        Returns:
            Индекс первого пересекающегося прямоугольника или -1, если пересечений нет.
        """
        ...

    def collidelistall(self, other_list: Sequence[RectLike]) -> List[int]:
        """
        Возвращает список индексов всех прямоугольников из списка, пересекающихся с текущим.
        
        Args:
            other_list: Последовательность прямоугольников.
        
        Returns:
            Список индексов пересекающихся прямоугольников.
        """
        ...

    def collidedict(self, other_dict: Dict[Any, RectLike]) -> Optional[Tuple[Any, RectLike]]:
        """
        Возвращает пару (ключ, значение) первого прямоугольника из словаря,
        пересекающегося с текущим.
        
        Args:
            other_dict: Словарь, значения которого — прямоугольники.
        
        Returns:
            Кортеж (ключ, значение) или None, если пересечений нет.
        """
        ...

    def collidedictall(
        self,
        other_dict: Dict[Any, RectLike],
        rects_values: int = 0,
    ) -> List[Tuple[Any, RectLike]]:
        """
        Возвращает список пар (ключ, значение) всех прямоугольников из словаря,
        пересекающихся с текущим.
        
        Args:
            other_dict: Словарь, значения которого — прямоугольники.
            rects_values: Флаг, указывающий, какие значения сравнивать (0 или 1).
        
        Returns:
            Список кортежей (ключ, значение) для всех пересекающихся прямоугольников.
        """
        ...

    # Методы объединения
    def union(self, other: RectLike) -> Rect:
        """
        Возвращает новый прямоугольник, охватывающий область обоих прямоугольников.
        
        Args:
            other: Другой прямоугольник.
        
        Returns:
            Новый экземпляр Rect.
        """
        ...

    def union_ip(self, other: RectLike) -> None:
        """
        Расширяет текущий прямоугольник, чтобы охватить область `other`, на месте.
        
        Args:
            other: Другой прямоугольник.
        """
        ...

    def unionall(self, other_seq: RectSequence) -> Rect:
        """
        Возвращает новый прямоугольник, являющийся объединением текущего
        и последовательности других прямоугольников.
        
        Args:
            other_seq: Последовательность прямоугольников.
        
        Returns:
            Новый экземпляр Rect.
        """
        ...

    def unionall_ip(self, other_seq: RectSequence) -> None:
        """
        Расширяет текущий прямоугольник, чтобы охватить последовательность
        других прямоугольников, на месте.
        
        Args:
            other_seq: Последовательность прямоугольников.
        """
        ...

    def gap(self, other: RectLike) -> Rect:
        """
        Возвращает новый прямоугольник, представляющий промежуток между двумя прямоугольниками.
        
        Если прямоугольники пересекаются, возвращается Rect нулевого размера.
        
        Args:
            other: Другой прямоугольник.
        
        Returns:
            Новый экземпляр Rect.
        """
        ...

    # Виртуальные атрибуты (свойства)
    top: int
    left: int
    bottom: int
    right: int
    center: Coordinate
    centerx: int
    centery: int
    topleft: Coordinate
    topright: Coordinate
    bottomleft: Coordinate
    bottomright: Coordinate
    midtop: Coordinate
    midleft: Coordinate
    midbottom: Coordinate
    midright: Coordinate
    size: Coordinate
    width: int
    height: int