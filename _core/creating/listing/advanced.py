from PyForge.tools import PfObject
from .structure import ListItems, Governance, AdvancedListItems
from ....markup import Size, Point
from typing import Tuple
from .calculations import event_size, update_size
import pygame as pg


class CoreAdvancedListOfItems(PfObject):
    def __init__(self, left_top: Point, width_height: Size, items: list[AdvancedListItems] | None = None, governance = Governance.DOWN, distance: int = 10):
        self.left_top = left_top
        width_height = width_height
        self.governance = governance
        self.distance = distance
        self.items = [] if items is None else items

        self.holst = pg.Surface(width_height.pixel, pg.SRCALPHA)

        self.koficent = 0
        self.offset = 0
    def update(self):
        for itm in self.items:
            itm.update()
    
    def draw_down(self, sceen):
        pass

    def event_down(self, event: pg.event.Event):
        pass
    def event_rightwrds(self, event: pg.event.Event):
        pass

    def event(self, event):
        if self.governance == Governance.DOWN:
            self.event_down(event)
        elif self.governance == Governance.RiGHTWARDS:
            self.event_rightwrds()
    def draw(self, sceen):
        sceen.blit(self.holst, (self.left_top))