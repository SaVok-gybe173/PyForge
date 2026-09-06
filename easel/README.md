
# Easel — модуль для создания оконных приложений на Pygame

**Easel** — это часть фреймворка PyForge, предоставляющая удобную объектно-ориентированную надстройку над `pygame-ce` для создания оконных приложений с поддержкой сцен, событий и модульной архитектуры.

## Возможности

- 🪟 **Управление окнами** — создание и настройка главного окна приложения
    
- 🎬 **Система сцен** — гибкая архитектура для организации разных экранов приложения
    
- 🖱️ **Полная обработка событий** — клавиатура, мышь, изменение размера окна и системные события
    
- 📦 **Поддержка модов** — динамическая загрузка плагинов из папки `mods`
    
- 🔄 **Многопроцессность** — создание дополнительных окон в отдельных процессах (кроме Android/iOS)
    
- 🪟 **Прозрачность окна** — только для Windows (через `pywin32`)
    
- 📱 **Кроссплатформенность** — определение Android, Linux, Windows, macOS, iOS
    
- 🎨 **OpenGL** — встроенная поддержка инициализации OpenGL
    

---

## Установка

```bash
pip install pygame-ce
```
# Для прозрачности окон на Windows:
```bash
pip install pywin32
```

Модуль является частью PyForge, поэтому импорт выглядит так:

```python

from PyForge.easel import Window, Scene, App, set_window_transparency
```
---

## Быстрый старт

### Минимальное приложение

```python

from PyForge.easel import Window, Scene
import pygame as pg
class MainScene(Scene):
    def draw(self, win: pg.Surface):
        win.fill((100, 150, 200))  # заливка фона
    def event(self, event: pg.event.Event):
        if event.type == pg.QUIT:
            self.page.running = False
# Создаём окно размером 800x600 со сценой MainScene
app = Window(size=(800, 600), scene=[MainScene])
app.start()
```

### Приложение со множеством сцен

```python

from PyForge.easel import Window, Scene
import pygame as pg
class MenuScene(Scene):
    def draw(self, win: pg.Surface):
        win.fill((50, 50, 50))
        # отрисовка меню...
    def keydown(self, key: int, mod: int, unicode: str, scancode: int):
        if key == pg.K_SPACE:
            # переключение на игровую сцену
            self.page.condition = 1  # индекс GameScene
class GameScene(Scene):
    def draw(self, win: pg.Surface):
        win.fill((30, 80, 30))
        # отрисовка игры...
    def keydown(self, key: int, mod: int, unicode: str, scancode: int):
        if key == pg.K_ESCAPE:
            self.page.condition = 0  # возврат в меню
app = Window(size=(800, 600), scene=[MenuScene, GameScene])
app.start()
```

### Приложение с модами

```python

from PyForge.easel import App
# App наследуется от Window и автоматически загружает моды из папки mods
app = App(size=(1024, 768), mods_dir="./my_mods")
app.start()
```

Структура мода (`mods/my_mod.py`):

```python

from PyForge.mods.mod import FrameMod
class Main(FrameMod):
    def start(self):
        print("Мод загружен!")
    def draw(self, win):
        # отрисовка поверх основного окна
        pass
    def event(self, event):
        # обработка событий
        pass
    def close(self):
        print("Мод выгружается")
```

### Создание второго окна (отдельный процесс)

```python

from PyForge.easel.window_processing import Window as ProcessWindow
from PyForge.easel import Scene
class SecondScene(Scene):
    def draw(self, win):
        win.fill((200, 100, 100))
# Создаём окно в отдельном процессе
win2 = ProcessWindow(size=(400, 300), scene=[SecondScene])
win2.start()  # запуск в новом процессе
win2.join()   # ожидание завершения
```

### Прозрачность окна (только Windows)

```python

from PyForge.easel import set_window_transparency
import pygame as pg
pg.display.set_mode((400, 300))
# Устанавливаем прозрачность 50% (alpha 0-255)
set_window_transparency(alpha_value=128)
```

---

## Справочник API

### Модуль `__init__.py`

Экспортирует основные классы и функции:

