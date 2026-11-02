# модуль для работы с буфером обмена

# система для работы с разными типами для буфера обмена
from .format import ClipboardData, FileList, Png, Text
from .buffer import ClipboardBackend, copy, paste

# модули от sdl2
from .sdl import (SetClipboardText, GetClipboardText, HasClipboardText,
                  SetPrimarySelectionText, GetPrimarySelectionText, HasPrimarySelectionText)
# оболочка над API sdl2
from .sdl import set_text_buffer, get_text_buffer

__all__ = [
    "ClipboardData",
    "FileList",
    "Png",
    "Text",
    "ClipboardBackend",
    "copy", "paste",
    "SetClipboardText", "GetClipboardText", "HasClipboardText",
    "SetPrimarySelectionText", "GetPrimarySelectionText", "HasPrimarySelectionText",
    "set_text_buffer", "get_text_buffer"
]