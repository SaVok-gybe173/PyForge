"""
Системные события и события окна:
    Константа	            Описание	                                                                    Атрибуты
    QUIT	                Запрос на закрытие окна (нажатие на крестик)	                                нет
    ACTIVEEVENT	            Окно получило/потеряло фокус или видимость	                                    gain, state
    VIDEORESIZE	            Изменение размера окна	                                                        w, h, size
    VIDEOEXPOSE	            Окно было перекрыто и снова показано	                                        нет
    RENDER_TARGETS_RESET    Сброс целей рендеринга (обычно после изменения окна)	                        нет
Клавиатура и текстовый ввод:
    Константа	Описание	                        Атрибуты
    KEYDOWN	    Клавиша нажата	                    key, mod, unicode, scancode
    KEYUP	    Клавиша отпущена	                key, mod, scancode
    TEXTEDITING	Редактирование текста (IME)	        text, start, length
    TEXTINPUT	Ввод текста (после завершения IME)	text
Мышь:
    Константа	    Описание	            Атрибуты
    MOUSEMOTION	    Перемещение мыши	    pos, rel, buttons, touch
    MOUSEBUTTONDOWN	Кнопка мыши нажата	    pos, button, touch
    MOUSEBUTTONUP	Кнопка мыши отпущена	pos, button, touch
    MOUSEWHEEL	    Прокрутка колеса мыши	x, y, flipped, which, precise_x, precise_y
Джойстик (классический API):
    Константа	    Описание	                Атрибуты
    JOYAXISMOTION	Движение оси джойстика	    joy, axis, value
    JOYBALLMOTION	Движение трекбола	        joy, ball, rel
    JOYHATMOTION	Изменение POV-переключателя	joy, hat, value
    JOYBUTTONDOWN	Кнопка джойстика нажата	    joy, button
    JOYBUTTONUP	    Кнопка джойстика отпущена	joy, button
Контроллеры (SDL2, Pygame 2):
    Константа	                Описание	                    Атрибуты
    CONTROLLERAXISMOTION	    Движение оси контроллера	    joy, axis, value
    CONTROLLERBUTTONDOWN	    Кнопка контроллера нажата	    joy, button
    CONTROLLERBUTTONUP	        Кнопка контроллера отпущена     joy, button
    CONTROLLERDEVICEADDED	    Контроллер подключён	        device_index
    CONTROLLERDEVICEREMOVED	    Контроллер отключён	            device_index
    CONTROLLERDEVICEREMAPPED	Раскладка контроллера обновлена	device_index
Сенсорный ввод и жесты:
    Константа	    Описание	                    Атрибуты
    FINGERDOWN	    Палец прикоснулся к экрану	    finger_id, x, y, pressure
    FINGERUP	    Палец поднят	                finger_id, x, y
    FINGERMOTION	Палец движется	                finger_id, x, y, dx, dy, pressure
    MULTIGESTURE	Мультитач-жест (щипок и т.п.)	touchId, x, y, pinched, rotated, numFingers
Аудиоустройства:
    Константа	Описание	Атрибуты
    AUDIODEVICEADDED	Аудиоустройство подключено	which, iscapture
    AUDIODEVICEREMOVED	Аудиоустройство отключено	which, iscapture
Drag and Drop (перетаскивание файлов/текста):
    Константа	    Описание	                Атрибуты
    DROPBEGIN	    Начало перетаскивания	    нет
    DROPCOMPLETE	Перетаскивание завершено	нет
    DROPFILE	    Файл перетащен в окно	    file
    DROPTEXT	    Текст перетащен в окно	    text
MIDI:
    Константа	Описание	            Атрибуты
    MIDIIN	    Получены данные MIDI	data, timestamp
    MIDIOUT	    Данные MIDI отправлены	data, timestamp
Пользовательские события
    Константа	Описание
    USEREVENT	Первый номер, с которого можно создавать свои типы. Например: MY_EVENT = pygame.USEREVENT + 1
Служебные константы
    Константа	Описание
    NOEVENT	    Значение 0, используется как "нет события"
    NUMEVENTS	Количество зарезервированных типов (последний индекс + 1). Все пользовательские события должны быть меньше этого числа

Диапазон пользовательских событий: от USEREVENT до NUMEVENTS - 1.
Чтобы избежать конфликтов, рекомендуется использовать pygame.event.custom_type() (Pygame 2) для выделения уникальных номеров.    
"""

from .scene import Scene