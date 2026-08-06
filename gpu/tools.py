import pygame as pg
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from pygame.typing import FileLike


def convert_surface(img: pg.Surface):
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.get_size()[0], img.get_size()[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, pg.image.tostring(img, "RGBA", True))
    # Настройка фильтрации и режима наложения
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id

def load(path: FileLike):
    img = pg.image.load(path).convert_alpha()
    return convert_surface(img)

