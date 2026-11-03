class InputTextCore:
    selectionX: int
    selectionY: int
    selection: bool

    def __init__(self, text: str = '') -> None: ...

    def addText(self, text: str) -> None:
        """Вставка с заменой выделения (если оно есть)."""

    def delText(self) -> bool:
        """Удалит символ или удали выделенную часть"""

    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, text: str) -> None: ...


    @property
    def shift(self) -> int: ...
    @shift.setter
    def shift(self, shift: int) -> None: ...

    def ShiftRight(self) -> bool:
        """
        Сдвиг на 1 в правую сторону
        """

    def ShiftLeft(self) -> bool:
        """
        Сдвиг на 1 в левую сторону
        """

    # выделение текста
    def clear_selection(self) -> None:
        "Очистка"

    def start_selection(self) -> None:
        """Начать выделение в текущей позиции курсора."""

    def update_selection(self) -> None:
        """Обновить конец выделения по текущему курсору."""

    def get_selected_text(self) -> str:
        "Возвращает выделенный текст"

    def has_selection(self) -> bool:
        "Проверяет на правильность выделения"

    def select_all(self) -> None:
        "Выделяет весь текст"

    def delete_selection(self):
        """
        Удалить выделенный фрагмент
        курсор ставится на место выделения.
        """