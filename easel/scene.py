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
        

if TYPE_CHECKING:
    from .window import Window
else:
    Window = Any

class Scene(CoreObject):
    name: str
    page: Window
    objects: list[PfObject] = () # для совместимости 
    
    def __init__(self, page: Window):
        self.page = page
        self.name = type(self).__name__
        self.objects: list[PfObject] = []

    def append(self, object: PfObject) -> None:
        """
        Добавляет объект в конец списка.
        """
        self.objects.append(object)

    def draw(self, win):
        for object in self.objects:
            object.draw(win)

    def update(self, dt):
        for object in self.objects:
            object.update(dt)

    def event(self, event):
        for object in self.objects:
            object.event(event)

    # Системные события
    def quit(self, common: CommonEvent, quit: QuitEvent) -> None:
        """
        SDL_QUIT
        Пользователь запросил закрытие приложения (нажал на крестик окна, Alt+F4 или эквивалент в оконной системе).
        """
        for object in self.objects:
            object.quit(common, quit)

    def app_terminating(self, common: CommonEvent) -> None:
        """
        SDL_APP_TERMINATING
        Приложение завершается ОС (iOS/Android)
        """
        for object in self.objects:
            object.app_terminating(common)

    def app_lowmemory(self, common: CommonEvent) -> None:
        """
        SDL_APP_LOWMEMORY
        Приложению не хватает памяти
        """
        for object in self.objects:
            object.app_lowmemory(common)

    def app_willenterbackground(self, common: CommonEvent) -> None:
        """
        SDL_APP_WILLENTERBACKGROUND
        Приложение собирается уйти в фон
        """
        for object in self.objects:
            object.app_willenterbackground(common)

    def app_didenterbackground(self, common: CommonEvent) -> None:
        """
        SDL_APP_DIDENTERBACKGROUND
        Приложение ушло в фон
        """
        for object in self.objects:
            object.app_didenterbackground(common)

    def app_willenterforeground(self, common: CommonEvent) -> None:
        """
        SDL_APP_WILLENTERFOREGROUND
        Приложение собирается вернуться на передний план
        """
        for object in self.objects:
            object.app_willenterforeground(common)

    def app_didenterforeground(self, common: CommonEvent) -> None:
        """
        SDL_APP_DIDENTERFOREGROUND
        Приложение снова активно
        """
        for object in self.objects:
            object.app_didenterforeground(common)

    def localechanged(self, common: CommonEvent) -> None:
        """
        SDL_LOCALECHANGED
        Изменились локальные настройки пользователя
        """
        for object in self.objects:
            object.localechanged(common)

    def displayevent(self, common: CommonEvent, display: DisplayEvent) -> None:
        """
        SDL_DISPLAYEVENT
        Изменение состояния дисплея
        """
        for object in self.objects:
            object.displayevent(common, display)

    def windowevent(self, common: CommonEvent, window: WindowEvent) -> None:
        """
        SDL_WINDOWEVENT
        Изменение состояния окна (фокус, размер, перемещение и т.п.)
        """
        for object in self.objects:
            object.windowevent(common, window)

    def syswmevent(self, common: CommonEvent, syswm: SysWMEvent) -> None:
        """
        SDL_SYSWMEVENT
        Системное событие оконного менеджера
        """
        for object in self.objects:
            object.syswmevent(common, syswm)

    def clipboardupdate(self, common: CommonEvent) -> None:
        """
        SDL_CLIPBOARDUPDATE
        Изменилось содержимое буфера обмена
        """
        for object in self.objects:
            object.clipboardupdate(common)

    def render_targets_reset(self, common: CommonEvent) -> None:
        """
        SDL_RENDER_TARGETS_RESET
        Цели рендеринга сброшены (нужно обновить содержимое)
        """
        for object in self.objects:
            object.render_targets_reset(common)

    def render_device_reset(self, common: CommonEvent) -> None:
        """
        SDL_RENDER_DEVICE_RESET
        Устройство рендеринга сброшено (нужно пересоздать текстуры)
        """
        for object in self.objects:
            object.render_device_reset(common)

    def sensorupdate(self, common: CommonEvent, sensor: SensorEvent) -> None:
        """
        SDL_SENSORUPDATE
        Обновились данные сенсора
        """
        for object in self.objects:
            object.sensorupdate(common, sensor)

    # События клавиатуры
    def keydown(self, common: CommonEvent, key: KeyboardEvent) -> None:
        """
        SDL_KEYDOWN
        Клавиша нажата
        """
        for object in self.objects:
            object.keydown(common, key)
        
    def keyup(self, common: CommonEvent, key: KeyboardEvent) -> None:
        """
        SDL_KEYUP
        Клавиша отпущена
        """
        for object in self.objects:
            object.keyup(common, key)

    def textediting(self, common: CommonEvent, edit: TextEditingEvent) -> None:
        """
        SDL_TEXTEDITING
        Редактирование текста (IME, композиция)
        """
        for object in self.objects:
            object.textediting(common, edit)

    def textinput(self, common: CommonEvent, text: TextInputEvent) -> None:
        """
        SDL_TEXTINPUT
        Ввод текста (после завершения IME)
        """
        for object in self.objects:
            object.textinput(common, text)

    def keymapchanged(self, common: CommonEvent) -> None:
        """
        SDL_KEYMAPCHANGED
        Раскладка клавиатуры изменилась системой
        """
        for object in self.objects:
            object.keymapchanged(common)

    def textediting_ext(self, common: CommonEvent, editExt: TextEditingExtEvent) -> None:
        """
        SDL_TEXTEDITING_EXT
        Расширенное редактирование текста (IME)
        """
        for object in self.objects:
            object.textediting_ext(common, editExt)

    # События мыши

    def mousemotion(self, common: CommonEvent, motion: MouseMotionEvent) -> None:
        """
        SDL_MOUSEMOTION
        Перемещение мыши
        """
        for object in self.objects:
            object.mousemotion(common, motion)

    def mousebuttondown(self, common: CommonEvent, button: MouseButtonEvent) -> None:
        """
        SDL_MOUSEBUTTONDOWN
        Кнопка мыши нажата
        """
        for object in self.objects:
            object.mousebuttondown(common, button)
    def mousebuttonup(self, common: CommonEvent, button: MouseButtonEvent) -> None:
        """
        SDL_MOUSEBUTTONUP
        Кнопка мыши отпущена
        """
        for object in self.objects:
            object.mousebuttonup(common, button)
    def mousewheel(self, common: CommonEvent, wheel: MouseWheelEvent) -> None:
        """
        SDL_MOUSEWHEEL
        Прокрутка колеса мыши
        """
        for object in self.objects:
            object.mousewheel(common, wheel)

    # Джойстик (классический API)

    def joyaxismotion(self, common: CommonEvent, jaxis: JoyAxisEvent) -> None:
        """
        SDL_JOYAXISMOTION
        Движение оси джойстика
        """
        for object in self.objects:
            object.joyaxismotion(common, jaxis)

    def joyballmotion(self, common: CommonEvent, jball: JoyBallEvent) -> None:
        """
        SDL_JOYBALLMOTION
        Движение трекбола
        """
        for object in self.objects:
            object.joyballmotion(common, jball)

    def joyhatmotion(self, common: CommonEvent, jhat: JoyHatEvent) -> None:
        """
        SDL_JOYHATMOTION
        Изменение POV-переключателя (hat)
        """
        for object in self.objects:
            object.joyhatmotion(common, jhat)

    def joybuttondown(self, common: CommonEvent, jbutton: JoyButtonEvent) -> None:
        """
        SDL_JOYBUTTONDOWN
        Кнопка джойстика нажата
        """
        for object in self.objects:
            object.joybuttondown(common, jbutton)

    def joybuttonup(self, common: CommonEvent, jbutton: JoyButtonEvent) -> None:
        """
        SDL_JOYBUTTONUP
        Кнопка джойстика отпущена
        """
        for object in self.objects:
            object.joybuttonup(common, jbutton)

    def joydeviceadded(self, common: CommonEvent, jdevice: JoyDeviceEvent) -> None:
        """
        SDL_JOYDEVICEADDED
        Джойстик подключён
        """
        for object in self.objects:
            object.joydeviceadded(common, jdevice)

    def joydeviceremoved(self, common: CommonEvent, jdevice: JoyDeviceEvent) -> None:
        """
        SDL_JOYDEVICEREMOVED
        Джойстик отключён
        """
        for object in self.objects:
            object.joydeviceremoved(common, jdevice)

    def joybatteryupdated(self, common: CommonEvent, jbattery: JoyBatteryEvent) -> None:
        """
        SDL_JOYBATTERYUPDATED
        Изменился уровень заряда джойстика
        """
        for object in self.objects:
            object.joybatteryupdated(common, jbattery)

    # Контроллеры (Game Controller API, SDL2)

    def controlleraxismotion(self, common: CommonEvent, caxis: ControllerAxisEvent) -> None:
        """
        SDL_CONTROLLERAXISMOTION
        Движение оси контроллера
        """
        for object in self.objects:
            object.controlleraxismotion(common, caxis)

    def controllerbuttondown(self, common: CommonEvent, cbutton: ControllerButtonEvent) -> None:
        """
        SDL_CONTROLLERBUTTONDOWN
        Кнопка контроллера нажата
        """
        for object in self.objects:
            object.controllerbuttondown(common, cbutton)

    def controllerbuttonup(self, common: CommonEvent, cbutton: ControllerButtonEvent) -> None:
        """
        SDL_CONTROLLERBUTTONUP
        Кнопка контроллера отпущена
        """
        for object in self.objects:
            object.controllerbuttonup(common, cbutton)

    def controllerdeviceadded(self, common: CommonEvent, cdevice: ControllerDeviceEvent) -> None:
        """
        SDL_CONTROLLERDEVICEADDED
        Контроллер подключён
        """
        for object in self.objects:
            object.controllerdeviceadded(common, cdevice)

    def controllerdeviceremoved(self, common: CommonEvent, cdevice: ControllerDeviceEvent) -> None:
        """
        SDL_CONTROLLERDEVICEREMOVED
        Контроллер отключён
        """
        for object in self.objects:
            object.controllerdeviceremoved(common, cdevice)

    def controllerdeviceremapped(self, common: CommonEvent, cdevice: ControllerDeviceEvent) -> None:
        """
        SDL_CONTROLLERDEVICEREMAPPED
        Раскладка контроллера обновлена
        """
        for object in self.objects:
            object.controllerdeviceremapped(common, cdevice)

    def controllertouchpaddown(self, common: CommonEvent, ctouchpad: ControllerTouchpadEvent) -> None:
        """
        SDL_CONTROLLERTOUCHPADDOWN
        Тачпад контроллера нажат
        """
        for object in self.objects:
            object.controllertouchpaddown(common, ctouchpad)

    def controllertouchpadmotion(self, common: CommonEvent, ctouchpad: ControllerTouchpadEvent) -> None:
        """
        SDL_CONTROLLERTOUCHPADMOTION
        Палец движется по тачпаду контроллера 
        """
        for object in self.objects:
            object.controllertouchpadmotion(common, ctouchpad)

    def controllertouchpadup(self, common: CommonEvent, ctouchpad: ControllerTouchpadEvent) -> None:
        """
        SDL_CONTROLLERTOUCHPADUP
        Палец отпущен с тачпада контроллера
        """
        for object in self.objects:
            object.controllertouchpadup(common, ctouchpad)

    def controllersensorupdate(self, common: CommonEvent, csensor: ControllerSensorEvent) -> None:
        """
        SDL_CONTROLLERSENSORUPDATE
        Обновились данные сенсора контроллера
        """
        for object in self.objects:
            object.controllersensorupdate(common, csensor)

   # Сенсорный ввод и жесты

    def fingerdown(self, common: CommonEvent, tfinger: TouchFingerEvent) -> None:
        """
        SDL_FINGERDOWN
        Палец коснулся экрана
        """
        for object in self.objects:
            object.fingerdown(common, tfinger)

    def fingerup(self, common: CommonEvent, tfinger: TouchFingerEvent) -> None:
        """
        SDL_FINGERUP
        Палец поднят
        """
        for object in self.objects:
            object.fingerup(common, tfinger)

    def fingermotion(self, common: CommonEvent, tfinger: TouchFingerEvent) -> None:
        """
        SDL_FINGERMOTION
        Палец движется
        """
        for object in self.objects:
            object.fingermotion(common, tfinger)

    def multigesture(self, common: CommonEvent, mgesture: MultiGestureEvent) -> None:
        """
        SDL_MULTIGESTURE
        Мультитач-жест (щипок, вращение)
        """
        for object in self.objects:
            object.multigesture(common, mgesture)

    def dollargesture(self, common: CommonEvent, dgesture: DollarGestureEvent) -> None:
        """
        SDL_DOLLARGESTURE
        Распознан долларовый жест (1-жест)
        """
        for object in self.objects:
            object.dollargesture(common, dgesture)

    def dollarrecord(self, common: CommonEvent, dgesture: DollarGestureEvent) -> None:
        """
        SDL_DOLLARRECORD
        Записан долларовый жест
        """
        for object in self.objects:
            object.dollarrecord(common, dgesture)

    # Аудиоустройства

    def audiodeviceadded(self, common: CommonEvent, adevice: AudioDeviceEvent) -> None:
        """
        SDL_AUDIODEVICEADDED
        Аудиоустройство подключено
        """
        for object in self.objects:
            object.audiodeviceadded(common, adevice)

    def audiodeviceremoved(self, common: CommonEvent, adevice: AudioDeviceEvent) -> None:
        """
        SDL_AUDIODEVICEREMOVED
        Аудиоустройство отключено
        """
        for object in self.objects:
            object.audiodeviceremoved(common, adevice)

    # Drag and Drop (перетаскивание файлов/текста)

    def dropbegin(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPBEGIN
        Начало перетаскивания
        """
        for object in self.objects:
            object.dropbegin(common, drop)

    def dropfile(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPFILE
        Файл перетащен в окно
        """
        for object in self.objects:
            object.dropfile(common, drop)

    def droptext(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPTEXT
        Текст перетащен в окно
        """
        for object in self.objects:
            object.droptext(common, drop)

    def dropcomplete(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPCOMPLETE
        Перетаскивание завершено
        """
        for object in self.objects:
            object.dropcomplete(common, drop)

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