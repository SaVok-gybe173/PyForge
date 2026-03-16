import importlib.util as util
import os

from .EaselPy.strukture import Window, T, extract_tb
try:
    from .mods.mod import FrameMod
except ImportError:
    from mods.mod import FrameMod


class Game(Window):
    
    mods_dir:str
    mods_list: list[FrameMod] = []
    mod_info = dict()
    
    
    def __init__(self, size=(400, 300), color=(255, 255, 255),scene: list[type[T]] = [], *, fps=60, mods_dir=None, _mod = True, flags = None, zi = []):
        self.mods_dir = mods_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mods')
        self._mod = _mod
        super().__init__( size, color, fps=fps,flags = flags, zi_set_mode = zi, scene= scene)
    def init(self, win):
        if self._mod:
            self.load_mods()
    def start(self):
        super().start()
        self.join()
        
    def draw(self, win):
        super().draw(win)
        for i in self.mods_list:
            i.draw(win)
        
    def event(self, event):
        super().event(event)
        for i in self.mods_list:
            i.event(event)
        
    def close(self):
        super().close()
        for i in self.mods_list:
            i.close()
        
    def load_mods(self):
        # Получаем список файлов в директории модов
        for filename in os.listdir(self.mods_dir):
            if filename.endswith('.py') or filename.endswith('.pyc') or filename.endswith('.pyd'):
                spec = util.spec_from_file_location(f"mods.{filename[:-3]}", os.path.join(self.mods_dir, filename))
                mod = util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, 'Main'):
                    try:
                        stucture: FrameMod = mod.Main(self)
                        self.mods_list.append(stucture)
                    except Exception as e:
                        for frame in extract_tb(e.__traceback__):
                            print("\033[31m"+ f" [ERROR] [{mod.__name__}] [{frame.name}] {e}" + "\033[0m")
if __name__ == '__main__':
    import multiprocessing
    import sys
    
    multiprocessing.freeze_support()
    
    if getattr(sys, 'frozen', False):
        os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
    
    Game().start()