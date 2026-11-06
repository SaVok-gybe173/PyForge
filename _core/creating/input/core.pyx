
cdef class InputTextCore:
    def __init__(self, str text = ""):
        self._text = text
        self._shift = 0
        self.clear_selection()
    
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, text):
        self._text = text
        if self._shift >= len(text):
            self._shift = len(text)
    
    cpdef void addText(self, str text):
        """Вставка с заменой выделения (если оно есть)."""
        if self.has_selection():
            self.delete_selection()
        self._text = self._text[:self._shift] + text + self._text[self._shift:]
        self._shift += len(text)
        self.clear_selection()

    cpdef bint backText(self):
        if self.has_selection():
            self.delete_selection()
            return True
        if self._shift > 0:
            self._text = self._text[:self._shift-1] + self._text[self._shift:]
            self._shift -= 1
            return True
        return False

    cpdef bint delText(self):
        """Удалит символ или удали выделенную часть"""
        if self.has_selection():
            self.delete_selection()
            return True
        if self._shift < len(self._text):
            self._text = self._text[:self._shift] + self._text[self._shift+1:]
            return True
        return False

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift):
        if shift <= 0:
            self._shift = 0
        elif shift >= len(self._text):
            self._shift = len(self._text)
        else:
            self._shift = shift

    cpdef bint ShiftRight(self, bint keep_selection=False):
        if not keep_selection and self.has_selection():
            # как в редакторах: стрелка вправо снимает выделение,
            # курсор встаёт в конец выделения
            self._shift = self.selectionX
            self.clear_selection()
            return True
        if self._shift < len(self._text):
            self._shift += 1
            if keep_selection:
                self.update_selection()
            return True
        return False

    cpdef bint ShiftLeft(self, bint keep_selection=False):
        if not keep_selection and self.has_selection():
            self._shift = self.selectionY
            self.clear_selection()
            return True
        if self._shift > 0:
            self._shift -= 1
            if keep_selection:
                self.update_selection()
            return True
        return False

    # выделение текста
    cpdef void clear_selection(self):
        self.selectionY = 0
        self.selectionX = 0
        self.selection = False

    cpdef void start_selection(self):
        """Начать выделение в текущей позиции курсора."""
        self.selectionY = self._shift
        self.selectionX = self._shift
        self.selection = True

    cpdef void update_selection(self):
        """Обновить конец выделения по текущему курсору."""
        if not self.selection:
            self.selectionY = self._shift
            self.selection = True
        self.selectionX = self._shift
        self._normalize()

    cdef void _normalize(self):
        # 0 <= selectionY <= selectionX <= len(_text)
        cdef int n = len(self._text)
        if self.selectionX < 0: self.selectionX = 0
        if self.selectionX > n: self.selectionX = n
        if self.selectionY < 0: self.selectionY = 0
        if self.selectionY > n: self.selectionY = n
        if self.selectionY > self.selectionX:
            self.selectionY, self.selectionX = self.selectionX, self.selectionY


    cpdef str get_selected_text(self):
        "Возвращает выделенный текст"
        if not self.selection:
            return ""
        self._normalize()
        return self._text[self.selectionY:self.selectionX]

    cpdef bint has_selection(self):
        return self.selection and self.selectionX > self.selectionY

    cpdef void select_all(self):
        self.selectionY = 0
        self.selectionX = len(self._text)
        self._shift = self.selectionX
        self.selection = True

    cpdef void delete_selection(self):
        """
        Удалить выделенный фрагмент
        курсор ставится на место выделения.
        """
        if not self.has_selection():
            self.clear_selection()
            return
        cdef int start = self.selectionY
        self._text = self._text[:start] + self._text[self.selectionX:]
        self._shift = start
        self.clear_selection()

    def __len__(self) -> int:
        return len(self._text)

    def __str__(self) -> str:
        return self._text

# позволяет работать попиксельно
cdef class GraphicsInputTextCore(InputTextCore):
    # доп фунция
    cpdef int hit_test(self, double x_px, list xs, list widths):
        """
        x_px  - x мыши в пикселях
        xs    - список x-начал каждого символа (из layout_text)
        widths - список advance ширин
        Возвращает индекс символа (0..len) для установки курсора.
        """
        cdef Py_ssize_t n = len(xs)
        if n == 0:
            return 0
        if x_px <= xs[0]:
            return 0
        for i in range(n - 1, -1, -1):
            if xs[i] <= x_px:
                if x_px > xs[i] + widths[i] * 0.5: # если клик ближе к правому краю символа - ставим после него
                    return i + 1
                return i
        return n

    cpdef void set_selection(self, int anchor, int cursor):
        """Установить выделение из двух индексов (для мыши).
        Если anchor == cursor - это каретка, выделение пустое."""
        cdef int n = len(self._text)
        if anchor < 0: anchor = 0
        elif anchor > n: anchor = n
        if cursor < 0: cursor = 0
        elif cursor > n: cursor = n

        self.selectionY = min(anchor, cursor)
        self.selectionX = max(anchor, cursor)
        self.selection = True
        self._shift = cursor     # курсор - где сейчас мышь