"""
Виртуальный список с рендером только видимого диапазона
Полностью избавляемся от items_holst/holst/image_streak - вместо этого
храним префиксные суммы размеров и индексы [visible_start, visible_end]

Математика в _list_math (Cython, с Python-fallback)
"""

# это базовый оптимизированный класс, 
# который принесет удобную структуру для будущих классов ListOfItems.
#
# Новая оптимизация дает скорость O(log n), а раньше было O(n), довольно большой прирост. 
#
# Было items_holst на весь контент (сотни МБ), стало array('q') с префиксами (~8 байт x n). 
#
# Больше нету: holst, image_streak, fons.
#
# раньше была путоница с значениями: koficent, offset, __h, max_k, сейчас тало: scroll_offset, _total_length, _max_scroll, _thumb_size, _thumb_travel
#
# Раньше index() ломался от разных высот, теперь работает коррекно.
#
# Раньше ползунок мог выйти за пределы, теперь thumb_travel = view − thumb_size позволяет избежать этого.
#
# ListItems больше не учасвствует, теперь пришел PfObjectIMG, ListOfItems будет поддерживать все класс наследуемые от PfObjectIMG.
#
# - это было крупное обновление и главные изменения для работы с классом списка. 
# Так же новый класс сохранил старый API для корректной работы со старыми модулями.

from array import array

from ....easel.object import PfObject, PfObjectIMG
from ....easel.scene import EVENTS_METHOD
from ....easel.surface import Surface
from ....easel.window import Window
from ....pfmath.markup import Size, Point
from ....pfmath.rect import Rect

