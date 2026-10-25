"""
Модуль для проверки платформы
"""
import sys
import os

def is_android():
    """
    Определяет, запущен ли Python-скрипт в среде Android.
    Учитывает распространенные способы запуска Python на Android:
    Kivy/Buildozer, Termux, Python-for-Android.
    """
    if not sys.platform.startswith('linux'):
        return False 
    if os.environ.get('KIVY_BUILD') == 'android':
        return True
    if os.environ.get('TERMUX_VERSION') is not None:
        return True
    try:
        import android 
        return True
    except ImportError:
        pass 
    return False

def is_linux():
    if not is_android():
        if sys.platform.startswith('linux'):
            return True
    return False

def is_window():
    if sys.platform.startswith('win32'):
        return True
    return False

def is_ios():
    if sys.platform == 'ios':
        return True
    return False

def is_macos():
    if sys.platform == 'darwin':
        return True
    return False