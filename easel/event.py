"""
Ниже — структурированный справочник по событиям SDL2. 
В SDL2 события — это не отдельные типы с фиксированным набором атрибутов, а объединение (union) структур. 
В таблицах для каждой константы указаны соответствующие поля структуры события, к которым можно получить доступ через event.key, event.motion, event.button и т.д.

Системные события и события окна
Константа	                Описание	                                                    Атрибуты (поля структуры)
SDL_QUIT	                Запрос на закрытие приложения	                                нет специфических полей (только type, timestamp)
SDL_APP_TERMINATING	        Приложение завершается ОС (iOS/Android)	                        нет
SDL_APP_LOWMEMORY	        Приложению не хватает памяти	                                нет
SDL_APP_WILLENTERBACKGROUND	Приложение собирается уйти в фон	                            нет
SDL_APP_DIDENTERBACKGROUND	Приложение ушло в фон	                                        нет
SDL_APP_WILLENTERFOREGROUND	Приложение собирается вернуться на передний план	            нет
SDL_APP_DIDENTERFOREGROUND	Приложение снова активно	                                    нет
SDL_LOCALECHANGED	        Изменились локальные настройки пользователя	                    нет
SDL_DISPLAYEVENT	        Изменение состояния дисплея	                                    display, event
SDL_WINDOWEVENT	            Изменение состояния окна (фокус, размер, перемещение и т.п.)	event, data1, data2
SDL_SYSWMEVENT	            Системное событие оконного менеджера	                        msg (указатель на системное сообщение)
SDL_CLIPBOARDUPDATE	        Изменилось содержимое буфера обмена	                            нет
SDL_RENDER_TARGETS_RESET	Цели рендеринга сброшены (нужно обновить содержимое)	        нет
SDL_RENDER_DEVICE_RESET	    Устройство рендеринга сброшено (нужно пересоздать текстуры)	    нет
SDL_SENSORUPDATE	        Обновились данные сенсора	                                    which, data (массив из 6 float)

Клавиатура и текстовый ввод
Константа	Описание	Атрибуты (поля SDL_KeyboardEvent / SDL_TextInputEvent)
SDL_KEYDOWN	Клавиша нажата	windowID, state, repeat, keysym (scancode, sym, mod)
SDL_KEYUP	Клавиша отпущена	windowID, state, keysym (scancode, sym, mod)
SDL_TEXTEDITING	Редактирование текста (IME, композиция)	windowID, text, start, length
SDL_TEXTINPUT	Ввод текста (после завершения IME)	windowID, text
SDL_KEYMAPCHANGED	Раскладка клавиатуры изменилась системой	нет
SDL_TEXTEDITING_EXT	Расширенное редактирование текста (IME)	windowID, text, start, length
sym в SDL_Keysym — это виртуальный код клавиши (аналог key в Pygame), scancode — аппаратный код, mod — модификаторы (Shift, Ctrl, Alt и т.д.).

Мышь
Константа	Описание	Атрибуты (поля соответствующих структур)
SDL_MOUSEMOTION	Перемещение мыши	which, state, x, y, xrel, yrel
SDL_MOUSEBUTTONDOWN	Кнопка мыши нажата	which, button, state, clicks, x, y
SDL_MOUSEBUTTONUP	Кнопка мыши отпущена	which, button, state, clicks, x, y
SDL_MOUSEWHEEL	Прокрутка колеса мыши	which, x, y, direction, preciseX, preciseY, mouseX, mouseY

Джойстик (классический API)
Константа	Описание	Атрибуты (поля структур SDL_Joy*Event)
SDL_JOYAXISMOTION	Движение оси джойстика	which, axis, value (-32768…32767)
SDL_JOYBALLMOTION	Движение трекбола	which, ball, xrel, yrel
SDL_JOYHATMOTION	Изменение POV-переключателя (hat)	which, hat, value (комбинация SDL_HAT_*)
SDL_JOYBUTTONDOWN	Кнопка джойстика нажата	which, button, state (SDL_PRESSED)
SDL_JOYBUTTONUP	Кнопка джойстика отпущена	which, button, state (SDL_RELEASED)
SDL_JOYDEVICEADDED	Джойстик подключён	which (индекс устройства)
SDL_JOYDEVICEREMOVED	Джойстик отключён	which (instance id)
SDL_JOYBATTERYUPDATED	Изменился уровень заряда джойстика	which, level

Контроллеры (Game Controller API, SDL2)
Константа	Описание	Атрибуты
SDL_CONTROLLERAXISMOTION	Движение оси контроллера	which, axis, value (-32768…32767)
SDL_CONTROLLERBUTTONDOWN	Кнопка контроллера нажата	which, button, state (SDL_PRESSED)
SDL_CONTROLLERBUTTONUP	Кнопка контроллера отпущена	which, button, state (SDL_RELEASED)
SDL_CONTROLLERDEVICEADDED	Контроллер подключён	which (индекс устройства)
SDL_CONTROLLERDEVICEREMOVED	Контроллер отключён	which (instance id)
SDL_CONTROLLERDEVICEREMAPPED	Раскладка контроллера обновлена	which (instance id)
SDL_CONTROLLERTOUCHPADDOWN	Тачпад контроллера нажат	which, touchpad, finger, x, y, pressure
SDL_CONTROLLERTOUCHPADMOTION	Палец движется по тачпаду контроллера	which, touchpad, finger, x, y, pressure
SDL_CONTROLLERTOUCHPADUP	Палец отпущен с тачпада контроллера	which, touchpad, finger, x, y, pressure
SDL_CONTROLLERSENSORUPDATE	Обновились данные сенсора контроллера	which, sensor, data (6 float)

Сенсорный ввод и жесты
Константа	Описание	Атрибуты
SDL_FINGERDOWN	Палец коснулся экрана	touchId, fingerId, x, y, dx, dy, pressure, windowID
SDL_FINGERUP	Палец поднят	touchId, fingerId, x, y, dx, dy, pressure, windowID
SDL_FINGERMOTION	Палец движется	touchId, fingerId, x, y, dx, dy, pressure, windowID
SDL_MULTIGESTURE	Мультитач-жест (щипок, вращение)	touchId, dTheta, dDist, x, y, numFingers
SDL_DOLLARGESTURE	Распознан долларовый жест (1-жест)	touchId, gestureId, numFingers, error, x, y
SDL_DOLLARRECORD	Записан долларовый жест	touchId, gestureId, numFingers, error, x, y

Аудиоустройства
Константа	Описание	Атрибуты
SDL_AUDIODEVICEADDED	Аудиоустройство подключено	which (индекс), iscapture (0 — вывод, ≠0 — захват)
SDL_AUDIODEVICEREMOVED	Аудиоустройство отключено	which (SDL_AudioDeviceID), iscapture

Drag and Drop (перетаскивание файлов/текста)
Константа	Описание	Атрибуты (поля SDL_DropEvent)
SDL_DROPBEGIN	Начало перетаскивания	file = NULL, windowID
SDL_DROPFILE	Файл перетащен в окно	file (имя файла, освобождать через SDL_free), windowID
SDL_DROPTEXT	Текст перетащен в окно	file (содержит текст), windowID
SDL_DROPCOMPLETE	Перетаскивание завершено	file = NULL, windowID
MIDI
В стандартном SDL2 (SDL2 core) нет встроенных констант событий MIDIIN/MIDIOUT в SDL_EventType. Работа с MIDI обычно выносится в отдельные библиотеки (например, SDL_mixer для проигрывания MIDI-файлов или сторонние MIDI-бэкенды). Если MIDI-события всё же доставляются через SDL, они будут приходить как пользовательские события (SDL_USEREVENT + смещение) или через отдельный механизм.

Пользовательские события
Константа	Описание
SDL_USEREVENT	Первый номер для пользовательских событий (значение 0x8000)
SDL_LASTEVENT	Верхняя граница зарезервированных типов (0xFFFF); пользовательские события должны быть меньше этого значения
Диапазон пользовательских событий: от SDL_USEREVENT (0x8000) до SDL_LASTEVENT - 1 (0xFFFE).
Регистрация: используйте SDL_RegisterEvents(int numevents) — функция выделяет уникальный диапазон и возвращает начальный номер (или (Uint32)-1 при нехватке).

Структура SDL_UserEvent содержит поля: type, timestamp, windowID, code, data1, data2.

Служебные константы
Константа	Описание
SDL_FIRSTEVENT	Значение 0, не используется (не удалять)
SDL_POLLSENTINEL	Сигнализирует о конце цикла опроса событий (0x7F00)
SDL_LASTEVENT	Последний зарезервированный тип (0xFFFF), используется для границ массивов

В SDL2, в отличие от Pygame, одному типу события может соответствовать несколько полей в union-структуре SDL_Event. 
Доступ к ним осуществляется через соответствующий член union: event.key, event.motion, event.button, event.wheel, event.jaxis, event.caxis, event.tfinger, event.mgesture, event.adevice, event.drop, event.user и т.д..



Атрибут	Структура	Тип(ы) события	Поля (имя: тип)	Краткое описание
type	Uint32	всегда	type: Uint32	Номер типа события. Сравнивайте с SDL_* константами.
common	SDL_CommonEvent	всегда (общие поля)	timestamp: Uint32	Метка времени в мс с момента SDL_Init. Используется для таймингов, замеров.
display	SDL_DisplayEvent	SDL_DISPLAYEVENT	display: Uint32, event: Uint8, data1: Sint32	Изменение дисплея: подключение/отключение, смена ориентации/DPI. event — подтип (SDL_DISPLAYEVENT_*).
window	SDL_WindowEvent	SDL_WINDOWEVENT	windowID: Uint32, event: Uint8, data1: Sint32, data2: Sint32	Изменение окна: перемещение, размер, фокус, видимость. event — подтип (SDL_WINDOWEVENT_*); data1/data2 зависят от подтипа (например, новая ширина/высота).
key	SDL_KeyboardEvent	SDL_KEYDOWN, SDL_KEYUP	windowID: Uint32, state: Uint8, repeat: Uint8, keysym: SDL_Keysym (scancode: SDL_Scancode, sym: SDL_Keycode, mod: Uint16)	Нажатие/отпускание клавиши. scancode — физическая клавиша (не зависит от раскладки), sym — виртуальный код, mod — модификаторы (Shift/Ctrl/Alt), repeat — автоповтор.
edit	SDL_TextEditingEvent	SDL_TEXTEDITING	windowID: Uint32, text: char[32], start: Sint32, length: Sint32	Промежуточный ввод через IME (композиция). text — текущая строка, start/length — выделенный фрагмент для отрисовки подсказки.
editExt	SDL_TextEditingExtEvent	SDL_TEXTEDITING_EXT	windowID: Uint32, text: char*, start: Sint32, length: Sint32	То же, что edit, но text — указатель на динамическую строку (для длинных IME-композиций). Освобождать через SDL_free.
text	SDL_TextInputEvent	SDL_TEXTINPUT	windowID: Uint32, text: char[32]	Готовый текст после завершения IME/нажатия клавиши. Используйте для текстовых полей ввода.
motion	SDL_MouseMotionEvent	SDL_MOUSEMOTION	which: Uint32, state: Uint32, x: Sint32, y: Sint32, xrel: Sint32, yrel: Sint32	Движение мыши. x,y — абсолютные координаты в окне; xrel,yrel — относительное смещение (для FPS-камеры); state — битовая маска нажатых кнопок.
button	SDL_MouseButtonEvent	SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP	which: Uint32, button: Uint8, state: Uint8, clicks: Uint8, x: Sint32, y: Sint32	Клик/отпускание кнопки мыши. button — SDL_BUTTON_LEFT/RIGHT/MIDDLE; clicks — число кликов (2 = двойной); x,y — координаты клика.
wheel	SDL_MouseWheelEvent	SDL_MOUSEWHEEL	which: Uint32, x: Sint32, y: Sint32, direction: Uint32, preciseX: float, preciseY: float, mouseX: Sint32, mouseY: Sint32	Прокрутка колеса/тачпада. y — вертикаль (+вверх), x — горизонталь; direction — SDL_MOUSEWHEEL_NORMAL/FLIPPED; precise* — плавные значения; mouse* — позиция курсора.
jaxis	SDL_JoyAxisEvent	SDL_JOYAXISMOTION	which: SDL_JoystickID, axis: Uint8, value: Sint16	Движение оси джойстика. value ∈ [-32768, 32767], axis — индекс оси.
jball	SDL_JoyBallEvent	SDL_JOYBALLMOTION	which: SDL_JoystickID, ball: Uint8, xrel: Sint16, yrel: Sint16	Движение трекбола. xrel,yrel — относительное смещение.
jhat	SDL_JoyHatEvent	SDL_JOYHATMOTION	which: SDL_JoystickID, hat: Uint8, value: Uint8	Движение POV-«шляпки». value — комбинация SDL_HAT_UP/DOWN/LEFT/RIGHT/CENTERED.
jbutton	SDL_JoyButtonEvent	SDL_JOYBUTTONDOWN, SDL_JOYBUTTONUP	which: SDL_JoystickID, button: Uint8, state: Uint8	Нажатие/отпускание кнопки джойстика. state — SDL_PRESSED/SDL_RELEASED.
jdevice	SDL_JoyDeviceEvent	SDL_JOYDEVICEADDED, SDL_JOYDEVICEREMOVED	which: Sint32	Подключение/отключение джойстика. ADDED → индекс; REMOVED → instance id.
jbattery	SDL_JoyBatteryEvent	SDL_JOYBATTERYUPDATED	which: SDL_JoystickID, level: SDL_JoystickPowerLevel	Изменение заряда джойстика. level — SDL_JOYSTICK_POWER_* (UNKNOWN/EMPTY/LOW/MEDIUM/FULL/WIRED).
caxis	SDL_ControllerAxisEvent	SDL_CONTROLLERAXISMOTION	which: SDL_JoystickID, axis: Uint8, value: Sint16	Ось геймпада. axis — SDL_CONTROLLER_AXIS_* (LEFTX, TRIGGERRIGHT и т.д.).
cbutton	SDL_ControllerButtonEvent	SDL_CONTROLLERBUTTONDOWN, SDL_CONTROLLERBUTTONUP	which: SDL_JoystickID, button: Uint8, state: Uint8	Кнопка геймпада. button — SDL_CONTROLLER_BUTTON_* (A, B, X, Y и т.д.).
cdevice	SDL_ControllerDeviceEvent 	SDL_CONTROLLERDEVICEADDED/REMOVED/REMAPPED	which: Sint32	Подключение/отключение/перепривязка геймпада.
ctouchpad	SDL_ControllerTouchpadEvent	SDL_CONTROLLERTOUCHPADDOWN/MOTION/UP	which: SDL_JoystickID, touchpad: Sint32, finger: Sint32, x: float, y: float, pressure: float	Тачпад геймпада (DualShock 4). Координаты нормализованы 0…1.
csensor	SDL_ControllerSensorEvent	SDL_CONTROLLERSENSORUPDATE	which: SDL_JoystickID, sensor: Sint32, data: float[3]	Данные сенсора геймпада (акселерометр, гироскоп). data — 3 значения.
sensor	SDL_SensorEvent	SDL_SENSORUPDATE	which: Sint32, data: float[6]	Данные аппаратного сенсора устройства (телефон/планшет). data — до 6 значений.
quit	SDL_QuitEvent	SDL_QUIT	(нет специфических полей)	Запрос на закрытие приложения (крестик, Alt+F4, SIGTERM). Завершайте главный цикл.
user	SDL_UserEvent	SDL_USEREVENT…SDL_LASTEVENT-1	windowID: Uint32, code: Sint32, data1: void*, data2: void*	Пользовательское событие (создаёте сами). code — ваш код типа; data1/data2 — указатели на данные.
syswm	SDL_SysWMEvent	SDL_SYSWMEVENT	msg: SDL_SysWMmsg*	Сырое сообщение оконной системы (WM_* в Windows, XEvent в X11). Для низкоуровневой интеграции.
tfinger	SDL_TouchFingerEvent	SDL_FINGERDOWN, SDL_FINGERUP, SDL_FINGERMOTION	touchId: SDL_TouchID, fingerId: SDL_FingerID, x: float, y: float, dx: float, dy: float, pressure: float, windowID: Uint32	Касание/движение пальца. x,y,dx,dy,pressure нормализованы 0…1. fingerId — конкретный палец (мультитач).
mgesture	SDL_MultiGestureEvent	SDL_MULTIGESTURE	touchId: SDL_TouchID, dTheta: float, dDist: float, x: float, y: float, numFingers: Uint16	Мультитач-жест (щипок, вращение). dTheta — поворот, dDist — изменение расстояния (zoom).
dgesture	SDL_DollarGestureEvent	SDL_DOLLARGESTURE, SDL_DOLLARRECORD	touchId: SDL_TouchID, gestureId: SDL_GestureID, numFingers: Uint32, error: float, x: float, y: float	Шаблонный жест (буква/фигура). gestureId — id шаблона; error — точность распознавания (меньше = точнее).
drop	SDL_DropEvent	SDL_DROPBEGIN, SDL_DROPFILE, SDL_DROPTEXT, SDL_DROPCOMPLETE	file: char*, windowID: Uint32	Drag&drop. Для DROPFILE — путь к файлу (освобождать SDL_free), для DROPTEXT — сам текст, для BEGIN/COMPLETE — NULL.
adevice	SDL_AudioDeviceEvent	SDL_AUDIODEVICEADDED, SDL_AUDIODEVICEREMOVED	which: Uint32, iscapture: Uint8	Аудиоустройство подключено/отключено. which — индекс (ADDED) или SDL_AudioDeviceID (REMOVED); iscapture ≠ 0 — микрофон/захват.
padding	—	—	—	Служебное поле для выравнивания union. Не использовать.

"""