|Имя|Описание|
|---|---|
|`Scene`|Базовый класс для всех сцен|
|`Window`|Главный класс управления окном|
|`App`|Класс приложения с поддержкой модов (наследует `Window`)|
|`WindowProcession`|Класс для создания окон в отдельных процессах|
|`EVENTS_METOD`|Словарь соответствия типов событий и методов сцены|
|`is_android()`|Проверка: запущено ли на Android|
|`is_linux()`|Проверка: запущено ли на Linux|
|`is_macos()`|Проверка: запущено ли на macOS|
|`is_ios()`|Проверка: запущено ли на iOS|
|`is_window()`|Проверка: запущено ли на Windows|
|`set_window_transparency()`|Установка прозрачности окна (только Windows)|

---

### Класс `Scene` (`scene.py`)

Базовый класс для всех сцен приложения.

**Атрибуты:**

- `name: str` — имя сцены (по умолчанию — имя класса)
    
- `page: Window` — ссылка на родительское окно
    

**Методы:**

|Метод|Описание|
|---|---|
|`draw(win: pg.Surface)`|Отрисовка объектов. Вызывается каждый кадр|
|`update(dt: float)`|Обновление логики. `dt` — время в секундах с прошлого кадра|
|`event(event: pg.event.Event)`|Обработка событий Pygame|
|`size_update(old, new, ratio)`|Изменение размера окна|
|`muve_window(old, new)`|Перемещение окна (pygame-ce)|
|`close()`|Закрытие окна (событие `QUIT`)|
|`activeevent(gain, state)`|Изменение фокуса окна|
|`videoresize(size, w, h)`|Изменение размера (событие `VIDEORESIZE`)|
|`videoexpose()`|Окно было перекрыто и снова показано|
|`render_targets_reset()`|Сброс целей рендеринга (pygame 2.x)|
|`keydown(key, mod, unicode, scancode)`|Нажатие клавиши|
|`keyup(key, mod, scancode)`|Отпускание клавиши|
|`textediting(text, start, length)`|Редактирование текста (IME)|
|`textinput(text)`|Ввод текста|
|`mousemotion(pos, rel, buttons, touch)`|Движение мыши|
|`mousedown(pos, button, touch)`|Нажатие кнопки мыши|
|`mouseup(pos, button, touch)`|Отпускание кнопки мыши|
|`mousewheel(x, y, flipped, which, precise_x, precise_y)`|Прокрутка колеса|

---

### Класс `Window` (`window.py`)

Главный класс управления окном.

**Конструктор:**

python

Window(size=(400, 300),
       color=(255, 255, 255),
       scene: list[Scene] | None = None,
       *,
       fps: int | float = 60,
       kwargs_set_mode: KwargsSetMode | None = None)

|Параметр|Описание|
|---|---|
|`size`|Размеры окна `(width, height)`|
|`color`|Цвет фона `(R, G, B)`|
|`scene`|Список классов сцен (наследников `Scene`)|
|`fps`|Кадров в секунду|
|`kwargs_set_mode`|Дополнительные параметры для `pg.display.set_mode()`: `flags`, `depth`, `display`, `vsync`|

**Методы:**

|Метод|Описание|
|---|---|
|`addScene(*scene: T)`|Добавляет сцены в список|
|`setIcon(icon, permission=(32,32))`|Устанавливает иконку окна|
|`setCaption(caption)`|Устанавливает заголовок окна|
|`init(win: pg.Surface)`|Инициализация (вызывается при старте)|
|`initOpenGL()`|Инициализация OpenGL|
|`run_window()`|Главный цикл приложения|
|`start_scenes()`|Инициализация всех сцен|
|`eventManager(event)`|Управление событиями сцен|
|`size_update(old, new, ratio)`|Обновление размера для всех сцен|
|`start()`|Запуск окна|
|`update_window()`|Обновление параметров окна|

---

### Класс `App` (`object.py`)

Наследует `Window` и добавляет поддержку модов.

**Конструктор:**

```python

App(size=(400, 300),
    color=(255, 255, 255),
    scene: list[T] | None = None,
    *,
    fps: int = 60,
    mods_dir: str | None = None,
    kwargs_set_mode: KwargsSetMode | None = None)
```

|Параметр|Описание|
|---|---|
|`mods_dir`|Путь к папке с модами (по умолчанию `./mods`)|

