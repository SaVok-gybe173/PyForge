try:
    from .pygames.creating.listitng import ListOfItems, ListItems
except:
    from pygames.creating.listitng import ListOfItems, ListItems
from dataclasses import dataclass
from threading import Thread
import os
try:
    import pygame as pg
    from pygame.font import Font, match_font
except ImportError as e:
    import sys
    print("102 - error:", e)
    sys.exit(102)

try:
    from .__info__ import __version__
except ImportError:
    from __info__ import __version__

class NewListItems(ListItems):
    @property
    def width(self):
        return self.image.get_size()[0]
    @width.setter
    def width(self, width):
        pass

@dataclass
class Comand:
    name: str
    flags: dict[str: str]
    args: list[str]
    none_name: list[str]
    error: str = ""


class HeartComand:
    __lines: str
    activ: bool = True
    _thread: Thread
    __environment:str = None
    _directory: str
    color = (255,255,255)

    @property
    def environment(self):
        return self.__environment

    def __init__(self):
        self.__lines = ""
        self._directory = os.path.expanduser("~") 

        self.print(f"Python PyForge [Version {__version__}]", "(c) Корпорация gybe173 (SaVok Corporation). Все права защищены.", sep='\n')

        self.__drip()
    def _update(self):
        pass
    def print(self, *values: object, sep: str | None = " ", end: str | None = "\n"):
        if sep is None: sep = " "
        if end is None: end = "\n"
        s = ""
        for i, el in enumerate(values):
            s += (el if type(el) is str else str(el)) + (sep if len(values) > i+1 else '')
        self.__lines += (end if self.__lines else '') + s
        self._update()
    def clear(self):
        self.__lines = ""
        self._update()
    
    @property
    def _lines(self):
        return self.__lines

    def input(self, line: str):
        self.print(line, end='')

        self.activ = False
        c = Comand("", dict(), list(), list())
        p = ""
        arg = False
        for i, l in enumerate( line.split()):
            try: 
                if arg:
                    arg = False
                    c.flags[p] = l
                if i == 0:
                    c.name = l
                elif '-' == l[0]:
                    c.flags[l] = None
                    p = l
                    arg = True
                else:
                    c.args.append(l)
            except Exception as e:
                c.error = e
        del p, arg
        self._thread =  Thread(target = self.comand, args = (c,), daemon=True).start()

    def comand(self, c: Comand):
        if c.name == "clear":
            self.clear()
        else:
            pass
        self.__drip()
        self.activ = True
    def __drip(self):
        self.print(self.__environment if not self.__environment is None else '', self._directory+'>', sep='')

class HeartComandRendr(HeartComand):
    def __init__(self, left: int, top: int, width: int, height: int, font: Font):
        '''
        командная строка HeartComandRend
        
        Args:
            left, top: int- кординаты
            width, height: int - размеры
            font: Font - шрифт
        '''
        self.font = font
        self._width, self._height = width, height
        self.cmd = ListOfItems((left, top), (width, height), distance = 0)
        self.draw = self.cmd.draw
        self.event = self.cmd.event
        self.update = self.cmd.update

        
        super().__init__()
    def _update(self):
        l = list()
        p = 0
        color_line = self.color
        for line in self._lines.split('\n'):
            self.lin_Surfase = pg.Surface((self._width, 15), pg.SRCALPHA)
            self.lin_Surfase.fill((0,0,0,0))
            if len(line) > 10 and "<color=" in line:
                for i in range(line.count("<color=")):
                    if line.find("<color="):
                        r = self.font.render(line[:line.find("<color=")], True, color_line)
                        self.lin_Surfase.blit(r, (p,0))
                        p += r.get_width()
                        print(p)
                        line = line[line.find("<color=")+len("<color="):len(line)]
                        print(line)
                        color_line = tuple(map(int, line[:line.index('>')].split(',')))
                        line = line[line.index('>')+1:len(line)]
                        print(color_line)
                self.lin_Surfase.blit(self.font.render(line, True, color_line), (p,0))
            else:
                self.lin_Surfase.blit(self.font.render(line, True, (255,255,255)), (0,0))
            l.append(NewListItems(self.lin_Surfase))
        self.cmd.items.clear()
        self.cmd.add(*l)
if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((800, 600))
    font15 = Font(match_font('dejavusans'), 14)
    se = HeartComandRendr(0,0, screen.get_width(), screen.get_height(), font15)
    clock = pg.time.Clock()
    se.print("ascasc<color=34,212,45>dsapoopo<color=255,0,34>dsaads")
    running = True
    while running:
        screen.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pass
            #print(se._lines)
            se.event(event)
        se.draw(screen)
        clock.tick(60)
        pg.display.flip()
    pg.quit()
        
        

