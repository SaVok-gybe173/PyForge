"""
Обёртка над sdl2, имитирующая pygame.event.

Каждая функция — тонкий слой над соответствующим вызовом SDL2.
Использование аналогично pygame, но с оговорками, описанными в docstring.
"""

from typing import Final
from sdl2.keyboard import SDL_Keysym, SDL_Scancode, SDL_Keycode
from sdl2.joystick import SDL_JoystickID, SDL_JoystickPowerLevel
from sdl2.syswm import SDL_SysWMmsg
from sdl2.touch import SDL_TouchID, SDL_FingerID
from sdl2.gesture import SDL_GestureID
from sdl2.video import SDL_Window


type uint32 = int   # беззнаковый 1 байт	0…255
type uint16 = int   # беззнаковый 2 байта	0…65535
type uint8 = int    # беззнаковый 1 байт	0…255
type sint64 = int   # 
type sint32 = int   # -2³¹…2³¹-1
type sint16 = int   # -32768…32767
type sint8 = int    # -128…127


"""

Таблица соответствия: атрибут -> тип события
Атрибут	    Структура	                Тип(ы) события (event.type)	                                                            Что внутри (основное)
type	    Uint32	                    всегда	                                                                                номер типа события
common	    SDL_CommonEvent	            всегда (общие поля)	                                                                    timestamp (мс с момента старта SDL)
display	    SDL_DisplayEvent	        SDL_DISPLAYEVENT	                                                                    display, event (подтип), data1
window	    SDL_WindowEvent	            SDL_WINDOWEVENT	                                                                        windowID, event (подтип), data1, data2
key	        SDL_KeyboardEvent	        SDL_KEYDOWN, SDL_KEYUP	                                                                windowID, state, repeat, keysym (.sym, .scancode, .mod)
edit	    SDL_TextEditingEvent	    SDL_TEXTEDITING	                                                                        windowID, text, start, length
editExt	    SDL_TextEditingExtEvent	    SDL_TEXTEDITING_EXT	                                                                    windowID, text (указатель), start, length
text	    SDL_TextInputEvent	        SDL_TEXTINPUT	                                                                        windowID, text
motion	    SDL_MouseMotionEvent	    SDL_MOUSEMOTION	                                                                        which, state, x, y, xrel, yrel
button	    SDL_MouseButtonEvent	    SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP	                                                which, button, state, clicks, x, y
wheel	    SDL_MouseWheelEvent	        SDL_MOUSEWHEEL	                                                                        which, x, y, direction, preciseX, preciseY, mouseX, mouseY
jaxis	    SDL_JoyAxisEvent	        SDL_JOYAXISMOTION	                                                                    which, axis, value
jball	    SDL_JoyBallEvent	        SDL_JOYBALLMOTION	                                                                    which, ball, xrel, yrel
jhat	    SDL_JoyHatEvent	            SDL_JOYHATMOTION	                                                                    which, hat, value
jbutton	    SDL_JoyButtonEvent	        SDL_JOYBUTTONDOWN, SDL_JOYBUTTONUP	                                                    which, button, state
jdevice	    SDL_JoyDeviceEvent	        SDL_JOYDEVICEADDED, SDL_JOYDEVICEREMOVED	                                            which
jbattery	SDL_JoyBatteryEvent	        SDL_JOYBATTERYUPDATED	                                                                which, level
caxis	    SDL_ControllerAxisEvent	    SDL_CONTROLLERAXISMOTION	                                                            which, axis, value
cbutton	    SDL_ControllerButtonEvent	SDL_CONTROLLERBUTTONDOWN, SDL_CONTROLLERBUTTONUP	                                    which, button, state
cdevice	    SDL_ControllerDeviceEvent	SDL_CONTROLLERDEVICEADDED, SDL_CONTROLLERDEVICEREMOVED, SDL_CONTROLLERDEVICEREMAPPED	which
ctouchpad	SDL_ControllerTouchpadEvent	SDL_CONTROLLERTOUCHPADDOWN/MOTION/UP	                                                which, touchpad, finger, x, y, pressure
csensor	    SDL_ControllerSensorEvent	SDL_CONTROLLERSENSORUPDATE	                                                            which, sensor, data
sensor	    SDL_SensorEvent	            SDL_SENSORUPDATE	                                                                    which, data
quit	    SDL_QuitEvent	            SDL_QUIT	                                                                            (полей нет, важен сам факт)
user	    SDL_UserEvent	            SDL_USEREVENT…SDL_LASTEVENT-1	                                                        windowID, code, data1, data2
syswm	    SDL_SysWMEvent	            SDL_SYSWMEVENT	                                                                        msg
tfinger	    SDL_TouchFingerEvent	    SDL_FINGERDOWN, SDL_FINGERUP, SDL_FINGERMOTION	                                        touchId, fingerId, x, y, dx, dy, pressure, windowID
mgesture	SDL_MultiGestureEvent	    SDL_MULTIGESTURE	                                                                    touchId, dTheta, dDist, x, y, numFingers
dgesture	SDL_DollarGestureEvent	    SDL_DOLLARGESTURE, SDL_DOLLARRECORD	                                                    touchId, gestureId, numFingers, error, x, y
drop	    SDL_DropEvent	            SDL_DROPBEGIN, SDL_DROPFILE, SDL_DROPTEXT, SDL_DROPCOMPLETE	                            file, windowID
adevice	    SDL_AudioDeviceEvent	    SDL_AUDIODEVICEADDED, SDL_AUDIODEVICEREMOVED	                                        which, iscapture
padding	    —	                        —	                                                                                    служебное выравнивание, не использовать

"""

