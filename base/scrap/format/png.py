from .basic import ClipboardData

class Png(ClipboardData):
    mime_types = ("image/png",)

    def __init__(self, data: bytes):
        self.data = data

    def to_bytes(self, mime: str = "image/png") -> bytes:
        return self.data

    @classmethod
    def from_bytes(cls, mime: str, data: bytes) -> "Png":
        return cls(data)