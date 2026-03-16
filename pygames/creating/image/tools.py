import pygame

def get_none_image(size):
    none_image = pygame.Surface(size)
    none_image.fill((255,255,255))
    im = pygame.Surface((size[0]//2, size[1]//2))
    im.fill((100, 0, 100))
    none_image.blit(im, (0,0))
    none_image.blit(im, (size[0]//2, size[1]//2))
    return none_image

def round_corners_numpy(image, radius):
    rect = image.get_rect()
    mask = pygame.Surface(rect.size, pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), rect, border_radius=radius)
    image_alpha = pygame.surfarray.pixels_alpha(image)
    mask_alpha = pygame.surfarray.array_alpha(mask)

    image_alpha[:] = mask_alpha
    del image_alpha  
    return image

def round_corners(image, radius):
    """Скругление углов изображения с заданным радиусом"""
    rect = image.get_rect()
    mask = pygame.Surface(rect.size, pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), rect, border_radius=radius)
    for x in range(rect.width):
        for y in range(rect.height):
            if mask.get_at((x, y))[0] == 0:  
                image.set_at((x, y), (0, 0, 0, 0))  
    return image

def round_image(image, radius):
    """Скругление изображения с заданным радиусом"""
    rect = image.get_rect()
    mask = pygame.Surface(rect.size, pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), rect, border_radius=radius)
    image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return image


def optimized_round_image(image, radius):
    """Оптимизированная функция для создания круглого изображения."""
    rect = image.get_rect() # Получаем Rect из image

    rounded = pygame.Surface(rect.size, pygame.SRCALPHA) # rect.size возвращает (width, height)
    pygame.draw.rect(rounded, (255, 255, 255), rect, border_radius=radius)

    image.blit(rounded, (0, 0), None, pygame.BLEND_RGBA_MIN)
    return rounded


def round_corners_alternative(surface, radius):
    """Альтернативный метод скругления углов"""
    width, height = surface.get_size()
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, width, height), border_radius=radius)
    result = pygame.Surface((width, height), pygame.SRCALPHA)
    result.blit(surface, (0, 0))
    result.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
    
    return result

def make_circle_image(image):
    """Создает круглое изображение"""
    size = max(image.get_size())
    circle = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(circle, (255, 255, 255), (size//2, size//2), size//2)
    result = pygame.Surface((size, size), pygame.SRCALPHA)
    result.blit(image, (0, 0))
    result.blit(circle, (0, 0), None, pygame.BLEND_RGBA_MIN)
    
    return result

def replace_color_on_surface(surface: pygame.Surface, color_to_replace: tuple[int, int, int, int], new_color: tuple[int, int, int, int]) -> pygame.Surface:
    """
    Заменяет один определенный цвет на другой на поверхности pygame.Surface,
    не затрагивая другие пиксели.

    Args:
        surface: Исходная поверхность (pygame.Surface), на которой нужно произвести замену.
        color_to_replace: Кортеж RGBA (красный, зеленый, синий, альфа), представляющий цвет, который нужно заменить.
                          Например: (255, 0, 0, 255) для непрозрачного красного.
        new_color: Кортеж RGBA, представляющий новый цвет.
                   Например: (0, 0, 255, 255) для непрозрачного синего.

    Returns:
        Новая поверхность pygame.Surface с замененным цветом.
        Оригинальная поверхность остается неизменной.
    """
    new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

    surface.lock()
    new_surface.lock()

    width, height = surface.get_size()

    for x in range(width):
        for y in range(height):
            current_color = surface.get_at((x, y))
            if current_color == color_to_replace:
                new_surface.set_at((x, y), new_color)
            else:
                new_surface.set_at((x, y), current_color)
    surface.unlock()
    new_surface.unlock()

    return new_surface