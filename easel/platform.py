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
    return sys.platform == "win32"

def is_ios():
    return sys.platform == 'ios'

def is_macos():
    return sys.platform == "darwin"