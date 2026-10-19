from sdl2.keyboard import SDL_Keysym, SDL_Scancode, SDL_Keycode
from sdl2.joystick import SDL_JoystickID, SDL_JoystickPowerLevel
from sdl2.syswm import SDL_SysWMmsg
from sdl2.touch import SDL_TouchID, SDL_FingerID
from sdl2.gesture import SDL_GestureID

type uint32 = int   # беззнаковый 1 байт	0…255
type uint16 = int   # беззнаковый 2 байта	0…65535
type uint8 = int    # беззнаковый 1 байт	0…255
type sint64 = int   # 
type sint32 = int   # -2³¹…2³¹-1
type sint16 = int   # -32768…32767
type sint8 = int    # -128…127


"""

Таблица соответствия: атрибут → тип события
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

QUIT: uint32                    # Запрос на закрытие приложения
APP_TERMINATING: uint32         # Приложение завершается ОС (iOS/Android)	
APP_LOWMEMORY: uint32           # Приложению не хватает памяти
APP_WILLENTERBACKGROUND: uint32 # Приложение собирается уйти в фон
APP_DIDENTERBACKGROUND: uint32  # Приложение ушло в фон
APP_WILLENTERFOREGROUND: uint32 # Приложение собирается вернуться на передний план
APP_DIDENTERFOREGROUND: uint32  # Приложение снова активно
LOCALECHANGED: uint32           # Изменились локальные настройки пользователя
DISPLAYEVENT: uint32            # Изменение состояния дисплея
WINDOWEVENT: uint32             # Изменение состояния окна (фокус, размер, перемещение и т.п.)
SYSWMEVENT: uint32              # Системное событие оконного менеджера
CLIPBOARDUPDATE: uint32         # Изменилось содержимое буфера обмена
RENDER_TARGETS_RESET: uint32    # Цели рендеринга сброшены (нужно обновить содержимое)	
RENDER_DEVICE_RESET: uint32     # Устройство рендеринга сброшено (нужно пересоздать текстуры)
SENSORUPDATE: uint32            # Обновились данные сенсора

KEYDOWN: uint32                 # Клавиша нажата
KEYUP: uint32                   # Клавиша отпущена
TEXTEDITING: uint32             # Редактирование текста (IME, композиция)
TEXTINPUT: uint32               # Ввод текста (после завершения IME)
KEYMAPCHANGED: uint32           # Раскладка клавиатуры изменилась системой
TEXTEDITING_EXT: uint32         # Расширенное редактирование текста (IME)

MOUSEMOTION: uint32             # Перемещение мыши
MOUSEBUTTONDOWN: uint32         # Кнопка мыши нажата
MOUSEBUTTONUP: uint32           # Кнопка мыши отпущена
MOUSEWHEEL: uint32              # Прокрутка колеса мыши

JOYAXISMOTION: uint32           # Движение оси джойстика
JOYBALLMOTION: uint32           # Движение трекбола
JOYHATMOTION: uint32            # Изменение POV-переключателя (hat)
JOYBUTTONDOWN: uint32           # Кнопка джойстика нажата
JOYBUTTONUP: uint32             # Кнопка джойстика отпущена
JOYDEVICEADDED: uint32          # Джойстик подключён
JOYDEVICEREMOVED: uint32        # Джойстик отключён
JOYBATTERYUPDATED: uint32       # Изменился уровень заряда джойстика

CONTROLLERAXISMOTION: uint32    # Движение оси контроллера
CONTROLLERBUTTONDOWN: uint32    # Кнопка контроллера нажата
CONTROLLERBUTTONUP: uint32      # Кнопка контроллера отпущена
CONTROLLERDEVICEADDED: uint32   # Контроллер подключён
CONTROLLERDEVICEREMOVED: uint32 # Контроллер отключён
CONTROLLERDEVICEREMAPPED: uint32# Раскладка контроллера обновлена
CONTROLLERTOUCHPADDOWN: uint32  # Тачпад контроллера нажат
CONTROLLERTOUCHPADMOTION: uint32# Палец движется по тачпаду контроллера
CONTROLLERTOUCHPADUP: uint32    # Палец отпущен с тачпада контроллера
CONTROLLERSENSORUPDATE: uint32  # Обновились данные сенсора контроллера

FINGERDOWN: uint32              # Палец коснулся экрана
FINGERUP: uint32                # Палец поднят
FINGERMOTION: uint32            # Палец движется
MULTIGESTURE: uint32            # Мультитач-жест (щипок, вращение)
DOLLARGESTURE: uint32           # Распознан долларовый жест (1-жест)
DOLLARRECORD: uint32            # Записан долларовый жест

AUDIODEVICEADDED: uint32        # Аудиоустройство подключено
AUDIODEVICEREMOVED: uint32      # Аудиоустройство отключено

DROPBEGIN: uint32               # Начало перетаскивания
DROPFILE: uint32                # Файл перетащен в окно
DROPTEXT: uint32                # Текст перетащен в окно
DROPCOMPLETE: uint32            # Перетаскивание завершено

USEREVENT: uint32               # Первый номер для пользовательских событий (значение 0x8000)
LASTEVENT: uint32               # Верхняя граница зарезервированных типов (0xFFFF)

FIRSTEVENT: uint32              # Значение 0, не используется (не удалять)
POLLSENTINEL: uint32            # Сигнализирует о конце цикла опроса событий (0x7F00)

EVENT_NAMES: dict[int, str]

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

class Enent:
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