"""
Модуль со структурой класса окна
"""
from typing import Type, TypeVar, TypedDict, NotRequired
from threading import Thread
from traceback import extract_tb
from .scene import Scene, EVENTS_METOD
from ..gpu.locals import IS_IMPORT_GL, InitGl
from ..logger import printError, printInfo

import pygame as pg
import sys

if IS_IMPORT_GL:
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *


class KwargsSetMode(TypedDict): # класс для параметров
    flags: NotRequired[int]     # Стадарт 0
    depth: NotRequired[int]     # Стадарт 0
    display: NotRequired[int]   # Стадарт 0
    vsync: NotRequired[int]     # Стадарт 0

T = TypeVar('Scene')
class Window:
    _scene: list[T]     # все сцены в приложении
    condition = 0       # номер сцены которя активна

    def addScene(self, *scene: T) -> None:
        for sc in scene:
            self._scene.append(sc(self.win))

    def setIcon(self, icon: pg.Surface | str, permission: tuple[int, int] = (32, 32)) -> None:
        if type(icon) is str:
            icon = pg.image.load(icon)
        pg.display.set_icon(pg.transform.smoothscale(icon, permission).convert_alpha())

    def setCaption(self, caption: str | object) -> None:
        if not type(caption) is str:
            caption = str(caption)
        pg.display.set_caption(caption)
    
    def init(self, win: pg.Surface) -> None:
        pass

    def initOpenGL(self) -> None:
        """
        Запускает инцилизацию OpenGL в любых случаев
        """
        self.opengl = InitGl()

        if self.opengl and IS_IMPORT_GL:
            glClearColor(self.color[0]/255, self.color[1]/255, self.color[2]/255, 1)
            self.opengl.initialization_fun()

    def __init__(self, 
                size: tuple[int, int] = (400, 300), 
                color: tuple[int, int, int] = (255, 255, 255), 
                scene: list[T] | None = None, 
                *, 
                fps: int | float = 60, 
                kwargs_set_mode: KwargsSetMode | None = None
                ):
        """
        Инцизация главного класса управление окном
        
        Args:
            size (tuple[int, int]): размеры окна (width, height)
            color (tuple[int, int, int]): Цветовая политра RGB заднего фона
            scene (list[T] | None): список классов сценн наследованые от главного класса (Scene)
            fps (int | float): кадры в секунду
            kwargs_set_mode (KwargsSetMode | None): парамерты для создание окна (pg.display.set_mode)
        """
        printInfo(f"Начало инцилизации класса {self}")
        self.kwargs_set_mode = {} if kwargs_set_mode is None else kwargs_set_mode

        if not "depth" in self.kwargs_set_mode:      self.kwargs_set_mode['depth'] = 0
        if not "display" in self.kwargs_set_mode:    self.kwargs_set_mode['display'] = 0
        if not "flags" in self.kwargs_set_mode:      self.kwargs_set_mode['flags'] = 0
        if not "vsync" in self.kwargs_set_mode:      self.kwargs_set_mode['vsync'] = 0

        self.__size = size
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
        pg.init()
        self.win = pg.display.set_mode(self.__size, flags=self.kwargs_set_mode['flags'], depth=self.kwargs_set_mode['depth'], display=self.kwargs_set_mode['display'], vsync=self.kwargs_set_mode['vsync'])

        self.clock_fps = pg.time.Clock()
        self.clock_tps = pg.time.Clock()

        # инцилизация OpenGL
        self.initOpenGL()
        # инцилизация сценн
        self.start_scenes()
        # инцилизация остольного
        self.init(self.win)

        while self.running:

            if self.opengl and IS_IMPORT_GL:
                self.opengl.clear()
            else:
                self.win.fill(self.color)

            # обновеление активной сценный
            self.update(self.clock_fps.tick(self.fps)/1000.0)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                elif event.type == pg.VIDEORESIZE:
                    # Обновляем поверхность отображения с новым размером
                    if self.min_size[0] > event.w:
                        event.w = self.min_size[0]
                    if self.min_size[1] > event.h:
                        event.h = self.min_size[1]
                    self.win = pg.display.set_mode((event.w, event.h), flags= self.flags, *self.zi)
                    self.size_update(self.__size, (event.w, event.h), (self.__size[0]/event.w, self.__size[1]/event.h))
                    self.__size = (event.w, event.h)
                else:
                    self.event(event)
                self.eventManager(event)    # запуск методов эвента

            self.draw(self.win)             # отрисовка активной сценны
            pg.display.flip()               # обновление экрана
               # ограничение фпс и тпс
        pg.quit()
        sys.exit()

    def eventManager(self, event: pg.event.Event):
        type = pg.event.event_name(event.type)
        if type in EVENTS_METOD:
            EVENTS_METOD[type](self._scene[self.condition], event)

    def size_update(self, old: tuple[int], new: tuple[int]):
        for scene in self._scene:
            scene.size_update(old, new)

    def event(self, event: pg.event.Event):
        self._scene[self.condition].event(event)

    def draw(self, sceen):
        self._scene[self.condition].draw(sceen)

    def close(self):
        self.running = False
        for scene in self._scene:
            scene.close()

    def update(self, dt: float) -> None:
        self._scene[self.condition].update(dt)

    def start(self) -> None:
        self.run_window()

    def is_alive(self) -> bool:
        return self.running
    
    def join(self) -> None: ... # затычка

    def kill(self) -> None:
        self.close()

    def update_window(self, 
                    size: tuple[int, int] | None = None, 
                    flags: int | None = None, 
                    depth: int | None = None,
                    display: int | None = None,
                    vsync: int | None = None
                    ) -> None:
        """
        Обновление параметров окна
        """
        self.__size = self.__size if size is None else size
        if not flags is None: self.kwargs_set_mode['flags'] = flags
        if not depth is None: self.kwargs_set_mode['depth'] = depth
        if not display is None: self.kwargs_set_mode['display'] = display
        if not vsync is None: self.kwargs_set_mode['vsync'] = vsync
        self.win = pg.display.set_mode(self.__size, flags=self.kwargs_set_mode['flags'], depth=self.kwargs_set_mode['depth'], display=self.kwargs_set_mode['display'], vsync=self.kwargs_set_mode['vsync'])

    @property
    def size(self):
        return self.__size
    @size.setter 
    def size(self, size: list[int, int]):
        self.__size = size

if __name__ == '__main__':
    print(type(Window), Window.__name__)
    # Создаем два окна с разными параметрами
    window1 = Window(color=(220, 110, 70),)
    window1.start()
