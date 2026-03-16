import sys
if sys.maxsize > 2**32:
    try:
        from .x64 import _Figur 
    except ImportError:
        try:
            from x64 import _Figur
        except ModuleNotFoundError:
            print(1)
else:
    print("100 - Нет для 32 битной системы")