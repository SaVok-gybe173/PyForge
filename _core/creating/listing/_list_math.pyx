# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False

"""Математическое ядро списка. Работает с memoryview array('q')."""

from array import array as _pyarray

def build_prefix(const long long[:] sizes, int distance=0):
    """
    prefix[i] = координата начала элемента i в контенте.
    prefix[0] = 0; prefix[i+1] = prefix[i] + sizes[i] + distance.
    Возвращает array('q').
    """
    cdef Py_ssize_t n = sizes.shape[0]
    cdef long long acc = 0
    cdef Py_ssize_t i

    result = _pyarray('q', [0]) * n        # n нулей, создаётся в C
    cdef long long[:] pv = result          # прямой доступ к буферу

    for i in range(n):
        pv[i] = acc
        acc += sizes[i] + distance
    return result


def total_length(const long long[:] prefix, const long long[:] sizes):
    cdef Py_ssize_t n = sizes.shape[0]
    if n == 0: return 0
    return prefix[n - 1] + sizes[n - 1]


def find_visible_range(const long long[:] prefix, const long long[:] sizes,
                       long long scroll_offset, long long view_length):
    """
    Возвращает (start, end) включительно. Если ничего не видно — (n, n-1).
    O(log n) через бинарный поиск.
    """
    cdef Py_ssize_t n = sizes.shape[0]
    if n == 0: return (0, -1)
    cdef long long view_end = scroll_offset + view_length
    cdef Py_ssize_t lo, hi, mid

    # первый i, у которого prefix[i] + sizes[i] > scroll_offset
    lo = 0; hi = n
    while lo < hi:
        mid = (lo + hi) >> 1
        if prefix[mid] + sizes[mid] > scroll_offset: hi = mid
        else: lo = mid + 1
    cdef Py_ssize_t start = lo

    # последний i, у которого prefix[i] < view_end
    lo = 0; hi = n
    while lo < hi:
        mid = (lo + hi) >> 1
        if prefix[mid] < view_end: lo = mid + 1
        else: hi = mid
    cdef Py_ssize_t end = lo - 1

    if start > end: return (n, n - 1)
    return (start, end)


def find_index_at(const long long[:] prefix, const long long[:] sizes,
                  long long content_pos):
    """Индекс элемента, содержащего content_pos, либо -1"""
    cdef Py_ssize_t n = sizes.shape[0]
    if n == 0:
        return -1
    cdef Py_ssize_t lo = 0, hi = n, mid
    while lo < hi:
        mid = (lo + hi) >> 1
        if prefix[mid] <= content_pos: lo = mid + 1
        else: hi = mid
    cdef Py_ssize_t idx = lo - 1
    if idx < 0 or content_pos >= prefix[idx] + sizes[idx]: return -1
    return idx


def scroll_metrics(long long total_length, long long view_length, int min_thumb):
    """(max_scroll, thumb_size, thumb_travel)."""
    cdef int thumb_size
    cdef long long max_scroll = total_length - view_length
    if max_scroll < 0: max_scroll = 0
    if total_length <= view_length:
        thumb_size = <int>view_length
    else:
        thumb_size = <int>((view_length * view_length) // total_length)
        if thumb_size < min_thumb: thumb_size = min_thumb
        if thumb_size > view_length: thumb_size = <int>view_length
    return (max_scroll, thumb_size, <int>view_length - thumb_size)


def thumb_from_scroll(long long scroll, long long max_scroll, int thumb_travel):
    if max_scroll <= 0 or thumb_travel <= 0: return 0
    return <int>((scroll * thumb_travel) // max_scroll)

def scroll_from_thumb(int thumb, long long max_scroll, int thumb_travel):
    if thumb_travel <= 0: return 0
    return (thumb * max_scroll) // thumb_travel

def clamp(long long v, long long lo, long long hi):
    if v < lo: return lo
    if v > hi: return hi
    return v

