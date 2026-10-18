"""
Ниже — структурированный справочник по событиям SDL2 в том же формате, что и ваш пример с Pygame. В SDL2 события — это не отдельные типы с фиксированным набором атрибутов, а объединение (union) структур. В таблицах для каждой константы указаны соответствующие поля структуры события, к которым можно получить доступ через event.key, event.motion, event.button и т.д.

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
В SDL2, в отличие от Pygame, одному типу события может соответствовать несколько полей в union-структуре SDL_Event. Доступ к ним осуществляется через соответствующий член union: event.key, event.motion, event.button, event.wheel, event.jaxis, event.caxis, event.tfinger, event.mgesture, event.adevice, event.drop, event.user и т.д..
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
    SDL_LASTEVENT as LASTEVENT

)

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

def event_add(type: int, name: str) -> None:
    "добавляет новый эвент в таблицу"
    if USEREVENT < type < LASTEVENT and (not type in EVENT_NAMES):
        EVENT_NAMES[type] = name
    else:
        raise ValueError("Event уже существует")

def event_name(type: int) -> str | None:
    "возвращает имя эвента"
    return EVENT_NAMES.get(type)

def event_type(name: str) -> int:
    "получает тип эвента по имени"
    return next((key for key, value in EVENT_NAMES.items() if value == name), None)