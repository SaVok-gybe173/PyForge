"""
Общая структура

Слой	                        Что делает	                                                Пример
Формат данных (ClipboardData)   знает, как сериализоваться в bytes и MIME-тип	            Text, FileList, Png
Бэкенд  (ClipboardBackend)      знает, как ОС хранит данные (WinAPI, NSPasteboard, xclip)	WindowsClipboard, X11Clipboard
Фасад	                        выбирает бэкенд по платформе, даёт copy() / paste()	        copy(Text("hi"))
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import ClassVar, TypeVar

T = TypeVar("T", bound="ClipboardData")

class ClipboardData(ABC):
    """Базовый формат данных для буфера обмена"""
    mime_types: ClassVar[tuple[str, ...]] = () # MIME типы

    @abstractmethod
    def to_bytes(self, mime: str) -> bytes: ...

    @classmethod
    @abstractmethod
    def from_bytes(cls: type[T], mime: str, data: bytes) -> T: ...