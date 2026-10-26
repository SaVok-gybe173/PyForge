from ....easel import Surface
from dataclasses import dataclass
from typing import Tuple, Any
from ...._core.creating.listing.list_of_items import CoreListOfItems 


class ListOfItems(CoreListOfItems):
    def draw(self, screen: Surface):
        screen.blit(self.fons, self.left_top.pixel)
        screen.blit(self.holst, self.left_top.pixel)
