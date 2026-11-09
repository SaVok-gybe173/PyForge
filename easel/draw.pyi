from typing import List, Sequence, Tuple, Union

from .surface import Surface
from ..pfmath.rect import Rect

type _Color = Union[
    Tuple[int, int, int],
    Tuple[int, int, int, int],
    List[int],
    int,
]
type _Point = Tuple[int, int]
type _RectLike = Union[
    Tuple[int, int, int, int],
    List[int],
    Rect,
]


# линии
def line(
    surface: Surface,
    color: _Color,
    start_pos: _Point,
    end_pos: _Point,
    width: int = 1,
) -> Rect:
    """Нарисовать прямую линию (Bresenham).

    :param surface: целевая поверхность
    :param color:   (r,g,b), (r,g,b,a) или упакованное int
    :param start_pos: (x, y) начало
    :param end_pos:   (x, y) конец
    :param width:   толщина в пикселях, >= 1
    :return: Rect ограничивающий нарисованные пиксели

    Аналог ``pygame.draw.line``.
    """
    ...

def lines(
    surface: Surface,
    color: _Color,
    closed: bool,
    points: Sequence[_Point],
    width: int = 1,
) -> Rect:
    """Нарисовать ломаную через несколько точек.

    :param closed: если True — соединить последнюю точку с первой
    :return: Rect bounding box
    :raises ValueError: если точек меньше 2

    Аналог ``pygame.draw.lines``.
    """
    ...

def aaline(
    surface: Surface,
    color: _Color,
    start_pos: _Point,
    end_pos: _Point,
    width: int = 1,
) -> Rect:
    """Сглаженная линия (Xiaolin Wu).

    Параметр ``width`` принимается для совместимости с pygame-ce,
    но антиалиасинг рисуется шириной 1 px (как в pygame-ce < 2.5.6).

    Аналог ``pygame.draw.aaline``.
    """
    ...

def aalines(
    surface: Surface,
    color: _Color,
    closed: bool,
    points: Sequence[_Point],
) -> Rect:
    """Сглаженная ломаная.

    :raises ValueError: если точек меньше 2

    Аналог ``pygame.draw.aalines``.
    """
    ...


# прямоугольник
def rect(
    surface: Surface,
    color: _Color,
    rect: _RectLike,
    width: int = 0,
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1,
) -> Rect:
    """Прямоугольник, опционально со скруглёнными углами.

    :param rect: (x, y, w, h) или Rect
    :param width: 0 — заливка, >0 — обводка заданной толщины
    :param border_radius: радиус скругления (общий);
        -1 = без скругления
    :param border_*_radius: индивидуальные радиусы; -1 = взять из
        ``border_radius``

    Если ``border_radius < 1`` и все индивидуальные < 1 — быстрый путь
    без скруглений (прямые ``_fill_rect``, SIMD).

    Аналог ``pygame.draw.rect``.
    """
    ...


# окружность
def circle(
    surface: Surface,
    color: _Color,
    center: _Point,
    radius: int,
    width: int = 0,
    draw_top_right: bool = False,
    draw_top_left: bool = False,
    draw_bottom_left: bool = False,
    draw_bottom_right: bool = False,
) -> Rect:
    """Окружность (midpoint algorithm).

    :param width: 0 — заливка, >0 — обводка
    :param draw_*: параметры принимаются для совместимости
        с pygame-ce 2.5+; в текущей версии квадранты не обрезаются
        (рисуется полный круг).

    Аналог ``pygame.draw.circle``.
    """
    ...

# эллипс
def aacircle(
    surface: Surface,
    color: _Color,
    center: _Point,
    radius: int,
    width: int = 0,
    draw_top_right: bool = False,
    draw_top_left: bool = False,
    draw_bottom_left: bool = False,
    draw_bottom_right: bool = False,
) -> Rect:
    """Сглаженная окружность (Xiaolin Wu).

    Квадранты (``draw_*``) пока принимаются, но не применяются.

    Аналог ``pygame.draw.aacircle`` (pygame-ce 2.5+).
    """
    ...

def ellipse(
    surface: Surface,
    color: _Color,
    rect: _RectLike,
    width: int = 0,
) -> Rect:
    """Эллипс, вписанный в прямоугольник.

    :param width: 0 — заливка (scanline), >0 — параметрический контур

    Аналог ``pygame.draw.ellipse``.
    """
    ...

# дуга
def arc(
    surface: Surface,
    color: _Color,
    rect: _RectLike,
    start_angle: float,
    stop_angle: float,
    width: int = 1,
) -> Rect:
    """Дуга эллипса от start_angle до stop_angle (радианы).

    :param width: толщина в пикселях (растёт «вниз» по y)

    Аналог ``pygame.draw.arc``.
    """
    ...


#  Полигон
def polygon(
    surface: Surface,
    color: _Color,
    points: Sequence[_Point],
    width: int = 0,
) -> Rect:
    """Замкнутый многоугольник.

    :param width: 0 — заливка (scanline even-odd), >0 — только контур
    :raises ValueError: если точек меньше 3

    Аналог ``pygame.draw.polygon``.
    """
    ...

#  Заливка
def flood_fill(
    surface: Surface,
    color: _Color,
    start_pos: _Point,
) -> Rect:
    """Scanline flood fill (залить область того же цвета, что в start_pos).

    Если цвет в start_pos уже равен ``color`` — ничего не рисует.

    Аналог ``pygame.draw.flood_fill`` (pygame-ce 2.5+).
    """
    ...