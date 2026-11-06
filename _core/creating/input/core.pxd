cdef class InputTextCore:
    cdef public str _text
    cdef public int _shift
    cdef int selectionX
    cdef int selectionY
    cdef bint selection

    cpdef void addText(self, str text)
    cpdef bint backText(self)
    cpdef bint delText(self)

    cpdef bint ShiftRight(self, bint keep_selection=*)
    cpdef bint ShiftLeft(self, bint keep_selection=*)

    cpdef void clear_selection(self)
    cpdef void start_selection(self)
    cpdef void update_selection(self)
    cdef void _normalize(self)
    cpdef str get_selected_text(self)
    cpdef bint has_selection(self)
    cpdef void select_all(self)
    cpdef void delete_selection(self)

cdef class GraphicsInputTextCore(InputTextCore):

    cpdef int hit_test(self, double x_px, list xs, list widths)
    cpdef void set_selection(self, int anchor, int cursor)