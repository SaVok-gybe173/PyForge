"""
Модуль для работы с кординатами и с размерами
"""
from ..tools import cordinate_transformation, relationship_transformation
from .._core.locals import GRAPHICS, GRAPHICS_GL_2D_ORTHO, GRAPHICS_PYGAME
from typing import Type, overload, Final, Literal, TypeAlias

# Флаги для классов
SIZE_RELATIONSHIP: Final[str]   = "size-relationship"
SIZE_PIXEL: Final[str]          = "size-pixel"

POINT_RELATIONSHIP: Final[str]  = "point-relationship"
POINT_PIXEL: Final[str]         = "point-pixel"

# типы
PointType: TypeAlias = Literal["point_pixel", "point_relationship"]
SizeType:  TypeAlias = Literal["size_pixel", "size_relationship"]

PixelCoord: TypeAlias = tuple[int, int]
RelCoord:   TypeAlias = tuple[float, float]
Coord:      TypeAlias = PixelCoord | RelCoord

#
def isListType(ls: tuple | set | list, len: int = 2, type: Type = int) -> bool:
    """
    Проверяет тип в массиве
    
    Args:
        ls (tuple | set | list):    Массив в котором храняться данные
        len (int):                  Длина массива
        type (Type):                Тип в массиве
        
    Return:
        bool: Если в масииве храняться int и длиной 2
    
    """
    try:
        if ls.__len__() == len:
            for i in ls:
                if not isinstance(i, type): return False
            else:
                return True
    except: ...
    return False

class _General:
    """
    Изначальная структура для вычеслений
    """
    _pixel: PixelCoord      # по пиксельно
    _relationship: RelCoord # относительно

    def __init__(self, num1: int, num2: int, type_data: str):
        """
        Сохраняет входные данные и запускает пересчёт.

        Args:
            num1: Первая компонента (x для точки, ширина для размера).
            num2: Вторая компонента (y для точки, высота для размера).
            type_data: Флаг системы координат входных данных. Допустимые
                значения задаются константами модуля и проверяются в
                :meth:`update`.

        Raises:
            ValueError: Если ``type_data`` не поддерживается конкретным
                наследником.
        """
        self.type = type_data
        self.data = (num1, num2)
        self.update()

    def update(self) -> None: 
        """Пересчитывает координаты во всех поддерживаемых системах.

        Вызывается автоматически из :meth:`__init__`, но может быть вызван
        повторно, если пользователь изменил ``data`` или ``type`` напрямую.

        Raises:
            NotImplementedError: Всегда, если наследник не переопределил
                метод.
        """
        raise NotImplementedError

    def get(self):
        """Возвращает координаты в системе активного бэкенда.

        Returns:
            Пиксельные координаты, если активен ``GRAPHICS_GL_2D_ORTHO``
            или ``GRAPHICS_PYGAME``; иначе — нормализованные координаты
            для OpenGL.
        """
        if GRAPHICS.get() == GRAPHICS_GL_2D_ORTHO or GRAPHICS.get() == GRAPHICS_PYGAME:
            return self._pixel
        else:
            return self._relationship

    # попиксельные размеры/кординаты
    @property
    def pixel(self) -> PixelCoord:
        """Координаты в пикселях экрана."""
        return self._pixel

    @pixel.setter
    def pixel(self, pix: PixelCoord) -> None:
        """Задаёт пиксельные координаты и пересчитывает относительные.

        Args:
            pix: Пара ``(x, y)`` в пикселях.
        """
        self._pixel = cordinate_transformation(pix)

    @property
    def relationship(self) -> RelCoord:
        """Координаты в нормализованном диапазоне OpenGL."""
        return self._relationship

    @relationship.setter
    def relationship(self, rel: RelCoord) -> None:
        """Задаёт относительные координаты и пересчитывает пиксельные.

        Args:
            rel: Пара ``(x, y)`` в диапазоне ``[0.0, 1.0]`` (обычно).
        """
        self._relationship = rel
        self._pixel = relationship_transformation(rel)


