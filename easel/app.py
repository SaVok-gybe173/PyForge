from .window import Window, _T, extract_tb, Scene
from ..mods.mod import FrameMod
from ..base.logger import printError
from .surface import Surface

import importlib.util as util
import os

class App(Window):
    
    mods_dir: str                       # Путь к папке с модами 
    mods_list: list[FrameMod] = []      # Объекты модов
    mod_info = dict()                   # Информация о моде
    mod_load = [".py", ".pyc", ".pyd"]  # Расширения которые нужно загрузить
    
    
    def __init__(self,
                caption: str | bytes,
                point: tuple[int, int] | None = None,
                size: tuple[int, int] = (400, 300), 
                color: tuple[int, int, int] = (255, 255, 255), 
                scene: list[_T] | None = None, 
                *, 
                fps: int | float = 60, 
                mods_dir: str | None = None, 
                flags: int = 0
                ):
        """
        Инициализация главного класса управление окном
        
        Args:
            size (tuple[int, int]): размеры окна (width, height)
            color (tuple[int, int, int]): Цветовая палитра RGB заднего фона
            scene (list[T] | None): список классов сцен наследованные от главного класса (Scene)
            fps (int | float): кадры в секунду
            mod_dir (str | None): путь к папке с модами
            kwargs_set_mode (KwargsSetMode | None): параметры для создание окна (pg.display.set_mode)
        """
        self.mods_dir = mods_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mods')
        self._mod = not mods_dir is None
        super().__init__(caption, point, size, color, scene, fps=fps, flags=flags)

    def init(self, win: Surface) -> None:
        if self._mod:
            self.load_mods()
            for mod in self.mods_list:
                mod.start()
        
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

        for filename in os.listdir(self.mods_dir):
            if max([filename.endswith(obf) for obf in self.mod_load]):
                spec = util.spec_from_file_location(f"{filename[:-3]}", os.path.join(self.mods_dir, filename))
                mod = util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, 'Main'):
                    try:
                        structure: FrameMod = mod.Main(self)
                        self.mods_list.append(structure)
                    except Exception as e:
                        for frame in extract_tb(e.__traceback__):
                            printError(f"[{mod.__name__}] [{frame.name}] {e}")

if __name__ == '__main__':
    import multiprocessing
    import sys
    
    multiprocessing.freeze_support()
    
    if getattr(sys, 'frozen', False):
        os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
    
    App().start()