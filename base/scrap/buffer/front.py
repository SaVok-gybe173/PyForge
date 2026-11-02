from .basic import ClipboardBackend
from ..format import ClipboardData
import os, sys

def _make_backend() -> ClipboardBackend:
    if sys.platform == "win32":
        from .clipboard.win import WindowsClipboard
        return WindowsClipboard()
    if sys.platform == "darwin":
        from .mac import MacClipboard
        return MacClipboard()
    if "ANDROID_ROOT" in os.environ:
        from .android import AndroidClipboard
        return AndroidClipboard()
    if sys.platform == "ios":
        from .ios import IOSClipboard
        return IOSClipboard()
    from .linux import LinuxClipboard
    return LinuxClipboard()

_backend: ClipboardBackend | None = None

def _get() -> ClipboardBackend:
    global _backend
    if _backend is None:
        _backend = _make_backend()
    return _backend

def copy(data: ClipboardData) -> None:
    _get().set(data)

def paste(mime: str = "text/plain") -> ClipboardData | None:
    return _get().get(mime)