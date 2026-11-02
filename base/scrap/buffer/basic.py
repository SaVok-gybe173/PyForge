from abc import ABC, abstractmethod
from ..format import ClipboardData

class ClipboardBackend(ABC):
    @abstractmethod
    def set(self, data: ClipboardData) -> None: ...

    @abstractmethod
    def get(self, mime: str) -> ClipboardData | None: ...

    @abstractmethod
    def available(self) -> list[str]: ...