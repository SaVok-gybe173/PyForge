from .core import LayoutNode
from .constants import AUTO, CENTER, NATURAL, FILL_W, FILL_H
from ...easel.object import PfObject
from ...easel.surface import Surface
from ...easel.draw import rect

class Container(LayoutNode):
    def __init__(self, page, widget: PfObject, size_w=AUTO, size_h=AUTO,
             align=CENTER, resize=NATURAL, padding=0, bgcolor=None):
        """
        widget    - ваш виджет
        align     - как разместить виджет внутри (CENTER / TOP_LEFT / Align(fx,fy))
        resize - что делать с размером виджета:
            NATURAL  - оставить natural_size
            FILL     - растянуть по обеим осям
            FILL_W / FILL_H - только по одной
            tuple    - точный размер (rw, rh)
    
        padding   - внутренние отступы
        bgcolor   - залить прямоугольник (для фона/отладки)
        """
        super().__init__(page, (0, 0), (0, 0))
        self.widget   = widget
        self.size_w, self.size_h = size_w, size_h
        self.align    = align
        self.resize   = resize
        self.padding  = padding
        self.bgcolor  = bgcolor

    def measure(self, avail_w, avail_h):
        w = self.resolve(self.size_w, avail_w)
        h = self.resolve(self.size_h, avail_h)
        if w is None or h is None:
            if isinstance(self.widget, LayoutNode):
                nw, nh = self.widget.measure(
                    w - 2*self.padding if w is not None else avail_w,
                    h - 2*self.padding if h is not None else avail_h,
                )
            else:
                nw, nh = self.widget.width_height
            if w is None: w = nw + 2*self.padding
            if h is None: h = nh + 2*self.padding
        return w, h

    def arrange(self, x, y, w, h):
        super().arrange(x, y, w, h)
        if isinstance(self.resize, tuple):
            rw, rh = self.resize
            cw = max(0, self.resolve(rw, w - 2*self.padding))
            ch = max(0, self.resolve(rh, h - 2*self.padding))
        else:
            if isinstance(self.widget, LayoutNode):
                nw, nh = self.widget.measure(w - 2*self.padding, h - 2*self.padding)
            else:
                nw, nh = self.widget.width_height
            cw = max(0, w - 2*self.padding) if self.resize & FILL_W else nw
            ch = max(0, h - 2*self.padding) if self.resize & FILL_H else nh

        cx, cy = self.place(
            x + self.padding, y + self.padding,
            w - 2*self.padding, h - 2*self.padding,
            cw, ch,
        )
        if isinstance(self.widget, LayoutNode):
            self.widget.arrange(cx, cy, cw, ch)
        else:
            self.widget.left_top     = (cx, cy)
            self.widget.width_height = (cw, ch)


    def draw(self, surf: Surface):
        if self.bgcolor is not None:
            rect(surf, self.bgcolor, self.rect)
        self.widget.draw(surf)

    def event(self, event):
        return self.widget.event(event)

    def update(self, dt):
        self.widget.update(dt)

   # события (переходник)

    def quit(self, common, quit):
        return self.widget.quit(common, quit)
    
    def app_terminating(self, common) -> None:
        return self.widget.app_terminating(common)

    def app_lowmemory(self, common):
        return self.widget.app_lowmemory(common)

    def app_willenterbackground(self, common):
        return self.widget.app_willenterbackground(common)

    def app_didenterbackground(self, common):
        return self.widget.app_didenterbackground(common)

    def app_willenterforeground(self, common):
        return self.widget.app_willenterforeground(common)
    
    def app_didenterforeground(self, common):
        return self.widget.app_didenterforeground(common)

    def localechanged(self, common):
        return self.widget.localechanged(common)

    def displayevent(self, common, display):
        return self.widget.displayevent(common, display)

    def windowevent(self, common, window):
        return self.widget.windowevent(common, window)

    def syswmevent(self, common, syswm):
        return self.widget.syswmevent(common, syswm)

    def clipboardupdate(self, common):
        return self.widget.clipboardupdate(common)
    
    def render_targets_reset(self, common):
        return self.widget.render_targets_reset(common)

    def render_device_reset(self, common):
        return self.widget.render_device_reset(common)

    def sensorupdate(self, common, sensor):
        return self.widget.sensorupdate(common, sensor)

    def keydown(self, common, key):
        return self.widget.keydown(common, key)

    def keyup(self, common, key):
        return self.widget.keyup(common, key)

    def textediting(self, common, edit):
        return self.widget.textediting(common, edit)

    def textinput(self, common, text):
        return self.widget.textinput(common, text)

    def keymapchanged(self, common):
        return self.widget.keymapchanged(common)

    def textediting_ext(self, common, editExt):
        return self.widget.textediting_ext(common, editExt)

    def mousemotion(self, common, motion):
        return self.widget.mousemotion(common, motion)

    def mousebuttondown(self, common, button):
        return self.widget.mousebuttondown(common, button)

    def mousebuttonup(self, common, button):
        return self.widget.mousebuttonup(common, button)

    def mousewheel(self, common, wheel):
        return self.widget.mousewheel(common, wheel)

    def joyaxismotion(self, common, jaxis):
        return self.widget.joyaxismotion(common, jaxis)

    def joyballmotion(self, common, jball):
        return self.widget.joyballmotion(common, jball)

    def joyhatmotion(self, common, jhat):
        return self.widget.joyhatmotion(common, jhat)

    def joybuttondown(self, common, jbutton):
        return self.widget.joybuttondown(common, jbutton)

    def joybuttonup(self, common, jbutton):
        return self.widget.joybuttonup(common, jbutton)

    def joydeviceadded(self, common, jdevice):
        return self.widget.joydeviceadded(common, jdevice)

    def joydeviceremoved(self, common, jdevice):
        return self.widget.joydeviceremoved(common, jdevice)

    def joybatteryupdated(self, common, jbattery):
        return self.widget.joybatteryupdated(common, jbattery)
    
    def controlleraxismotion(self, common, caxis):
        return self.widget.controlleraxismotion(common, caxis)

    def controllerbuttondown(self, common, cbutton):
        return self.widget.controllerbuttondown(common, cbutton)

    def controllerbuttonup(self, common, cbutton):
        return self.widget.controllerbuttonup(common, cbutton)

    def controllerdeviceadded(self, common, cdevice):
        return self.widget.controllerdeviceadded(common, cdevice)

    def controllerdeviceremoved(self, common, cdevice):
        return self.widget.controllerdeviceremoved(common, cdevice)
    
    def controllerdeviceremapped(self, common, cdevice):
        return self.widget.controllerdeviceremapped(common, cdevice)
    
    def controllertouchpaddown(self, common, ctouchpad):
        return self.widget.controllertouchpaddown(common, ctouchpad)

    def controllertouchpadmotion(self, common, ctouchpad):
        return self.widget.controllertouchpadmotion(common, ctouchpad)
    
    def controllertouchpadup(self, common, ctouchpad):
        return self.widget.controllertouchpadup(common, ctouchpad)

    def controllersensorupdate(self, common, csensor):
        return self.widget.controllersensorupdate(common, csensor)

    def fingerdown(self, common, tfinger):
        return self.widget.fingerdown(common, tfinger)
    
    def fingerup(self, common, tfinger):
        return self.widget.fingerup(common, tfinger)

    def fingermotion(self, common, tfinger):
        return self.widget.fingermotion(common, tfinger)

    def multigesture(self, common, mgesture):
        return self.widget.multigesture(common, mgesture)
    
    def dollargesture(self, common, dgesture):
        return self.widget.dollargesture(common, dgesture)

    def dollarrecord(self, common, dgesture):
        return self.widget.dollarrecord(common, dgesture)
    
    def audiodeviceadded(self, common, adevice):
        return self.widget.audiodeviceadded(common, adevice)

    def audiodeviceremoved(self, common, adevice):
        return self.widget.audiodeviceremoved(common, adevice)

    def dropbegin(self, common, drop):
        return self.widget.dropbegin(common, drop)
    
    def dropfile(self, common, drop):
        return self.widget.dropfile(common, drop)

    def droptext(self, common, drop):
        return self.widget.droptext(common, drop)
    
    def dropcomplete(self, common, drop):
        return self.widget.dropcomplete(common, drop)