from ....easel.event import (Event,
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

from ._list_math import (
    build_prefix, total_length, find_visible_range, find_index_at,
    scroll_metrics, thumb_from_scroll, clamp,
)

class CoreListOfItemsBase(PfObject):
    """
    База. Реализует всё, что не зависит от направления.
    Наследники переопределяют только 6 методов оси.
    """

    def __init__(
        self,
        page: Window,
        left_top: Point | tuple[int, int],
        width_height: Size | tuple[int, int],
        items: list[PfObjectIMG] | None = None,
        distance: int = 10,
        size_streak: int = 10,
        min_thumb: int = 20,
        color_streak: tuple[int, int, int] = (170, 170, 170),
        speed: int = 30,
    ):
        """
        Args:
            left_top, width_height: позиция и размеры окна списка.
            items: начальные элементы (PfObjectIMG с .img и .height/.width).
            distance: отступ между элементами.
            size_streak: толщина полосы прокрутки.
            min_thumb: минимальная длина ползунка.
            color_streak: цвет полосы/ползунка.
            speed: пикселей за один тик колеса.
        """
        super().__init__(page, left_top, width_height)
        self.distance = distance
        self.size_streak = size_streak
        self.min_thumb = min_thumb
        self.color_streak = color_streak
        self.speed = speed

        self.items: list[PfObjectIMG] = list(items) if items else []

        # кэш математики
        self._sizes = array('q')          # размеры элементов вдоль оси
        self._prefix = array('q')         # префиксные суммы
        self._total_length = 0
        self._max_scroll = 0
        self._thumb_size = 0
        self._thumb_travel = 0

        # состояние
        self.scroll_offset = 0
        self.visible_start = 0
        self.visible_end = -1

        self._rebuild_cache()

    # абстрактные методы (реализуются в наследниках)
    def _item_size(self, item) -> int:                          raise NotImplementedError
    def _view_length(self) -> int:                              raise NotImplementedError
    def _view_rect(self) -> Rect:                               raise NotImplementedError
    def _axis_offset(self) -> int:                              raise NotImplementedError
    def _mouse_axis(self) -> int:                               raise NotImplementedError
    def _blit_item(self, screen, item, screen_pos):             raise NotImplementedError
    def _draw_thumb(self, screen, thumb_pos):                   raise NotImplementedError
    def _item_global_pos(self, idx: int) -> tuple[int, int]:    raise NotImplementedError

    # кэш и видимый диапазон
    def _rebuild_cache(self):
        sizes = array('q', (self._item_size(it) for it in self.items))
        self._sizes = sizes
        self._prefix = build_prefix(sizes, self.distance)
        self._total_length = total_length(self._prefix, sizes)
        self._max_scroll, self._thumb_size, self._thumb_travel = scroll_metrics(self._total_length, self._view_length(), self.min_thumb)
        self.scroll_offset = clamp(self.scroll_offset, 0, self._max_scroll)
        self._update_visible()
        self._sync_positions()

    def _sync_positions(self) -> None:
        """Записать глобальные координаты в left_top видимых элементов."""
        if self.visible_start > self.visible_end:
            return
        for i in range(self.visible_start, self.visible_end + 1):
            gx, gy = self._item_global_pos(i)
            self.items[i].left, self.items[i].top = gx, gy

    def _update_visible(self):
        self.visible_start, self.visible_end = find_visible_range(
            self._prefix, self._sizes, self.scroll_offset, self._view_length(),
        )

    def resize(self, width_height):
        self.width_height = width_height if isinstance(width_height, Size) else Size(*width_height)
        self._rebuild_cache()

    # публичный API
    def add(self, *args):
        "добавляет несколько объектов"
        self.items.extend(args)
        self._rebuild_cache()

    def append(self, item):
        self.items.append(item)
        self._rebuild_cache()

    def clear(self, is_update: bool = True):
        self.items.clear()
        if is_update:
            self._rebuild_cache()

    def update(self, dt=None):
        for itm in self.items:
            itm.update(dt)

    def retention(self, pos) -> bool:
        return self._view_rect().collidepoint(*pos)

    def index(self) -> int | None:
        """Индекс элемента под курсором или None. O(log n)."""
        if not self.items:
            return None
        content_pos = self._mouse_axis() - self._axis_offset() + self.scroll_offset
        idx = find_index_at(self._prefix, self._sizes, content_pos)
        return idx if idx >= 0 else None

    def mousewheel(self, common: CommonEvent, wheel: MouseWheelEvent):
        """Обрабатывает колесо. Возвращает True, если прокрутил."""
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                if self.items[index].mousewheel(common, wheel):
                    return True

        if not self.retention(self.page.mouse_pos): return False
        self._scroll_by(-wheel.y * self.speed)
        
        return True

    def _scroll_by(self, delta: int):
        new = clamp(self.scroll_offset + delta, 0, self._max_scroll)
        if new != self.scroll_offset:
            self.scroll_offset = new
            self._update_visible()
            self._sync_positions()

    @property
    def visible(self) -> list:
        """Элементы в видимом диапазоне (создаёт новый список!)."""
        if self.visible_start > self.visible_end: return []
        return self.items[self.visible_start:self.visible_end + 1]

    @property
    def visible_pos(self) -> list:
        """Экранные координаты вдоль оси для видимых элементов."""
        base = self._axis_offset() - self.scroll_offset
        return [base + self._prefix[i] for i in range(self.visible_start, self.visible_end + 1)]

    @property
    def content_length(self) -> int:
        return self._total_length

    @property
    def _h(self) -> int: # обратная совместимость
        return self._total_length

    ### обратная совместимость

    # Системные события (для всех)
    def quit(self, common: CommonEvent, quit: QuitEvent) -> None:
        """
        SDL_QUIT
        Пользователь запросил закрытие приложения (нажал на крестик окна, Alt+F4 или эквивалент в оконной системе).
        """
        for object in self.items:
            object.quit(common, quit)

    def app_terminating(self, common: CommonEvent) -> None:
        """
        SDL_APP_TERMINATING
        Приложение завершается ОС (iOS/Android)
        """
        for object in self.items:
            object.app_terminating(common)

    def app_lowmemory(self, common: CommonEvent) -> None:
        """
        SDL_APP_LOWMEMORY
        Приложению не хватает памяти
        """
        for object in self.items:
            object.app_lowmemory(common)

    def app_willenterbackground(self, common: CommonEvent) -> None:
        """
        SDL_APP_WILLENTERBACKGROUND
        Приложение собирается уйти в фон
        """
        for object in self.items:
            object.app_willenterbackground(common)

    def app_didenterbackground(self, common: CommonEvent) -> None:
        """
        SDL_APP_DIDENTERBACKGROUND
        Приложение ушло в фон
        """
        for object in self.items:
            object.app_didenterbackground(common)

    def app_willenterforeground(self, common: CommonEvent) -> None:
        """
        SDL_APP_WILLENTERFOREGROUND
        Приложение собирается вернуться на передний план
        """
        for object in self.items:
            object.app_willenterforeground(common)

    def app_didenterforeground(self, common: CommonEvent) -> None:
        """
        SDL_APP_DIDENTERFOREGROUND
        Приложение снова активно
        """
        for object in self.items:
            object.app_didenterforeground(common)

    def localechanged(self, common: CommonEvent) -> None:
        """
        SDL_LOCALECHANGED
        Изменились локальные настройки пользователя
        """
        for object in self.items:
            object.localechanged(common)

    def displayevent(self, common: CommonEvent, display: DisplayEvent) -> None:
        """
        SDL_DISPLAYEVENT
        Изменение состояния дисплея
        """
        for object in self.items:
            object.displayevent(common, display)

    def windowevent(self, common: CommonEvent, window: WindowEvent) -> None:
        """
        SDL_WINDOWEVENT
        Изменение состояния окна (фокус, размер, перемещение и т.п.)
        """
        for object in self.items:
            object.windowevent(common, window)

    def syswmevent(self, common: CommonEvent, syswm: SysWMEvent) -> None:
        """
        SDL_SYSWMEVENT
        Системное событие оконного менеджера
        """
        for object in self.items:
            object.syswmevent(common, syswm)

    def clipboardupdate(self, common: CommonEvent) -> None:
        """
        SDL_CLIPBOARDUPDATE
        Изменилось содержимое буфера обмена
        """
        for object in self.items:
            object.clipboardupdate(common)

    def render_targets_reset(self, common: CommonEvent) -> None:
        """
        SDL_RENDER_TARGETS_RESET
        Цели рендеринга сброшены (нужно обновить содержимое)
        """
        for object in self.items:
            object.render_targets_reset(common)

    def render_device_reset(self, common: CommonEvent) -> None:
        """
        SDL_RENDER_DEVICE_RESET
        Устройство рендеринга сброшено (нужно пересоздать текстуры)
        """
        for object in self.items:
            object.render_device_reset(common)

    def sensorupdate(self, common: CommonEvent, sensor: SensorEvent) -> None:
        """
        SDL_SENSORUPDATE
        Обновились данные сенсора
        """
        for object in self.items:
            object.sensorupdate(common, sensor)

    # События клавиатуры
    def keydown(self, common: CommonEvent, key: KeyboardEvent) -> None:
        """
        SDL_KEYDOWN
        Клавиша нажата
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].keydown(common, key)
        
    def keyup(self, common: CommonEvent, key: KeyboardEvent) -> None:
        """
        SDL_KEYUP
        Клавиша отпущена
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].keyup(common, key)

    def textediting(self, common: CommonEvent, edit: TextEditingEvent) -> None:
        """
        SDL_TEXTEDITING
        Редактирование текста (IME, композиция)
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].textediting(common, edit)

    def textinput(self, common: CommonEvent, text: TextInputEvent) -> None:
        """
        SDL_TEXTINPUT
        Ввод текста (после завершения IME)
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].textinput(common, text)

    def keymapchanged(self, common: CommonEvent) -> None:
        """
        SDL_KEYMAPCHANGED
        Раскладка клавиатуры изменилась системой
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].keymapchanged(common)

    def textediting_ext(self, common: CommonEvent, editExt: TextEditingExtEvent) -> None:
        """
        SDL_TEXTEDITING_EXT
        Расширенное редактирование текста (IME)
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].textediting_ext(common, editExt)

    # События мыши

    def mousemotion(self, common: CommonEvent, motion: MouseMotionEvent) -> None:
        """
        SDL_MOUSEMOTION
        Перемещение мыши
        """
        if self.rect.collidepoint(motion.x, motion.y):
            index = self.index()
            if not index is None:
                self.items[index].mousemotion(common, motion)

    def mousebuttondown(self, common: CommonEvent, button: MouseButtonEvent) -> None:
        """
        SDL_MOUSEBUTTONDOWN
        Кнопка мыши нажата
        """
        if self.rect.collidepoint(button.x, button.y):
            index = self.index()
            if not index is None:
                self.items[index].mousebuttondown(common, button)

    def mousebuttonup(self, common: CommonEvent, button: MouseButtonEvent) -> None:
        """
        SDL_MOUSEBUTTONUP
        Кнопка мыши отпущена
        """
        if self.rect.collidepoint(button.x, button.y):
            index = self.index()
            if not index is None:
                self.items[index].mousebuttonup(common, button)

