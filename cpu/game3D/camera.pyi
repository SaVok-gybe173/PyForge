from ..._core.game3D.rect import Rect3D
from pygame import Surface

class Camera:
    def __init__(self, rects: list[Rect3D], fov: int = 90, width: int = 800, height: int = 600):
        """
        Получение аргументов для работы.
        
        Args:
            rects (list[Rect3D]): Cписок всех структур
            fov (int): Угол обзора
            width (int): Ширена
            height (int): Длина
            
        """

    def set_position(self, x: float, y: float, z: float) -> None:
        """
        Установка позиции

        Args:
            x (int): Установка координаты x.
            y (int): Установка координаты y.
            z (int): Установка координаты z.

        """

    def translate(self, dx: float, dy: float, dz: float) -> None:
        """
        Смещение по координатам

        Args:
            dx (int): Сдвиг по координате x.
            dy (int): Сдвиг по координате y.
            dz (int): Сдвиг по коорденате z.
        
        """

    def set_rotation(self, ax: float, ay: float, az: float) -> None:
        """
        Установка поворот камеры в радиантах

        Args:
            x (float): Поворот по x.
            y (float): Поворот по y.
            z (float): Поворот по z.

        """

    def rotate(self, ax: float, ay: float, az: float) -> None:
        """
        Поворот камеры в радиантах
                
        Args:
            ax (float): Поворот по x.
            ay (float): Поворот по y.
            az (float): Поворот по z.
        
        """

    def set_color_line(self, r: int, g: int, b: int) -> None:
        """
        Установка цвета линий для draw_vertices в формате rgb

        Args:
            r (int): красный
            g (int): зеленый
            b (int): синий

        """

    def get_color_line(self) -> tuple[int, int, int]:
        """
        Возвращает текущий цвет линий
        
        Return:
            tuple[int, int, int]: красный, зеленый, синий

        """

    def draw_vertices(self, scene: Surface):
        """
        Рисует полигоны
        
        Args:
            scene (Surface): Поверхность для отрисовки

        """

    def draw_solid(self, scene: Surface, color: tuple[int, int, int] = (255, 255, 255)):
        """
        Рисует все объекты залитыми треугольниками одного цвета.
        Сортирует треугольники по глубине (painter's algorithm).

        Args:
            scene (Surface): Поверхность для отрисовки
            color (tuple[int, int, int]): цвет заливки
            
        """