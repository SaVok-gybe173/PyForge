class ProgressBarCalc:
    """Калькулятор состояния прогресс-бара.

    Хранит счётчики (percent/quantity) и вычисляет длину заливки в пикселях.
    Геометрия передаётся снаружи в update_progress().
    """

    def __init__(self) -> None: ...

    def update_progress(self, width_height: tuple[int, int]) -> None:
        """Пересчитать _pixel_progress по текущему состоянию и (w, h).

        Если включён quantity-режим, _percent перевычисляется из
        _quantity/_quantity_main; иначе используется текущий _percent.
        Результат сохраняется в _pixel_progress (целое, усечённое).
        """

    def math_quantity(self) -> None:
        """Пересчитать _quantity из _percent (только в quantity-режиме)."""

    # pixel
    def set_pixel(self, pixel: int) -> None:
        """Установить _pixel_progress напрямую, без ограничений."""

    def get_pixel(self) -> int:
        """Текущая длина заливки в пикселях."""

    # percent
    def set_percent(self, percent: float) -> None:
        """Установить процент (0..100). update_progress не вызывается."""

    def get_percent(self) -> float:
        """Текущий процент (0..100)."""

    def add_percent(self, percent: float) -> None:
        """Прибавить к проценту (может выйти за 0..100 — клампится в update_progress)."""

    # quantity 
    def set_quantity_main(self, quantity: int) -> None:
        """Включить quantity-режим и задать «всего»."""

    def get_quantity_main(self) -> int:
        """Текущее значение «всего»."""

    def add_quantity_main(self, quantity: int) -> None:
        """Включить quantity-режим и прибавить к «всего»."""

    def get_quantity(self) -> int:
        """Текущее значение «сделано»."""

    def set_quantity(self, quantity: int) -> None:
        """Включить quantity-режим и задать «сделано»."""

    def add_quantity(self, quantity: int) -> None:
        """Включить quantity-режим и прибавить к «сделано»."""

    def clear_quantity(self) -> None:
        """Включить quantity-режим и сбросить «сделано» в 0."""

    def del_quantity(self) -> None:
        """Выключить quantity-режим; сбросить _quantity в 0, _quantity_main в 100."""