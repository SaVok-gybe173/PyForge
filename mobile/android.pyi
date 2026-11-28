"""
Stub-файл для модуля `android` (python-for-android).

Предоставляет доступ к функциям Android: вибрация, датчики, клавиатура,
информация об устройстве и т.п.
"""

from typing import Any, Callable, Optional, Tuple


# вибрация

def vibrate(seconds: float) -> None:
    """Включить вибрацию на `seconds` секунд. Требует разрешения VIBRATE."""


# акселерометр

def accelerometer_enable(enable: bool) -> None:
    """Включить (`True`) или выключить (`False`) акселерометр."""

def accelerometer_reading() -> Tuple[float, float, float]:
    """
    Получить текущее ускорение по трём осям.

    Returns:
        (x, y, z) - ускорение в м/с² (или условных единицах Android).
    """


# информация об устройстве

def get_dpi() -> int:
    """Вернуть DPI (dots per inch) экрана устройства."""

def get_buildinfo() -> dict[str, str]:
    """
    Информация о сборке Android.

    Returns:
        Словарь с ключами: MANUFACTURER, MODEL, VERSION.RELEASE, VERSION.SDK_INT и др.
    """


# экранная клавиатура

def show_keyboard(
    target: Any,
    input_type: str = "text",
) -> None:
    """
    Показать экранную клавиатуру для указанного виджета/окна.

    Args:
        target: Объект-виджет (обычно из Kivy) или иной target для IME.
        input_type: Тип ввода:
            'text', 'number', 'url', 'mail', 'datetime', 'tel', 'decimal', 'address'.
    """

def hide_keyboard() -> None:
    """Скрыть экранную клавиатуру."""


# другие функции

def get_android_version() -> str:
    """Вернуть версию Android (например, '13')."""
    ...

def get_device_orientation() -> int:
    """
    Текущая ориентация устройства.

    Значения (см. android.content.res.Configuration):
        1 - портретная, 2 - ландшафтная, 0 - не определена.
    """
    ...

def get_activity() -> Any:
    """Вернуть ссылку на текущую Activity (jnius-обёртку)."""
    ...


# cсылки на Activity и Context (заполняются при инициализации)
mActivity: Any
"""Ссылка на текущую Activity (jnius.JavaClass). Доступна после инициализации приложения."""
mContext: Any
"""Ссылка на контекст приложения (jnius.JavaClass)."""