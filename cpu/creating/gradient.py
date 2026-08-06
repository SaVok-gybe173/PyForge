import pygame

def make_gradient(width, height, color1, color2):
    surf = pygame.Surface((width, height))
    for y in range(height):
        # интерполяция цвета
        r = color1[0] + (color2[0] - color1[0]) * y // height
        g = color1[1] + (color2[1] - color1[1]) * y // height
        b = color1[2] + (color2[2] - color1[2]) * y // height
        pygame.draw.line(surf, (r, g, b), (0, y), (width, y))
    return surf