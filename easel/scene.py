"""
Модуль со структурой сценны
"""
from typing import Any, TYPE_CHECKING, Self
from .object import CoreObject, PfObject
import pygame as pg

if TYPE_CHECKING:
    from .window import Window
else:
    type Window = Any

class Scene(CoreObject):
    name: str
    page: Window
    
    def __init__(self, win = None):
        self._win = win
        self.name = type(self).__name__
        self.objects: list[PfObject] = []

    def append(self, object: PfObject):
        self.objects.append(object)

    def activeevent(self, gain, state):
        for object in self.objects:
            object.activeevent(gain, state)
    def videoresize(self, size, w, h):
        for object in self.objects:
            object.videoresize(size, w, h)
    def videoexpose(self):
        for object in self.objects:
            object.videoexpose()
    def render_targets_reset(self):
        for object in self.objects:
            object.render_targets_reset()

    def keydown(self, key, mod, unicode, scancode):
        for object in self.objects:
            object.keydown(key, mod, unicode, scancode)
    def keyup(self, key, mod, scancode):
        for object in self.objects:
            object.keyup(key, mod, scancode)
    def textediting(self, text, start, length):
        for object in self.objects:
            object.textediting(text, start, length)
    def textinput(self, text):
        for object in self.objects:
            object.textinput(text)

    def mousemotion(self, pos, rel, buttons, touch):
        for object in self.objects:
            object.mousemotion(pos, rel, buttons, touch)
    def mousebuttondown(self, pos, button, touch):
        for object in self.objects:
            object.mousebuttondown(pos, button, touch)
    def mousebuttonup(self, pos, button, touch):
        for object in self.objects:
            object.mousebuttonup(pos, button, touch)
    def mousewheel(self, x, y, flipped, which, precise_x, precise_y):
        for object in self.objects:
            object.mousewheel(x, y, flipped, which, precise_x, precise_y)

# методы эвентов по их типу
EVENTS_METOD = {
    pg.event.event_name(pg.ACTIVEEVENT): (lambda obj, event: obj.activeevent(event.gain, event.state)),
    pg.event.event_name(pg.VIDEORESIZE):  (lambda obj, event: obj.videoresize(event.size, event.w, event.h)), 
    pg.event.event_name(pg.VIDEOEXPOSE): (lambda obj, _: obj.videoexpose()), 
    pg.event.event_name(pg.RENDER_TARGETS_RESET):  (lambda obj, _: obj.render_targets_reset()),

    pg.event.event_name(pg.KEYDOWN): (lambda obj, event: obj.keydown(event.key, event.mod, event.unicode, event.scancode)), 
    pg.event.event_name(pg.KEYUP): (lambda obj, event: obj.keyup(event.key, event.mod, event.scancode)), 
    pg.event.event_name(pg.TEXTEDITING): (lambda obj, event: obj.textediting(event.text, event.start, event.length)), 
    pg.event.event_name(pg.TEXTINPUT): (lambda obj, event: obj.textinput(event.text)),

    pg.event.event_name(pg.MOUSEMOTION): (lambda obj, event: obj.mousemotion(event.pos, event.rel, event.buttons, event.touch)),
    pg.event.event_name(pg.MOUSEBUTTONDOWN): (lambda obj, event: obj.mousebuttondown(event.pos, event.button, event.touch)),
    pg.event.event_name(pg.MOUSEBUTTONUP): (lambda obj, event: obj.mousebuttonup(event.pos, event.button, event.touch)),
    pg.event.event_name(pg.MOUSEWHEEL): (lambda obj, event: obj.mousewheel(event.x, event.y, event.flipped, event.which, event.precise_x, event.precise_y)),

}