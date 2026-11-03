# clipboard/win.py
import ctypes
import struct
from ctypes import wintypes
from pathlib import Path
from PIL import Image
import io

from ...format import ClipboardData, Text, FileList, Png
from ..basic import ClipboardBackend

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32

# константы форматов
CF_UNICODETEXT = 13
CF_DIB = 8
CF_HDROP = 15

# настройка типов функций WinAPI
user32.OpenClipboard.argtypes = [wintypes.HWND]
user32.OpenClipboard.restype = wintypes.BOOL
user32.CloseClipboard.restype = wintypes.BOOL
user32.EmptyClipboard.restype = wintypes.BOOL
user32.IsClipboardFormatAvailable.argtypes = [wintypes.UINT]
user32.IsClipboardFormatAvailable.restype = wintypes.BOOL
user32.GetClipboardData.argtypes = [wintypes.UINT]
user32.GetClipboardData.restype = wintypes.HANDLE
user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
user32.SetClipboardData.restype = wintypes.HANDLE

kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalLock.restype = wintypes.LPVOID
kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalUnlock.restype = wintypes.BOOL
kernel32.GlobalSize.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalSize.restype = ctypes.c_size_t

shell32.DragQueryFileW.argtypes = [wintypes.HANDLE, wintypes.UINT, ctypes.c_void_p, wintypes.UINT]
shell32.DragQueryFileW.restype = wintypes.UINT

GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040


class WindowsClipboard(ClipboardBackend):
    """Бэкенд для Windows: CF_UNICODETEXT, CF_HDROP, CF_DIB/PNG."""

    def set(self, data: ClipboardData) -> None:
        if not user32.OpenClipboard(None):
            raise RuntimeError("Не удалось открыть буфер обмена Windows")
        try:
            user32.EmptyClipboard()
            if isinstance(data, Text):      self._set_text(data.text)
            elif isinstance(data, FileList):self._set_files(data.paths)
            elif isinstance(data, Png):     self._set_png(data.data)
            else: raise TypeError(f"WindowsClipboard не умеет формат {type(data).__name__}")
        finally:
            user32.CloseClipboard()

    #внутренние методы для каждого формата
    def _set_text(self, text: str) -> None:
        raw = text.encode("utf-16-le") + b"\x00\x00"
        h = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(raw))
        p = kernel32.GlobalLock(h)
        ctypes.memmove(p, raw, len(raw))
        kernel32.GlobalUnlock(h)
        user32.SetClipboardData(CF_UNICODETEXT, h)

    def _set_files(self, paths: list[Path]) -> None:
        file_buffer = "\0".join(str(p.resolve()) for p in paths) + "\0\0"
        encoded = file_buffer.encode("utf-16-le")
        header = struct.pack("IIIII", 20, 0, 0, 0, 1)  # pFiles=20
        raw = header + encoded
        h = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(raw))
        p = kernel32.GlobalLock(h)
        ctypes.memmove(p, raw, len(raw))
        kernel32.GlobalUnlock(h)
        user32.SetClipboardData(CF_HDROP, h)

    def _set_png(self, png_bytes: bytes) -> None:
        try:
            bmp = io.BytesIO()
            Image.open(io.BytesIO(png_bytes)).save(bmp, format="BMP")
            dib = bmp.getvalue()[14:] # Пропускаем 14-байтовый BITMAPFILEHEADER, остаётся CF_DIB
            h = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(dib))
            p = kernel32.GlobalLock(h)
            ctypes.memmove(p, dib, len(dib))
            kernel32.GlobalUnlock(h)
            user32.SetClipboardData(CF_DIB, h)
        except Exception:
            h = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(png_bytes))
            ctypes.memmove(kernel32.GlobalLock(h), png_bytes, len(png_bytes))
            kernel32.GlobalUnlock(h)
            user32.SetClipboardData(user32.RegisterClipboardFormatW("PNG"), h)

    def get(self, mime: str) -> ClipboardData | None:
        if not user32.OpenClipboard(None):
            return None
        try:
            if mime == "text/plain":
                if not user32.IsClipboardFormatAvailable(CF_UNICODETEXT): return None
                h = user32.GetClipboardData(CF_UNICODETEXT)
                if not h: return None
                p = kernel32.GlobalLock(h)
                if not p: return None
                try:
                    text = ctypes.wstring_at(p).rstrip("\x00")
                finally:
                    kernel32.GlobalUnlock(h)
                return Text(text)

            if mime == "text/uri-list":
                if not user32.IsClipboardFormatAvailable(CF_HDROP): return None
                h = user32.GetClipboardData(CF_HDROP)
                if not h: return None
                count = shell32.DragQueryFileW(h, 0xFFFFFFFF, None, 0)
                if count == 0:
                    return None
                paths: list[Path] = []
                for i in range(count):
                    buf = ctypes.create_unicode_buffer(32768)
                    got = shell32.DragQueryFileW(h, i, buf, len(buf))
                    if got:
                        paths.append(Path(buf.value))
                return FileList(paths) if paths else None

            if mime == "image/png":
                fmt = user32.RegisterClipboardFormatW("PNG")
                if fmt and user32.IsClipboardFormatAvailable(fmt):
                    h = user32.GetClipboardData(fmt) 
                    if not h:
                        return None
                    p = kernel32.GlobalLock(h)
                    size = kernel32.GlobalSize(h)
                    try:
                        data = ctypes.string_at(p, size)
                    finally:
                        kernel32.GlobalUnlock(h)
                    return Png(data)

                if user32.IsClipboardFormatAvailable(CF_DIB):
                    try:
                        h = user32.GetClipboardData(CF_DIB)
                        if not h: return None
                        p = kernel32.GlobalLock(h)
                        size = kernel32.GlobalSize(h)
                        try:
                            dib = ctypes.string_at(p, size)
                        finally:
                            kernel32.GlobalUnlock(h)
                        bmp_header = struct.pack("<2sIHHI", b"BM", 14 + size, 0, 0, 14)
                        img = Image.open(io.BytesIO(bmp_header + dib))
                        out = io.BytesIO()
                        img.save(out, format="PNG")
                        return Png(out.getvalue())
                    except Exception:
                        return None
                if user32.IsClipboardFormatAvailable(CF_HDROP):
                    h = user32.GetClipboardData(CF_HDROP)
                    if not h:
                        return None
                    count = shell32.DragQueryFileW(h, 0xFFFFFFFF, None, 0)
                    for i in range(count):
                        buf = ctypes.create_unicode_buffer(32768)
                        if not shell32.DragQueryFileW(h, i, buf, len(buf)):
                            continue
                        p = Path(buf.value)
                        if p.suffix.lower() == ".png" and p.is_file():
                            return Png(p.read_bytes())
                return None

            return None
        finally:
            user32.CloseClipboard()

    def available(self) -> list[str]:
        result = []
        if not user32.OpenClipboard(None): return result
        try:
            if user32.IsClipboardFormatAvailable(CF_UNICODETEXT):
                result.append("text/plain")
            if user32.IsClipboardFormatAvailable(CF_HDROP):
                result.append("text/uri-list")
            if user32.IsClipboardFormatAvailable(CF_DIB):
                result.append("image/png")  # предлагаем как PNG через конвертацию
        finally:
            user32.CloseClipboard()
        return result