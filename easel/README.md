# Easel — модуль для создания оконных приложений на PyForge

**Easel** — это часть фреймворка PyForge, предоставляющая удобную объектно-ориентированную надстройку над `pysdl2` для создания оконных приложений с поддержкой сцен, событий и модульной архитектуры.

## Возможности

- **Управление окнами** — создание и настройка главного окна приложения
- **Система сцен** — гибкая архитектура для организации разных экранов приложения
- **Полная обработка событий** — клавиатура, мышь, изменение размера окна и системные события
- **Поддержка модов** — динамическая загрузка плагинов из папки `mods`
- **Многопроцессность** — создание дополнительных окон в отдельных процессах (кроме Android/iOS)
- **Кроссплатформенность** — определение Android, Linux, Windows, macOS, iOS
- **OpenGL** — встроенная поддержка инициализации OpenGL
- **Логирование** — встроенная система логирования для каждого класса
- **Рисование** — набор примитивов (`line`, `rect`, `circle` и др.) через Cython-модуль `draw`
- **Низкоуровневая работа с поверхностями** — класс `Surface` с прямым доступом к пикселям

---

## Установка

```bash
pip install pysdl2
pip install pysdl2-dll
```

Модуль является частью PyForge, поэтому импорт выглядит так:

```python
from PyForge.easel import Window, Scene, App
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

    def close(self):
        print("Окно закрыто")

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
        ...  # отрисовка меню

    def keydown(self, key: int, mod: int, unicode: str, scancode: int):
        if key == pg.K_SPACE:
            self.page.condition = 1  # переключение на игровую сцену

class GameScene(Scene):
    def draw(self, win: pg.Surface):
        win.fill((30, 80, 30))  # отрисовка игры

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
    ...

# Создаём окно в отдельном процессе
win2 = ProcessWindow(size=(400, 300), scene=[SecondScene])
win2.start()   # запуск в новом процессе
win2.join()    # ожидание завершения
```

---

## Справочник API

### Модуль `__init__.py`

Экспортирует основные классы и функции:

| Имя | Описание |
|---|---|
| `Scene` | Базовый класс для всех сцен |
| `Window` | Главный класс управления окном |
| `App` | Класс приложения с поддержкой модов (наследует `Window`) |
| `WindowProcession` | Класс для создания окон в отдельных процессах |
| `is_android()`, `is_linux()`, `is_macos()`, `is_ios()`, `is_window()` | Проверка платформы |
| `Surface` | Обёртка над `SDL_Surface` |
| `CoreObject`, `PfObject`, `PfObjectIMG` | Базовые объекты сцены |
| `event_name`, `event_add`, `event_type`, `EVENT_NAMES` | Утилиты для работы с событиями |

---

### Класс `Scene` (`scene.py`)

Базовый класс для всех сцен приложения.

**Атрибуты:**

- `name: str` — имя сцены (по умолчанию — имя класса)
- `page: Window` — ссылка на родительское окно
- `objects: list[PfObject]` — список объектов на сцене

**Методы:**

| Метод | Описание |
|---|---|
| `append(object)` | Добавляет объект в конец списка |
| `draw(win)` | Отрисовка всех объектов |
| `update(dt)` | Обновление логики |
| `event(event)` | Обработка событий |
| `keydown`, `keyup`, `mousemotion`, `mousebuttondown`, `mousebuttonup`, `mousewheel`, `textinput` | Проброс событий к объектам |

---

### Класс `Window` (`window.py`)

Главный класс управления окном.

**Конструктор:**

```python
Window(
    caption: str | bytes = b'My Engine',
    point: tuple[int, int] | None = None,
    size: tuple[int, int] = (400, 300),
    color: tuple[int, int, int] = (255, 255, 255),
    scene: list[Scene] | None = None,
    *,
    fps: int | float = 60,
    flags: int = 0,
)
```

**Методы:**

| Метод | Описание |
|---|---|
| `start()` | Запускает главный цикл окна |
| `addScene(*scene)` | Добавляет и инициализирует сцены |
| `initOpenGL()` | Инициализирует OpenGL |

**Флаги окна** (импортируются из `window.pyi`): `WINDOW_FULLSCREEN`, `WINDOW_FULLSCREEN_DESKTOP`, `WINDOW_OPENGL`, `WINDOW_HIDDEN`, `WINDOW_RESIZABLE`, `WINDOW_MAXIMIZED`, `WINDOW_SHOWN` и позиционные константы `WINDOWPOS_CENTERED`, `WINDOWPOS_CENTERED_DISPLAY`, `WINDOWPOS_ISCENTERED`.