QUIT: Final[uint32]                     # Запрос на закрытие приложения
APP_TERMINATING: Final[uint32]          # Приложение завершается ОС (iOS/Android)	
APP_LOWMEMORY: Final[uint32]            # Приложению не хватает памяти
APP_WILLENTERBACKGROUND: Final[uint32]  # Приложение собирается уйти в фон
APP_DIDENTERBACKGROUND: Final[uint32]   # Приложение ушло в фон
APP_WILLENTERFOREGROUND: Final[uint32]  # Приложение собирается вернуться на передний план
APP_DIDENTERFOREGROUND: Final[uint32]   # Приложение снова активно
LOCALECHANGED: Final[uint32]            # Изменились локальные настройки пользователя
DISPLAYEVENT: Final[uint32]             # Изменение состояния дисплея
WINDOWEVENT: Final[uint32]              # Изменение состояния окна (фокус, размер, перемещение и т.п.)
SYSWMEVENT: Final[uint32]               # Системное событие оконного менеджера
CLIPBOARDUPDATE: Final[uint32]          # Изменилось содержимое буфера обмена
RENDER_TARGETS_RESET: Final[uint32]     # Цели рендеринга сброшены (нужно обновить содержимое)	
RENDER_DEVICE_RESET: Final[uint32]      # Устройство рендеринга сброшено (нужно пересоздать текстуры)
SENSORUPDATE: Final[uint32]             # Обновились данные сенсора

KEYDOWN: Final[uint32]                  # Клавиша нажата
KEYUP: Final[uint32]                    # Клавиша отпущена
TEXTEDITING: Final[uint32]              # Редактирование текста (IME, композиция)
TEXTINPUT: Final[uint32]                # Ввод текста (после завершения IME)
KEYMAPCHANGED: Final[uint32]            # Раскладка клавиатуры изменилась системой
TEXTEDITING_EXT: Final[uint32]          # Расширенное редактирование текста (IME)

MOUSEMOTION: Final[uint32]              # Перемещение мыши
MOUSEBUTTONDOWN: Final[uint32]          # Кнопка мыши нажата
MOUSEBUTTONUP: Final[uint32]            # Кнопка мыши отпущена
MOUSEWHEEL: Final[uint32]               # Прокрутка колеса мыши

JOYAXISMOTION: Final[uint32]            # Движение оси джойстика
JOYBALLMOTION: Final[uint32]            # Движение трекбола
JOYHATMOTION: Final[uint32]             # Изменение POV-переключателя (hat)
JOYBUTTONDOWN: Final[uint32]            # Кнопка джойстика нажата
JOYBUTTONUP: Final[uint32]              # Кнопка джойстика отпущена
JOYDEVICEADDED: Final[uint32]           # Джойстик подключён
JOYDEVICEREMOVED: Final[uint32]         # Джойстик отключён
JOYBATTERYUPDATED: Final[uint32]        # Изменился уровень заряда джойстика

