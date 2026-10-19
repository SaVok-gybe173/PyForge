import pygame as pg
import os
from copy import deepcopy
from .logger import ObjectMeta
from .markup import Size, Point, isListType

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

    def draw(self, win: pg.Surface):
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

    def event(self, event: pg.event.Event) -> None:
        '''
        Сработыет при вызове жвента

        Args:
            event (pg.event.Event): Основной класс эвента
        '''

    def size_update(self, old: tuple[int, int], new: tuple[int, int], ratio: tuple[int, int]):
        '''
        Обновление размер окна

        Метод как videoresize, но также передает старое число

        Args:
            old (tuple[int, int]): Старый размер
            new (tuple[int, int]): Новый размер
            ratio (tuple[int, int]): Коэфицент между новым и старым размером (new/old)
        '''
    def muve_window(self, old: tuple[int, int], new: tuple[int, int]) -> None:
        '''
        Перемещение окна

        Работает на pygame-ce

        Args:
            old (tuple[int, int]): Старая позиция
            new (tuple[int, int]): Новоя позиция
        '''

    # Системные события

    def close(self) -> None:
        """
        QUIT
        Когда вызывается: 
            Пользователь запросил закрытие приложения (нажал на крестик окна, Alt+F4 или эквивалент в оконной системе).

        Атрибуты: 
            Специфических полей нет — важен сам факт события. 
            При получении SDL_QUIT приложение обычно завершает главный цикл и освобождает ресурсы.
        """
        return True
    

    def localechanged(self) -> None:
        """
        LOCALECHANGED
        Когда вызывается: 
            Пользователь изменил локальные настройки (язык, региональные стандарты) в системе.

        Атрибуты: 
            Нет специфических полей. 
            Сигнализирует, что текстовые ресурсы или форматы (даты, числа) могут требовать обновления.
        """

    def displayevent(self, display: int, event: int) -> None:
        """
        SDL_DISPLAYEVENT
            Когда вызывается: 
                Изменилось состояние дисплея (например, монитор был подключён/отключён, изменено его разрешение или ориентация).

            Атрибуты:
                display — индекс дисплея, с которым произошло изменение.
                event — конкретное подсостояние (например, SDL_DISPLAYEVENT_CONNECTED, SDL_DISPLAYEVENT_ORIENTATION).
        """

    def windowevent(self, event: int, *args) -> None:
        """
        SDL_WINDOWEVENT
        Когда вызывается: 
            Любое изменение состояния окна: перемещение, изменение размера, сворачивание/разворачивание, получение/потеря фокуса, изменение видимости и т.п.

        Атрибуты:
            event — конкретное подсостояние (например, SDL_WINDOWEVENT_RESIZED, SDL_WINDOWEVENT_FOCUS_GAINED).
            data1, data2 — зависят от event. Например, для SDL_WINDOWEVENT_RESIZED в data1 и data2 лежат новые ширина и высота окна.
        """

    def syswmevent(self, msg: object) -> None:
        """
        SDL_SYSWMEVENT
        Когда вызывается: 
            Оконная система передаёт «сырое» системное сообщение (например, WM_* в Windows или XEvent в X11), которое SDL не обработала сама.

        Атрибуты: 
            msg — указатель на системно-зависимую структуру сообщения. 
            Нужен для низкоуровневой интеграции с оконной системой.
        """

    def clipboardupdate(self) -> None:
        """
        SDL_CLIPBOARDUPDATE
        Когда вызывается: 
            Содержимое системного буфера обмена изменилось.

        Атрибуты: 
            Нет. Позволяет приложению вовремя обновить своё представление буфера обмена.
        """

    def render_targets_reset(self) -> None:
        """
        SDL_RENDER_TARGETS_RESET, SDL_RENDER_DEVICE_RESET
        Когда вызывается: 
            Сброс целей рендеринга или устройства рендеринга (например, после потери контекста OpenGL/Direct3D или изменения параметров окна).

        Атрибуты: 
            Нет. Сигнализирует, что все текстуры и цели рендеринга нужно пересоздать.
        """

    def render_device_reset(self) -> None:
        """
        SDL_RENDER_TARGETS_RESET, SDL_RENDER_DEVICE_RESET
        Когда вызывается: 
            Сброс целей рендеринга или устройства рендеринга (например, после потери контекста OpenGL/Direct3D или изменения параметров окна).

        Атрибуты: 
            Нет. Сигнализирует, что все текстуры и цели рендеринга нужно пересоздать.
        """

    def sensorupdate(self) -> None:
        """
        SDL_SENSORUPDATE
        Когда вызывается: 
            С аппаратного сенсора (акселерометр, гироскоп) поступили новые данные.

        Атрибуты: 
            which (идентификатор сенсора), 
            data (массив из 6 float с показаниями). Используется для управления на основе наклона/вращения устройства.
        """

    # События клавиатуры

    def keydown(self, sym: int, mod: int, unicode: str, scancode: int) -> None:
        """
        SDL_KEYDOWN / SDL_KEYUP
        Когда вызывается: 
            Физическая клавиша была нажата или отпущена.

        Зачем нужны атрибуты keysym:

            scancode — аппаратный код клавиши, зависящий от физического расположения. 
            Используйте его для игрового управления (например, «клавиша W» на QWERTY и «клавиша Z» на AZERTY имеют разный sym, но одинаковый scancode).

            sym — виртуальный код клавиши (например, SDLK_w, SDLK_RETURN). 
            Удобен для привязки действий к конкретным клавишам с учётом раскладки.

            mod — текущие модификаторы (KMOD_SHIFT, KMOD_CTRL, KMOD_ALT). Позволяет различать, например, Ctrl+S и просто S.
        
        Дополнительно: repeat (для KEYDOWN) — 1, если событие сгенерировано автоповтором при удержании клавиши.
        """

    def keyup(self, key: int, mod: int, scancode: int) -> None:
        """
        SDL_KEYDOWN / SDL_KEYUP
        Когда вызывается: 
            Физическая клавиша была нажата или отпущена.

        Зачем нужны атрибуты keysym:

            scancode — аппаратный код клавиши, зависящий от физического расположения. 
            Используйте его для игрового управления (например, «клавиша W» на QWERTY и «клавиша Z» на AZERTY имеют разный sym, но одинаковый scancode).

            sym — виртуальный код клавиши (например, SDLK_w, SDLK_RETURN). 
            Удобен для привязки действий к конкретным клавишам с учётом раскладки.

            mod — текущие модификаторы (KMOD_SHIFT, KMOD_CTRL, KMOD_ALT). Позволяет различать, например, Ctrl+S и просто S.
        
        Дополнительно: repeat (для KEYDOWN) — 1, если событие сгенерировано автоповтором при удержании клавиши.
        """

    def textediting(self, text: str, start: int, length: int) -> None:
        """
        SDL_TEXTEDITING / SDL_TEXTEDITING_EXT
        Когда вызывается: 
            Пользователь вводит текст через IME (Input Method Editor — например, для китайского, японского или корейского языков). 
            Это промежуточный этап, когда символы ещё не зафиксированы.

        Атрибуты:
            text — текущая строка композиции (может содержать ещё не подтверждённые символы).
            start, length — позиция и длина выделенной части внутри text. Нужны для отрисовки подсказки IME.
        """

    def textediting_ext(self, text: str, start: int, length: int) -> None:
        """
        SDL_TEXTEDITING / SDL_TEXTEDITING_EXT
        Когда вызывается: 
            Пользователь вводит текст через IME (Input Method Editor — например, для китайского, японского или корейского языков). 
            Это промежуточный этап, когда символы ещё не зафиксированы.

        Атрибуты:
            text — текущая строка композиции (может содержать ещё не подтверждённые символы).
            start, length — позиция и длина выделенной части внутри text. Нужны для отрисовки подсказки IME.
        """


    def textinput(self, text: str) -> None:
        """
        SDL_TEXTINPUT
        Когда вызывается: 
            Пользователь завершил ввод символа (подтвердил выбор в IME или нажал обычную клавишу).

        Атрибуты: 
            text — готовая строка для вставки в текстовое поле. В отличие от KEYDOWN, здесь приходит именно текст (с учётом раскладки и IME), а не код клавиши.
        """

    def keymapchanged(self) -> None:
        """
        SDL_KEYMAPCHANGED
        Когда вызывается: 
            Система сменила раскладку клавиатуры или язык ввода.

        Атрибуты: 
            Нет. Позволяет приложению обновить отображаемые подсказки клавиш.
        """

    # События мыши

    def mousemotion(self, pos: tuple[int, int], rel: tuple[int, int], state: bool) -> None:
        """
        SDL_MOUSEMOTION
        Когда вызывается: 
            Пользователь переместил мышь внутри окна приложения или была вызвана SDL_WarpMouse() (программное перемещение курсора).

        Зачем нужны атрибуты:

            x, y — абсолютные координаты курсора относительно левого верхнего угла окна. 
            Удобны для позиционирования UI-элементов, курсоров, прицеливания.

            xrel, yrel — относительное смещение с момента предыдущего события. 
            Критично для управления камерой от первого лица: даже если курсор упрётся в край экрана (при захвате ввода), xrel/yrel продолжат приходить, позволяя бесконечно вращать камеру.

            state — текущее состояние кнопок мыши в момент движения (битовая маска). 
            Позволяет реализовать перетаскивание (drag) без отслеживания отдельных BUTTONDOWN/UP — достаточно проверять state в MOTION.
        """

    def mousebuttondown(self, pos: tuple[int, int], button: int, clicks: int) -> None:
        """
        SDL_MOUSEBUTTONDOWN / SDL_MOUSEBUTTONUP
        Когда вызывается: 
            Кнопка мыши была нажата или отпущена.

        Зачем нужны атрибуты:
            x, y — координаты курсора в момент нажатия/отпускания. 
            Нужны для определения, куда именно пришёлся клик.

            button — номер кнопки (SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_BUTTON_MIDDLE). 
            Позволяет различать действия.

            clicks — количество кликов (1 для одиночного, 2 для двойного). 
            Удобно для обработки двойного клика без ручного замера времени.
            
        """

    def mousebuttonup(self, pos: tuple[int, int], button: int, clicks: int) -> None:
        """
        SDL_MOUSEBUTTONDOWN / SDL_MOUSEBUTTONUP
        Когда вызывается: 
            Кнопка мыши была нажата или отпущена.

        Зачем нужны атрибуты:
            x, y — координаты курсора в момент нажатия/отпускания. 
            Нужны для определения, куда именно пришёлся клик.

            button — номер кнопки (SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_BUTTON_MIDDLE). 
            Позволяет различать действия.

            clicks — количество кликов (1 для одиночного, 2 для двойного). 
            Удобно для обработки двойного клика без ручного замера времени.
            
        """

    def mousewheel(self, x: int, y: int, flipped: bool, precise_x: float, precise_y: float) -> None:
        """
        SDL_MOUSEWHEEL
        Когда вызывается: 
            Пользователь прокрутил колесо мыши или сделал жест прокрутки на тачпаде.

        Зачем нужны атрибуты:

            x, y — направление и величина прокрутки (целые числа). 
            y обычно отвечает за вертикальную прокрутку (вверх/вниз), x — за горизонтальную.

            direction — SDL_MOUSEWHEEL_NORMAL (прямое направление) или SDL_MOUSEWHEEL_FLIPPED (обратное, в зависимости от настроек ОС). 
            Позволяет корректно интерпретировать направление.

            preciseX, preciseY — более точные значения с плавающей точкой (для тачпадов с плавной прокруткой).

            mouseX, mouseY — координаты курсора в момент прокрутки (в некоторых версиях SDL2).
        """
        

class PfObject(CoreObject):
    rect: pg.Rect | None = None

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
    img: pg.Surface # изображение

    def __init__(self, left_top: Point | tuple[int, int], img: pg.Surface | tuple[bytes, Size | tuple[int, int]] | str, *args, **kvargs):
        """
        Прокаченый PfObject, но поддерживает хранение изображения.
        """
        if isinstance(img, str):
            img = pg.image.load(img).convert_alpha()
            
        elif isinstance(img, bytes):
            img = pg.image.frombytes(img[0], img[1] if isinstance(img[1], tuple | list) else img[1].pixel)
        elif not isinstance(img, pg.Surface):
            raise ValueError(f"Ожидаеться pygame.Surface, пришло {type(img)}")
        
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


    def convert_alpha(self) -> pg.Surface:
        """
        Конвертирует основной класс и возвращает ссылку на pygame.Surface
        """
        self.img = self.img.convert_alpha()
        return self.img

    def convert(self) -> pg.Surface:
        """
        Конвертирует основной класс и возвращает ссылку на pygame.Surface
        """
        self.img = self.img.convert()
        return self.img