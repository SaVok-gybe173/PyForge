"""
Функции инициализации

    init_2d_ortho – для плоских игр (координаты как в Pygame: верхний левый угол – (0,0)).

    init_3d_perspective – классический трёхмерный вид с глубиной.

    init_3d_isometric – изометрический вид (как в стратегиях).

    init_2d_pixel_perfect – 2D с началом координат в левом нижнем углу.

    init_custom_setup – позволяет самому задать матрицы проекции.

Класс InitGl

    Теперь у него есть метод set_initialization(функция, параметры), который меняет режим и сразу применяет его.

    Метод apply() просто запускает выбранную функцию с параметрами.

    Поле clear_mask по умолчанию очищает и цвет, и глубину – для 2D можно убрать | GL_DEPTH_BUFFER_BIT.

"""

import sys
from PyForge._core.locals import changing_graphics, GRAPHICS_GL_2D_ORTHO, GRAPHICS_GL_3D_PERSPECTIVE, GRAPHICS_GL_2D_PIXEL_PERSPECTIVE, GRAPHICS_GL_CUSTOM_SETUP, GRAPHICS_GL_3D_ISOMERIC

try:
    import pygame as pg
except ImportError as e:
    sys.exit(102)

try:
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *

    def check_opengl_with_pygame():
        """Проверка работоспособности OpenGL через Pygame"""
        try:
            pg.init()
            pg.display.set_mode((1, 1), pg.OPENGL | pg.DOUBLEBUF)
            version = glGetString(GL_VERSION)
            vendor = glGetString(GL_VENDOR)
            renderer = glGetString(GL_RENDERER)
            info = {
                "version": version.decode() if version else None,
                "vendor": vendor.decode() if vendor else None,
                "renderer": renderer.decode() if renderer else None,
            }
            pg.quit()
            return True, info
        except Exception as e:
            try:
                pg.quit()
            except:
                pass
            return False, str(e)

    IS_IMPORT_GL, _ = check_opengl_with_pygame()
except (ModuleNotFoundError, ImportError) as e:
    IS_IMPORT_GL = False


def set_import_gl(_is: bool):
    """Ручное изменение флага доступности OpenGL"""
    global IS_IMPORT_GL
    IS_IMPORT_GL = _is


# ------------------- ТИПЫ ИНИЦИАЛИЗАЦИЙ -------------------

def init_2d_ortho(width=None, height=None):
    """
    Ортографическая проекция для 2D графики.
    Координаты экрана: (0,0) в левом верхнем углу, (width, height) в правом нижнем.
    Глубина не используется, всё рисуется на плоскости.
    """
    if width is None or height is None:
        # берём текущий размер окна Pygame
        width, height = pg.display.get_window_size()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)   # лево, право, низ, верх, near, far
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)              # в 2D тест глубины не нужен
    glEnable(GL_BLEND)                    # для прозрачности
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    changing_graphics(GRAPHICS_GL_2D_ORTHO)

def init_3d_perspective(fov=45, near=0.1, far=100.0):
    """
    Классическая перспективная проекция для 3D.
    fov - угол обзора по вертикали (в градусах)
    near/far - ближняя и дальняя плоскости отсечения
    """
    width, height = pg.display.get_window_size()
    aspect = width / height if height != 0 else 1
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, aspect, near, far)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)               # включаем тест глубины для корректного перекрытия
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    changing_graphics(GRAPHICS_GL_3D_PERSPECTIVE)


def init_3d_isometric(tile_width=32, tile_height=16):
    """
    Изометрическая проекция (ортографическая с поворотом камеры).
    Полезна для 2.5D игр (как в Diablo, Age of Empires).
    tile_width, tile_height - размеры тайла в пикселях для настройки масштаба.
    """
    width, height = pg.display.get_window_size()
    # ортографическая проекция на основе размеров тайлов
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-width/2, width/2, -height/2, height/2, -1000, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(35.264, 1, 0, 0)   # угол для изометрии: 35.264°
    glRotatef(45, 0, 1, 0)        # поворот на 45° вокруг Y
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    changing_graphics(GRAPHICS_GL_2D_PIXEL_PERSPECTIVE)


def init_2d_pixel_perfect():
    """
    Альтернативная 2D-инициализация, где 1 единица = 1 пиксель.
    Центр координат в левом нижнем углу (как в OpenGL по умолчанию).
    """
    width, height = pg.display.get_window_size()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)   # лево, право, низ, верх
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    changing_graphics(GRAPHICS_GL_3D_ISOMERIC)


def init_custom_setup(projection_matrix, modelview_matrix=None):
    """
    Полностью ручная настройка.
    projection_matrix - список из 16 чисел (матрица 4x4) для проекции.
    modelview_matrix - матрица вида (если не указана, единичная).
    """
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixf(projection_matrix)
    glMatrixMode(GL_MODELVIEW)
    if modelview_matrix:
        glLoadMatrixf(modelview_matrix)
    else:
        glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    changing_graphics(GRAPHICS_GL_CUSTOM_SETUP)


class InitGl:
    __instance = None
    initialization_fun = init_2d_ortho   # функция по умолчанию (можно сменить)
    clear_mask = GL_COLOR_BUFFER_BIT #| GL_DEPTH_BUFFER_BIT
    _is = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def clear(self):
        """Очищает буфер(ы) согласно clear_mask"""
        glClear(self.clear_mask)

    def set_initialization(self, func, *args, **kwargs):
        """Выбрать другую функцию инициализации и сразу выполнить её"""
        self.initialization_fun = func
        self.apply(*args, **kwargs)

    def apply(self, *args, **kwargs):
        """Выполнить текущую функцию инициализации с переданными параметрами"""
        if callable(self.initialization_fun):
            self.initialization_fun(*args, **kwargs)
            self._is = True

    def __bool__(self):
        return self._is
    
