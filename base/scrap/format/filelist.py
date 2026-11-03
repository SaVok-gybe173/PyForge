from .basic import ClipboardData
from urllib.parse import urlparse, unquote
from pathlib import Path

class FileList(ClipboardData):
    mime_types = ("text/uri-list", "x-special/gnome-copied-files")

    def __init__(self, paths: list[Path | str] | Path | str):
        if isinstance(paths, (str, Path)): paths = [paths]
        self.paths: list[Path] = [self._p(x) for x in paths if str(x).strip()]

    @staticmethod
    def _p(x: Path | str) -> Path:
        if isinstance(x, Path): return x
        x = str(x).strip(); u = urlparse(x)
        return Path(unquote(u.path)) if u.scheme == "file" else (Path(x) if not u.scheme else Path(x))

    def to_bytes(self, mime: str = "text/uri-list") -> bytes:
        uris = "\r\n".join(p.resolve().as_uri() for p in self.paths)
        return f"copy\n{uris}".encode("utf-8") if mime == "x-special/gnome-copied-files" else uris.encode("utf-8")

    @classmethod
    def from_bytes(cls, mime: str, data: bytes) -> "FileList":
        text = data.decode("utf-8", errors="replace").strip()
        if not text: return cls([])
        if mime == "x-special/gnome-copied-files": text = "\n".join(text.splitlines()[1:])
        return cls([l.strip() for l in text.splitlines() if l.strip()])