"""
Модуль со структурой сценны
"""
from typing import Any, TYPE_CHECKING, Self
import pygame as pg

if TYPE_CHECKING:
    from .window import Window
else:
    type Window = Any

class Scene:
    name: str
    page: Window
    
    def __init__(self, win = None):
        self._win = win

    def draw(self, screen: pg.Surface):
        '''
        сработает при каждом цикле
        Аргументы:
            screen: pg.display.set_mode
        '''
    def update(self):
        '''
        сработает при обновление
        '''

    def event(self, event: pg.event.Event) -> None:
        '''
        Сработыет 

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

    def close(self) -> bool | None:
        """
        QUIT

        Срабатывает при эвенте закрытие окна
        
        Return:
            Завершить ли работы или нет
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

    def keyup(key: int, mod, scancode) -> None:
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

# методы эвентов по их типу
EVENTS_METOD = {
    pg.event.event_name(pg.ACTIVEEVENT): (lambda obj, event: Scene.activeevent(obj, event.gain, event.state)),
    pg.event.event_name(pg.VIDEORESIZE):  (lambda obj, event: Scene.videoresize(obj, event.size, event.w, event.h)), 
    pg.event.event_name(pg.VIDEOEXPOSE): (lambda obj, _: Scene.videoexpose(obj)), 
    pg.event.event_name(pg.RENDER_TARGETS_RESET):  (lambda obj, _: Scene.render_targets_reset(obj)),

    pg.event.event_name(pg.KEYDOWN): (lambda obj, event: Scene.keydown(obj, event.key, event.mod, event.unicode, event.scancode)), 
    pg.event.event_name(pg.KEYUP): (lambda obj, event: Scene.keyup(obj, event.key, event.mod, event.scancode)), 
    pg.event.event_name(pg.TEXTEDITING): (lambda obj, event: Scene.textediting(obj, event.text, event.start, event.length)), 
    pg.event.event_name(pg.TEXTINPUT): (lambda obj, event: Scene.textinput(obj, event.text)),

    pg.event.event_name(pg.MOUSEMOTION): (lambda obj, event: Scene.mousemotion(obj, event.pos, event.rel, event.buttons, event.touch)),
    pg.event.event_name(pg.MOUSEBUTTONDOWN): (lambda obj, event: Scene.mousebuttondown(obj, event.pos, event.button, event.touch)),
    pg.event.event_name(pg.MOUSEBUTTONUP): (lambda obj, event: Scene.mousebuttonup(obj, event.pos, event.button, event.touch)),
    pg.event.event_name(pg.MOUSEWHEEL): (lambda obj, event: Scene.mousewheel(obj, event.x, event.y, event.flipped, event.which, event.precise_x, event.precise_y)),

}