from sdl2.events import (
    SDL_QUIT as QUIT,
    SDL_APP_TERMINATING as APP_TERMINATING,
    SDL_APP_LOWMEMORY as APP_LOWMEMORY,
    SDL_APP_WILLENTERBACKGROUND as APP_WILLENTERBACKGROUND,
    SDL_APP_DIDENTERBACKGROUND as APP_DIDENTERBACKGROUND,
    SDL_APP_WILLENTERFOREGROUND as APP_WILLENTERFOREGROUND,
    SDL_APP_DIDENTERFOREGROUND as APP_DIDENTERFOREGROUND,
    SDL_LOCALECHANGED as LOCALECHANGED,
    SDL_DISPLAYEVENT as DISPLAYEVENT,
    SDL_WINDOWEVENT as WINDOWEVENT,
    SDL_SYSWMEVENT as SYSWMEVENT,
    SDL_CLIPBOARDUPDATE as CLIPBOARDUPDATE,
    SDL_RENDER_TARGETS_RESET as RENDER_TARGETS_RESET,
    SDL_RENDER_DEVICE_RESET as RENDER_DEVICE_RESET,
    SDL_SENSORUPDATE as SENSORUPDATE,

    SDL_KEYDOWN as KEYDOWN,
    SDL_KEYUP as KEYUP,
    SDL_TEXTEDITING as TEXTEDITING,
    SDL_TEXTINPUT as TEXTINPUT,
    SDL_KEYMAPCHANGED as KEYMAPCHANGED,
    SDL_TEXTEDITING_EXT as TEXTEDITING_EXT,

    SDL_MOUSEMOTION as MOUSEMOTION,
    SDL_MOUSEBUTTONDOWN as MOUSEBUTTONDOWN,
    SDL_MOUSEBUTTONUP as MOUSEBUTTONUP,
    SDL_MOUSEWHEEL as MOUSEWHEEL,

    SDL_JOYAXISMOTION as JOYAXISMOTION,
    SDL_JOYBALLMOTION as JOYBALLMOTION,
    SDL_JOYHATMOTION as JOYHATMOTION,
    SDL_JOYBUTTONDOWN as JOYBUTTONDOWN,
    SDL_JOYBUTTONUP as JOYBUTTONUP,
    SDL_JOYDEVICEADDED as JOYDEVICEADDED,
    SDL_JOYDEVICEREMOVED as JOYDEVICEREMOVED,
    SDL_JOYBATTERYUPDATED as JOYBATTERYUPDATED,

    SDL_CONTROLLERAXISMOTION as CONTROLLERAXISMOTION,
    SDL_CONTROLLERBUTTONDOWN as CONTROLLERBUTTONDOWN,
    SDL_CONTROLLERBUTTONUP as CONTROLLERBUTTONUP,
    SDL_CONTROLLERDEVICEADDED as CONTROLLERDEVICEADDED,
    SDL_CONTROLLERDEVICEREMOVED	as CONTROLLERDEVICEREMOVED,
    SDL_CONTROLLERDEVICEREMAPPED as CONTROLLERDEVICEREMAPPED,
    SDL_CONTROLLERTOUCHPADDOWN as CONTROLLERTOUCHPADDOWN,
    SDL_CONTROLLERTOUCHPADMOTION as CONTROLLERTOUCHPADMOTION,
    SDL_CONTROLLERTOUCHPADUP as CONTROLLERTOUCHPADUP,
    SDL_CONTROLLERSENSORUPDATE as CONTROLLERSENSORUPDATE,

    SDL_FINGERDOWN as FINGERDOWN,
    SDL_FINGERUP as FINGERUP,
    SDL_FINGERMOTION as FINGERMOTION,
    SDL_MULTIGESTURE as MULTIGESTURE,
    SDL_DOLLARGESTURE as DOLLARGESTURE,
    SDL_DOLLARRECORD as DOLLARRECORD,

    SDL_AUDIODEVICEADDED as AUDIODEVICEADDED,
    SDL_AUDIODEVICEREMOVED as AUDIODEVICEREMOVED,

    SDL_DROPBEGIN as DROPBEGIN,
    SDL_DROPFILE as DROPFILE,
    SDL_DROPTEXT as DROPTEXT,
    SDL_DROPCOMPLETE as DROPCOMPLETE,

    SDL_USEREVENT as USEREVENT,
    SDL_LASTEVENT as LASTEVENT,

    SDL_FIRSTEVENT as FIRSTEVENT,
    SDL_POLLSENTINEL as POLLSENTINEL,

    Uint8 as uint8,
    Uint16 as uint16,
    Uint32 as uint32,

    Sint32 as sint32,
    Sint16 as sint16,

    SDL_CommonEvent as CommonEvent,
    SDL_DisplayEvent as DisplayEvent,
    SDL_WindowEvent	as WindowEvent,    
    SDL_KeyboardEvent as KeyboardEvent,   
    SDL_TextEditingEvent as TextEditingEvent,   
    SDL_TextEditingExtEvent as TextEditingExtEvent,
    SDL_TextInputEvent as TextInputEvent,
    SDL_MouseMotionEvent as MouseMotionEvent,  
    SDL_MouseButtonEvent as MouseButtonEvent,  
    SDL_MouseWheelEvent	as MouseWheelEvent,
    SDL_JoyAxisEvent as JoyAxisEvent,
    SDL_JoyBallEvent as JoyBallEvent,
    SDL_JoyHatEvent	as JoyHatEvent, 
    SDL_JoyButtonEvent as JoyButtonEvent,
    SDL_JoyDeviceEvent as JoyDeviceEvent,
    SDL_JoyBatteryEvent	as JoyBatteryEvent,
    SDL_ControllerAxisEvent	as ControllerAxisEvent,
    SDL_ControllerButtonEvent as ControllerButtonEvent,
    SDL_ControllerDeviceEvent as ControllerDeviceEvent,
    SDL_ControllerTouchpadEvent	as ControllerTouchpadEvent,
    SDL_ControllerSensorEvent as ControllerSensorEvent,
    SDL_SensorEvent	as SensorEvent,
    SDL_QuitEvent as QuitEvent,
    SDL_UserEvent as UserEvent,
    SDL_SysWMEvent as SysWMEvent,
    SDL_TouchFingerEvent as TouchFingerEvent,
    SDL_MultiGestureEvent as MultiGestureEvent,
    SDL_DollarGestureEvent as DollarGestureEvent,
    SDL_DropEvent as DropEvent,
    SDL_AudioDeviceEvent as AudioDeviceEvent,

    SDL_Event as Event,

    SDL_EventState,
    SDL_MOUSEMOTION,
    SDL_IGNORE,
    SDL_ENABLE,
    SDL_QUERY,
    SDL_FlushEvents,
    SDL_FIRSTEVENT,
    SDL_LASTEVENT,
    SDL_PushEvent,
)

