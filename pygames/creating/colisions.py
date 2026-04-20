import pygame as pg
import math
try:
    import numpy as np
except ModuleNotFoundError:
    print("установите numpy ??\npip3 install numpy")

def collision_surface(surface1, pos1, surface2, pos2, use_pixel_perfect=False):
    """
    Проверяет коллизию между двумя Surface объектами
    
    Аргументы:
        surface1, surface2: поверхности Pygame
        pos1, pos2: позиции поверхностей (x, y)
        use_pixel_perfect: если True, использует точную пиксельную проверку
    
    Возвращает:
        True если есть коллизия, иначе False
    """
    rect1 = surface1.get_rect(topleft=pos1)
    rect2 = surface2.get_rect(topleft=pos2)
    if not rect1.colliderect(rect2):
        return False
    if use_pixel_perfect:
        mask1 = pg.mask.from_surface(surface1)
        mask2 = pg.mask.from_surface(surface2)
        offset = (rect2.x - rect1.x, rect2.y - rect1.y)
        return mask1.overlap(mask2, offset) is not None
    return True

def collision_maus(surface, pos, mouse_pos, use_pixel_perfect=False):
    """
    Проверяет коллизию между Surface объектом и позицией мыши
    
    Аргументы:
        surface: поверхность Pygame
        pos: позиция поверхности (x, y)
        mouse_pos: позиция мыши (x, y)
        use_pixel_perfect: если True, использует точную пиксельную проверку
    
    Возвращает:
        True если есть коллизия, иначе False
    """
    rect = surface.get_rect(topleft=pos)
    if not rect.collidepoint(mouse_pos):
        return False
    if use_pixel_perfect:
        mask = pg.mask.from_surface(surface)
        local_x = mouse_pos[0] - pos[0]
        local_y = mouse_pos[1] - pos[1]
        try:
            return mask.get_at((local_x, local_y))
        except IndexError:
            return False
    return True

def check_rounded_rect_collision(rect1: pg.Rect, radius1: int, rect2: pg.Rect, radius2: int):
    """
    Проверяет коллизию между двумя скругленными прямоугольниками
    """
    inner_rect1 = pg.Rect(rect1.left + radius1, rect1.top + radius1,
                         rect1.width - 2*radius1, rect1.height - 2*radius1)
    inner_rect2 = pg.Rect(rect2.left + radius2, rect2.top + radius2,
                         rect2.width - 2*radius2, rect2.height - 2*radius2)
    
    if inner_rect1.colliderect(inner_rect2):
        return True
    corners1 = [
        (rect1.left + radius1, rect1.top + radius1),  # Левый верхний
        (rect1.right - radius1, rect1.top + radius1),  # Правый верхний
        (rect1.left + radius1, rect1.bottom - radius1),  # Левый нижний
        (rect1.right - radius1, rect1.bottom - radius1)  # Правый нижний
    ]
    
    corners2 = [
        (rect2.left + radius2, rect2.top + radius2),
        (rect2.right - radius2, rect2.top + radius2),
        (rect2.left + radius2, rect2.bottom - radius2),
        (rect2.right - radius2, rect2.bottom - radius2)
    ]
    for corner in corners1:
        if point_in_rounded_rect(corner, rect2, radius2): return True
    for corner in corners2:
        if point_in_rounded_rect(corner, rect1, radius1): return True
    for corner1 in corners1:
        for corner2 in corners2:
            dx = corner1[0] - corner2[0]
            dy = corner1[1] - corner2[1]
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < radius1 + radius2:
                return True
    
    return False

def point_in_rounded_rect(point: list[int, int] | tuple[int, int], rect: pg.Rect, radius: int):
    """
    Проверяет, находится ли точка внутри скругленного прямоугольника
    """
    x, y = point
    if (rect.left + radius <= x <= rect.right - radius and
        rect.top + radius <= y <= rect.bottom - radius):
        return True
    if x < rect.left + radius and y < rect.top + radius:
        dx = x - (rect.left + radius)
        dy = y - (rect.top + radius)
        return dx*dx + dy*dy <= radius*radius
    if x > rect.right - radius and y < rect.top + radius:
        dx = x - (rect.right - radius)
        dy = y - (rect.top + radius)
        return dx*dx + dy*dy <= radius*radius
    if x < rect.left + radius and y > rect.bottom - radius:
        dx = x - (rect.left + radius)
        dy = y - (rect.bottom - radius)
        return dx*dx + dy*dy <= radius*radius
    if x > rect.right - radius and y > rect.bottom - radius:
        dx = x - (rect.right - radius)
        dy = y - (rect.bottom - radius)
        return dx*dx + dy*dy <= radius*radius
    
    return False

def point_in_rounded_rect_numpy(point: tuple[int, int], rect: pg.Rect, radius: int) -> bool:
    """
    Проверяет, находится ли точка внутри скругленного прямоугольника, используя NumPy.
    (Предполагает, что точка представлена как NumPy array)
    """
    x, y = point
    rx, ry, rw, rh = rect
    x = np.array(x)
    y = np.array(y)
    radius_sq = radius * radius
    if rx + radius <= x <= rx + rw - radius and ry + radius <= y <= ry + rh - radius:
        return True
    corners = np.array([(rx + radius, ry + radius), (rx + rw - radius, ry + radius),
                        (rx + radius, ry + rh - radius), (rx + rw - radius, ry + rh - radius)])
    distances_sq = np.sum((np.array([x,y]) - corners)**2, axis=1)

    return np.any(distances_sq <= radius_sq)