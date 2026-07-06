import pygame as pg
from PyForge.tools import PfObject
from dataclasses import dataclass
from typing import Tuple, Any
from ...._core.creating.listing import CoreListOfItems 


class ListOfItems(CoreListOfItems):
    def draw(self, screen: pg.Surface):
        screen.blit(self.fons, self.left_top.pixel)
        screen.blit(self.holst, self.left_top.pixel)
