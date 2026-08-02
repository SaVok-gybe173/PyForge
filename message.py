from multiprocessing import Queue, Process
from PyForge.easel.window import Window
from PyForge.tools import PfObject
from PyForge.easel.window_transparency import set_window_transparency
from typing import Callable
from dataclasses import dataclass
import pygame as pg
import pyautogui
import threading
import time

SIZES = {"windows": [350, 100], "macos": [380, 110], "linux": [320, 90]}

def make_cross_surface(width: int, height: int, color=(255, 0, 0), thickness: int = 2) -> pg.Surface:
    """
    Создаёт поверхность с крестиком заданного размера.
    
    Аргументы:
        width (int): ширина поверхности
        height (int): высота поверхности
        color (tuple): цвет крестика в формате (R, G, B), по умолчанию красный
        thickness (int): толщина линий, по умолчанию 2
    
    Возвращает:
        pygame.Surface: поверхность с прозрачным фоном и крестиком
    """
    surf = pg.Surface((width, height), pg.SRCALPHA)
    pg.draw.line(surf, color, (0, 0), (width, height), thickness)
    pg.draw.line(surf, color, (width, 0), (0, height), thickness)
    return surf

def get_fun_standart(img: pg.Surface, name: str, message: str, platform = "windows", color = (55,55,55)):
    win = pg.Surface(SIZES[platform])
    font30 = pg.font.Font(None, 30)
    font24 = pg.font.Font(None, 24)

    win.fill(color)
    img = pg.transform.scale(img, (SIZES[platform][1]-20, SIZES[platform][1]-20))
    win.blit(make_cross_surface(10, 10, (170,170,170), 3), (SIZES[platform][0]-20, 20))
    win.blit(font30.render(name, True, (255,255,255)), (110, 10))
    win.blit(font24.render(message, True, (255,255,255)), (110, 45))

    rect_close = Rect(SIZES[platform][0]-20, 15, 20, 20, "close")

    win.blit(img, (10, 10))
    return [getParams(win)], [rect_close]

@dataclass
class Message:
    objects: list[bytes]
    rects: list["Rect"]
    clikc_fun: Callable = lambda _pos: _pos
    color: tuple[int, int, int] = (255, 255, 255)

    _win: Window|None = None
    que: Queue = None

@dataclass
class Params:
    width: int
    height: int
    data: bytes
    format: str

@dataclass
class Rect:
    left: int
    top: int
    width: int
    height: int
    name: str

def getParams(img: pg.Surface):
    format = "RGB" if img.get_alpha() is None else "RGBA"
    return Params(img.get_width(), img.get_height(), pg.image.tostring(img, format), format)

class MessageWindow(Window):
    def __init__(self, timeaut: int, pos, size=(400, 300), color=(255, 255, 255), scene: list | None = None, *, fps=60, flags = 0, zi_set_mode = ()):
        self.pos = pos
        self.timeaut = timeaut
        super().__init__(size, color, scene, fps=fps, flags=flags, zi_set_mode=zi_set_mode)

    def start(self, cfg: list[bytes], rects: list[Rect], que:Queue):
        self.cfg: list[pg.Surface] = cfg
        self.que = que
        self.rects = rects
        return super().start()
    
    def init(self, win):
        self.time = 0
        self.rect: list[pg.Rect] = []
        for i, cf in enumerate(self.cfg):
            self.cfg[i] = pg.image.fromstring(cf.data, (cf.width, cf.height), cf.format)
        for i, cf in enumerate(self.rects):
            self.rect.append(pg.Rect(cf.left, cf.top, cf.width, cf.height))

        pg.display.set_window_position(self.pos) # pip3 install pygame-ce

        threading.Thread(target=self.updatemess, daemon=True,).start()

    def updatemess(self):
        try:
            data: dict = self.que.get()
            if data["type"] == "pos":
                pg.display.set_window_position(data["pos"])
        except:
            self.close()

    def draw(self, sceen: pg.Surface):
        for cf in self.cfg:
            sceen.blit(cf, (0, 0))

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
           if event.button == 1:
               for i, rect in enumerate(self.rect):
                   #print(rect.collidepoint(event.pos), rect.left, rect.top, rect.width, rect.height)
                   if rect.collidepoint(event.pos):
                       if self.rects[i].name == "close":
                           self.close()

    def update(self):
        self.time += 1/60
        set_window_transparency(alpha_value=int( 255-min( (self.time/self.timeaut)*255,  255)))
        if self.time > self.timeaut-self.time/10:
            self.close()
    

class ManagerMessage:
    windows: list[MessageWindow] = []

    def __init__(self, size: list = SIZES["windows"], time:int =-1, max_win:int = 3, distance: int = 20):
        self.set(size, time, max_win, distance)

    @classmethod
    def set(cls, size: list= SIZES["windows"], time:int =5, max_win:int = 3, distance: int = 5):
        if max_win<1: raise ValueError(f"Должно быть max_win > 0 -> У тебя {max_win=} <= 0?")
        cls.distance = distance
        cls.size = size
        cls.time = time
        cls.max_win = max_win

    @classmethod
    def _start(cls, mess: Message):
        width, height = pyautogui.size()
        que = Queue()
        mess._win = MessageWindow(cls.time, (width-cls.size[0], height-cls.size[1]*(len(cls.windows)+1)-cls.distance*len(cls.windows)), cls.size, flags=pg.NOFRAME)
        mess.que = que
        mess._win.start(mess.objects, mess.rects, que)
        cls.windows.append(mess._win)

    @classmethod
    def add(cls,  mess: Message):
        windows = []
        for i in cls.windows:
            if i.is_alive():
                windows.append(i)
        width, height = pyautogui.size()
        cls.windows.clear()
        cls.windows.extend(windows)
        for i in enumerate(cls.windows):
            try:
                i.que.put({"type": "pos","pos":(width-cls.size[0], height-cls.size[1]*(i+1)-cls.distance*i) })
            except: ...
        if len(cls.windows) < cls.max_win:
            cls._start(mess)
            
def init():
    ManagerMessage.set()

if __name__ == "__main__":
    init()
    pg.font.init()
    objects,fun=get_fun_standart(pg.Surface((100, 100)), "Telegramm", "Пример")
    ManagerMessage.add(Message(objects, fun))
