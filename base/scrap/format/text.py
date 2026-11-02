from .basic import ClipboardData

class Text(ClipboardData):
    mime_types = ("text/plain",)

    def __init__(self, text: str):
        self.text = text

    def to_bytes(self, mime: str = "text/plain") -> bytes:
        return self.text.encode("utf-8")

    @classmethod
    def from_bytes(cls, mime: str, data: bytes) -> "Text":
        return cls(data.decode("utf-8"))
