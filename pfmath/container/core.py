from .constants import AUTO, CENTER
from .wrapper import Container
from ...easel.object import PfObject
from ...easel.surface import Surface
from ...easel.event import (
        Event,
        CommonEvent,
        DisplayEvent,
        WindowEvent,
        KeyboardEvent,
        TextEditingEvent,
        TextEditingExtEvent,
        TextInputEvent,
        MouseMotionEvent,
        MouseButtonEvent,
        MouseWheelEvent,
        JoyAxisEvent,
        JoyBallEvent,
        JoyHatEvent,
        JoyButtonEvent,
        JoyDeviceEvent,
        JoyBatteryEvent,
        ControllerAxisEvent,
        ControllerButtonEvent,
        ControllerDeviceEvent,
        ControllerTouchpadEvent,
        ControllerSensorEvent,
        SensorEvent,
        QuitEvent,
        UserEvent,
        SysWMEvent,
        TouchFingerEvent,
        MultiGestureEvent,
        DollarGestureEvent,
        DropEvent,
        AudioDeviceEvent
    )


class LayoutNode(PfObject):
    align: tuple[int, int]
    # Размеры, которые запросил пользователь (px / frac / AUTO)
    size_w = AUTO
    size_h = AUTO

    def measure(self, avail_w, avail_h):
        """Сколько нужно места при доступном (avail_w, avail_h).
        не меняет self.rect и не двигает детей.
        Возвращает (w, h) - желаемый размер."""
        raise NotImplementedError

    def arrange(self, x, y, w, h):
        """Окончательный прямоугольник (x, y, w, h).
        Поставь self.rect и разложи детей рекурсивно.
        это единственное место, где вообще меняется rect."""
        self.left, self.top = x, y
        self.width, self.height = w, h

    @staticmethod
    def resolve(value, available):
        """Превратить в пиксели, зная сколько места дали родители.
        Возвращает None, если размер AUTO (пусть решает родитель)."""
        if value is None: return None
        if value > 1: return value
        return available * value

    def place(self, px_, py_, pw, ph, cw, ch):
        """Где поставить ребёнка размера (cw, ch),
        внутри прямоугольника (px_, py_, pw, ph).
        Возвращает (x, y) левого верхнего угла ребёнка."""
        x = px_ + (pw - cw) * self.align[0]
        y = py_ + (ph - ch) * self.align[1]
        return x, y


