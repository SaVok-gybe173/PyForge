"""
Модуль со структурой сцены
"""
from typing import Any, TYPE_CHECKING, Self
from .object import CoreObject, PfObject
from .event import (event_name,
        QUIT,
        APP_TERMINATING,
        APP_LOWMEMORY,
        APP_WILLENTERBACKGROUND,
        APP_DIDENTERBACKGROUND,
        APP_WILLENTERFOREGROUND,
        APP_DIDENTERFOREGROUND,
        LOCALECHANGED,
        DISPLAYEVENT,
        WINDOWEVENT,
        SYSWMEVENT,
        CLIPBOARDUPDATE,
        RENDER_TARGETS_RESET,
        RENDER_DEVICE_RESET,
        SENSORUPDATE,

        KEYDOWN,
        KEYUP,
        TEXTEDITING,
        TEXTINPUT,
        KEYMAPCHANGED,
        TEXTEDITING_EXT,

        MOUSEMOTION,
        MOUSEBUTTONDOWN,
        MOUSEBUTTONUP,
        MOUSEWHEEL,

        JOYAXISMOTION,
        JOYBALLMOTION,
        JOYHATMOTION,
        JOYBUTTONDOWN,
        JOYBUTTONUP,
        JOYDEVICEADDED,
        JOYDEVICEREMOVED,
        JOYBATTERYUPDATED,

        CONTROLLERAXISMOTION,
        CONTROLLERBUTTONDOWN,
        CONTROLLERBUTTONUP,
        CONTROLLERDEVICEADDED,
        CONTROLLERDEVICEREMOVED,
        CONTROLLERDEVICEREMAPPED,
        CONTROLLERTOUCHPADDOWN,
        CONTROLLERTOUCHPADMOTION,
        CONTROLLERTOUCHPADUP,
        CONTROLLERSENSORUPDATE,

        FINGERDOWN,
        FINGERUP,
        FINGERMOTION,
        MULTIGESTURE,
        DOLLARGESTURE,
        DOLLARRECORD,

        AUDIODEVICEADDED,
        AUDIODEVICEREMOVED,

        DROPBEGIN,
        DROPFILE,
        DROPTEXT,
        DROPCOMPLETE,

        USEREVENT,
        LASTEVENT,

        FIRSTEVENT,
        POLLSENTINEL,
        )

if TYPE_CHECKING:
    from .window import Window
else:
    Window = Any

class Scene(CoreObject):
    name: str
    page: Window
    
    def __init__(self, page: Window):
        self.page = page
        self.name = type(self).__name__
        self.objects: list[PfObject] = []

    def append(self, object: PfObject) -> None:
        """
        Добавляет объект в конец списка.
        """
        self.objects.append(object)

    def quit(self, common, quit):
        for object in self.objects:
            object.quit(common, quit)

    def draw(self, win):
        for object in self.objects:
            object.draw(win)

    def update(self, dt):
        for object in self.objects:
            object.update(dt)

    def event(self, event):
        for object in self.objects:
            object.event(event)

    def render_targets_reset(self, common):
        for object in self.objects:
            object.render_targets_reset(common)

    def keydown(self, common, key):
        for object in self.objects:
            object.keydown(key, common, key)
    def keyup(self, common, key):
        for object in self.objects:
            object.keyup(common, key)

    def mousemotion(self, common, motion):
        for object in self.objects:
            object.mousemotion(common, motion)
    def mousebuttondown(self, common, button):
        for object in self.objects:
            object.mousebuttondown(common, button)
    def mousebuttonup(self, common, button):
        for object in self.objects:
            object.mousebuttonup(common, button)
    def mousewheel(self, common, wheel):
        for object in self.objects:
            object.mousewheel(common, wheel)

