from .basic import ClipboardData
from pathlib import Path

class FileList(ClipboardData):
    mime_types = ("text/uri-list", "x-special/gnome-copied-files")

    def __init__(self, paths: list[Path | str]):
        self.paths = paths

    def to_bytes(self, mime: str = "text/uri-list") -> bytes:
        uris = "\r\n".join(Path(p).as_uri() if isinstance(p, str) else p.as_uri() for p in self.paths)
        if mime == "x-special/gnome-copied-files":
            return f"copy\n{uris}".encode("utf-8")
        return uris.encode("utf-8")