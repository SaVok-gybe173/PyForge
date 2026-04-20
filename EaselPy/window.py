try:
    from .strukture import Window as _window
except ImportError:
    from strukture import Window as _window
import os
from multiprocessing import Process

#работает с pygame v2.0


class Window(_window):
    name = None
    daemon = False

    def start(self):
        if self.process is None or not self.process.is_alive():
            self.process = Process(target=self.run_window, name=self.name, daemon=self.daemon)
            self.process.start()
    def is_alive(self):
        if self.process is None:
            return False
        else:
            return self.process.is_alive()
    def join(self):
        if self.process is not None:
            self.process.join()
    def kill(self):
        try:
            super().kill()
        except Exception as e:
            print("[ERROR] [KILL]", e)
        self.process.kill()
            
if __name__ == '__main__':
    import multiprocessing, sys
    multiprocessing.freeze_support()
    
    if getattr(sys, 'frozen', False):
        os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
    
    # Создаем два окна с разными параметрами
    window1 = Window(color=(220, 110, 70))
    window2 = Window()

    window1.start()
    window2.start()

    window1.join()
    window2.join()