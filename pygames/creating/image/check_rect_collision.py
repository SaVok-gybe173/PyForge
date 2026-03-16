import pygame as pg
import math
try:
    import numpy as np
except ModuleNotFoundError:
    print("установите numpy ??\npip3 install numpy")

def check_rounded_rect_collision(rect1: pg.Rect, radius1: int, rect2: pg.Rect, radius2: int):
    """
    Проверяет коллизию между двумя скругленными прямоугольниками
    """
    # 1. Проверка центральных прямоугольников
    inner_rect1 = pg.Rect(rect1.left + radius1, rect1.top + radius1,
                         rect1.width - 2*radius1, rect1.height - 2*radius1)
    inner_rect2 = pg.Rect(rect2.left + radius2, rect2.top + radius2,
                         rect2.width - 2*radius2, rect2.height - 2*radius2)
    
    if inner_rect1.colliderect(inner_rect2):
        return True
    
    # 2. Проверка угловых кругов
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
    
    # Проверка кругов из первого прямоугольника со вторым прямоугольником
    for corner in corners1:
        if point_in_rounded_rect(corner, rect2, radius2):
            return True
    
    # Проверка кругов из второго прямоугольника с первым
    for corner in corners2:
        if point_in_rounded_rect(corner, rect1, radius1):
            return True
    
    # 3. Проверка пересечений между угловыми кругами
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
    
    # Проверка центральной прямоугольной области
    if (rect.left + radius <= x <= rect.right - radius and
        rect.top + radius <= y <= rect.bottom - radius):
        return True
    
    # Проверка угловых кругов
    # Левый верхний угол
    if x < rect.left + radius and y < rect.top + radius:
        dx = x - (rect.left + radius)
        dy = y - (rect.top + radius)
        return dx*dx + dy*dy <= radius*radius
    
    # Правый верхний угол
    if x > rect.right - radius and y < rect.top + radius:
        dx = x - (rect.right - radius)
        dy = y - (rect.top + radius)
        return dx*dx + dy*dy <= radius*radius
    
    # Левый нижний угол
    if x < rect.left + radius and y > rect.bottom - radius:
        dx = x - (rect.left + radius)
        dy = y - (rect.bottom - radius)
        return dx*dx + dy*dy <= radius*radius
    
    # Правый нижний угол
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

    # Центральная прямоугольная область
    if rx + radius <= x <= rx + rw - radius and ry + radius <= y <= ry + rh - radius:
        return True

    # Угловые круги
    corners = np.array([(rx + radius, ry + radius), (rx + rw - radius, ry + radius),
                        (rx + radius, ry + rh - radius), (rx + rw - radius, ry + rh - radius)])
    distances_sq = np.sum((np.array([x,y]) - corners)**2, axis=1)  # Квадраты расстояний до углов

    return np.any(distances_sq <= radius_sq)