CONTROLLERAXISMOTION: Final[uint32]     # Движение оси контроллера
CONTROLLERBUTTONDOWN: Final[uint32]     # Кнопка контроллера нажата
CONTROLLERBUTTONUP: Final[uint32]       # Кнопка контроллера отпущена
CONTROLLERDEVICEADDED: Final[uint32]    # Контроллер подключён
CONTROLLERDEVICEREMOVED: Final[uint32]  # Контроллер отключён
CONTROLLERDEVICEREMAPPED: Final[uint32] # Раскладка контроллера обновлена
CONTROLLERTOUCHPADDOWN: Final[uint32]   # Тачпад контроллера нажат
CONTROLLERTOUCHPADMOTION: Final[uint32] # Палец движется по тачпаду контроллера
CONTROLLERTOUCHPADUP: Final[uint32]     # Палец отпущен с тачпада контроллера
CONTROLLERSENSORUPDATE: Final[uint32]   # Обновились данные сенсора контроллера

FINGERDOWN: Final[uint32]               # Палец коснулся экрана
FINGERUP: Final[uint32]                 # Палец поднят
FINGERMOTION: Final[uint32]             # Палец движется
MULTIGESTURE: Final[uint32]             # Мультитач-жест (щипок, вращение)
DOLLARGESTURE: Final[uint32]            # Распознан долларовый жест (1-жест)
DOLLARRECORD: Final[uint32]             # Записан долларовый жест

AUDIODEVICEADDED: Final[uint32]         # Аудиоустройство подключено
AUDIODEVICEREMOVED: Final[uint32]       # Аудиоустройство отключено

DROPBEGIN: Final[uint32]                # Начало перетаскивания
DROPFILE: Final[uint32]                 # Файл перетащен в окно
DROPTEXT: Final[uint32]                 # Текст перетащен в окно
DROPCOMPLETE: Final[uint32]             # Перетаскивание завершено

USEREVENT: Final[uint32]                # Первый номер для пользовательских событий (значение 0x8000)
LASTEVENT: Final[uint32]                # Верхняя граница зарезервированных типов (0xFFFF)

FIRSTEVENT: Final[uint32]               # Значение 0, не используется (не удалять)
POLLSENTINEL: Final[uint32]             # Сигнализирует о конце цикла опроса событий (0x7F00)

EVENT_NAMES: dict[int, str]


WINDOWEVENT_NONE: Final[uint32]             # нет события (служебное значение).
WINDOWEVENT_SHOWN: Final[uint32]            # окно показано.
WINDOWEVENT_HIDDEN: Final[uint32]           # окно скрыто.
WINDOWEVENT_EXPOSED: Final[uint32]          # содержимое окна нужно перерисовать.
WINDOWEVENT_MOVED: Final[uint32]            # окно перемещено (новые координаты в data1/data2).
WINDOWEVENT_RESIZED: Final[uint32]          # окно изменено пользователем/системой (новый размер в data1/data2).
WINDOWEVENT_SIZE_CHANGED: Final[uint32]     # размер окна изменился (в т.ч. программно).
WINDOWEVENT_MINIMIZED: Final[uint32]        # окно свёрнуто.
WINDOWEVENT_MAXIMIZED: Final[uint32]        # окно развёрнуто.
WINDOWEVENT_RESTORED: Final[uint32]         # окно восстановлено из свёрнутого/развёрнутого.
WINDOWEVENT_ENTER: Final[uint32]            # курсор мыши вошёл в окно.
WINDOWEVENT_LEAVE: Final[uint32]            # курсор мыши покинул окно.
WINDOWEVENT_FOCUS_GAINED: Final[uint32]     # окно получило фокус ввода.
WINDOWEVENT_FOCUS_LOST: Final[uint32]       # окно потеряло фокус ввода.
WINDOWEVENT_CLOSE: Final[uint32]            # запрошено закрытие окна.
WINDOWEVENT_TAKE_FOCUS: Final[uint32]       # запрос на передачу фокуса окну (от WM).
WINDOWEVENT_HIT_TEST: Final[uint32]         # запрос на hit-test (какие области окна «кликабельны»).
WINDOWEVENT_ICCPROF_CHANGED: Final[uint32]  # изменился ICC-профиль дисплея.
WINDOWEVENT_DISPLAY_CHANGED: Final[uint32]  # окно переместилось на другой дисплей.

