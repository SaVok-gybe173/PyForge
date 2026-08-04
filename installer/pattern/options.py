from typing import Callable
from PyForge.button import Button

try:
    from .theme import TEMA, get_TEMA
    from .language import TRANSLATION, get_TRANSLATION
except (ModuleNotFoundError, ImportError):
    from PyForge.installer.pattern.theme import TEMA, get_TEMA
    from PyForge.installer.pattern.language import TRANSLATION, get_TRANSLATION
try:
    from .create import create_mark_off, create_mark_on
except (ModuleNotFoundError, ImportError):
    from PyForge.installer.pattern.create import create_mark_off, create_mark_on

try:
    from ...tools import PfObject
except: 
    from PyForge.tools import PfObject

from ..shortcut import create_and_move_shortcut

import pygame as pg
import os

# класс для дополнительных операциий
class _Options(PfObject):
    switch: Callable = lambda self, _: print(_)

    def __init__(self, left_top, name: str, fun: Callable, *, activ: bool = False):
        self.name = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12).render(name, True,  TEMA[get_TEMA()]['text'])
        self.on = create_mark_on()
        self.off = create_mark_off()
        self.activ = activ # текущий актив
        self.fun = fun # вызов когда закончиться установка

        if activ:
            self.buton = Button(left_top, self.on)
        else:
            self.buton = Button(left_top, self.off)

    def draw(self, sceen):
        self.buton.draw(sceen)
        sceen.blit(self.name, (self.buton.x+20, self.buton.y))

    def update(self):
        self.buton.update()

    def event(self, event):
        self.buton.event(event)

        if self.buton.lcm(event):
            if self.activ:
                self.buton.image = self.off
                self.switch(False)
            else:
                self.buton.image = self.on
                self.switch(True)
            self.activ = not self.activ

    def set_switch(self, switch: Callable):
        self.switch = switch

    def start(self, main):
        pass

def Options(name: str, fun, *, activ: bool = False, color=(0,0,0)) -> _Options:
    return _Options((0,0), name, fun,  activ, color)

def Options_icon(exeName):
    def fun(exe):
        create_and_move_shortcut(exe, os.path.expanduser("~/Desktop"))
    o = _Options((0,0), TRANSLATION[get_TRANSLATION()]["additionally-icon"], fun)
    o.start = lambda main: o.fun(os.path.join(main.path, main.name, exeName)) if o.activ else None
    return o
