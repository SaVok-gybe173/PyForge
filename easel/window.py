"""
Модуль со структурой класса окна
"""
from typing import Type, TypeVar, TypedDict, NotRequired
from threading import Thread
from traceback import extract_tb
from .scene import Scene, EVENTS_METHOD
from ..gpu.locals import IS_IMPORT_GL, InitGl
from ..base.logger import printError, printInfo
from ..math.time import Clock
from .event import EVENT_NAMES, CommonEvent, QuitEvent
from .surface import Surface
from .display import set_window_size
from sdl2.video import (
    SDL_WINDOW_FULLSCREEN as WINDOW_FULLSCREEN,
    SDL_WINDOW_FULLSCREEN_DESKTOP as WINDOW_FULLSCREEN_DESKTOP,
    SDL_WINDOW_OPENGL as WINDOW_OPENGL,
    SDL_WINDOW_HIDDEN as WINDOW_HIDDEN,
    SDL_WINDOW_RESIZABLE as WINDOW_RESIZABLE,
    SDL_WINDOW_MAXIMIZED as WINDOW_MAXIMIZED,
    SDL_WINDOW_SHOWN as WINDOW_SHOWN,

    SDL_WINDOWPOS_CENTERED as WINDOWPOS_CENTERED,
    SDL_WINDOWPOS_CENTERED_MASK as WINDOWPOS_CENTERED_MASK,
    SDL_WINDOWPOS_CENTERED_DISPLAY as WINDOWPOS_CENTERED_DISPLAY,
    SDL_WINDOWPOS_ISCENTERED as WINDOWPOS_ISCENTERED
)
from sdl2.surface import SDL_Surface
from sdl2.video import SDL_CreateWindow, SDL_GL_SwapWindow,  SDL_Window, SDL_DestroyWindow, SDL_GetWindowSurface, SDL_UpdateWindowSurface,  SDL_SetWindowTitle, SDL_GetWindowTitle
from sdl2.events import SDL_QUIT, SDL_PollEvent, SDL_Event as Event, SDL_WINDOWEVENT
from sdl2.error import SDL_GetError
from sdl2 import SDL_MapRGB, ext, SDL_FillRect, SDL_WINDOWEVENT_RESIZED, SDL_Init, SDL_INIT_VIDEO, SDL_DisplayMode, SDL_GetCurrentDisplayMode, SDL_GetNumVideoDisplays, SDL_GetDesktopDisplayMode


import sys