def pump() -> None:
    """Обновить внутреннее состояние очереди событий SDL.

    Аналог pygame.event.pump().

    Прокачивает очередь: забирает сообщения из оконной системы и
    кладёт их во внутреннюю очередь SDL. Нужно вызывать только если
    ты НЕ используешь poll()/wait()/get() — эти функции вызывают
    SDL_PumpEvents автоматически.

    Соответствие SDL2: sdl2.SDL_PumpEvents()

    Пример:
        # Если ты не читаешь события, но хочешь, чтобы состояние
        # клавиатуры/мыши обновлялось:
        sdl2.SDL_PumpEvents()
    """

def get() -> list[Event]:
    """Забрать все накопившиеся события из очереди.

    Аналог pygame.event.get().

    Возвращает список структур Enent. Очередь после вызова пуста.
    Внутри автоматически вызывает SDL_PumpEvents.

    Соответствие SDL2: sdl2.ext.get_events()
                      (обёртка над sdl2.SDL_PollEvent в цикле)

    Returns:
        list[Enent]: список событий (может быть пустым).

    Пример:
        for event in get():
            if event.type == QUIT:
                running = False
    """

def clear() -> None:
    """Полностью очистить очередь событий.

    Аналог pygame.event.clear().

    Удаляет все события всех типов. Если нужно удалить только
    определённые типы — используй set_blocked() до этого или
    SDL_FlushEvent(type) напрямую.

    Соответствие SDL2: sdl2.SDL_FlushEvents(SDL_FIRSTEVENT, SDL_LASTEVENT)

    Пример:
        clear()  # выкинуть всё, что накопилось
    """

def set_blocked(*types: int) -> None:
    """Заблокировать приём событий указанных типов.

    Аналог pygame.event.set_blocked().

    Заблокированные события не попадают в очередь (сбрасываются
    в момент генерации). Если не передать ни одного типа — блокирует
    ВСЕ события.

    Соответствие SDL2: sdl2.SDL_EventState(type, sdl2.SDL_IGNORE)

    Args:
        *types: типы событий для блокировки (например, SDL_MOUSEMOTION).

    Пример:
        set_blocked(sdl2.SDL_MOUSEMOTION, sdl2.SDL_MOUSEBUTTONDOWN)
    """

def get_blocked() -> list:
    """Получить список заблокированных типов событий.

    Аналог pygame.event.get_blocked().

    В SDL2 нет списка «заблокировано» — состояние спрашивается
    по одному типу через SDL_EventState(..., SDL_QUERY). Здесь
    реализовано перебором диапазона SDL_FIRSTEVENT..SDL_LASTEVENT.

    Соответствие SDL2: sdl2.SDL_EventState(type, sdl2.SDL_QUERY)

    Returns:
        list[int]: типы событий, находящиеся в состоянии IGNORE.

    Пример:
        blocked = get_blocked()
        if sdl2.SDL_MOUSEMOTION in blocked:
            print("мышь заблокирована")
    """


def set_allowed(*types: int) -> None:
    """Разрешить приём событий указанных типов.

    Аналог pygame.event.set_allowed().

    Снимает блокировку с указанных типов. Если не передать ни
    одного типа — разрешает ВСЕ события (эквивалент очистки фильтра).

    Соответствие SDL2: sdl2.SDL_EventState(type, sdl2.SDL_ENABLE)

    Args:
        *types: типы событий для разблокировки.

    Пример:
        set_allowed(sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP)
    """

def post(event: Event) -> bool:
    """Положить готовое событие в очередь.

    Аналог pygame.event.post().

    ВАЖНО: соответствие в SDL2 — SDL_PushEvent (Push), а НЕ
    SDL_PeepEvents (Peep). Push кладёт событие в очередь и
    прогоняет его через фильтр. Peep — подсматривает/вставляет
    в обход фильтра.

    Для пользовательских событий используй зарегистрированный тип:
        custom_type = sdl2.SDL_RegisterEvents(1)
    или стандартный sdl2.SDL_USEREVENT.

    Соответствие SDL2: sdl2.SDL_PushEvent(event)

    Args:
        event: заранее заполненная структура SDL_Event.

    Returns:
        bool: True при успехе, False при ошибке.

    Пример:
        ev = sdl2.SDL_Event()
        ev.type = sdl2.SDL_USEREVENT
        ev.user.code = 42
        post(ev)
    """

