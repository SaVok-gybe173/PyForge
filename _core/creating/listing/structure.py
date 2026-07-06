from PyForge.tools import PfObject
from dataclasses import dataclass
from typing import Tuple, Any
import pygame as pg


class ListItems(PfObject): 
    def __init__(self, image: pg.Surface, info: Any = ''):
        self.image: pg.Surface = image
        self.info = info

    @property
    def width(self):
        return self.image.get_width()
    @width.setter
    def width(self, width):
        pass

    @property
    def heigh(self):
        return self.image.get_height()
    @heigh.setter
    def heigh(self, heigh):
        pass
    
    def blit(self):
        return self.image
    
    def __call__(self):
        return self.image

    def collidepoint(self, otpos):
        return self.image.get_rect(left=0,top=0).collidepoint(otpos)
    
    def click(self, otpos):
        pass

    def visible_update(self):
        pass

    def copy(self):
        ListItems(self.image.copy(), self.info)

    

class Governance:
    DOWN = 0
    RiGHTWARDS = 1