from sdl2.video import SDL_SetWindowGrab, SDL_GetWindowGrab
from sdl2.stdinc import SDL_TRUE, SDL_FALSE
from sdl2.ext import get_events as get

sint64 = int
sint8 = int

from sdl2.keyboard import SDL_Keysym, SDL_Scancode, SDL_Keycode
from sdl2.joystick import SDL_JoystickID, SDL_JoystickPowerLevel
from sdl2.syswm import SDL_SysWMmsg
from sdl2.touch import SDL_TouchID, SDL_FingerID
from sdl2.gesture import SDL_GestureID

EVENT_NAMES = {
    QUIT: "QUIT",
    APP_TERMINATING: "APP_TERMINATING",
    APP_LOWMEMORY: "APP_LOWMEMORY",
    APP_WILLENTERBACKGROUND: "APP_WILLENTERBACKGROUND",
    APP_DIDENTERBACKGROUND: "APP_DIDENTERBACKGROUND",
    APP_WILLENTERFOREGROUND: "APP_WILLENTERFOREGROUND",
    APP_DIDENTERFOREGROUND: "APP_DIDENTERFOREGROUND",
    LOCALECHANGED: "LOCALECHANGED",
    DISPLAYEVENT: "DISPLAYEVENT",
    WINDOWEVENT: "WINDOWEVENT",
    SYSWMEVENT: "SYSWMEVENT",
    CLIPBOARDUPDATE: "CLIPBOARDUPDATE",
    RENDER_TARGETS_RESET: "RENDER_TARGETS_RESET",
    RENDER_DEVICE_RESET: "RENDER_DEVICE_RESET",
    SENSORUPDATE: "SENSORUPDATE",

    KEYDOWN: "KEYDOWN",
    KEYUP: "KEYUP",
    TEXTEDITING: "TEXTEDITING",
    TEXTINPUT: "TEXTINPUT",
    KEYMAPCHANGED: "KEYMAPCHANGED",
    TEXTEDITING_EXT: "TEXTEDITING_EXT",

    MOUSEMOTION: "MOUSEMOTION",
    MOUSEBUTTONDOWN: "MOUSEBUTTONDOWN",
    MOUSEBUTTONUP: "MOUSEBUTTONUP",
    MOUSEWHEEL: "MOUSEWHEEL",

    JOYAXISMOTION: "JOYAXISMOTION",
    JOYBALLMOTION: "JOYBALLMOTION",
    JOYHATMOTION: "JOYHATMOTION",
    JOYBUTTONDOWN: "JOYBUTTONDOWN",
    JOYBUTTONUP: "JOYBUTTONUP",
    JOYDEVICEADDED: "JOYDEVICEADDED",
    JOYDEVICEREMOVED: "JOYDEVICEREMOVED",
    JOYBATTERYUPDATED: "JOYBATTERYUPDATED",

    CONTROLLERAXISMOTION: "CONTROLLERAXISMOTION",
    CONTROLLERBUTTONDOWN: "CONTROLLERBUTTONDOWN",
    CONTROLLERBUTTONUP: "CONTROLLERBUTTONUP",
    CONTROLLERDEVICEADDED: "CONTROLLERDEVICEADDED",
    CONTROLLERDEVICEREMOVED: "CONTROLLERDEVICEREMOVED",
    CONTROLLERDEVICEREMAPPED: "CONTROLLERDEVICEREMAPPED",
    CONTROLLERTOUCHPADDOWN: "CONTROLLERTOUCHPADDOWN",
    CONTROLLERTOUCHPADMOTION: "CONTROLLERTOUCHPADMOTION",
    CONTROLLERTOUCHPADUP: "CONTROLLERTOUCHPADUP",
    CONTROLLERSENSORUPDATE: "CONTROLLERSENSORUPDATE",

    FINGERDOWN: "FINGERDOWN",
    FINGERUP: "FINGERUP",
    FINGERMOTION: "FINGERMOTION",
    MULTIGESTURE: "MULTIGESTURE",
    DOLLARGESTURE: "DOLLARGESTURE",
    DOLLARRECORD: "DOLLARRECORD",

    AUDIODEVICEADDED: "AUDIODEVICEADDED",
    AUDIODEVICEREMOVED: "AUDIODEVICEREMOVED",

    DROPBEGIN: "DROPBEGIN",
    DROPFILE: "DROPFILE",
    DROPTEXT: "DROPTEXT",
    DROPCOMPLETE: "DROPCOMPLETE",

}

