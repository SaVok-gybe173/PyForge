# OpenGL рендеринг на C++ с текстурами

import numpy as np

class TextureGL:

    # Загрузка текстуры из данных numpy массива
    def load_from_data(image_data: np.full, width_: int, height_: int, channels_: int = 3) -> bool:
        '''
        *Аргументы:
            image_data: np.full = текструта
            width_: int, height_: int = размеры
            channels_: int = канал (3 - RGB, 4 - RGBA, 1 - grayscels)
        *Пример:
            image_data: np.full = np.full((64, 64, 3), [225, 0, 0], dtype = np.uint8)
            channels_: int = 3
        *Назначение:
            загрузить текстуры из изображения
        '''

    # Создание простой текстуры программно
    def create_color_texture(width_: int, height_: int, color: list) -> bool:
        '''
        *Аргументы:
            width_: int, height_: int = размеры
            color: list = список RGB от 0 до 255
        *Пример:
            color: list = [0, 255, 0]
        *Назначение:
            Создание одноцветной текстуры
        '''
    
    # Активации текстур
    def __bind() -> None:
        ''' 
        *Аргументы:
            нету
        *Назначение:
            Активирует для использование в OpenGL
        '''

    # Деактивирует текстур
    def __unbind() -> None:
        ''' 
        *Аргументы:
            нету
        *Назначение:
            Деактивирует текстуру в OpenGL
        '''

    def __get_texture_id() -> int:
        ''' 
        *Аргументы:
            нету
        *Назначение:
            возвращает текстуры в OpenGL
        '''
    
    # возвращает ширину
    def get_width() -> int: ...
    # возвращает длину
    def get_height() -> int: ...

class _FigurGL:
    def __init__(self, width_: int, height_: int, position_: list[float]) -> None: ...


    def set_vertices(self): ...
    def set_edges(self): ...
    def set_faces(self): ...

    def set_texture_coords(self): ...
    def set_texture(self): ...

    def enable_texture(self): ...


    def update(self): ...

    def turn_x(self): ...
    def turn_y(self): ...
    def turn_z(self): ...

    def render_3d_scene(self): ...

    def get_projected_vertices(self): ...
    def get_edges(self): ...

    def set_line_color(self): ...
    def set_point_color(self): ...
    def set_line_width(self): ...
    def set_point_size(self): ...

    
