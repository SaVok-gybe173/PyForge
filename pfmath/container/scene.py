from ...easel.object import PfObject
from ...easel.surface import Surface
from ...pfmath.markup import Point, Size
from .core import LayoutNode

class EmbeddedScene(PfObject):
    _dirty = True

    # это виджет-переходник между твоей ручной сценой и авто-лейаутом
    def __init__(self, page, container: LayoutNode, left_top: Point | tuple[int, int], width_height: Size | tuple[int, int],):
        super().__init__(page, left_top, width_height)
        self.container  = container

    def invalidate(self):
        self._dirty = True

    def _ensure_layout(self):
        if self._dirty:
            self.container.arrange(self.left, self.top, self.width, self.height)
            self._dirty = False

    def draw(self, surf: Surface):
        self._ensure_layout()
        self.container.draw(surf)

    def update(self, dt):
        self._ensure_layout()
        self.container.update(dt)


    # события (переходник)

    def quit(self, common, quit):
        return self.container.quit(common, quit)
    
    def app_terminating(self, common) -> None:
        return self.container.app_terminating(common)

    def app_lowmemory(self, common):
        return self.container.app_lowmemory(common)

    def app_willenterbackground(self, common):
        return self.container.app_willenterbackground(common)

    def app_didenterbackground(self, common):
        return self.container.app_didenterbackground(common)

    def app_willenterforeground(self, common):
        return self.container.app_willenterforeground(common)
    
    def app_didenterforeground(self, common):
        return self.container.app_didenterforeground(common)

    def localechanged(self, common):
        return self.container.localechanged(common)

    def displayevent(self, common, display):
        return self.container.displayevent(common, display)

    def windowevent(self, common, window):
        return self.container.windowevent(common, window)

    def syswmevent(self, common, syswm):
        return self.container.syswmevent(common, syswm)

    def clipboardupdate(self, common):
        return self.container.clipboardupdate(common)
    
    def render_targets_reset(self, common):
        return self.container.render_targets_reset(common)

    def render_device_reset(self, common):
        return self.container.render_device_reset(common)

    def sensorupdate(self, common, sensor):
        return self.container.sensorupdate(common, sensor)

    def keydown(self, common, key):
        return self.container.keydown(common, key)

    def keyup(self, common, key):
        return self.container.keyup(common, key)

    def textediting(self, common, edit):
        return self.container.textediting(common, edit)

    def textinput(self, common, text):
        return self.container.textinput(common, text)

    def keymapchanged(self, common):
        return self.container.keymapchanged(common)

    def textediting_ext(self, common, editExt):
        return self.container.textediting_ext(common, editExt)

    def mousemotion(self, common, motion):
        return self.container.mousemotion(common, motion)

    def mousebuttondown(self, common, button):
        return self.container.mousebuttondown(common, button)

    def mousebuttonup(self, common, button):
        return self.container.mousebuttonup(common, button)

    def mousewheel(self, common, wheel):
        return self.container.mousewheel(common, wheel)

    def joyaxismotion(self, common, jaxis):
        return self.container.joyaxismotion(common, jaxis)

    def joyballmotion(self, common, jball):
        return self.container.joyballmotion(common, jball)

    def joyhatmotion(self, common, jhat):
        return self.container.joyhatmotion(common, jhat)

    def joybuttondown(self, common, jbutton):
        return self.container.joybuttondown(common, jbutton)

    def joybuttonup(self, common, jbutton):
        return self.container.joybuttonup(common, jbutton)

    def joydeviceadded(self, common, jdevice):
        return self.container.joydeviceadded(common, jdevice)

    def joydeviceremoved(self, common, jdevice):
        return self.container.joydeviceremoved(common, jdevice)

    def joybatteryupdated(self, common, jbattery):
        return self.container.joybatteryupdated(common, jbattery)
    
    def controlleraxismotion(self, common, caxis):
        return self.container.controlleraxismotion(common, caxis)

    def controllerbuttondown(self, common, cbutton):
        return self.container.controllerbuttondown(common, cbutton)

    def controllerbuttonup(self, common, cbutton):
        return self.container.controllerbuttonup(common, cbutton)

    def controllerdeviceadded(self, common, cdevice):
        return self.container.controllerdeviceadded(common, cdevice)

    def controllerdeviceremoved(self, common, cdevice):
        return self.container.controllerdeviceremoved(common, cdevice)
    
    def controllerdeviceremapped(self, common, cdevice):
        return self.container.controllerdeviceremapped(common, cdevice)
    
    def controllertouchpaddown(self, common, ctouchpad):
        return self.container.controllertouchpaddown(common, ctouchpad)

    def controllertouchpadmotion(self, common, ctouchpad):
        return self.container.controllertouchpadmotion(common, ctouchpad)
    
    def controllertouchpadup(self, common, ctouchpad):
        return self.container.controllertouchpadup(common, ctouchpad)

    def controllersensorupdate(self, common, csensor):
        return self.container.controllersensorupdate(common, csensor)

    def fingerdown(self, common, tfinger):
        return self.container.fingerdown(common, tfinger)
    
    def fingerup(self, common, tfinger):
        return self.container.fingerup(common, tfinger)

    def fingermotion(self, common, tfinger):
        return self.container.fingermotion(common, tfinger)

    def multigesture(self, common, mgesture):
        return self.container.multigesture(common, mgesture)
    
    def dollargesture(self, common, dgesture):
        return self.container.dollargesture(common, dgesture)

    def dollarrecord(self, common, dgesture):
        return self.container.dollarrecord(common, dgesture)
    
    def audiodeviceadded(self, common, adevice):
        return self.container.audiodeviceadded(common, adevice)

    def audiodeviceremoved(self, common, adevice):
        return self.container.audiodeviceremoved(common, adevice)

    def dropbegin(self, common, drop):
        return self.container.dropbegin(common, drop)
    
    def dropfile(self, common, drop):
        return self.container.dropfile(common, drop)

    def droptext(self, common, drop):
        return self.container.droptext(common, drop)
    
    def dropcomplete(self, common, drop):
        return self.container.dropcomplete(common, drop)