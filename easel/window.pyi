from typing import TypeVar, Final, Callable
from .event import Event, CommonEvent, QuitEvent
from sdl2.surface import SDL_Surface

# флаги для Window
WINDOW_FULLSCREEN: Final[int]	        # Открывает окно на весь экран, меняя разрешение рабочего стола
WINDOW_FULLSCREEN_DESKTOP: Final[int]   # Открывает окно на весь экран с разрешением текущего рабочего стола
WINDOW_OPENGL: Final[int]	            # Создаёт окно с поддержкой контекста OpenGL
WINDOW_HIDDEN: Final[int]	            # Изначально скрывает окно
WINDOW_RESIZABLE: Final[int]	        # Разрешает пользователю изменять размер окна
WINDOW_MAXIMIZED: Final[int]	        # Разворачивает окно в максимальное состояние
WINDOW_SHOWN: Final[int]	            # Сразу отображает окно

WINDOWPOS_CENTERED: Final[int]                      # окно по центру основного дисплея (эквивалент CENTERED_DISPLAY(0))
WINDOWPOS_CENTERED_MASK: Final[int]                 # внутренняя битовая маска (0x2FFF0000), которой помечается «центрированная» позиция; напрямую обычно не нужна.
WINDOWPOS_CENTERED_DISPLAY: Callable[[int], int]    # окно по центру дисплея с индексом X. WINDOWPOS_CENTERED_DISPLAY(x)
WINDOWPOS_ISCENTERED: Callable[[int], int]          # проверяет, помечено ли значение X как «центрированное» (возвращает true/false).

_T = TypeVar('Scene')
class Window:
    _scene: list[_T]                        # все сцены в приложении
    condition = 0                           # номер сцены которая активна
    min_size: tuple[int, int] = (50, 50)    # минимальный размер

    def start(self) -> None:
        """
        Запуск окно.
        """

    def __init__(self,
            caption: str | bytes = b'My Engine',
            point: tuple[int, int] | None = None,
            size: tuple[int, int] = (400, 300), 
            color: tuple[int, int, int] = (255, 255, 255), 
            scene: list[_T] | None = None, 
            *, 
            fps: int | float = 60, 
            flags: int = 0,
            ):
        """
        Инициализация главного класса управление окном,
        для запуска выполните \"run_window\"
        
        Args:
            title (bytes | str): Заголовок окна. В PySDL2 строки часто передаются как bytes, например b"My Engine", но можно строку.
            
            point (tuple[int, int] | None): В реальных условиях не используется, он может принимать список из WINDOWPOS_*. (на телефонах этот пункт не учитывается)
            
            size (tuple[int, int]): размеры окна (width, height), по стандарту (400, 300), он не должен быть больше размеры экрана и не меньше минимального размера (на телефонах этот пункт не учитывается).
            
            color (tuple[int, int, int]): Цветовая палитра RGB заднего фона.
            
            scene (list[T] | None): список классов сцен наследованные от главного класса (Scene)
            
            fps (int | float): кадры и тики в секунду

            flags (int): принимает WINDOW_*, можно объединять с помощью побитового или ( \"|\" ), стандартное идет 0.
        """


    def initOpenGL(self) -> None:
        """
        Запуск инициализацию OpenGL в любых случаев
        """

    def addScene(self, *scene: _T) -> None:
        """
        Добавляет в конец и инициализирует сцену (или сцены) 
        """

    def run_window(self):
        """
        Главный цикл для работы, в нем работает полный цикл sdl2,
        обработка сцен, обработка OpenGL, закрашивание, передачу событий и тд.
        """

    def eventManager(self, event: Event) -> None:
        """
        Он принимает любой ивент и отправляет текущей сцене событие которое сработало.
        """

    def size_update(self, old: tuple[int], new: tuple[int], scale: tuple[int, int]) -> None:
        """
        Отправляет все сценам событие об изменение экрана.
        """

    def event(self, event: Event) -> None:
        """
        Отправляет событие активному сцене,
        но сцене только срабатывает ивент .event
        """

    # размеры
    @property
    def size(self): ...
    @size.setter 
    def size(self, size: list[int, int]): ...

    # поверхность
    @property
    def holst(self) -> SDL_Surface: ...

    # название
    @property
    def caption(self) -> str: ...

    @caption.setter
    def caption(self, caption: str | object | bytes) -> None: ...