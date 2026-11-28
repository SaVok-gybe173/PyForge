"""
Константы ориентации экрана и подсказки для SDL.

Значения соответствуют android.content.pm.ActivityInfo.SCREEN_ORIENTATION_*
и могут передаваться в mActivity.setRequestedOrientation(...).
"""

from typing import Final


# Значения из android.content.pm.ActivityInfo

SCREEN_ORIENTATION_UNSPECIFIED: Final[int] = -1
"""Ориентация не задана - поведение по умолчанию системы."""

SCREEN_ORIENTATION_LANDSCAPE: Final[int] = 0
"""Ландшафт (обычный)."""

SCREEN_ORIENTATION_PORTRAIT: Final[int] = 1
"""Портрет (обычный)."""

SCREEN_ORIENTATION_USER: Final[int] = 2
"""Ориентация, выбранная пользователем."""

SCREEN_ORIENTATION_BEHIND: Final[int] = 3
"""Ориентация Activity, находящейся позади."""

SCREEN_ORIENTATION_SENSOR: Final[int] = 4
"""Определяется датчиком (акселерометром) - полный авто-поворот."""

SCREEN_ORIENTATION_NOSENSOR: Final[int] = 5
"""Игнорировать датчики."""

SCREEN_ORIENTATION_SENSOR_LANDSCAPE: Final[int] = 6
"""Датчик только для ландшафтных ориентаций."""

SCREEN_ORIENTATION_SENSOR_PORTRAIT: Final[int] = 7
"""Датчик только для портретных ориентаций."""

SCREEN_ORIENTATION_REVERSE_LANDSCAPE: Final[int] = 8
"""Обратный ландшафт (перевёрнутый на 180°)."""

SCREEN_ORIENTATION_REVERSE_PORTRAIT: Final[int] = 9
"""Обратный портрет (перевёрнутый на 180°)."""

SCREEN_ORIENTATION_FULL_SENSOR: Final[int] = 10
"""Полный авто-поворот по всем четырём направлениям (датчик)."""

SCREEN_ORIENTATION_USER_LANDSCAPE: Final[int] = 11
"""Пользовательский выбор среди ландшафтных ориентаций."""

SCREEN_ORIENTATION_USER_PORTRAIT: Final[int] = 12
"""Пользовательский выбор среди портретных ориентаций."""

SCREEN_ORIENTATION_FULL_USER: Final[int] = 13
"""Полный пользовательский выбор (все 4 направления)."""

SCREEN_ORIENTATION_LOCKED: Final[int] = 14
"""Ориентация зафиксирована в текущем положении (блокировка поворота)."""


# Значения SDL_HINT_ORIENTATIONS (строки для SDL_SetHint)

SDL_ORIENTATION_PORTRAIT: Final[bytes] = b"Portrait"
"""Только портретная ориентация (подсказка SDL)."""

SDL_ORIENTATION_LANDSCAPE: Final[bytes] = b"Landscape"
"""Только ландшафтная ориентация (подсказка SDL)."""

SDL_ORIENTATION_LANDSCAPE_LEFT: Final[bytes] = b"LandscapeLeft"
"""Ландшафт с поворотом влево (подсказка SDL)."""

SDL_ORIENTATION_LANDSCAPE_RIGHT: Final[bytes] = b"LandscapeRight"
"""Ландшафт с поворотом вправо (подсказка SDL)."""

SDL_ORIENTATION_PORTRAIT_UPSIDE_DOWN: Final[bytes] = b"PortraitUpsideDown"
"""Портрет «вверх ногами» (подсказка SDL)."""