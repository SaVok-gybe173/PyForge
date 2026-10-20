"""
Модуль со структурой класса окна
"""
from typing import Type, TypeVar, TypedDict, NotRequired
from threading import Thread
from traceback import extract_tb
from .scene import Scene, EVENTS_METOD
from ..gpu.locals import IS_IMPORT_GL, InitGl
from .logger import printError, printInfo
from .time import Clock
from .event import EVENT_NAMES
from .surface import Surface
from sdl2.surface import SDL_Surface
from sdl2.video import SDL_CreateWindow, SDL_GL_SwapWindow,  SDL_Window, SDL_DestroyWindow, SDL_GetWindowSurface, SDL_UpdateWindowSurface,  SDL_SetWindowTitle, SDL_GetWindowTitle
from sdl2.events import SDL_QUIT, SDL_PollEvent, SDL_Event as Event, SDL_WINDOWEVENT
from sdl2.error import SDL_GetError
from sdl2 import SDL_MapRGB, ext, SDL_FillRect, SDL_WINDOWEVENT_RESIZED, SDL_Init, SDL_INIT_VIDEO, SDL_DisplayMode, SDL_GetCurrentDisplayMode, SDL_GetNumVideoDisplays, SDL_GetDesktopDisplayMode

import sys


"""
SDL_WINDOW_FULLSCREEN	Открывает окно на весь экран, меняя разрешение рабочего стола
SDL_WINDOW_FULLSCREEN_DESKTOP	Открывает окно на весь экран с разрешением текущего рабочего стола
SDL_WINDOW_OPENGL	Создаёт окно с поддержкой контекста OpenGL
SDL_WINDOW_HIDDEN	Изначально скрывает окно
SDL_WINDOW_RESIZABLE	Разрешает пользователю изменять размер окна
SDL_WINDOW_MAXIMIZED	Разворачивает окно в максимизированное состояние
SDL_WINDOW_SHOWN	Сразу отображает окно
"""

