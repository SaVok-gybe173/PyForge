import os
import sys
import sdl2
from typing import Final

try:
    import multiprocessing
    def init():
        multiprocessing.freeze_support()
        if getattr(sys, 'frozen', False):
            os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
    _multiprocessing_activ = True
except Exception:
    def init():
        if getattr(sys, 'frozen', False):
            os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
    _multiprocessing_activ = False

from .__info__ import __version__

def is_admin():
    if sys.platform == "win32":
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    elif sys.platform == "darwin" or sys.platform.startswith("linux"):
        return os.geteuid() == 0
    else: # Для других ОС, предполагаем, что не админ
        return False

'''
if _multiprocessing_activ:
    import easel.window
else:
    import easel.strukture as window
'''
try:
    from .easel.window_processing import Window
except:
    from .easel.window import Window

from .easel.app import App
from .mods.mod import FrameMod

from .easel.window import Scene

from .cpu.creating.image import get_none_image, round_image, resize_image_with_aspect_ratio, extract_square_fast, extract_square