class MultiChildNode(LayoutNode):
    """Общий предок Row/Column: несколько детей, проксирование вызовов."""

    def __init__(self, page, children: list[Container], size_w=AUTO, size_h=AUTO, padding=0):
        super().__init__(page, (0, 0), (0, 0))
        self.children = list(children)   # копия, чтобы не мутировать вход
        self.size_w   = size_w
        self.size_h   = size_h
        self.padding  = padding

    def draw(self, surf: Surface):
        for c in self.children:
            c.draw(surf)

    def update(self, dt):
        for c in self.children:
            c.update(dt)

    ### обратная совместимость
    
    # Системные события
    def quit(self, common: CommonEvent, quit: QuitEvent) -> None:
        """
        SDL_QUIT
        Пользователь запросил закрытие приложения (нажал на крестик окна, Alt+F4 или эквивалент в оконной системе).
        """
        for object in self.children:
            object.quit(common, quit)

    def app_terminating(self, common: CommonEvent) -> None:
        """
        SDL_APP_TERMINATING
        Приложение завершается ОС (iOS/Android)
        """
        for object in self.children:
            object.app_terminating(common)

    def app_lowmemory(self, common: CommonEvent) -> None:
        """
        SDL_APP_LOWMEMORY
        Приложению не хватает памяти
        """
        for object in self.children:
            object.app_lowmemory(common)

    def app_willenterbackground(self, common: CommonEvent) -> None:
        """
        SDL_APP_WILLENTERBACKGROUND
        Приложение собирается уйти в фон
        """
        for object in self.children:
            object.app_willenterbackground(common)

    def app_didenterbackground(self, common: CommonEvent) -> None:
        """
        SDL_APP_DIDENTERBACKGROUND
        Приложение ушло в фон
        """
        for object in self.children:
            object.app_didenterbackground(common)

    def app_willenterforeground(self, common: CommonEvent) -> None:
        """
        SDL_APP_WILLENTERFOREGROUND
        Приложение собирается вернуться на передний план
        """
        for object in self.children:
            object.app_willenterforeground(common)

    def app_didenterforeground(self, common: CommonEvent) -> None:
        """
        SDL_APP_DIDENTERFOREGROUND
        Приложение снова активно
        """
        for object in self.children:
            object.app_didenterforeground(common)

    def localechanged(self, common: CommonEvent) -> None:
        """
        SDL_LOCALECHANGED
        Изменились локальные настройки пользователя
        """
        for object in self.children:
            object.localechanged(common)

    def displayevent(self, common: CommonEvent, display: DisplayEvent) -> None:
        """
        SDL_DISPLAYEVENT
        Изменение состояния дисплея
        """
        for object in self.children:
            object.displayevent(common, display)

    def windowevent(self, common: CommonEvent, window: WindowEvent) -> None:
        """
        SDL_WINDOWEVENT
        Изменение состояния окна (фокус, размер, перемещение и т.п.)
        """
        for object in self.children:
            object.windowevent(common, window)

    def syswmevent(self, common: CommonEvent, syswm: SysWMEvent) -> None:
        """
        SDL_SYSWMEVENT
        Системное событие оконного менеджера
        """
        for object in self.children:
            object.syswmevent(common, syswm)

    def clipboardupdate(self, common: CommonEvent) -> None:
        """
        SDL_CLIPBOARDUPDATE
        Изменилось содержимое буфера обмена
        """
        for object in self.children:
            object.clipboardupdate(common)

    def render_targets_reset(self, common: CommonEvent) -> None:
        """
        SDL_RENDER_TARGETS_RESET
        Цели рендеринга сброшены (нужно обновить содержимое)
        """
        for object in self.children:
            object.render_targets_reset(common)

    def render_device_reset(self, common: CommonEvent) -> None:
        """
        SDL_RENDER_DEVICE_RESET
        Устройство рендеринга сброшено (нужно пересоздать текстуры)
        """
        for object in self.children:
            object.render_device_reset(common)

    def sensorupdate(self, common: CommonEvent, sensor: SensorEvent) -> None:
        """
        SDL_SENSORUPDATE
        Обновились данные сенсора
        """
        for object in self.children:
            object.sensorupdate(common, sensor)

    # События клавиатуры
    def keydown(self, common: CommonEvent, key: KeyboardEvent) -> None:
        """
        SDL_KEYDOWN
        Клавиша нажата
        """
        for object in self.children:
            object.keydown(common, key)
        
    def keyup(self, common: CommonEvent, key: KeyboardEvent) -> None:
        """
        SDL_KEYUP
        Клавиша отпущена
        """
        for object in self.children:
            object.keyup(common, key)

    def textediting(self, common: CommonEvent, edit: TextEditingEvent) -> None:
        """
        SDL_TEXTEDITING
        Редактирование текста (IME, композиция)
        """
        for object in self.children:
            object.textediting(common, edit)

    def textinput(self, common: CommonEvent, text: TextInputEvent) -> None:
        """
        SDL_TEXTINPUT
        Ввод текста (после завершения IME)
        """
        for object in self.children:
            object.textinput(common, text)

    def keymapchanged(self, common: CommonEvent) -> None:
        """
        SDL_KEYMAPCHANGED
        Раскладка клавиатуры изменилась системой
        """
        for object in self.children:
            object.keymapchanged(common)

    def textediting_ext(self, common: CommonEvent, editExt: TextEditingExtEvent) -> None:
        """
        SDL_TEXTEDITING_EXT
        Расширенное редактирование текста (IME)
        """
        for object in self.children:
            object.textediting_ext(common, editExt)

    # События мыши

    def mousemotion(self, common: CommonEvent, motion: MouseMotionEvent) -> None:
        """
        SDL_MOUSEMOTION
        Перемещение мыши
        """
        for object in self.children:
            object.mousemotion(common, motion)

    def mousebuttondown(self, common: CommonEvent, button: MouseButtonEvent) -> None:
        """
        SDL_MOUSEBUTTONDOWN
        Кнопка мыши нажата
        """
        for object in self.children:
            object.mousebuttondown(common, button)
            
    def mousebuttonup(self, common: CommonEvent, button: MouseButtonEvent) -> None:
        """
        SDL_MOUSEBUTTONUP
        Кнопка мыши отпущена
        """
        for object in self.children:
            object.mousebuttonup(common, button)

    def mousewheel(self, common: CommonEvent, wheel: MouseWheelEvent) -> None:
        """
        SDL_MOUSEWHEEL
        Прокрутка колеса мыши
        """
        for object in self.children:
            object.mousewheel(common, wheel)

    # Джойстик (классический API)

    def joyaxismotion(self, common: CommonEvent, jaxis: JoyAxisEvent) -> None:
        """
        SDL_JOYAXISMOTION
        Движение оси джойстика
        """
        for object in self.children:
            object.joyaxismotion(common, jaxis)

    def joyballmotion(self, common: CommonEvent, jball: JoyBallEvent) -> None:
        """
        SDL_JOYBALLMOTION
        Движение трекбола
        """
        for object in self.children:
            object.joyballmotion(common, jball)

    def joyhatmotion(self, common: CommonEvent, jhat: JoyHatEvent) -> None:
        """
        SDL_JOYHATMOTION
        Изменение POV-переключателя (hat)
        """
        for object in self.children:
            object.joyhatmotion(common, jhat)

    def joybuttondown(self, common: CommonEvent, jbutton: JoyButtonEvent) -> None:
        """
        SDL_JOYBUTTONDOWN
        Кнопка джойстика нажата
        """
        for object in self.children:
            object.joybuttondown(common, jbutton)

    def joybuttonup(self, common: CommonEvent, jbutton: JoyButtonEvent) -> None:
        """
        SDL_JOYBUTTONUP
        Кнопка джойстика отпущена
        """
        for object in self.children:
            object.joybuttonup(common, jbutton)

    def joydeviceadded(self, common: CommonEvent, jdevice: JoyDeviceEvent) -> None:
        """
        SDL_JOYDEVICEADDED
        Джойстик подключён
        """
        for object in self.children:
            object.joydeviceadded(common, jdevice)

    def joydeviceremoved(self, common: CommonEvent, jdevice: JoyDeviceEvent) -> None:
        """
        SDL_JOYDEVICEREMOVED
        Джойстик отключён
        """
        for object in self.children:
            object.joydeviceremoved(common, jdevice)

    def joybatteryupdated(self, common: CommonEvent, jbattery: JoyBatteryEvent) -> None:
        """
        SDL_JOYBATTERYUPDATED
        Изменился уровень заряда джойстика
        """
        for object in self.children:
            object.joybatteryupdated(common, jbattery)

    # Контроллеры (Game Controller API, SDL2)

    def controlleraxismotion(self, common: CommonEvent, caxis: ControllerAxisEvent) -> None:
        """
        SDL_CONTROLLERAXISMOTION
        Движение оси контроллера
        """
        for object in self.children:
            object.controlleraxismotion(common, caxis)

    def controllerbuttondown(self, common: CommonEvent, cbutton: ControllerButtonEvent) -> None:
        """
        SDL_CONTROLLERBUTTONDOWN
        Кнопка контроллера нажата
        """
        for object in self.children:
            object.controllerbuttondown(common, cbutton)

    def controllerbuttonup(self, common: CommonEvent, cbutton: ControllerButtonEvent) -> None:
        """
        SDL_CONTROLLERBUTTONUP
        Кнопка контроллера отпущена
        """
        for object in self.children:
            object.controllerbuttonup(common, cbutton)

    def controllerdeviceadded(self, common: CommonEvent, cdevice: ControllerDeviceEvent) -> None:
        """
        SDL_CONTROLLERDEVICEADDED
        Контроллер подключён
        """
        for object in self.children:
            object.controllerdeviceadded(common, cdevice)

    def controllerdeviceremoved(self, common: CommonEvent, cdevice: ControllerDeviceEvent) -> None:
        """
        SDL_CONTROLLERDEVICEREMOVED
        Контроллер отключён
        """
        for object in self.children:
            object.controllerdeviceremoved(common, cdevice)

    def controllerdeviceremapped(self, common: CommonEvent, cdevice: ControllerDeviceEvent) -> None:
        """
        SDL_CONTROLLERDEVICEREMAPPED
        Раскладка контроллера обновлена
        """
        for object in self.children:
            object.controllerdeviceremapped(common, cdevice)

    def controllertouchpaddown(self, common: CommonEvent, ctouchpad: ControllerTouchpadEvent) -> None:
        """
        SDL_CONTROLLERTOUCHPADDOWN
        Тачпад контроллера нажат
        """
        for object in self.children:
            object.controllertouchpaddown(common, ctouchpad)

    def controllertouchpadmotion(self, common: CommonEvent, ctouchpad: ControllerTouchpadEvent) -> None:
        """
        SDL_CONTROLLERTOUCHPADMOTION
        Палец движется по тачпаду контроллера 
        """
        for object in self.children:
            object.controllertouchpadmotion(common, ctouchpad)

    def controllertouchpadup(self, common: CommonEvent, ctouchpad: ControllerTouchpadEvent) -> None:
        """
        SDL_CONTROLLERTOUCHPADUP
        Палец отпущен с тачпада контроллера
        """
        for object in self.children:
            object.controllertouchpadup(common, ctouchpad)

    def controllersensorupdate(self, common: CommonEvent, csensor: ControllerSensorEvent) -> None:
        """
        SDL_CONTROLLERSENSORUPDATE
        Обновились данные сенсора контроллера
        """
        for object in self.children:
            object.controllersensorupdate(common, csensor)

    # Сенсорный ввод и жесты

    def fingerdown(self, common: CommonEvent, tfinger: TouchFingerEvent) -> None:
        """
        SDL_FINGERDOWN
        Палец коснулся экрана
        """
        for object in self.children:
            object.fingerdown(common, tfinger)

    def fingerup(self, common: CommonEvent, tfinger: TouchFingerEvent) -> None:
        """
        SDL_FINGERUP
        Палец поднят
        """
        for object in self.children:
            object.fingerup(common, tfinger)

    def fingermotion(self, common: CommonEvent, tfinger: TouchFingerEvent) -> None:
        """
        SDL_FINGERMOTION
        Палец движется
        """
        for object in self.children:
            object.fingermotion(common, tfinger)

    def multigesture(self, common: CommonEvent, mgesture: MultiGestureEvent) -> None:
        """
        SDL_MULTIGESTURE
        Мультитач-жест (щипок, вращение)
        """
        for object in self.children:
            object.multigesture(common, mgesture)

    def dollargesture(self, common: CommonEvent, dgesture: DollarGestureEvent) -> None:
        """
        SDL_DOLLARGESTURE
        Распознан долларовый жест (1-жест)
        """
        for object in self.children:
            object.dollargesture(common, dgesture)

    def dollarrecord(self, common: CommonEvent, dgesture: DollarGestureEvent) -> None:
        """
        SDL_DOLLARRECORD
        Записан долларовый жест
        """
        for object in self.children:
            object.dollarrecord(common, dgesture)

    # Аудиоустройства

    def audiodeviceadded(self, common: CommonEvent, adevice: AudioDeviceEvent) -> None:
        """
        SDL_AUDIODEVICEADDED
        Аудиоустройство подключено
        """
        for object in self.children:
            object.audiodeviceadded(common, adevice)

    def audiodeviceremoved(self, common: CommonEvent, adevice: AudioDeviceEvent) -> None:
        """
        SDL_AUDIODEVICEREMOVED
        Аудиоустройство отключено
        """
        for object in self.children:
            object.audiodeviceremoved(common, adevice)

    # Drag and Drop (перетаскивание файлов/текста)

    def dropbegin(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPBEGIN
        Начало перетаскивания
        """
        for object in self.children:
            object.dropbegin(common, drop)

    def dropfile(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPFILE
        Файл перетащен в окно
        """
        for object in self.children:
            object.dropfile(common, drop)

    def droptext(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPTEXT
        Текст перетащен в окно
        """
        for object in self.children:
            object.droptext(common, drop)

    def dropcomplete(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPCOMPLETE
        Перетаскивание завершено
        """
        for object in self.children:
            object.dropcomplete(common, drop)