# пропустили контроллеры
# пропустили сенсорный ввод и жесты

    # Аудиоустройства

    def audiodeviceadded(self, common: CommonEvent, adevice: AudioDeviceEvent) -> None:
        """
        SDL_AUDIODEVICEADDED
        Аудиоустройство подключено
        """
        for object in self.items:
            object.render_device_reset(common, adevice)

    def audiodeviceremoved(self, common: CommonEvent, adevice: AudioDeviceEvent) -> None:
        """
        SDL_AUDIODEVICEREMOVED
        Аудиоустройство отключено
        """
        for object in self.items:
            object.audiodeviceremoved(common, adevice)

        # Drag and Drop (перетаскивание файлов/текста)

    def dropbegin(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPBEGIN
        Начало перетаскивания
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].dropbegin(common, drop)

    def dropfile(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPFILE
        Файл перетащен в окно
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].dropfile(common, drop)

    def droptext(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPTEXT
        Текст перетащен в окно
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].droptext(common, drop)

    def dropcomplete(self, common: CommonEvent, drop: DropEvent) -> None:
        """
        SDL_DROPCOMPLETE
        Перетаскивание завершено
        """
        if self.rect.collidepoint(*self.page.mouse_pos):
            index = self.index()
            if not index is None:
                self.items[index].dropcomplete(common, drop)