# методы событий по их типу
EVENTS_METHOD = {
    event_name(QUIT): (lambda obj, event: obj.quit(event.common, event.quit)),
    event_name(APP_TERMINATING):  (lambda obj, event: obj.app_terminating(event.common)), 
    event_name(APP_LOWMEMORY): (lambda obj, event: obj.app_lowmemory(event.common)), 
    event_name(APP_WILLENTERBACKGROUND): (lambda obj, event: obj.app_willenterbackground(event.common)), 
    event_name(APP_DIDENTERBACKGROUND): (lambda obj, event: obj.app_didenterbackground(event.common)), 
    event_name(APP_WILLENTERFOREGROUND): (lambda obj, event: obj.app_willenterforeground(event.common)), 
    event_name(APP_DIDENTERFOREGROUND): (lambda obj, event: obj.app_didenterforeground(event.common)), 
    event_name(LOCALECHANGED): (lambda obj, event: obj.localechanged(event.common)), 
    event_name(DISPLAYEVENT): (lambda obj, event: obj.displayevent(event.common, event.display)), 
    event_name(WINDOWEVENT): (lambda obj, event: obj.windowevent(event.common, event.window)), 
    event_name(SYSWMEVENT): (lambda obj, event: obj.syswmevent(event.common, event.syswm)), 
    event_name(CLIPBOARDUPDATE): (lambda obj, event: obj.clipboardupdate(event.common)), 
    event_name(RENDER_TARGETS_RESET): (lambda obj, event: obj.render_targets_reset(event.common)), 
    event_name(RENDER_DEVICE_RESET): (lambda obj, event: obj.render_device_reset(event.common)), 
    event_name(SENSORUPDATE): (lambda obj, event: obj.sensorupdate(event.common, event.sensor)), 

    event_name(KEYDOWN): (lambda obj, event: obj.keydown(event.common, event.key)), 
    event_name(KEYUP): (lambda obj, event: obj.keyup(event.common, event.key)), 
    event_name(TEXTEDITING): (lambda obj, event: obj.textediting(event.common, event.edit)), 
    event_name(TEXTINPUT): (lambda obj, event: obj.textinput(event.common, event.text)), 
    event_name(KEYMAPCHANGED): (lambda obj, event: obj.keymapchanged(event.common)), 
    event_name(TEXTEDITING_EXT): (lambda obj, event: obj.textediting_ext(event.common, event.editExt)), 

    event_name(MOUSEMOTION): (lambda obj, event: obj.mousemotion(event.common, event.motion)), 
    event_name(MOUSEBUTTONDOWN): (lambda obj, event: obj.mousebuttondown(event.common, event.button)), 
    event_name(MOUSEBUTTONUP): (lambda obj, event: obj.mousebuttonup(event.common, event.button)), 
    event_name(MOUSEWHEEL): (lambda obj, event: obj.mousewheel(event.common, event.wheel)), 

    event_name(JOYAXISMOTION): (lambda obj, event: obj.joyaxismotion(event.common, event.jaxis)), 
    event_name(JOYBALLMOTION): (lambda obj, event: obj.joyballmotion(event.common, event.jball)), 
    event_name(JOYHATMOTION): (lambda obj, event: obj.joyhatmotion(event.common, event.jhat)), 
    event_name(JOYBUTTONDOWN): (lambda obj, event: obj.joybuttondown(event.common, event.jbutton)), 
    event_name(JOYBUTTONUP): (lambda obj, event: obj.joybuttonup(event.common, event.jbutton)), 
    event_name(JOYDEVICEADDED): (lambda obj, event: obj.joydeviceadded(event.common, event.jdevice)), 
    event_name(JOYDEVICEREMOVED): (lambda obj, event: obj.joydeviceremoved(event.common, event.jdevice)), 
    event_name(JOYBATTERYUPDATED): (lambda obj, event: obj.joybatteryupdated(event.common, event.jbattery)), 

    event_name(CONTROLLERAXISMOTION): (lambda obj, event: obj.controlleraxismotion(event.common, event.caxis)), 
    event_name(CONTROLLERBUTTONDOWN): (lambda obj, event: obj.controllerbuttondown(event.common, event.cbutton)), 
    event_name(CONTROLLERBUTTONUP): (lambda obj, event: obj.controllerbuttonup(event.common, event.cbutton)), 
    event_name(CONTROLLERDEVICEADDED): (lambda obj, event: obj.controllerdeviceadded(event.common, event.cdevice)), 
    event_name(CONTROLLERDEVICEREMOVED): (lambda obj, event: obj.controllerdeviceremoved(event.common, event.cdevice)),
    event_name(CONTROLLERDEVICEREMAPPED): (lambda obj, event: obj.controllerdeviceremapped(event.common, event.cdevice)),
    event_name(CONTROLLERTOUCHPADDOWN): (lambda obj, event: obj.controllertouchpaddown(event.common, event.ctouchpad)),
    event_name(CONTROLLERTOUCHPADMOTION): (lambda obj, event: obj.controllertouchpadmotion(event.common, event.ctouchpad)),
    event_name(CONTROLLERTOUCHPADUP): (lambda obj, event: obj.controllertouchpadup(event.common, event.ctouchpad)),
    event_name(CONTROLLERSENSORUPDATE): (lambda obj, event: obj.controllersensorupdate(event.common, event.csensor)),

    event_name(FINGERDOWN): (lambda obj, event: obj.fingerdown(event.common, event.tfinger)),
    event_name(FINGERUP): (lambda obj, event: obj.fingerup(event.common, event.tfinger)),
    event_name(FINGERMOTION): (lambda obj, event: obj.fingermotion(event.common, event.tfinger)),
    event_name(MULTIGESTURE): (lambda obj, event: obj.multigesture(event.common, event.mgesture)),
    event_name(DOLLARGESTURE): (lambda obj, event: obj.dollargesture(event.common, event.dgesture)),
    event_name(DOLLARRECORD): (lambda obj, event: obj.dollarrecord(event.common, event.dgesture)),

    event_name(AUDIODEVICEADDED): (lambda obj, event: obj.audiodeviceadded(event.common, event.adevice)),
    event_name(AUDIODEVICEREMOVED): (lambda obj, event: obj.audiodeviceremoved(event.common, event.adevice)),

    event_name(DROPBEGIN): (lambda obj, event: obj.dropbegin(event.common, event.drop)),
    event_name(DROPFILE): (lambda obj, event: obj.dropfile(event.common, event.drop)),
    event_name(DROPTEXT): (lambda obj, event: obj.droptext(event.common, event.drop)),
    event_name(DROPCOMPLETE): (lambda obj, event: obj.dropcomplete(event.common, event.drop)),
}