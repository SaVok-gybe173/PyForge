import pygame as pg
from copy import deepcopy
from .markup import Size, Point, isListType

class CoreObject:
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

        Срабатывает при эвенте закрытие окна
        """
        return True

    def activeevent(self, gain: bool, state: bool) -> None:  # ACTIVEEVENT
        """
        ACTIVEEVENT

        Окно получило или потеряло фокус.

        Args: 
            gain (bool): 1 — получен, 0 — потерян
            state (int): флаги состояния
        """

    def videoresize(self, size: tuple[int, int], w: int, h: int) -> None:
        """
        VIDEORESIZE

        Изменение размера окна. 
        
        Args:
            size (tuple[int, int]): Новый размер (w, h) 
            w (int): Новая ширина
            h (int): Новая высота

        """

    def videoexpose(self) -> None:
        """
        VIDEOEXPOSE

        Окно было частично или полностью перекрыто и снова показано
        """

    def render_targets_reset(self) -> None:
        """
        RENDER_TARGETS_RESET

        Добавлено в pygame 2.x
        """

    # События клавиатуры

    def keydown(self, key: int, mod: int, unicode: str, scancode: int) -> None:
        """
        KEYDOWN
        
        Клавиша нажата

        Args:
            key (int): код клавиши (например K_a, K_SPACE).
            mod (int): битовая маска модификаторов (KMOD_SHIFT, KMOD_CTRL, KMOD_ALT, KMOD_CAPS и т.д.).
            unicode (str): символ, соответствующий нажатой клавише (учитывает модификаторы и раскладку).
            scancode (int): аппаратный скан-код клавиши (не зависит от раскладки).
        
        """

    def keyup(self, key: int, mod: int, scancode: int) -> None:
        """
        KEYUP

        Клавиша отпущена

        Args:
            key (int): код клавиши (например K_a, K_SPACE).
            mod (int): битовая маска модификаторов (KMOD_SHIFT, KMOD_CTRL, KMOD_ALT, KMOD_CAPS и т.д.).
            scancode (int): аппаратный скан-код клавиши (не зависит от раскладки).
        """

    def textediting(self, text: str, start: int, length: int) -> None:
        """
        TEXTEDITING

        Редактирование текста (IME)

        Args:
            text (str): редактируемый текст (может быть пустым).
            start (int): начальная позиция выделения в тексте.
            length (int): длина выделения.
        """

    def textinput(self, text: str) -> None:
        """
        TEXTINPUT

        Ввод текста (после завершения IME)

        Args:
            text (str): введённый текст (обычно один символ, но может быть несколько при автодополнении).
        """

    # События мыши

    def mousemotion(self, pos: tuple[int, int], rel: tuple[int, int], buttons: tuple[bool, bool, bool], touch: bool) -> None:
        """
        MOUSEMOTION

        Перемещение мыши

        Args:
            pos (tuple[int, int]): текущие координаты курсора (x, y).
            rel (tuple[int, int]): относительное перемещение с прошлого события (dx, dy).
            buttons (tuple[bool, bool, bool]): состояние трёх кнопок (левая, средняя, правая) в виде кортежа (True/False, ...).
            touch (bool): было ли событие вызвано касанием сенсорного экрана.
        """

    def mousebuttondown(self, pos: tuple[int, int], button: int, touch: bool) -> None:
        """
        MOUSEBUTTONDOWN

        Кнопка мыши нажата

        Args:
            pos (tuple[int, int]): координаты курсора в момент нажатия/отпускания.
            button (int) номер кнопки: 1 – левая, 2 – средняя, 3 – правая, 4 – прокрутка вверх, 5 – прокрутка вниз (для старых версий).
            touch (bool) было ли касание на тачскрине.
        """

    def mousebuttonup(self, pos: tuple[int, int], button: int, touch: bool) -> None:
        """
        MOUSEBUTTONUP

        Кнопка мыши отпущена

        Args:
            pos (tuple[int, int]): координаты курсора в момент нажатия/отпускания.
            button (int) номер кнопки: 1 – левая, 2 – средняя, 3 – правая, 4 – прокрутка вверх, 5 – прокрутка вниз (для старых версий).
            touch (bool) было ли касание на тачскрине.
        """

    def mousewheel(self, x: int, y: int, flipped: bool, which: int, precise_x: float, precise_y: float) -> None:
        """
        MOUSEWHEEL

        Прокрутка колеса мыши

        Args:
            x (int): горизонтальная прокрутка (положительное значение – вправо).
            y (int): вертикальная прокрутка (положительное – вверх).
            flipped (bool): True, если значения осей были «перевёрнуты» (зависит от настроек ОС).
            which (int): идентификатор устройства (обычно 0).
            precise_x (float) точное значение горизонтальной прокрутки (дробное).
            precise_y (float) точное значение вертикальной прокрутки.
        """

class PfObject(CoreObject):
    def __init__(self, left_top: Point | tuple[int, int], width_height: Size | tuple[int, int], *args: CoreObject, **kvargs):
        if isinstance(left_top, Point):
            self._left_top = left_top
        elif isinstance(left_top, tuple) and isListType(left_top):
            self._left_top = Point(left_top[0], left_top[1])
        else:
            raise ValueError(f"Не верный аргумент {self._left_top}")

        if isinstance(width_height, Point):
            self._width_height = width_height
        elif isinstance(width_height, tuple) and isListType(width_height):
            self._width_height = Point(width_height[0], width_height[1])
        else:
            raise ValueError(f"Не верный аргумент {self._width_height}")

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
        

    @top.setter
    def top(self, num: int) -> None:
        self._left_top.pixel = (self._left_top.pixel[0], num)

    # Size
    @property
    def width(self) -> int:
        self._width_height[0]

    @property
    def height(self) -> int:
        return self._width_height[1]

    @width.setter
    def width(self, num: int) -> None:
        self._width_height.pixel = (num, self._width_height[1])

    @height.setter
    def height(self, num: int) -> None:
        self._width_height.pixel = (self._width_height[0], num)