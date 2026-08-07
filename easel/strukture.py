import sys
from typing import Type, TypeVar
from threading import Thread
from traceback import extract_tb

try:
    import pygame as pg
except ImportError as e:
    sys.exit(102)

from PyForge.gpu.locals import IS_IMPORT_GL, InitGl

if IS_IMPORT_GL:
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *


class Scene:
    name: str
    
    def __init__(self, win = None):
        self._win = win
    def close(self):
        '''
        сработает при нажатии на крестик
        '''
    def event(self, event: pg.event.Event):
        '''
        сработает for event in pg.event.get()
        Аргументы:
            event: pg.event.get
        '''
    def draw(self, screen: pg.Surface):
        '''
        сработает при каждом цикле
        Аргументы:
            screen: pg.display.set_mode
        '''
    def update(self):
        '''
        сработает при обновление
        '''
    def size_update(self, old: tuple[int], new: tuple[int]):
        '''
        обновление размер окна
        '''
    def muve_window(self, old: tuple[int], new: tuple[int]):
        '''
        обновление перемещение экрана
        '''

T = TypeVar('Scene')
class Window(Scene):
    _scene: list[T] # все сцены в приложении
    condition = 0 # номер сцены которя активна
    range_p = False

    @property
    def size(self):
        return self.__size
    @size.setter 
    def size(self, size: list[int, int]):
        self.__size = size
    
    def add_scene(self, *scene: T | Scene):
        for sc in scene:
            self._scene.append(sc(self.win))

    def set_icon(self, icon: pg.Surface | str, permission = (32, 32)):
        if type(icon) is str:
            icon = pg.image.load(icon)
        pg.display.set_icon(pg.transform.smoothscale(icon, permission).convert_alpha())

    def set_caption(self, caption: str | object):
        if not type(caption) is str:
            caption = str(caption)
        pg.display.set_caption(caption)
    
    def init(self, win):
        pass

    def logger(self, text, info=None):
        print(text)

    def __init__(self, size=(400, 300), color=(255, 255, 255), scene: list[Type[T]] | None = None, *, fps=60,flags = 0, zi_set_mode = ()):
        self.logger("[INIT] Начало инцилизации", "INIT")
        self.flags = flags
        self.zi= zi_set_mode
        self.__size = size
        self.color = color
        self.fps = fps

        self.process = None
        self.running = True

        self._scene = []
        self.temporarily_scene = [] if scene is None else scene

        self.min_size = [0, 0]
    def _st(self):
        pass
    
    def _ran_scene(self, index: int):
        self.logger(f"[INFO] [START] {self.temporarily_scene[index].__name__}")
        try:
            self._scene[index] = self.temporarily_scene[index](self.win)
            self.logger(f"[INFO] [FINISH] {self.temporarily_scene[index].__name__}")
        except Exception as e:
            self._scene[index] = Scene(self.win)
            for frame in extract_tb(e.__traceback__):
                self.logger(f" [ERROR] [{self.temporarily_scene[index].__name__}] [{frame.name}] {e}")
            raise e
    def start_scenes(self):
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
        pg.display.init()
        self.win = pg.display.set_mode(self.__size, flags= self.flags, *self.zi)

        self.clock_fps = pg.time.Clock()
        self.clock_tps = pg.time.Clock()

        self.gl_init()
        self.opengl = InitGl()

        if self.opengl and IS_IMPORT_GL:
            glClearColor(self.color[0]/255, self.color[1]/255, self.color[2]/255, 1)
            self.opengl.initialization_fun()
        self.range_p = True

        self.start_scenes()
        self.init(self.win)


        while self.running:
            if self.opengl and IS_IMPORT_GL:
                self.opengl.clear()
            else:
                self.win.fill(self.color)
            self.update()
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
                    self.size_update(self.__size, (event.w, event.h))
                    self.__size = (event.w, event.h)
                else:
                    self.event(event)
            self.draw(self.win)
            pg.display.flip()
            self.clock_fps.tick(self.fps)
        pg.quit()
        sys.exit()
    
    def gl_init(self):
        pass

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

    def update(self):
        self._scene[self.condition].update()


        
    def start(self):
        self.run_window()

    def is_alive(self):
        return self.running
    
    def join(self):
        pass

    def kill(self):
        self.close()

    def update_window(self, size=None, flags=None, zi=None):
        self.__size = self.__size if size is None else size
        self.flags = self.flags if flags is None else flags
        self.zi = self.zi if zi is None else zi
        self.win = pg.display.set_mode(self.__size, pg.RESIZABLE)

if __name__ == '__main__':
    print(type(Window), Window.__name__)
    # Создаем два окна с разными параметрами
    window1 = Window(color=(220, 110, 70),)
    window1.start()
