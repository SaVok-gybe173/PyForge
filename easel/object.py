import pygame as pg
import os
from copy import deepcopy
from .surface import Surface
from ..base.logger import ObjectMeta
from ..math.markup import Size, Point, isListType
from .event import (Event,
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
from sdl2.rect import SDL_Rect as Rect

class CoreObject(metaclass=ObjectMeta):
    __abstract__ = True
    """
    initial class for all objects
    начальный класс для всех обьектов 
    """
    
    def copy(self):
        """
        Копирование полностью обьекта
        """
        return deepcopy(self)
    
    def __bool__(self) -> bool:
        return False

    def draw(self, win: Surface):
        '''

        Отрисовка обьектов.
        Cработает при каждом цикле
        
        Args:
            win (pg.Surface): Холст главного окна
        '''
    def update(self, dt: float):
        '''
        сработает при обновление

        Args:
            dt (float): Время в секундах
        '''

    def close(self, common: CommonEvent, quit: QuitEvent):
        """
        Срабатывает для всех сцен
        """

    def event(self, event: Event) -> None:
        '''
        Срабатывает при вызове события

        Args:
            event (Event): Основной класс события
        '''

    def size_update(self, old: tuple[int, int], new: tuple[int, int], scale: tuple[int, int]):
        '''
        Обновление размер окна

        Метод как videoresize, но также передает старое число

        Args:
            old (tuple[int, int]): Старый размер
            new (tuple[int, int]): Новый размер
            ratio (tuple[int, int]): Коэффициент между новым и старым размером (new/old)
        '''
    def muve_window(self, old: tuple[int, int], new: tuple[int, int], scale: tuple[int, int]) -> None:
        '''
        Перемещение окна

        Args:
            old (tuple[int, int]): Старая позиция
            new (tuple[int, int]): Новая позиция
        '''

    # Системные события

    def quit(self, common: CommonEvent, quit: QuitEvent) -> bool:
        """
        SDL_QUIT
        Пользователь запросил закрытие приложения (нажал на крестик окна, Alt+F4 или эквивалент в оконной системе).
        """
        return True
    

    def app_terminating(self, common: CommonEvent) -> None:
        """
        SDL_APP_TERMINATING
        Приложение завершается ОС (iOS/Android)
        """

    def app_lowmemory(self, common: CommonEvent) -> None:
        """
        SDL_APP_LOWMEMORY
        Приложению не хватает памяти
        """

    def app_willenterbackground(self, common: CommonEvent) -> None:
        """
        SDL_APP_WILLENTERBACKGROUND
        Приложение собирается уйти в фон
        """

    def app_didenterbackground(self, common: CommonEvent) -> None:
        """
        SDL_APP_DIDENTERBACKGROUND
        Приложение ушло в фон
        """

    def app_willenterforeground(self, common: CommonEvent) -> None:
        """
        SDL_APP_WILLENTERFOREGROUND
        Приложение собирается вернуться на передний план
        """

    def app_didenterforeground(self, common: CommonEvent) -> None:
        """
        SDL_APP_DIDENTERFOREGROUND
        Приложение снова активно
        """

    def localechanged(self, common: CommonEvent) -> None:
        """
        SDL_LOCALECHANGED
        Изменились локальные настройки пользователя
        """

    def displayevent(self, common: CommonEvent, display: DisplayEvent) -> None:
        """
        SDL_DISPLAYEVENT
        Изменение состояния дисплея
        """

    def windowevent(self, common: CommonEvent, window: WindowEvent) -> None:
        """
        SDL_WINDOWEVENT
        Изменение состояния окна (фокус, размер, перемещение и т.п.)
        """

    def syswmevent(self, common: CommonEvent, syswm: SysWMEvent) -> None:
        """
        SDL_SYSWMEVENT
        Системное событие оконного менеджера
        """

    def clipboardupdate(self, common: CommonEvent) -> None:
        """
        SDL_CLIPBOARDUPDATE
        Изменилось содержимое буфера обмена
        """

    def render_targets_reset(self, common: CommonEvent) -> None:
        """
        SDL_RENDER_TARGETS_RESET
        Цели рендеринга сброшены (нужно обновить содержимое)
        """

    def render_device_reset(self, common: CommonEvent) -> None:
        """
        SDL_RENDER_DEVICE_RESET
        Устройство рендеринга сброшено (нужно пересоздать текстуры)
        """

    def sensorupdate(self, common: CommonEvent, sensor: SensorEvent) -> None:
        """
        SDL_SENSORUPDATE
        Обновились данные сенсора
        """

    # События клавиатуры

    def keydown(self, common: CommonEvent, key: KeyboardEvent) -> None:
        """
        SDL_KEYDOWN
        Клавиша нажата
        """

    def keyup(self, common: CommonEvent, key: KeyboardEvent) -> None:
        """
        SDL_KEYUP
        Клавиша отпущена
        """

    def textediting(self, common: CommonEvent, edit: TextEditingEvent) -> None:
        """
        SDL_TEXTEDITING
        Редактирование текста (IME, композиция)
        """

    def textinput(self, common: CommonEvent, text: TextInputEvent) -> None:
        """
        SDL_TEXTINPUT
        Ввод текста (после завершения IME)
        """

    def keymapchanged(self, common: CommonEvent) -> None:
        """
        SDL_KEYMAPCHANGED
        Раскладка клавиатуры изменилась системой
        """

    def textediting_ext(self, common: CommonEvent, editExt: TextEditingExtEvent) -> None:
        """
        SDL_TEXTEDITING_EXT
        Расширенное редактирование текста (IME)
        """

    # События мыши

    def mousemotion(self, common: CommonEvent, motion: MouseMotionEvent) -> None:
        """
        SDL_MOUSEMOTION
        Перемещение мыши
        """

    def mousebuttondown(self, common: CommonEvent, button: MouseButtonEvent) -> None:
        """
        SDL_MOUSEBUTTONDOWN
        Кнопка мыши нажата
        """

    def mousebuttonup(self, common: CommonEvent, button: MouseButtonEvent) -> None:
        """
        SDL_MOUSEBUTTONUP
        Кнопка мыши отпущена
        """

    def mousewheel(self, common: CommonEvent, wheel: MouseWheelEvent) -> None:
        """
        SDL_MOUSEWHEEL
        Прокрутка колеса мыши
        """

    # Джойстик (классический API)
    def joyaxismotion(self, common: CommonEvent, jaxis: JoyAxisEvent) -> None:
        """
        SDL_JOYAXISMOTION
        Движение оси джойстика
        """

    def joyballmotion(self, common: CommonEvent, jball: JoyBallEvent) -> None:
        """
        SDL_JOYBALLMOTION
        Движение трекбола
        """

    def joyhatmotion(self, common: CommonEvent, jhat: JoyHatEvent) -> None:
        """
        SDL_JOYHATMOTION
        Изменение POV-переключателя (hat)
        """

    def joybuttondown(self, common: CommonEvent, jbutton: JoyButtonEvent) -> None:
        """
        SDL_JOYBUTTONDOWN
        Кнопка джойстика нажата
        """

    def joybuttonup(self, common: CommonEvent, jbutton: JoyButtonEvent) -> None:
        """
        SDL_JOYBUTTONUP
        Кнопка джойстика отпущена
        """

    def joydeviceadded(self, common: CommonEvent, jdevice: JoyDeviceEvent) -> None:
        """
        SDL_JOYDEVICEADDED
        Джойстик подключён
        """

    def joydeviceremoved(self, common: CommonEvent, jdevice: JoyDeviceEvent) -> None:
        """
        SDL_JOYDEVICEREMOVED
        Джойстик отключён
        """
    def joybatteryupdated(self, common: CommonEvent, jbattery: JoyBatteryEvent) -> None:
        """
        SDL_JOYBATTERYUPDATED
        Изменился уровень заряда джойстика
        """

    # Контроллеры (Game Controller API, SDL2)

    def controlleraxismotion(self, common: CommonEvent, caxis: ControllerAxisEvent) -> None:
        """
        SDL_CONTROLLERAXISMOTION
        Движение оси контроллера
        """

    def controllerbuttondown(self, common: CommonEvent, cbutton: ControllerButtonEvent) -> None:
        """
        SDL_CONTROLLERBUTTONDOWN
        Кнопка контроллера нажата
        """

    def controllerbuttonup(self, common: CommonEvent, cbutton: ControllerButtonEvent) -> None:
        """
        SDL_CONTROLLERBUTTONUP
        Кнопка контроллера отпущена
        """

    def controllerdeviceadded(self, common: CommonEvent, cdevice: ControllerDeviceEvent) -> None:
        """
        SDL_CONTROLLERDEVICEADDED
        Контроллер подключён
        """

    def controllerdeviceremoved(self, common: CommonEvent, cdevice: ControllerDeviceEvent) -> None:
        """
        SDL_CONTROLLERDEVICEREMOVED
        Контроллер отключён
        """

    def controllerdeviceremapped(self, common: CommonEvent, cdevice: ControllerDeviceEvent) -> None:
        """
        SDL_CONTROLLERDEVICEREMAPPED
        Раскладка контроллера обновлена
        """

    def controllertouchpaddown(self, common: CommonEvent, ctouchpad: ControllerTouchpadEvent) -> None:
        """
        SDL_CONTROLLERTOUCHPADDOWN
        Тачпад контроллера нажат
        """

    def controllertouchpadmotion(self, common: CommonEvent, ctouchpad: ControllerTouchpadEvent) -> None:
        """
        SDL_CONTROLLERTOUCHPADMOTION
        Палец движется по тачпаду контроллера
        """

    def controllertouchpadup(self, common: CommonEvent, ctouchpad: ControllerTouchpadEvent) -> None:
        """
        SDL_CONTROLLERTOUCHPADUP
        Палец отпущен с тачпада контроллера
        """

    def controllersensorupdate(self, common: CommonEvent, csensor: ControllerSensorEvent) -> None:
        """
        SDL_CONTROLLERSENSORUPDATE
        Обновились данные сенсора контроллера
        """

    # Сенсорный ввод и жесты

    def fingerdown(self, common: CommonEvent, tfinger: TouchFingerEvent) -> None:
        """
        SDL_FINGERDOWN
        Палец коснулся экрана
        """

    def fingerup(self, common: CommonEvent, tfinger: TouchFingerEvent) -> None:
        """
        SDL_FINGERUP
        Палец поднят
        """

    def fingermotion(self, common: CommonEvent, tfinger: TouchFingerEvent) -> None:
        """
        SDL_FINGERMOTION
        Палец движется
        """

    def multigesture(self, common: CommonEvent, mgesture: MultiGestureEvent) -> None:
        """
        SDL_MULTIGESTURE
        Мультитач-жест (щипок, вращение)
        """

    def dollargesture(self, common: CommonEvent, dgesture: DollarGestureEvent) -> None:
        """
        SDL_DOLLARGESTURE
        Распознан долларовый жест (1-жест)
        """

    def dollarrecord(self, common: CommonEvent, dgesture: DollarGestureEvent) -> None:
        """
        SDL_DOLLARRECORD
        Записан долларовый жест
        """

    # Аудиоустройства

    def audiodeviceadded(self, common: CommonEvent, adevice: AudioDeviceEvent) -> None:
        """
        SDL_AUDIODEVICEADDED
        Аудиоустройство подключено
        """

    def audiodeviceremoved(self, common: CommonEvent, adevice: AudioDeviceEvent) -> None:
        """
        SDL_AUDIODEVICEREMOVED
        Аудиоустройство отключено
        """

    # Drag and Drop (перетаскивание файлов/текста)

    def dropbegin(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPBEGIN
        Начало перетаскивания
        """

    def dropfile(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPFILE
        Файл перетащен в окно
        """

    def droptext(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPTEXT
        Текст перетащен в окно
        """

    def dropcomplete(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPCOMPLETE
        Перетаскивание завершено
        """

class PfObject(CoreObject):
    rect: Rect | None = None

    def __init__(self, left_top: Point | tuple[int, int], width_height: Size | tuple[int, int], *args: CoreObject, **kvargs):
        """
        Класс создан для основы остальных классов.

        Принимает размеры и кординаты.
        """
        self.rect = pg.Rect()
        self.left_top = left_top
        self.width_height = width_height
        

    # сеттеры и геттеры
    # Point
    @property
    def left(self) -> int:
        return self._left_top.pixel[0]

    @property
    def top(self) -> int:
        return self._left_top.pixel[1]
    
    @left.setter
    def left(self, num: int) -> None:
        self._left_top.pixel = (num, self._left_top.pixel[1])
        if not self.rect is None:
            self.rect.left = num

    @top.setter
    def top(self, num: int) -> None:
        self._left_top.pixel = (self._left_top.pixel[0], num)
        if not self.rect is None:
            self.rect.top = num

    @property
    def left_top(self) -> Point:
        return self._left_top

    @left_top.setter
    def left_top(self, left_top: Point | tuple[int, int]) -> None:
        if isinstance(left_top, Point):
            self._left_top = left_top
        elif isinstance(left_top, tuple) and isListType(left_top):
            self._left_top = Point(left_top[0], left_top[1])
        else:
            raise ValueError(f"Не верный аргумент {self._left_top}")

        if not self.rect is None:
            self.rect.left, self.top = self._left_top.pixel
        
    # Size
    @property
    def width(self) -> int:
        return self._width_height.pixel[0]

    @property
    def height(self) -> int:
        return self._width_height.pixel[1]

    @width.setter
    def width(self, num: int) -> None:
        self._width_height.pixel = (num, self._width_height.pixel[1])
        if not self.rect is None:
            self.rect.width = num

    @height.setter
    def height(self, num: int) -> None:
        self._width_height.pixel = (self._width_height.pixel[0], num)
        if not self.rect is None:
            self.rect.height = num

    @property
    def width_height(self) -> Size:
        return self._width_height

    @width_height.setter
    def width_height(self, width_height: Size | tuple[int, int]) -> None:
        if isinstance(width_height, Point):
            self._width_height = width_height
        elif isinstance(width_height, tuple) and isListType(width_height):
            self._width_height = Point(width_height[0], width_height[1])
        else:
            raise ValueError(f"Не верный аргумент {self._width_height}")

        if not self.rect is None:
            self.rect.width, self.rect.height = self._width_height.pixel


class PfObjectIMG(PfObject):
    img: Surface # изображение

    def __init__(self, left_top: Point | tuple[int, int], img: Surface | tuple[bytes, Size | tuple[int, int]] | str, *args, **kvargs):
        """
        Прокаченый PfObject, но поддерживает хранение изображения.
        """
        if isinstance(img, str):
            img = pg.image.load(img).convert_alpha()
            
        elif isinstance(img, bytes):
            img = pg.image.frombytes(img[0], img[1] if isinstance(img[1], tuple | list) else img[1].pixel)
        elif not isinstance(img, Surface):
            raise ValueError(f"Ожидаеться Surface, пришло {type(img)}")
        
        self.img = img
        super().__init__(left_top, img.get_size(), *args, **kvargs)

    def to_bytes(self) -> bytes:
        return self.width.to_bytes(4) + self.height.to_bytes(4) + pg.image.tobytes(self.img)
    
    @staticmethod
    def from_bytes(byte: bytes, point: Point | tuple[int, int] = (0, 0)) -> "PfObjectIMG":
        return PfObjectIMG(point, (
                                    byte[0x08:],
                                   (int.from_bytes(byte[0x00:0x04]), int.from_bytes(byte[0x04:0x08]))
                                   ))


    def convert_alpha(self) -> Surface:
        """
        Конвертирует основной класс и возвращает ссылку на Surface
        """
        self.img = self.img.convert_alpha()
        return self.img

    def convert(self) -> Surface:
        """
        Конвертирует основной класс и возвращает ссылку на Surface
        """
        self.img = self.img.convert()
        return self.img