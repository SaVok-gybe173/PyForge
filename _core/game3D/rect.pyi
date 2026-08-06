import numpy as np

class Rect3D:
    def __init__(self, vertices_list: tuple[tuple[int, int, int], ...],
                indices_list: tuple[tuple[int, int], ...],
                normals_list: tuple[tuple[float, float, float], ...] | None = None,
                uvs_list: list[tuple[float, float]] | None = None,
                colors_list: tuple[tuple[float, float, float], ...] | tuple[tuple[float, float, float, float], ...] | None = None
                ):
        """
        Получение аргументов для работы.

        Args:
            vertices_list (list[tuple[int, int, int]]): Cписок всех вершин (точек) объекта в локальной системе координат. Каждая вершина — это кортеж из трёх чисел (x, y, z)
            indices_list (tuple[int]): Индексы вершин, определяющие, как соединять вершины в треугольники. Каждые три подряд идущих числа образуют один треугольник.
            normals_list (tuple[tuple[float, float, float], ...] | None): Нормали для каждой вершины – векторы, указывающие направление «наружу» от поверхности в данной вершине. Используются для освещения. Каждая нормаль — три числа (nx, ny, nz), длина обычно равна 1 (нормализованный вектор).
            uvs_list (list[tuple[float, float]] | None): Текстурные координаты (UV) для каждой вершины. Каждая UV-пара — два числа (u, v) в диапазоне [0, 1], определяющие, какой участок текстуры (изображения) соответствует данной вершине. Используется для текстурирования.
            colors_list (tuple[tuple[float, float, float], ...] | tuple[tuple[float, float, float, float], ...] | None): Цвет для каждой вершины в формате (R, G, B) (или (R, G, B, A) с альфа-прозрачностью). Значения в диапазоне [0, 1].

        """

    def rotate(self, ax: float, ay: float, az: float):
        """
        Поворот всего обьекта вокруг своей оси в радиантах
        
        Args:
            ax (float): Поворот по x.
            ay (float): Поворот по y.
            az (float): Поворот по z.

        """

    def offset( x: int, y: int, z: int):
        """
        Сдвигает текущие кординаты

        Args:
            x (int): Сдвиг по кординате x.
            y (int): Сдвиг по кординате y.
            z (int): Сдвиг по корденате z.

        """

    def get_aabb(self):
        """
        Возвращает ограничивающий параллелепипед (AABB) текущих вершин.
        
        Return:
            tuple[float, float, float, float, float, float, float]

        """

    def collidepoint(self, x: float, y: float, z: float):
        """
        Проверяет, находится ли точка (x,y,z) внутри AABB объекта.

        Args:
            x (float): Кордината x
            y (float): Кордината y
            z (float): Кордината z

        Return:
            bool: Есть или нету пересечение с кординатами
        """

    def colliderect(self, other: Rect3D):
        """
        Проверяет пересечение AABB текущего объекта с другим объектом.
        
        Args:
            other (Rect3D): Обьект с которым проверяем пересечение

        Return:
            bool: Есть или нету пересечение с обьектом
        
        """

    def get_vertices(self) -> np.NDArray[tuple[int, int, int], ...]:
        """
        Return:
            np.NDArray[tuple[int, int, int], ...]: Вершины в numpy массиве
        """
    
    def set_vertices(self, vertices_list: tuple[tuple[int, int, int], ...]):
        """
        Args:
            vertices_list (list[tuple[int, int, int]]): Cписок всех вершин (точек) объекта в локальной системе координат. Каждая вершина — это кортеж из трёх чисел (x, y, z)
        """

