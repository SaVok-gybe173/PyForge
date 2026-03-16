import sys

if sys.platform  == 'win32':
    from .windows.CalculateGL import _FigurGL, TextureGL