---

### Класс `App` (`app.py`)

Наследует `Window`, добавляет автоматическую загрузку модов из папки `mods_dir`.

**Дополнительные атрибуты:**

- `mods_dir` — путь к папке с модами
- `mods_list: list[FrameMod]` — загруженные моды

**Методы `load_mods()`** — сканирует папку и загружает модули с расширениями `.py`, `.pyc`, `.pyd`.

---

### Класс `WindowProcession` (`window_processing.py`)

Позволяет создавать дополнительные окна в отдельных процессах (недоступно на Android/iOS).

**Методы:**

| Метод | Описание |
|---|---|
| `start()` | Запускает окно в новом процессе |
| `is_alive()` | Проверяет, активен ли процесс |
| `join(timeout=None)` | Ожидает завершения процесса |
| `kill()` | Принудительно завершает процесс |

---

### Модуль `platform.py`

Функции для определения платформы:

| Функция | Описание |
|---|---|
| `is_android()` | Android (Kivy/Buildozer, Termux, python-for-android) |
| `is_linux()` | Linux (кроме Android) |
| `is_window()` | Windows |
| `is_macos()` | macOS |
| `is_ios()` | iOS |

---

### Модуль `draw.pyx` / `draw.pyi`

Cython-модуль с низкоуровневыми примитивами рисования. Все функции принимают `Surface` и возвращают `Rect` (bounding box).

| Функция | Описание |
|---|---|
| `line(surface, color, start_pos, end_pos, width=1)` | Прямая линия (Bresenham) |
| `lines(surface, color, closed, points, width=1)` | Ломаная линия |
| `aaline(surface, color, start_pos, end_pos, width=1)` | Сглаженная линия (Xiaolin Wu) |
| `aalines(surface, color, closed, points)` | Сглаженная ломаная |
| `rect(surface, color, rect, width=0, border_radius=-1, ...)` | Прямоугольник (опционально со скруглёнными углами) |
| `circle(surface, color, center, radius, width=0, ...)` | Окружность (midpoint algorithm) |

---

### Класс `Surface` (`surface.pyx` / `surface.pyi` / `surface.pxd`)

Обёртка над `SDL_Surface` с прямым доступом к пиксельным данным.

**Основные методы:**

| Метод | Описание |
|---|---|
| `fill(color)` | Заливает всю поверхность цветом |
| `blit(source_surface, dest_pos)` | Копирует другую поверхность |
| `blit_scaled(src, dst_rect)` | Копирование с масштабированием |
| `set_colorkey(color)` | Устанавливает цветовой ключ |
| `clear_colorkey()` | Снимает цветовой ключ |
| `set_alpha(alpha)` | Устанавливает общую прозрачность (0–255) |
| `set_blendmode(mode)` | Устанавливает режим смешивания |
| `get_blendmode()` | Возвращает текущий режим смешивания |
| `get_at(pos)` | Возвращает цвет пикселя |
| `set_at(pos, color)` | Устанавливает цвет пикселя |
| `set_clip(clip)` | Устанавливает область отсечения |
| `get_clip()` | Возвращает область отсечения |

**Константы режимов смешивания:** `BLEND_NONE`, `BLEND_ALPHA`, `BLEND_ADD`, `BLEND_MOD`, `BLEND_DEFAULT`, `BLEND_MULT`.  
**Флаги поверхности:** `PREALLOC`, `RLEACCEL`, `SRCALPHA`.

---

### Модуль `event.py` / `event.pyi`

Обёртка над событиями SDL2, имитирующая `pygame.event`. Содержит константы событий и вспомогательные функции `event_name`, `event_add`, `event_type`, а также словарь `EVENT_NAMES`.

Поддерживаются все стандартные события SDL2: системные, клавиатура, мышь, джойстик, контроллер, сенсор, жесты, аудиоустройства и пользовательские события.

---

### Базовые объекты (`object.py`)

Иерархия объектов сцены:

- `CoreObject` — абстрактный базовый класс с методами `draw`, `update`, `event`, `close`, `size_update`, `move_window` и обработчиками системных событий.
- `PfObject` — расширяемый объект (наследует `CoreObject`).
- `PfObjectIMG` — объект-изображение.

Все объекты можно добавлять в сцену через `Scene.append()`.

---

## Лицензия

Модуль распространяется в составе PyForge. Подробности уточняйте в основном репозитории проекта.