def set_grab(win: SDL_Window, enable: bool) -> None:
    """Захватить (или отпустить) ввод мышью в пределах окна.

    Аналог pygame.event.set_grab().

    В SDL2 захват привязан к конкретному окну — это окно должно
    быть создано заранее и передано в функцию. Если окно одно,
    можно обернуть так, чтобы окно подставлялось автоматически.

    Соответствие SDL2: sdl2.SDL_SetWindowGrab(window, SDL_TRUE/SDL_FALSE)

    Args:
        enable: True — захватить, False — отпустить.

    Пример:
        set_grab(True)   # включить (FPS-стиль)
        set_grab(False)  # выключить
    """


def get_grab(win: SDL_Window) -> bool:
    """Узнать, захвачен ли ввод окном.

    Аналог pygame.event.get_grab().

    Соответствие SDL2: sdl2.SDL_GetWindowGrab(window)

    Returns:
        bool: True, если ввод захвачен.

    Пример:
        if get_grab():
            print("мышь заперта в окне")
    """

def event_add(type: int, name: str) -> None:
    "добавляет новый эвент в таблицу"

def event_name(type: int) -> str | None:
    "возвращает имя эвента"

def event_type(name: str) -> int | None:
    "получает тип эвента по имени"

class CommonEvent: ...          # всегда (общие поля)

class DisplayEvent:             # SDL_DISPLAYEVENT
    # Изменение дисплея: подключение/отключение, смена ориентации/DPI
    display: uint32
    event: uint8 # подтип (SDL_DISPLAYEVENT_*)
    data1: sint32

class WindowEvent:              # SDL_WindowEvent	SDL_WINDOWEVENT
    # Изменение окна: перемещение, размер, фокус, видимость
    windowID: uint32 
    event: uint8 # подтип (SDL_WINDOWEVENT_*)
    # data1/data2 зависят от подтипа (например, новая ширина/высота).
    data1: sint32 
    data2: sint32

class KeyboardEvent:            # SDL_KEYDOWN, SDL_KEYUP
    # Нажатие/отпускание клавиши
    windowID: uint32
    state: uint8
    repeat: uint8       # автоповтор
    keysym: SDL_Keysym
    scancode: SDL_Scancode  # физическая клавиша (не зависит от раскладки)
    sym: SDL_Keycode    # виртуальный код
    mod: uint16         # модификаторы (Shift/Ctrl/Alt)

class TextEditingEvent:         # SDL_TEXTEDITING
    # Промежуточный ввод через IME (композиция)
    windowID: uint32
    text: str # char[32] текущая строка
    # выделенный фрагмент для отрисовки подсказки
    start: sint32
    length: sint32

class TextEditingExtEvent:      # SDL_TEXTEDITING_EXT
    # То же, что edit
    windowID: uint32
    text: str   # указатель на динамическую строку (для длинных IME-композиций)
    # Освобождать через SDL_free
    start: sint32
    length: sint32

class TextInputEvent:           # SDL_TEXTINPUT
    # Готовый текст после завершения IME/нажатия клавиши. Используйте для текстовых полей ввода.
    windowID: uint32
    text: str

class MouseMotionEvent:         # SDL_MOUSEMOTION
    # Движение мыши
    which: uint32
    state: uint32 # битовая маска нажатых кнопок
    # x,y — абсолютные координаты в окне
    x: sint32
    y: sint32
    # xrel,yrel — относительное смещение (для FPS-камеры)
    xrel: sint32
    yrel: sint32

class MouseButtonEvent:         # SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP
    # Клик/отпускание кнопки мыши
    which: uint32
    button: uint8   # SDL_BUTTON_LEFT/RIGHT/MIDDLE
    state: uint8
    clicks: uint8   # число кликов (2 = двойной)
    # x,y — координаты клика
    x: sint32
    y: sint32

