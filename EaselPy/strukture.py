import sys
from typing import Type, TypeVar
from threading import Thread
from traceback import extract_tb
import logging

logger = logging.getLogger("main_window")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('main_window.log')
file_handler.setLevel(logging.WARNING)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
#logger.addHandler(file_handler)

def file_handler_set_name(name):
    global file_handler, logger, formatter
    file_handler = logging.FileHandler(name)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

logger.info("init")

try:
    import pygame as pg
except ImportError as e:
    logger.error("102 - error: " + str(e))
    #sys.exit(102)


try:
    from OpenGL.GL import *
    def check_opengl_with_pygame():
        try:
            pg.init()
            pg.display.set_mode((1, 1), pg.OPENGL | pg.DOUBLEBUF)
            version = glGetString(GL_VERSION)
            vendor  = glGetString(GL_VENDOR)
            renderer = glGetString(GL_RENDERER)
            info = {
                "version": version.decode() if version else None,
                "vendor": vendor.decode() if vendor else None,
                "renderer": renderer.decode() if renderer else None,
            }
            pg.quit()
            return True, info
        except Exception as e:
            try:
                pg.quit()
            except:
                pass
            return False, str(e)
    import_openGL, _ = check_opengl_with_pygame()
except (ModuleNotFoundError, ImportError) as e:
    import_openGL = False
    logger.error("104 - error: " + str(e))

class FrameWindow:
    def __init__(self):
        
        pass
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

class Scene(FrameWindow):
    def __init__(self, screen: pg.Surface):
        pass

T = TypeVar('Scene')
class Window(FrameWindow):
    _scene: list[T | Scene] # все сцены в приложении
    condition = 0 # номер сцены которя активна
    range_p = False
    @property
    def size(self):
        return self.__size
    @size.setter 
    def size(self, size: list[int, int]):
        self.__size = size
    
    def add_scene(self, *scene: T | Scene):
        for s in scene:
            self._scene.append(s(self.win))

    def set_icon(self, icon: pg.Surface | str):
        if type(icon) is str:
            icon = pg.image.load(icon)
        pg.display.set_icon(icon) 
    def set_caption(self, caption: str | object):
        if not type(caption) is str:
            caption = str(caption)
        pg.display.set_caption(caption)
    def init(self, win):
        pass
    def __init__(self, size=(400, 300), color=(255, 255, 255), scene: list[Type[T]] | None = None, *, fps=60,flags = 0, zi_set_mode = ()):
        logger.info("init_class")
        self.flags = flags
        self.zi= zi_set_mode
        self.__size = size
        self.color = color
        self.fps = fps

        self.process = None
        self.running = True
        self.opengl = False

        self._scene = []
        self.temporarily_scene = [] if scene is None else scene
    def _st(self):
        pass

    def _ran_scene(self, index: int):
        logger.info(0, f"[INFO] [START] {self.temporarily_scene[index].__name__}", "da")
        print(f"[INFO] [START] {self.temporarily_scene[index].__name__}")
        try:
            self._scene[index] = self.temporarily_scene[index](self.win)
            logger.info(f"[INFO] [FINISH] {self.temporarily_scene[index].__name__}")
            print(f"[INFO] [FINISH] {self.temporarily_scene[index].__name__}")
        except Exception as e:
            for frame in extract_tb(e.__traceback__):
                logger.error(f" [ERROR] [{self.temporarily_scene[index].__name__}] [{frame.name}] {e}")
                print("\033[31m"+ f" [ERROR] [{self.temporarily_scene[index].__name__}] [{frame.name}] {e}" + "\033[0m")

    def run_window(self):
        pg.init()

        self.win = pg.display.set_mode(self.__size, flags= self.flags, *self.zi)
        self._st()
        
        self.clock_fps = pg.time.Clock()
        self.clock_tps = pg.time.Clock()

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

        if self.opengl and import_openGL:
            glClearColor(self.color[0]/255, self.color[1]/255, self.color[2]/255, 1)
        self.range_p = True
        self.init(self.win)
        while self.running:
            if (not self.opengl) or (not import_openGL):
                self.win.fill(self.color)
            self.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                else:
                    self.event(event)
            self.draw(self.win)
            if (not self.opengl) or (not import_openGL):
                #pg.display.update()
                pass
            else:
                glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()
            self.clock_fps.tick(self.fps)
        pg.quit()
        sys.exit()
    
    def event(self, event: pg.event.Event):
        try:
            self._scene[self.condition].event(event)
        except IndexError: pass
    def draw(self, screen):
        try:
            self._scene[self.condition].draw(screen)
        except IndexError: pass
    def close(self):
        self.running = False
        for scene in self._scene:
            scene.close()
    def update(self):
        try:
            self._scene[self.condition].update()
        except IndexError: pass
        
    def start(self):
        self.run_window()
    def is_alive(self):
        return self.running
    def join(self):
        pass
            
            
if __name__ == '__main__':
    print(type(Window), Window.__name__)
    # Создаем два окна с разными параметрами
    window1 = Window(color=(220, 110, 70),)
    window1.start()
