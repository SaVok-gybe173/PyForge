"""
Stub-файл для PyJNIus (JNI-мост Python <=> Java на Android).

Позволяет получать доступ к Java-классам Android SDK через JNI.
Используется совместно с python-for-android.
"""

from typing import Any, Callable, Type, TypeVar, overload


_T = TypeVar("_T", bound="JavaClass")


class JavaException(Exception):
    """Исключение, выбрасываемое при ошибке в Java-коде."""
    classname: str
    """Полное имя Java-класса, где произошла ошибка (например, 'java.lang.NullPointerException')."""
    innermessage: str
    """Сообщение об ошибке из Java (аналог .getMessage())."""
    stacktrace: str
    """Стек-трейс Java как строка."""


class JavaObject:
    """Базовый объект, представляющий любой Java-объект (не класс-обёртку)."""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...


class JavaClass:
    """
    Базовый класс для описания Java-класса через наследование.

    Пример:
        class Rect(JavaClass):
            __javaclass__ = 'android/graphics/Rect'
            left = JavaField('I')
            def __init__(self, *args): ...
    """
    __javaclass__: str
    """Полное имя Java-класса в JNI-нотации (через '/'), например 'android/content/pm/ActivityInfo'."""

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...


class JavaMethod:
    """Описание экземплярного Java-метода внутри JavaClass."""
    signature: str
    """JNI-сигнатура (например, '(I)V' - принимает int, возвращает void)."""

    def __init__(self, signature: str, static: bool = False) -> None: ...


class JavaStaticMethod(JavaMethod):
    """Описание статического Java-метода."""


class JavaField:
    """Описание экземплярного Java-поля внутри JavaClass."""
    signature: str
    """JNI-сигнатура типа поля (например, 'I', 'Ljava/lang/String;')."""

    def __init__(self, signature: str, static: bool = False) -> None: ...


class JavaStaticField(JavaField):
    """Описание статического Java-поля."""


class PythonJavaClass:
    """
    Позволяет объявить Java-класс, реализуемый на Python.

    Используется для колбэков из Java в Python (например, интерфейсы слушателей).
    """
    __javainterfaces__: list[str]
    """Список полных имён Java-интерфейсов (JNI-нотация), которые реализует класс."""

    __javacontext__: str
    """Контекст загрузки класса: 'app' (по умолчанию) или 'system'."""


@overload
def autoclass(name: str, include_protected: bool = True, include_private: bool = True) -> Type[JavaClass]: ...
@overload
def autoclass(name: str, *, cache: bool = True, **kwargs: Any) -> Type[Any]: ...

def autoclass(name: str, include_protected: bool = True, include_private: bool = True) -> Type[JavaClass]:
    """
    Получить Python-обёртку над Java-классом по его имени.

    Args:
        name: Полное имя Java-класса, например 'android.content.pm.ActivityInfo'.
        include_protected: Включать protected-члены.
        include_private: Включать private-члены.

    Returns:
        Python-класс, через который доступны статические методы и поля Java-класса.
        Экземпляры этого класса можно создавать для доступа к экземплярным членам.

    Raises:
        JavaException: если класс не найден.
    """


def cast(destclass: Type[_T], obj: Any) -> _T:
    """
    Привести Java-объект к указанному типу.

    Полезно, когда autoclass вернул базовый JavaObject, а нужен конкретный интерфейс.

    Args:
        destclass: Целевой JavaClass-тип.
        obj: Java-объект (обычно JavaObject).

    Returns:
        Объект, приведённый к destclass.
    """


def find_javaclass(name: str) -> Type[JavaClass]:
    """Найти Java-класс по имени без инстанциирования (низкоуровневая функция)."""


def detach() -> None:
    """Отсоединить текущий Python-поток от JVM (вызывать перед завершением потока)."""
