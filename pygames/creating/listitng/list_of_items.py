import pygame as pg

from dataclasses import dataclass
from typing import Tuple

@dataclass
class ListItems: 
    image: pg.Surface
    
    @property
    def width(self):
        return self.image.get_size()[0]
    @width.setter
    def width(self, width):
        pass

    @property
    def heigh(self):
        return self.image.get_size()[1]
    @heigh.setter
    def heigh(self, heigh):
        pass
    
    def blit(self):
        return self.image
    def __call__(self):
        return self.image



class ListOfItems:
    def __init__(self, left_top: Tuple[int, int], width_height: Tuple[int, int], items: list[ListItems] | None = None, distance: int = 10, hitbox: bool = False, shadow: int = 10, size_streak = 10, color_streak = (255,255,255), speed = 5):
        '''
        список элементов ListItems
        
        Args:
            left_top: Tuple[int, int] - кординаты
            width_height: Tuple[int, int] - размеры
            
            items: list[ListItems] - элементы в списке
            distance: int - растояние между элементами
            
        не передаваемые:
            outline_color: Tuple[int, int, int] - цвет обводки
            outline: int - обводка
        '''
        self.outline_color = (255,255,255)
        self.outline = 0
        
        self.hitbox = hitbox
        
        self.left, self.top = left_top
        self.width, self.height = width_height
        self.distance = distance
        self.speed = speed
        self._color_streak = color_streak
        
        self.items = [] if items is None else items
        self.holst = pg.Surface(width_height, pg.SRCALPHA)
        self.items_holst = pg.Surface(width_height, pg.SRCALPHA)
        self._size_streak = size_streak
        
        self.collor = (0, 0, 0, shadow)
        
        self.koficent = 0
        self.offset_y = 0
        self.__h = 0
        if items:
            self._update()
    def add(self, *args: Tuple[ListItems]):
        self.items.extend(args)
        self._update()
    def append(self, item):
        self.items.append(item)
        self._update()
    def _update(self):
        self.items_holst = pg.Surface((self.width, sum([(el.heigh + self.distance if i != len(self.items)-1 else el.heigh) for (i, el) in enumerate(self.items)])), pg.SRCALPHA)
        self.items_holst.fill(self.collor)
        
        self.image_streak = pg.Surface((self._size_streak, self._update_size(self.items_holst.get_height(), self.holst.get_height())[0]))
        self.image_streak.fill(self._color_streak)
        
        top = 0
        for i in self.items:
            i.width = self.width-self._size_streak 
            self.items_holst.blit(i.image, (0, top))
            top += i.heigh + self.distance
        self.__h = top
        self.holst.fill(self.collor)
        self.holst.blit(self.items_holst, (0, self.offset_y))
        if self.__h > self.height:
            self.holst.blit(self.image_streak, (self.width-self._size_streak, self.koficent))
        
    @staticmethod
    def _update_size(h: int, h2: int):
        #выводит текуще каэфицент 
        try:
            return int(h2/(h/h2)), int(h2-h2/(h/h2))
        except ZeroDivisionError:
            return 0, h2
    @staticmethod
    def _event_size( h: int, h2: int, hs: int):
        #выводит текуще расположение у 
        p = int(h2-h2/(h/h2))

        if p*hs != 0:
            return int((h-h2)/p*hs)
        else:
            return 0
            raise TypeError("не верный коэфицент")
    def retention(self, pos) -> bool:
        if self.holst.get_rect(left = self.left, top = self.top).collidepoint(pos):
            return True 
        return False
    def index(self):
            # при больших кординатах срабатывает плохо
            for i, el in enumerate(self.items):
                if el.image.get_rect(left = self.left, top = (self.top +  i*(el.heigh + self.distance))+ self.offset_y).collidepoint(pg.mouse.get_pos()):
                    return i
            else:
                return None
    def event(self,event):
        #if event.type == 4352:
        #    self.holst.fill(self.collor)
        #    self.holst.blit(self.items_holst, (0, self._event_size(self.items_holst.get_height(), self.holst.get_height(), 1 )))
        #    self.holst.blit(self.image_streak, (self.width-self._size_streak, self.koficent))
        if event.type == pg.MOUSEBUTTONDOWN and self.__h > self.height:
            if event.button == 4 and self.retention(event.pos):
                self.koficent = max(0, self.koficent-self.speed )
            elif event.button == 5 and self.retention(event.pos):
                self.koficent = min(self._update_size(self.items_holst.get_height(), self.holst.get_height())[1], self.koficent+self.speed )
            self.holst.fill(self.collor)
            self.offset_y = -self._event_size(self.items_holst.get_height(), self.holst.get_height(),self.koficent )
            self.holst.blit(self.items_holst, (0, self.offset_y))
            self.holst.blit(self.image_streak, (self.width-self._size_streak, self.koficent))
        return False
    def draw(self, screen: pg.Surface):
        screen.blit(self.holst, (self.left, self.top))
        if self.outline:
            pg.draw.rect(screen, self.outline_color, self.holst.get_rect(left=self.left, top=self.top), self.outline )
    def update(self): ...


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
    def clear(self, update = True):
        self.items.clear()
        if update:
            self._update()
    
if __name__ == '__main__':

    pg.init()
    screen = pg.display.set_mode((800, 600))
    se = ListOfItems((50, 50), (200, 200), hitbox=1, speed = 0.5)
    clock = pg.time.Clock()
    pg.display.flip()
    d = pg.Surface((1, 100))
    d.fill((32,45,23))
    da = pg.Surface((40, 100))
    da.fill((90,200,3))
    da1 = pg.Surface((40, 100))
    da1.fill((90,200,3))
    da2 = pg.Surface((44, 100))
    da2.fill((90,200,3))
    se.add(ListItems( d), ListItems( da), ListItems( da), ListItems( da))

    running = True
    while running:
        screen.fill((25, 25, 25))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if se.retention(event.pos):
                    print(se.index())
            
            se.event(event)
        se.draw(screen)
        clock.tick(60)
        pg.display.flip()
    pg.quit()