T = TypeVar('Scene')
class Window:
    _scene: list[T]     # все сцены в приложении
    condition = 0       # номер сцены которя активна

    def addScene(self, *scene: T) -> None:
        for sc in scene:
            self._scene.append(sc(self.win))

    #def setIcon(self, icon: Surface | str, permission: tuple[int, int] = (32, 32)) -> None:
    #    if type(icon) is str:
    #        icon = sdl2.surface.load(icon)
    #    pg.display.set_icon(pg.transform.smoothscale(icon, permission).convert_alpha())

    


    def initOpenGL(self) -> None:
        """
        Запускает инцилизацию OpenGL в любых случаев
        """
        self.opengl = InitGl()

        if self.opengl and IS_IMPORT_GL:
            #glClearColor(self.color[0]/255, self.color[1]/255, self.color[2]/255, 1)
            self.opengl.initialization_fun()

    def __init__(self,
                caption: str | bytes = b'My Engine',
                point: tuple[int, int] | None = None,
                size: tuple[int, int] = (400, 300), 
                color: tuple[int, int, int] = (255, 255, 255), 
                scene: list[T] | None = None, 
                *, 
                fps: int | float = 60, 
                flags: int = 0,
                display_index: int = 0
                ):
        """
        Инцизация главного класса управление окном
        
        Args:
            title (bytes | str): Заголовок окна. В PySDL2 строки часто передаются как bytes, например b"My Engine".
            size (tuple[int, int]): размеры окна (width, height)
            color (tuple[int, int, int]): Цветовая политра RGB заднего фона
            scene (list[T] | None): список классов сценн наследованые от главного класса (Scene)
            fps (int | float): кадры в секунду
            kwargs_set_mode (KwargsSetMode | None): парамерты для создание окна (pg.display.set_mode)
        """
        printInfo(f"Начало инцилизации класса {self}")
        
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

        self.min_size = [50, 50]    # минимальный размер
    
    def _ran_scene(self, index: int):
        printInfo(f"[START] {self.temporarily_scene[index].__name__}")
        try:
            self._scene[index] = self.temporarily_scene[index](self.win)
            printInfo(f"[FINISH] {self.temporarily_scene[index].__name__}")
        except Exception as e:
            self._scene[index] = Scene(self.win)
            for frame in extract_tb(e.__traceback__):
                printError(f"[{self.temporarily_scene[index].__name__}] [{frame.name}] {e}")
            raise e

    def start_scenes(self) -> None:
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
        SDL_Init(SDL_INIT_VIDEO)
        if SDL_GetNumVideoDisplays() < self.__display_index:
            self.__display_index = SDL_GetNumVideoDisplays()
        elif self.__display_index < 0:
            self.__display_index = SDL_GetNumVideoDisplays()-self.__display_index

        mode = SDL_DisplayMode()
        SDL_GetCurrentDisplayMode(self.__display_index, mode)
        self.__point = self.__point if not self.__point is None else (int((mode.w-self.__size[0])/2), int((mode.h-self.__size[1])/2))

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
        self.start_scenes()

        printInfo("Тип self.win:", type(self.win))
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
                r, g, b = self.color[:3]
                pixel = SDL_MapRGB(self.surface._surface.contents.format, r, g, b)
                SDL_FillRect(self.surface._surface, None, pixel)

            # обновеление активной сценный
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
                    self.size_update(self.__size, (new_w, new_h))
                    self.__size = (new_w, new_h)

                    if self.opengl and IS_IMPORT_GL:
                        # Обновляем viewport OpenGL
                        import OpenGL.GL as GL
                        GL.glViewport(0, 0, new_w, new_h)
                    
                    self.eventManager(event)
                    continue
                else:
                    self.event(event)
                #self.eventManager(event)    # запуск методов эвента

            self.draw(self.surface)             # отрисовка активной сценны
            if use_gl:
                SDL_GL_SwapWindow(self.win)
            else:
                SDL_UpdateWindowSurface(self.win)
               # ограничение фпс и тпс
        SDL_DestroyWindow(self.win)
        sys.exit()

    def eventManager(self, event):
        name = EVENT_NAMES.get(event.type)
        if name and name in EVENTS_METOD:
            EVENTS_METOD[name](self._scene[self.condition], event)

    def size_update(self, old: tuple[int], new: tuple[int]):
        for scene in self._scene:
            scene.size_update(old, new)

    def event(self, event: Event):
        self._scene[self.condition].event(event)

    def draw(self, sceen):
        self._scene[self.condition].draw(sceen)

    def close(self, common, quit):
        self.running = False
        for scene in self._scene:
            scene.quit(common, quit)

    def update(self, dt: float) -> None:
        self._scene[self.condition].update(dt)

    def start(self) -> None:
        self.run_window()

    def is_alive(self) -> bool:
        return self.running
    
    def join(self) -> None: ... # затычка

    def kill(self) -> None:
        self.close()

    #def update_window(self, 
    #                size: tuple[int, int] | None = None, 
    #                flags: int | None = None, 
    #                depth: int | None = None,
    #                display: int | None = None,
    #                vsync: int | None = None
    #                ) -> None:
    #    """
    #    Обновление параметров окна
    #    """
    #    self.__size = self.__size if size is None else size
    #    if not flags is None: self.kwargs_set_mode['flags'] = flags
    #    if not depth is None: self.kwargs_set_mode['depth'] = depth
    #    if not display is None: self.kwargs_set_mode['display'] = display
    #    if not vsync is None: self.kwargs_set_mode['vsync'] = vsync
    #    self.win = pg.display.set_mode(self.__size, flags=self.kwargs_set_mode['flags'], depth=self.kwargs_set_mode['depth'], display=self.kwargs_set_mode['display'], vsync=self.kwargs_set_mode['vsync'])

    @property
    def size(self):
        return self.__size
    @size.setter 
    def size(self, size: list[int, int]):
        self.__size = size

    @property
    def holst(self) -> SDL_Surface:
        return SDL_GetWindowSurface(self.win)

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
    
if __name__ == '__main__':
    print(type(Window), Window.__name__)
    # Создаем два окна с разными параметрами
    window1 = Window(color=(220, 110, 70),)
    window1.start()