def clear() -> None:
    SDL_FlushEvents(SDL_FIRSTEVENT, SDL_LASTEVENT)

def set_blocked(*types):
    """Аналог pygame.event.set_blocked(). Без аргументов — блокирует всё."""
    if not types:
        for t in range(SDL_FIRSTEVENT, SDL_LASTEVENT + 1):
            SDL_EventState(t, SDL_IGNORE)
    else:
        for t in types:
            SDL_EventState(t, SDL_IGNORE)

def set_allowed(*types):
    """Аналог pygame.event.set_allowed(). Без аргументов — разрешает всё."""
    if not types:
        for t in range(SDL_FIRSTEVENT, SDL_LASTEVENT + 1):
            SDL_EventState(t, SDL_ENABLE)
    else:
        for t in types:
            SDL_EventState(t, SDL_ENABLE)

def get_blocked():
    """Аналог pygame.event.get_blocked(). Список заблокированных типов."""
    result = []
    for t in range(SDL_FIRSTEVENT, SDL_LASTEVENT + 1):
        if SDL_EventState(t, SDL_QUERY) == SDL_IGNORE:
            result.append(t)
    return result

def post(event):
    """Аналог pygame.event.post(). Положить событие в очередь.

    Возвращает True при успехе.
    """
    return SDL_PushEvent(event) >= 0

def set_grab(win, enable):
    """Аналог pygame.event.set_grab(). Требует set_window()."""
    if win is None:
        raise RuntimeError("Сначала вызови set_window(window)")
    SDL_SetWindowGrab(win, SDL_TRUE if enable else SDL_FALSE)


def get_grab(win):
    """Аналог pygame.event.get_grab(). Требует set_window()."""
    if win is None:
        raise RuntimeError("Сначала вызови set_window(window)")
    return SDL_GetWindowGrab(win) == SDL_TRUE

def event_add(type: int, name: str) -> None:
    "добавляет новый эвент в таблицу"
    if USEREVENT < type < LASTEVENT and (not type in EVENT_NAMES):
        EVENT_NAMES[type] = name
    else:
        raise ValueError("Event уже существует")

def event_name(type: int) -> str | None:
    "возвращает имя эвента"
    return EVENT_NAMES.get(type)

def event_type(name: str) -> int | None:
    "получает тип эвента по имени"
    return next((key for key, value in EVENT_NAMES.items() if value == name), None)