class Size(_General):
    """Размер прямоугольной области в двух системах координат.

    Поддерживает два способа создания — парой чисел или кортежем::

        Size(100, 50)               # width=100, height=50
        Size((100, 50))             # то же самое
        Size((0.5, 0.25), SIZE_RELATIONSHIP)

    Attributes:
        type: Одно из ``SIZE_PIXEL`` или ``SIZE_RELATIONSHIP``.
        data: Исходная пара ``(width, height)``.

    Example:
        >>> s = Size(1920, 1080)
        >>> s.pixel
        (1920, 1080)
        >>> s.relationship
        (1.0, 1.0)
    """

    type: SizeType
    data: PixelCoord

    @overload
    def __init__(self, data: PixelCoord, type_data: SizeType = ...) -> None: ...
    @overload
    def __init__(self, num1: int, num2: int, type_data: SizeType = ...) -> None: ...
    def __init__(
        self,
        num1: int | PixelCoord,
        num2: int | None = None,
        type_data: SizeType = SIZE_PIXEL,
    ) -> None:
        """Создаёт размер.

        Args:
            num1: Ширина, либо кортеж ``(width, height)``.
            num2: Высота. Должна быть ``None``, если ``num1`` — кортеж.
            type_data: Система координат входных данных —
                ``SIZE_PIXEL`` (по умолчанию) или ``SIZE_RELATIONSHIP``.

        Raises:
            TypeError: Если ``num1`` — не кортеж, а ``num2`` не задан.
            ValueError: Если ``type_data`` не поддерживается.
        """
        if num2 is None:
            if not isinstance(num1, tuple):
                raise TypeError("Ожидался tuple[int, int]")
            num1, num2 = num1
        super().__init__(num1, num2, type_data)

    def update(self):
        """Пересчитывает размер в пикселях и в относительных единицах.

        Raises:
            ValueError: Если ``self.type`` не входит в ``SizeType``.
        """

        if self.type == SIZE_PIXEL:
            self.relationship =  relationship_transformation(self.data)
            self.pixel = self.data
        elif self.type == SIZE_RELATIONSHIP:
            self.pixel = cordinate_transformation(self.data)
            self.relationship = self.data
        else:
            raise ValueError(f"тип: {self.type} не существует")
    
        
class Point(_General):
    """Кординаты прямоугольной области в двух системах координат.
    
    Поддерживает два способа создания — парой чисел или кортежем::
    
        Point(100, 50)              # left=100, top=50
        Point((100, 50))            # то же самое
        Point((0.5, 0.25), POINT_RELATIONSHIP)
    
    Attributes:
        type: Одно из ``POINT_PIXEL`` или ``POINT_RELATIONSHIP``.
        data: Исходная пара ``(left, top)``.
    
    Example:
        >>> s = Point(1920, 1080)
        >>> s.pixel
        (1920, 1080)
        >>> s.relationship
        (1.0, 1.0)
    """
    
    type: PointType
    data: PixelCoord

    @overload
    def __init__(self, data: PixelCoord, type_data: SizeType = ...) -> None: ...
    @overload
    def __init__(self, num1: int, num2: int, type_data: SizeType = ...) -> None: ...

    def __init__(
        self,
        num1: int | PixelCoord,
        num2: int | None = None,
        type_data: PointType = POINT_PIXEL,
    ) -> None:
        """Создаёт размер.

        Args:
            num1: Расположение по x, либо кортеж ``(left, top)``.
            num2: Расположение по y. Должна быть ``None``, если ``num1`` — кортеж.
            type_data: Система координат входных данных —
                ``POINT_PIXEL`` (по умолчанию) или ``POINT_RELATIONSHIP``.

        Raises:
            TypeError: Если ``num1`` — не кортеж, а ``num2`` не задан.
            ValueError: Если ``type_data`` не поддерживается.
        """

        if num2 is None:
            if not isinstance(num1, tuple):
                raise TypeError("Ожидался tuple[int, int]")
            num1, num2 = num1
        super().__init__(num1, num2, type_data)

    def update(self) -> None:
        """Пересчитывает координаты в пикселях и в относительных единицах.

        Raises:
            ValueError: Если ``self.type`` не входит в ``PointType``.
        """

        if self.type == POINT_PIXEL:
            self._relationship = relationship_transformation(self.data)
            self._pixel = self.data
        elif self.type == POINT_RELATIONSHIP:
            self._pixel = cordinate_transformation(self.data)
            self._relationship = self.data
        else:
            raise ValueError(f"тип: {self.type} не существует")