_T = TypeVar('Scene')
class Window:
    _scene: list[Scene]            # все сцены в приложении
    condition: int = 0          # номер сцены которая активна
    min_size: tuple[int, int] = (50, 50)    # минимальный размер

    def addScene(self, *scene: _T) -> None: # Добавляет в конец и инициализирует сцену
        for sc in scene:
            self._scene.append(sc(self.win))

    def initOpenGL(self) -> None: # Запуск инициализацию OpenGL в любых случаев
        self.opengl = InitGl() 

        if self.opengl and IS_IMPORT_GL:
            #glClearColor(self.color[0]/255, self.color[1]/255, self.color[2]/255, 1)
            self.opengl.initialization_fun()

    def __init__(self,
                caption: str | bytes = b'My Engine',
                point: tuple[int, int] | None = None,
                size: tuple[int, int] = (400, 300), 
                color: tuple[int, int, int] = (255, 255, 255), 
                scene: list[_T] | None = None, 
                *, 
                fps: int | float = 60, 
                flags: int = 0,
                display_index: int = 0
                ):
        printInfo(f"Начало инициализации класса {self}")
        
        self.__flags = flags
        self.__size = size
        self.__point = point
        self.__caption = caption if isinstance(caption, bytes) else caption.encode("utf-8")
        self.__display_index = display_index

        self.color = color
        self.fps = fps

        self.process = None
        self.running = True

        self._scene = []
        self.temporarily_scene = [Scene] if scene is None else scene
    
    def _ran_scene(self, index: int):
        printInfo(f"[START] {self.temporarily_scene[index].__name__}")
        try:
            self._scene[index] = self.temporarily_scene[index]()
            printInfo(f"[FINISH] {self.temporarily_scene[index].__name__}")
        except Exception as e:
            self._scene[index] = Scene()
            for frame in extract_tb(e.__traceback__):
                printError(f"[{self.temporarily_scene[index].__name__}] [{frame.name}] {e}")
            raise e

    def _start_scenes(self) -> None:
        for _ in range(self.temporarily_scene.__len__()):
            self._scene.append(None)

        threads: list[Thread] = []
        for scene in range(self.temporarily_scene.__len__()):
            
            threads.append(Thread(target=self._ran_scene , args = (scene, ), daemon=True),)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        del self.temporarily_scene

    def run_window(self):
        """
        Главный цикл для работы
        """
        SDL_Init(SDL_INIT_VIDEO)
        if SDL_GetNumVideoDisplays() < self.__display_index:
            self.__display_index = SDL_GetNumVideoDisplays()
        elif self.__display_index < 0:
            self.__display_index = SDL_GetNumVideoDisplays()-self.__display_index

        mode = SDL_DisplayMode()
        SDL_GetCurrentDisplayMode(self.__display_index, mode)
        self.__point = self.__point if not self.__point is None else (int((mode.w-self.__size[0])/2), int((mode.h-self.__size[1])/2))

        # главное окно
        self.win: SDL_Window = SDL_CreateWindow(
            self.__caption,
            self.__point[0], self.__point[1],
            self.__size[0], self.__size[1],
            self.__flags,
        )
        if not self.win:
            printError(SDL_GetError().decode())

        # Инициализация подсистем
        self.initOpenGL()
        self._start_scenes()

        printInfo("Значение self.win:", self.win)


        self.surface = Surface(self.holst, owned=False)
        self.clock_fps = Clock()

        while self.running:
            use_gl = self.opengl and IS_IMPORT_GL
            dt = self.clock_fps.tick(self.fps) / 1000.0

            if use_gl:
                self.opengl.clear()
            else:
                self.surface._surface = self.holst
                # self.color должен быть кортежем (r,g,b) или sdl2.SDL_Color
                self.surface.fill(self.color)

            # обновление активной сцены
            self.update(dt)

            for event in ext.get_events():
                if event.type == SDL_QUIT:
                    self.close(event.common, event.quit)
                elif event.type == SDL_WINDOWEVENT and \
                 event.window.event == SDL_WINDOWEVENT_RESIZED:
                    new_w = event.window.data1
                    new_h = event.window.data2
                    old_w, old_h = self.__size
                    scale = (old_w / new_w, old_h / new_h)
                    self.size_update(self.__size, (new_w, new_h), scale)
                    self.__size = (new_w, new_h)

                    if self.opengl and IS_IMPORT_GL:
                        # Обновляем viewport OpenGL
                        import OpenGL.GL as GL
                        GL.glViewport(0, 0, new_w, new_h)
                    
                    self.eventManager(event)
                    continue
                else:
                    self.event(event)
                self.eventManager(event)    # запуск методов с событием

            self.draw(self.surface)
            if use_gl:
                SDL_GL_SwapWindow(self.win)
            else:
                SDL_UpdateWindowSurface(self.win)
               # ограничение фпс и тпс
        SDL_DestroyWindow(self.win)
        sys.exit()

    def eventManager(self, event: Event) -> None:
        name = EVENT_NAMES.get(event.type)
        if name and name in EVENTS_METHOD:
            EVENTS_METHOD[name](self._scene[self.condition], event)

    def size_update(self, old: tuple[int], new: tuple[int], scale: tuple[int, int]) -> None:
        set_window_size(new)
        for scene in self._scene:
            scene.size_update(old, new, scale)

    def event(self, event: Event) -> None:
        self._scene[self.condition].event(event)

    def draw(self, scene: Surface) -> None: # отрисовка активной сцены
        self._scene[self.condition].draw(scene)

    def close(self, common: CommonEvent, quit: QuitEvent) -> None:
        self.running = False
        for scene in self._scene:
            scene.close(common, quit)

    def update(self, dt: float) -> None:
        self._scene[self.condition].update(dt)

    def start(self) -> None:
        self.run_window()

    def is_alive(self) -> bool:
        return self.running
    
    def join(self) -> None: ... # затычка

    def kill(self) -> None:
        self.close()

    def fill(self, color: tuple[int, int, int]) -> None:
        self.color = color

    # размеры
    @property
    def size(self):
        return self.__size
    @size.setter 
    def size(self, size: list[int, int]):
        self.__size = size

    # поверхность
    @property
    def holst(self) -> SDL_Surface:
        return SDL_GetWindowSurface(self.win)

    # название
    @property
    def caption(self) -> str:
        """
        Возвращает текущий заголовок.
        """
        return self.__caption.decode("utf-8")

    @caption.setter
    def caption(self, caption: str | object | bytes) -> None:
        """
        Устанавливает новый заголовок окна.
        """
        if isinstance(caption, bytes):
            caption = bytes.decode(caption, "utf-8")
        elif not type(caption) is str:
            caption = str(caption)
        self.__caption = caption.encode("utf-8")
        SDL_SetWindowTitle(self.win, self.__caption)
    

