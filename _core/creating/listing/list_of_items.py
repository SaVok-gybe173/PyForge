import pygame as pg
from PyForge.tools import PfObject
from typing import Tuple
from .structure import ListItems, Governance
from ....markup import Size, Point
from .calculations import event_size, update_size

class CoreListOfItems(PfObject):
    def __init__(self, left_top: Point|tuple[int, int], width_height: Size|tuple[int, int], items: list[ListItems] | None = None, governance = Governance.DOWN, distance: int = 10, size_streak = 10, color_streak = (170, 170, 170), speed = 10):
        '''
        список элементов ListItems
        
        Args:
            left_top: Point - кординаты
            width_height: Size - размеры
            
            items: list[ListItems] - элементы в списке
            governance: направление куда будет смотреть список
            distance: int - растояние между элементами

            size_streak - линия нахождения
            color_streak - цвет линии
            
            speed - скорость пролистования
        
        не передаваемые:
            fons - задний фон
        '''


        self.governance = governance
        self.left_top = left_top if type(left_top) is Point else Point(*left_top)
        self.width_height = width_height if type(width_height) is Size else Size(*width_height)
        self.distance = distance
        self.speed = speed
        self._color_streak = color_streak
        
        self.items = [] if items is None else items
        self.holst = pg.Surface(self.width_height.pixel, pg.SRCALPHA)
        self.items_holst = pg.Surface(self.width_height.pixel, pg.SRCALPHA)
        self._size_streak = size_streak
        
        self.collor = (0, 0, 0, 0)

        self.koficent = 0
        self.offset = 0
        self.__h = 0
        if items:
            self._update()
        self.fons = pg.Surface((0, 0), pg.SRCALPHA)

        self.visible: list[ListItems] = []
        self.visible_pos = []

    def add(self, *args: Tuple[ListItems]):
        self.items.extend(args)
        self._update()

    def append(self, item):
        self.items.append(item)
        self._update()

    def update(self):
        for itm in self.items:
            itm.update()
        for itm in self.visible:
            itm.visible_update()
        
    def _update_down(self):

        self.items_holst = pg.Surface((self.width_height.pixel[0], sum([(el.heigh + self.distance if i != len(self.items)-1 else el.heigh) for (i, el) in enumerate(self.items)])), pg.SRCALPHA)
        #self.items_holst.fill(self.collor)
        
        self.image_streak = pg.Surface((self._size_streak, update_size(self.items_holst.get_height(), self.holst.get_height())[0]), pg.SRCALPHA)
        self.image_streak.fill(self._color_streak)
        
        self.__h = 0
        for i in self.items:
            #i.width = self.width_height.pixel[0]-self._size_streak 
            self.items_holst.blit(i.image, (0, self.__h))
            self.__h += i.heigh + self.distance
            #print(self.__h+self.offset > 0, self.__h, i.heigh, self.offset, self.width_height.pixel[1])
            if self.__h+self.offset > 0 and self.__h-i.heigh+self.offset< self.width_height.pixel[1] :
                self.visible.append(i)
                self.visible_pos.append((0, self.__h-(i.heigh + self.distance)))
        self.holst.fill(self.collor)
        self.holst.blit(self.items_holst, (0, self.offset))
        if self.__h > self.width_height.pixel[1]:
            self.holst.blit(self.image_streak, (self.width_height.pixel[0]-self._size_streak, self.koficent))

    def _update_rightwards(self):

        self.items_holst = pg.Surface((sum([(el.width + self.distance if i != len(self.items)-1 else el.width) for (i, el) in enumerate(self.items)]), self.width_height.pixel[1]), pg.SRCALPHA)
        self.image_streak = pg.Surface((update_size(self.items_holst.get_width(), self.holst.get_width())[0], self._size_streak), pg.SRCALPHA)
        self.image_streak.fill(self._color_streak)
        self.__h = 0
        for i in self.items:
            #i.heigh = self.width_height.pixel[1]-self._size_streak 
            self.items_holst.blit(i.image, (self.__h, self._size_streak))
            self.__h += i.width + self.distance
            if self.__h-self.offset > 0 and self.__h-i.width-self.offset< self.width_height.pixel[0] :
                self.visible.append(i)
                self.visible_pos.append((self.__h-(i.width + self.distance), 0))
        self.holst.fill(self.collor)
        self.holst.blit(self.items_holst, (self.offset, self._size_streak))
        if self.__h > self.width_height.pixel[0]:
            self.holst.blit(self.image_streak, (self.koficent, 0))

    def _update(self):
        self.visible = []
        self.visible_pos = []
        if self.governance == Governance.DOWN:
            self._update_down()
        elif self.governance == Governance.RiGHTWARDS:
            self._update_rightwards()
        else:
            raise ValueError("governance передан не правельно, используйте Governance класс")
        #print(self.visible_pos, self.visible)
        
    
    
    def _event_down(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self._update()
            if self.__h > self.width_height.pixel[1]:
                items_h = self.items_holst.get_height()
                view_h = self.holst.get_height()
                max_k = update_size(items_h, view_h)[1]

                if items_h == view_h:
                    return False

                delta = self.speed * max_k / (items_h - view_h)

                if event.button == 4 and self.retention(event.pos):
                    self.koficent = max(0, self.koficent - delta)
                elif event.button == 5 and self.retention(event.pos):
                    self.koficent = min(max_k, self.koficent + delta)

                self.holst.fill(self.collor)
                self.offset = -event_size(items_h, view_h, self.koficent)
                self.holst.blit(self.items_holst, (0, self.offset))
                self.holst.blit(self.image_streak, (self.width_height.pixel[0] - self._size_streak, self.koficent))
        return False
    
    def _event_rightwards(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self._update()

            if self.__h > self.width_height.pixel[0]:
                items_w = self.items_holst.get_width()
                view_w = self.holst.get_width()
                max_k = update_size(items_w, view_w)[1]
                if items_w == view_w:                 
                    return False

                delta = self.speed * max_k / (items_w - view_w)

                if event.button == 4 and self.retention(event.pos):

                    self.koficent = max(0, self.koficent - delta)
                elif event.button == 5 and self.retention(event.pos):
                    self.koficent = min(max_k, self.koficent + delta)

                self.holst.fill(self.collor)
                self.offset = -event_size(items_w, view_w, self.koficent)
                self.holst.blit(self.items_holst, (self.offset, 0))
                self.holst.blit(self.image_streak, (self.koficent, 0))
        return False
    
            
    def event(self,event):
        if self.governance == Governance.DOWN:
            self._event_down(event)
        elif self.governance == Governance.RiGHTWARDS:
            self._event_rightwards(event)
        else:
            raise ValueError("governance передан не правельно, используйте Governance класс")
        
    def draw(self, screen: pg.Surface):
        pass

    @property
    def shadow(self):
        return self.collor[3]
    @shadow.setter
    def shadow(self, shadow):
        self.collor = (*self.color, shadow)
    
    @property
    def color(self):
        return (self.collor[0], self.collor[1], self.collor[2])
    @color.setter
    def color(self, color: list):
        self.collor = (*color, self.shadow)

    @staticmethod
    def _update_size(h: int, h2: int):
        #выводит текуще каэфицент 
        try:
            return int(h2/(h/h2)), int(h2-h2/(h/h2))
        except ZeroDivisionError:
            return 0, h2  
    
    def retention(self, pos) -> bool:
        if self.holst.get_rect(left = self.left_top.pixel[0], top = self.left_top.pixel[1]).collidepoint(pos):
            return True 
        return False


    def clear(self, is_update = True):
        self.items.clear()
        if is_update:
            self._update()
    
    def index(self):
            # при больших кординатах срабатывает плохо
            pos = pg.mouse.get_pos()
            for i, el in enumerate(self.items):

                if el.image.get_rect(left = self.left_top.pixel[0], top = (self.left_top.pixel[1] +  i*(el.heigh + self.distance))+ self.offset).collidepoint(pos):
                    return i
            else:
                return None
    
    @property
    def _h(self):
        return self.__h
            