class MouseWheelEvent:          # SDL_MOUSEWHEEL
    # Прокрутка колеса/тачпада
    which: uint32
    x: sint32 # вертикаль (+вверх)
    y: sint32 # горизонталь
    direction: uint32 # SDL_MOUSEWHEEL_NORMAL/FLIPPED
    # precise* — плавные значения
    preciseX: float
    preciseY: float
    # mouse* — позиция курсора
    mouseX: sint32
    mouseY: sint32

class JoyAxisEvent:             # SDL_JOYAXISMOTION
    # Движение оси джойстика
    which: SDL_JoystickID
    axis: uint8 # индекс оси
    value: uint16   # value ∈ [-32768, 32767]

class JoyBallEvent:             # SDL_JOYBALLMOTION
    # Движение трекбола
    which: SDL_JoystickID 
    ball: uint8
    # xrel,yrel — относительное смещение
    xrel: sint16
    yrel: sint16

class JoyHatEvent:              # SDL_JOYHATMOTION
    # Движение POV-«шляпки»
    which: SDL_JoystickID
    hat: uint8
    value: uint8 # комбинация SDL_HAT_UP/DOWN/LEFT/RIGHT/CENTERED

class JoyButtonEvent:           # SDL_JOYBUTTONDOWN, SDL_JOYBUTTONUP
    # Нажатие/отпускание кнопки джойстика
    which: SDL_JoystickID
    button: uint8
    state: uint8 # SDL_PRESSED/SDL_RELEASED

class JoyDeviceEvent:           # SDL_JOYDEVICEADDED, SDL_JOYDEVICEREMOVED
    # Подключение/отключение джойстика. ADDED → индекс; REMOVED → instance id
    which: sint32

class JoyBatteryEvent:          # SDL_JOYBATTERYUPDATED
    # Изменение заряда джойстика
    which: SDL_JoystickID
    level: SDL_JoystickPowerLevel # SDL_JOYSTICK_POWER_* (UNKNOWN/EMPTY/LOW/MEDIUM/FULL/WIRED)

class ControllerAxisEvent:      # SDL_CONTROLLERAXISMOTION
    # Ось геймпада
    which: SDL_JoystickID 
    axis: uint8 # SDL_CONTROLLER_AXIS_* (LEFTX, TRIGGERRIGHT и т.д.)
    value: sint16

class ControllerButtonEvent:    # SDL_CONTROLLERBUTTONDOWN, SDL_CONTROLLERBUTTONUP
    # Кнопка геймпада
    which: SDL_JoystickID
    button: uint8 # SDL_CONTROLLER_BUTTON_* (A, B, X, Y и т.д.).
    state: uint8

class ControllerDeviceEvent:    # SDL_CONTROLLERDEVICEADDED/REMOVED/REMAPPED
    # Подключение/отключение/перепривязка геймпада
    which: sint32

class ControllerTouchpadEvent:  # SDL_CONTROLLERTOUCHPADDOWN/MOTION/UP
    # Тачпад геймпада (DualShock 4)
    which: SDL_JoystickID
    touchpad: sint32
    finger: sint32
    # Координаты нормализованы 0…1
    x: float
    y: float
    pressure: float

class ControllerSensorEvent:    # SDL_CONTROLLERSENSORUPDATE
    # Данные сенсора геймпада (акселерометр, гироскоп)
    which: SDL_JoystickID
    sensor: sint32
    data: tuple[float, float, float] # 3 значения

class SensorEvent:              # SDL_SENSORUPDATE
    # Данные аппаратного сенсора устройства (телефон/планшет)
    which: sint32
    data: tuple[float, ...] # до 6 значений

class QuitEvent: ...            # SDL_QUIT
    # Запрос на закрытие приложения (крестик, Alt+F4, SIGTERM). Завершайте главный цикл.

class UserEvent:                # SDL_USEREVENT…SDL_LASTEVENT-1
    # Пользовательское событие (создаёте сами)
    windowID: uint32
    code: sint32 # ваш код типа
    # data1/data2 — указатели на данные
    data1: object
    data2: object


class SysWMEvent:               # SDL_SYSWMEVENT
    # Сырое сообщение оконной системы (WM_* в Windows, XEvent в X11)
    # Для низкоуровневой интеграции
    msg: SDL_SysWMmsg

