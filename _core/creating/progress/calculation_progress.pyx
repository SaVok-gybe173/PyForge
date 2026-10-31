# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
# cython: nonecheck=False


cdef class ProgressBarCalc:
    cdef bint   _is_quantity
    cdef int    _quantity_main
    cdef int    _quantity
    cdef double _percent          # 0..100
    cdef int    _pixel_progress

    def __cinit__(self):
        self._is_quantity    = False
        self._quantity_main  = 100
        self._quantity       = 0
        self._percent        = 0.0
        self._pixel_progress = 0

    cpdef void update_progress(self, width_height):
        """
        Пересчитать _pixel_progress из текущего состояния и переданной геометрии.
        width_height — (w, h).
        """
        cdef double p = self._percent
        if p > 100.0:
            p = 100.0
        elif p < 0.0:
            p = 0.0

        if self._is_quantity:
            if self._quantity_main <= 0:
                self._quantity_main = 100

            if self._quantity > self._quantity_main:
                self._quantity = self._quantity_main
            elif self._quantity < 0:
                self._quantity = 0

            if self._quantity == 0:
                p = 0.0
            else:
                p = (<double>self._quantity / <double>self._quantity_main) * 100.0

        self._percent = p

        cdef int w = <int>width_height[0]
        cdef int h = <int>width_height[1]
        cdef double scale = p * 0.01
        if w > h:
            self._pixel_progress = <int>(scale * w)
        else:
            self._pixel_progress = <int>(scale * h)

    cpdef void math_quantity(self):
        if self._is_quantity:
            self._quantity = <int>(self._quantity_main * (self._percent * 0.01))

    # pixel/percent
    cpdef void set_pixel(self, pixel):
        self._pixel_progress = <int>pixel

    cpdef int get_pixel(self):
        return self._pixel_progress

    cpdef void set_percent(self, percent):
        self._percent = <double>percent
        # update_progress вызывается снаружи при рендере

    cpdef double get_percent(self):
        return self._percent

    cpdef void add_percent(self, percent):
        self._percent += <double>percent

    # quantity
    cpdef void set_quantity_main(self, quantity):
        self._is_quantity   = True
        self._quantity_main = <int>quantity

    cpdef int get_quantity_main(self):
        return self._quantity_main

    cpdef void add_quantity_main(self, quantity):
        self._is_quantity   = True
        self._quantity_main += <int>quantity

    cpdef int get_quantity(self):
        return self._quantity

    cpdef void set_quantity(self, quantity):
        self._is_quantity = True
        self._quantity    = <int>quantity

    cpdef void add_quantity(self, quantity):
        self._is_quantity = True
        self._quantity   += <int>quantity

    cpdef void clear_quantity(self):
        self._is_quantity = True
        self._quantity    = 0

    cpdef void del_quantity(self):
        self._quantity      = 0
        self._quantity_main = 100
        self._is_quantity   = False