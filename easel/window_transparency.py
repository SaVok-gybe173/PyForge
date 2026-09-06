import pygame
from ..logger import printError
try:
    import win32api
    import win32con
    import win32gui
except ImportError:
    win32api = None
    win32con = None
    win32gui = None
    printError("Модули pywin32 не найдены. Функциональность прозрачности окна не будет работать.")

def set_window_transparency(hwnd = None, alpha_value = 255):
    """
    Функция для установки прозрачности окна (только для Windows)
    """
    if hwnd is None: 
        hwnd = pygame.display.get_wm_info()['window']
    if win32api and win32con and win32gui:
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if not (ex_style & win32con.WS_EX_LAYERED):
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, alpha_value, win32con.LWA_ALPHA)
        return True
    else:
        return False

