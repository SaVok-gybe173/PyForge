from PyForge.button import AnimationButton, Impuls
import pygame as pg

# cсоздание серой кнопки
def _create_gray_button(name, cords, color):
    sur = pg.Surface((79, 24), pg.SRCALPHA)
    sur.fill((0, 0, 0, 30))
    text_surf = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 14).render(name, True,  color)
    x = (sur.get_width() - text_surf.get_width()) // 2
    y = (sur.get_height() - text_surf.get_height()) // 2
    sur.blit(text_surf, (x, y))
    pg.draw.rect(sur, (160, 160, 160), sur.get_rect(), 2)
    return  AnimationButton(cords, sur, Impuls(shadow=20, clic_shadow=50))

# создание синей кнопки
def _create_blue_button(name, cords, color):
    sur = pg.Surface((79, 24), pg.SRCALPHA)
    sur.fill((0, 0, 0, 30))
    text_surf = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 14).render(name, True,  color)
    x = (sur.get_width() - text_surf.get_width()) // 2
    y = (sur.get_height() - text_surf.get_height()) // 2
    sur.blit(text_surf, (x, y))
    pg.draw.rect(sur, (0, 120, 215), sur.get_rect(), 2)
    return  AnimationButton(cords, sur, Impuls(shadow=20, clic_shadow=50))

# создагие изображение без галочки
def create_mark_off():
    sur = pg.surface.Surface((13, 13), pg.SRCALPHA)
    pg.draw.rect(sur, (30, 30, 30), sur.get_rect(), 1)
    return sur

# создагие изображение с галочкой
def create_mark_on():
    sur = create_mark_off()
    pg.draw.line(sur, (50, 50, 50), (1, 6), (5, 11), 2)
    pg.draw.line(sur, (50, 50, 50), (11, 3), (5, 11), 2)
    return sur

