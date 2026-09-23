"""
Модуль для работы с кординатами и с размерами
"""
from ..tools import cordinate_transformation, relationship_transformation
from .._core.locals import GRAPHICS, GRAPHICS_GL_2D_ORTHO, GRAPHICS_PYGAME
from typing import Type

SIZE_RELATIONSHIP = "size-relationship"
SIZE_PIXEL = "size-pixel"

POINT_RELATIONSHIP = "point-relationship"
POINT_PIXEL = "point-pixel"



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
    pixel: tuple        # по пиксельно
    relationship: tuple # относительно

    def __init__(self, num1: int, num2: int, type_data: str):
        self.type = type_data
        self.data = (num1, num2)
        self.update()

    def update(self) -> None: 
        """
        Обновления и вычесления
        """

    def get(self):
        """
        Возвращает те кординаты в зависимости от флага
        """
        if GRAPHICS.get() == GRAPHICS_GL_2D_ORTHO or GRAPHICS.get() == GRAPHICS_PYGAME:
            return self.pixel
        else:
            return self.relationship

class Size(_General):
    pixel: tuple        # по пиксельно
    relationship: tuple # относительно

    """
    Кординаты
    """
    def __init__(self, num1: int, num2: int, type_data: str = SIZE_PIXEL):
        """
        Принимает и изменят размеры

        Args:
            num1 (int): Ширина
            num2 (int): Длина
            
            type_data (str): Флаг типа позиции (SIZE_PIXEL по пиксельно, POINT_RELATIONSHI относильно для OpenGL)
        """
        super().__init__(num1, num2, type_data)

    def update(self):
        """
        Вычесление всех типов размеров
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
    def __init__(self, num1: int, num2: int, type_data: str = POINT_PIXEL):
        super().__init__(num1, num2, type_data)

    def update(self):
        """
        Вычесление всех типов кординат
        """
        if self.type == POINT_PIXEL:
            self.relationship =  relationship_transformation(self.data)
            self.pixel = self.data
        elif self.type == POINT_RELATIONSHIP:
            self.pixel = cordinate_transformation(self.data)
            self.relationship = self.data
        else:
            raise ValueError(f"тип: {self.type} не существует")
        

class SizeTup(Size):
    def __init__(self, data: tuple[int, int], type_data=SIZE_PIXEL):
        super().__init__(*data, type_data)

class PointTup(Point):
    def __init__(self, data: tuple[int, int], type_data = POINT_PIXEL):
        super().__init__(*data, type_data)
