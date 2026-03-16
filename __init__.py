import os, sys
from typing import Final

try:
    from pygame import OPENGL, DOUBLEBUF
except ImportError as e:
    print("102 - error:", e)
    sys.exit(102)
        
OPENGL: Final[int] = DOUBLEBUF | OPENGL
del DOUBLEBUF

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
    import EaselPy.window
else:
    import EaselPy.strukture as window
'''
if _multiprocessing_activ:
    try:
        from .EaselPy.window import Window
    except ImportError:
        from EaselPy.window import Window
else:
    try:
        from .EaselPy.strukture import Window
    except ImportError:
        from EaselPy.strukture import Window

try:
    from .game_obgect import Game
except ImportError:
    from game_obgect import Game

try:
    from .mods.mod import FrameMod
except ImportError:
    from mods.mod import FrameMod

# используйте пути для импорта

from .EaselPy.strukture import Scene

from .pygames.creating.colisions import point_in_rounded_rect, check_rounded_rect_collision
from .pygames.creating.image import get_none_image, round_image, resize_image_with_aspect_ratio, extract_square_fast, extract_square



try:
    from .pygames.StGame.glk_3d.scene import degrees_to_radians, load_obj, Figure, get_figyre
except (ImportError , Exception) as e:
    print("101 - error:", e)

