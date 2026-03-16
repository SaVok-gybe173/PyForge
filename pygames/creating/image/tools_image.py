import pygame as pg

def extract_square(surface: pg.Surface, center_x, center_y, size):
    """
    Вырезает квадратную область из поверхности.
    
    Args:
        surface (pg.Surface): Исходная поверхность
        center_x (int): X-координата центра квадрата
        center_y (int): Y-координата центра квадрата
        size (int): Размер стороны квадрата
    
    Returns:
        pg.Surface: Новая поверхность с вырезанным квадратом
    """
    # Вычисляем координаты верхнего левого угла квадрата
    x = center_x - size // 2
    y = center_y - size // 2
    
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x + size > surface.get_width():
        x = surface.get_width() - size
    if y + size > surface.get_height():
        y = surface.get_height() - size
    if x < 0 or y < 0 or size <= 0:
        return pg.Surface((1, 1), pg.SRCALPHA)

    rect = pg.Rect(x, y, size, size)
    square_surface = pg.Surface((size, size), pg.SRCALPHA)
    square_surface.blit(surface, (0, 0), rect)
    return square_surface

# Альтернативная версия с использованием subsurface (более эффективная)
def extract_square_fast(surface: pg.Surface, center_x, center_y, size):
    """
    Вырезает квадратную область из поверхности с использованием subsurface.
    Более эффективна, но исходная поверхность должна оставаться в памяти.
    
    Args:
        surface (pg.Surface): Исходная поверхность
        center_x (int): X-координата центра квадрата
        center_y (int): Y-координата центра квадрата
        size (int): Размер стороны квадрата
    
    Returns:
        pg.Surface: Подповерхность с вырезанным квадратом
    """
    x = center_x - size // 2
    y = center_y - size // 2

    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x + size > surface.get_width():
        x = surface.get_width() - size
    if y + size > surface.get_height():
        y = surface.get_height() - size
    if x < 0 or y < 0 or size <= 0:
        return pg.Surface((1, 1), pg.SRCALPHA)

    rect = pg.Rect(x, y, size, size)
    return surface.subsurface(rect)

def resize_image_with_aspect_ratio(image: pg.Surface, new_width: int, new_height: int) -> pg.Surface:
    """Изменяет размер изображения, сохраняя пропорции."""
    width, height = image.get_size()
    aspect_ratio = width / height

    if new_width / new_height > aspect_ratio:
        new_width = int(new_height * aspect_ratio)
    else:
        new_height = int(new_width / aspect_ratio)

    resized_image = pg.transform.scale(image, (new_width, new_height))
    return resized_image