class TouchFingerEvent:          # SDL_FINGERDOWN, SDL_FINGERUP, SDL_FINGERMOTION
    # Касание/движение пальца
    touchId: SDL_TouchID
    fingerId: SDL_FingerID # конкретный палец (мультитач)
    # x,y,dx,dy,pressure нормализованы 0…1
    x: float
    y: float
    dx: float
    dy: float
    pressure: float 
    windowID: uint32

class MultiGestureEvent:        # SDL_MULTIGESTURE
    # Мультитач-жест (щипок, вращение)
    touchId: SDL_TouchID
    dTheta: float # поворот
    dDist: float # изменение расстояния (zoom)
    x: float
    y: float
    numFingers: uint16

class DollarGestureEvent:       # SDL_DOLLARGESTURE, SDL_DOLLARRECORD
    # Шаблонный жест (буква/фигура)
    touchId: SDL_TouchID 
    gestureId: SDL_GestureID # id шаблона
    numFingers: uint32
    error: float # точность распознавания (меньше = точнее)
    x: float
    y: float

class DropEvent:                # SDL_DROPBEGIN, SDL_DROPFILE, SDL_DROPTEXT, SDL_DROPCOMPLETE
    # Drag&drop
    # Для DROPFILE — путь к файлу (освобождать SDL_free), для DROPTEXT — сам текст, для BEGIN/COMPLETE — NULL.
    file: str
    windowID: uint32

class AudioDeviceEvent:         # SDL_AUDIODEVICEADDED, SDL_AUDIODEVICEREMOVED
    # Аудиоустройство подключено/отключено
    which: uint32 # индекс (ADDED) или SDL_AudioDeviceID (REMOVED)
    iscapture: uint8 # iscapture ≠ 0 — микрофон/захват

class Event:
    type: uint32 # всегда
    common: CommonEvent # всегда
    display: DisplayEvent # SDL_DISPLAYEVENT
    key: KeyboardEvent # SDL_KEYDOWN, SDL_KEYUP
    edit: TextEditingEvent # SDL_TEXTEDITING
    editExt: TextEditingExtEvent # SDL_TEXTEDITING_EXT
    text: TextInputEvent # SDL_TEXTINPUT
    motion: MouseMotionEvent # SDL_MOUSEMOTION
    button: MouseButtonEvent # SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP
    wheel: MouseWheelEvent # SDL_MOUSEWHEEL
    jaxis: JoyAxisEvent # SDL_JOYAXISMOTION
    jball: JoyBallEvent # SDL_JOYBALLMOTION
    jhat: JoyHatEvent # SDL_JOYHATMOTION
    jbutton: JoyButtonEvent # SDL_JOYBUTTONDOWN, SDL_JOYBUTTONUP
    jdevice: JoyDeviceEvent # SDL_JOYDEVICEADDED, SDL_JOYDEVICEREMOVED
    jbattery: JoyBatteryEvent # SDL_JOYBATTERYUPDATED
    caxis: ControllerAxisEvent # SDL_CONTROLLERAXISMOTION
    cbutton: ControllerButtonEvent # SDL_CONTROLLERBUTTONDOWN, SDL_CONTROLLERBUTTONUP
    cdevice: ControllerDeviceEvent # SDL_CONTROLLERDEVICEADDED/REMOVED/REMAPPED
    ctouchpad: ControllerTouchpadEvent # SDL_CONTROLLERTOUCHPADDOWN/MOTION/UP
    csensor: ControllerSensorEvent # SDL_CONTROLLERSENSORUPDATE
    sensor: SensorEvent # SDL_SENSORUPDATE
    quit: QuitEvent # SDL_QUIT
    user: UserEvent # SDL_USEREVENT…SDL_LASTEVENT-1
    syswm: SysWMEvent # SDL_SYSWMEVENT
    tfinger: TouchFingerEvent # SDL_FINGERDOWN, SDL_FINGERUP, SDL_FINGERMOTION
    mgesture: MultiGestureEvent # SDL_MULTIGESTURE
    dgesture: DollarGestureEvent # SDL_DOLLARGESTURE, SDL_DOLLARRECORD
    drop: DropEvent # SDL_DROPBEGIN, SDL_DROPFILE, SDL_DROPTEXT, SDL_DROPCOMPLETE
    adevice: AudioDeviceEvent # SDL_AUDIODEVICEADDED, SDL_AUDIODEVICEREMOVED
    padding: object # Служебное поле для выравнивания union. Не использовать.