**Дополнительные методы:**

- `load_mods()` — загружает все модули из папки `mods_dir`
    
- Автоматически вызывает методы `start()`, `draw()`, `event()`, `close()` у загруженных модов
    

**Структура мода:**  
Мод — это Python-файл в папке `mods`, содержащий класс `Main`, наследующий `FrameMod` из `PyForge.mods.mod`.

---

### Класс `WindowProcession` (`window_processing.py`)

Класс для создания окон в отдельных процессах. **Недоступен на Android и iOS.**

**Особенности:**

- Создаёт новый процесс с изолированной памятью
    
- Для обмена данными используйте `multiprocessing.Queue`
    
- Не передавайте кастомные классы между процессами — используйте JSON или простые структуры
    

**Методы:**

|Метод|Описание|
|---|---|
|`start()`|Запускает окно в новом процессе|
|`is_alive()`|Проверяет, активен ли процесс|
|`join(timeout=None)`|Ожидает завершения процесса|
|`kill()`|Принудительно завершает процесс|

**Пример с очередью:**

```python

from multiprocessing import Process, Queue
def worker(q):
    q.put("Сообщение из процесса")
q = Queue()
p = Process(target=worker, args=(q,))
p.start()
print(q.get())
p.join()
```

---

### Модуль `platform.py`

Функции для определения платформы:

|Функция|Описание|
|---|---|
|`is_android()`|Android (Kivy/Buildozer, Termux, python-for-android)|
|`is_linux()`|Linux (кроме Android)|
|`is_window()`|Windows|
|`is_macos()`|macOS|
|`is_ios()`|iOS|

---

### Модуль `window_transparency.py`

**Доступно только на Windows.**

```python

def set_window_transparency(hwnd=None, alpha_value=255) -> bool: ...
```

|Параметр|Описание|
|---|---|
|`hwnd`|Дескриптор окна (если `None` — берётся текущее окно Pygame)|
|`alpha_value`|Прозрачность от 0 (полностью прозрачный) до 255 (непрозрачный)|

**Требования:** установленный пакет `pywin32`.

---

## Константы событий Pygame-ce

Easel поддерживает все стандартные события Pygame:

### Системные события

|Константа|Описание|
|---|---|
|`QUIT`|Запрос на закрытие окна|
|`ACTIVEEVENT`|Окно получило/потеряло фокус|
|`VIDEORESIZE`|Изменение размера окна|
|`VIDEOEXPOSE`|Окно было перекрыто и снова показано|
|`RENDER_TARGETS_RESET`|Сброс целей рендеринга|

### Клавиатура

|Константа|Описание|Атрибуты|
|---|---|---|
|`KEYDOWN`|Клавиша нажата|`key`, `mod`, `unicode`, `scancode`|
|`KEYUP`|Клавиша отпущена|`key`, `mod`, `scancode`|
|`TEXTEDITING`|Редактирование текста (IME)|`text`, `start`, `length`|
|`TEXTINPUT`|Ввод текста|`text`|

### Мышь

|Константа|Описание|Атрибуты|
|---|---|---|
|`MOUSEMOTION`|Перемещение мыши|`pos`, `rel`, `buttons`, `touch`|
|`MOUSEBUTTONDOWN`|Кнопка мыши нажата|`pos`, `button`, `touch`|
|`MOUSEBUTTONUP`|Кнопка мыши отпущена|`pos`, `button`, `touch`|
|`MOUSEWHEEL`|Прокрутка колеса|`x`, `y`, `flipped`, `which`, `precise_x`, `precise_y`|

### Джойстик

|Константа|Описание|
|---|---|
|`JOYAXISMOTION`|Движение оси джойстика|
|`JOYBALLMOTION`|Движение трекбола|
|`JOYHATMOTION`|Движение хата|
|`JOYBUTTONDOWN`|Нажатие кнопки джойстика|
|`JOYBUTTONUP`|Отпускание кнопки джойстика|
|`JOYDEVICEADDED`|Подключение джойстика|
|`JOYDEVICEREMOVED`|Отключение джойстика|

---

## Лицензия

Модуль распространяется в составе PyForge. Подробности уточняйте в основном репозитории проекта.