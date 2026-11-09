# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
# cython: nonecheck=False

from libc.stdint cimport uint32_t, uint8_t
from libc.math cimport sqrt, sin, cos, floor, fabs, M_PI
from libc.stdlib cimport malloc, free, realloc

from .surface cimport Surface
from ..pfmath.rect cimport Rect


#  Inline-примитивы (работают напрямую с памятью)

cdef inline uint32_t _map_color(Surface s, object color):
    cdef uint32_t v = 0
    if isinstance(color, (tuple, list)):
        v  = (<uint32_t>int(color[0]) << s._Rshift) & s._Rmask
        v |= (<uint32_t>int(color[1]) << s._Gshift) & s._Gmask
        v |= (<uint32_t>int(color[2]) << s._Bshift) & s._Bmask
        if s._Amask:
            if len(color) >= 4:
                v |= (<uint32_t>int(color[3]) << s._Ashift) & s._Amask
            else:
                v |= (<uint32_t>0xFF << s._Ashift) & s._Amask
    else:
        v = <uint32_t>int(color)
    return v


cdef inline void _put_px(Surface s, int x, int y, uint32_t color) noexcept:
    if 0 <= x < s._w and 0 <= y < s._h:
        s._px[y * s._pitch_u32 + x] = color


cdef inline uint32_t _get_px(Surface s, int x, int y) noexcept:
    return s._px[y * s._pitch_u32 + x]


cdef inline void _blend_px(Surface s, int x, int y,
                           uint32_t color, uint8_t a) noexcept:
    if a == 0 or not (0 <= x < s._w and 0 <= y < s._h):
        return
    cdef uint32_t* p = s._px + y * s._pitch_u32 + x
    cdef uint32_t dst = p[0]
    cdef uint32_t sr = (color & s._Rmask) >> s._Rshift
    cdef uint32_t sg = (color & s._Gmask) >> s._Gshift
    cdef uint32_t sb = (color & s._Bmask) >> s._Bshift
    cdef uint32_t dr = (dst & s._Rmask) >> s._Rshift
    cdef uint32_t dg = (dst & s._Gmask) >> s._Gshift
    cdef uint32_t db = (dst & s._Bmask) >> s._Bshift
    cdef uint32_t ia = 255 - a
    cdef uint32_t nr = (sr * a + dr * ia) // 255
    cdef uint32_t ng = (sg * a + dg * ia) // 255
    cdef uint32_t nb = (sb * a + db * ia) // 255
    p[0] = ((nr << s._Rshift) & s._Rmask) | \
           ((ng << s._Gshift) & s._Gmask) | \
           ((nb << s._Bshift) & s._Bmask) | \
           (dst & s._Amask)


# bounding box
cdef struct _BB:
    int minx, miny, maxx, maxy

cdef inline void _bb_init(_BB* b) noexcept:
    b.minx = 0x7fffffff
    b.miny = 0x7fffffff
    b.maxx = -1
    b.maxy = -1

cdef inline void _bb_upd(_BB* b, int x, int y) noexcept:
    if x < b.minx: b.minx = x
    if x > b.maxx: b.maxx = x
    if y < b.miny: b.miny = y
    if y > b.maxy: b.maxy = y

cdef inline Rect _bb_to_rect(_BB* b, int fx, int fy):
    cdef Rect r = Rect.__new__(Rect)
    if b.maxx < b.minx:
        r.x = fx; r.y = fy; r.w = 0; r.h = 0
    else:
        r.x = b.minx
        r.y = b.miny
        r.w = b.maxx - b.minx + 1
        r.h = b.maxy - b.miny + 1
    return r


# линии / заливка
cdef inline void _draw_line_1px(Surface s, int x0, int y0, int x1, int y1,
                                uint32_t color, _BB* bb) noexcept:
    cdef int dx = abs(x1 - x0), sx = 1 if x0 < x1 else -1
    cdef int dy = -abs(y1 - y0), sy = 1 if y0 < y1 else -1
    cdef int err = dx + dy, e2
    while True:
        if 0 <= x0 < s._w and 0 <= y0 < s._h:
            s._px[y0 * s._pitch_u32 + x0] = color
            _bb_upd(bb, x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x0 += sx
        if e2 <= dx:
            err += dx; y0 += sy


cdef void _wu_line(Surface s, uint32_t color,
                   double x0, double y0, double x1, double y1,
                   _BB* bb) noexcept:
    cdef bint steep = fabs(y1 - y0) > fabs(x1 - x0)
    cdef double t
    if steep:
        t = x0; x0 = y0; y0 = t
        t = x1; x1 = y1; y1 = t
    if x0 > x1:
        t = x0; x0 = x1; x1 = t
        t = y0; y0 = y1; y1 = t
    cdef double dx = x1 - x0
    cdef double gradient = 1.0 if dx == 0 else (y1 - y0) / dx
    cdef double intery = y0 + gradient
    cdef int x, y, xi, yi
    cdef double frac
    xi = <int>floor(x0)
    yi = <int>floor(y0)
    frac = y0 - yi
    if steep:
        _blend_px(s, yi, xi, color, <uint8_t>((1-frac)*255))
        _blend_px(s, yi+1, xi, color, <uint8_t>(frac*255))
        if 0 <= xi < s._w and 0 <= yi < s._h: _bb_upd(bb, yi, xi)
        if 0 <= xi < s._w and 0 <= yi+1 < s._h: _bb_upd(bb, yi+1, xi)
    else:
        _blend_px(s, xi, yi, color, <uint8_t>((1-frac)*255))
        _blend_px(s, xi, yi+1, color, <uint8_t>(frac*255))
        if 0 <= xi < s._w and 0 <= yi < s._h: _bb_upd(bb, xi, yi)
        if 0 <= xi < s._w and 0 <= yi+1 < s._h: _bb_upd(bb, xi, yi+1)
    x = xi + 1
    cdef int xend = <int>floor(x1)
    while x <= xend:
        yi = <int>floor(intery)
        frac = intery - yi
        if steep:
            _blend_px(s, yi, x, color, <uint8_t>((1-frac)*255))
            _blend_px(s, yi+1, x, color, <uint8_t>(frac*255))
            if 0 <= x < s._w and 0 <= yi < s._h: _bb_upd(bb, yi, x)
            if 0 <= x < s._w and 0 <= yi+1 < s._h: _bb_upd(bb, yi+1, x)
        else:
            _blend_px(s, x, yi, color, <uint8_t>((1-frac)*255))
            _blend_px(s, x, yi+1, color, <uint8_t>(frac*255))
            if 0 <= x < s._w and 0 <= yi < s._h: _bb_upd(bb, x, yi)
            if 0 <= x < s._w and 0 <= yi+1 < s._h: _bb_upd(bb, x, yi+1)
        intery += gradient
        x += 1


cdef inline void _fill_rect(Surface s, int x, int y, int w, int h,
                            uint32_t color, _BB* bb) noexcept:
    if w <= 0 or h <= 0:
        return
    cdef int x0 = x if x > 0 else 0
    cdef int y0 = y if y > 0 else 0
    cdef int x1 = x + w
    cdef int y1 = y + h
    if x1 > s._w: x1 = s._w
    if y1 > s._h: y1 = s._h
    if x0 >= x1 or y0 >= y1:
        return
    cdef int i, j
    cdef uint32_t* row
    for j in range(y0, y1):
        row = s._px + j * s._pitch_u32
        for i in range(x0, x1):
            row[i] = color
    _bb_upd(bb, x0, y0)
    _bb_upd(bb, x1 - 1, y1 - 1)


# дуга окружности (нужна в rect)
cdef void _draw_circle_arc(Surface s, int cx, int cy, int r,
                           double a0, double a1, int width,
                           uint32_t color, _BB* bb) noexcept:
    if r <= 0:
        return
    cdef double step = 1.0 / r
    if step > 0.1: step = 0.1
    cdef double a = a0 * M_PI / 180.0
    cdef double aend = a1 * M_PI / 180.0
    cdef int i, j, px, py
    while a <= aend:
        px = <int>(cx + r * cos(a))
        py = <int>(cy + r * sin(a))
        for i in range(width):
            for j in range(width):
                _put_px(s, px - i, py - j, color)
                _bb_upd(bb, px - i, py - j)
        a += step


#  Публичный API

def line(Surface surface, color, start_pos, end_pos, width=1):
    """line(surface, color, start_pos, end_pos, width=1) -> Rect"""
    cdef int x0 = <int>start_pos[0], y0 = <int>start_pos[1]
    cdef int x1 = <int>end_pos[0],   y1 = <int>end_pos[1]
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    cdef int w = <int>width
    cdef int half, i, ox, oy
    cdef bint steep
    if w < 1:
        return _bb_to_rect(&bb, x0, y0)
    if w == 1:
        _draw_line_1px(surface, x0, y0, x1, y1, c, &bb)
    else:
        half = w // 2
        steep = abs(y1 - y0) > abs(x1 - x0)
        for i in range(-half, w - half):
            if steep:
                ox = i; oy = 0
            else:
                ox = 0; oy = i
            _draw_line_1px(surface, x0 + ox, y0 + oy,
                           x1 + ox, y1 + oy, c, &bb)
    return _bb_to_rect(&bb, x0, y0)


def lines(Surface surface, color, closed, points, width=1):
    """lines(surface, color, closed, points, width=1) -> Rect"""
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    cdef int n = len(points)
    if n < 2:
        raise ValueError("len(points) < 2")
    cdef int i, x0, y0, x1, y1
    cdef int w = <int>width
    cdef int half, j, ox, oy
    cdef bint steep
    cdef int half2, j2, ox2, oy2
    cdef bint steep2

    x0 = <int>points[0][0]; y0 = <int>points[0][1]
    for i in range(1, n):
        x1 = <int>points[i][0]; y1 = <int>points[i][1]
        if w == 1:
            _draw_line_1px(surface, x0, y0, x1, y1, c, &bb)
        else:
            half = w // 2
            steep = abs(y1 - y0) > abs(x1 - x0)
            for j in range(-half, w - half):
                if steep: ox = j; oy = 0
                else:     ox = 0; oy = j
                _draw_line_1px(surface, x0+ox, y0+oy, x1+ox, y1+oy, c, &bb)
        x0 = x1; y0 = y1
    if closed and n > 1:
        x1 = <int>points[0][0]; y1 = <int>points[0][1]
        if w == 1:
            _draw_line_1px(surface, x0, y0, x1, y1, c, &bb)
        else:
            half2 = w // 2
            steep2 = abs(y1 - y0) > abs(x1 - x0)
            for j2 in range(-half2, w - half2):
                if steep2: ox2 = j2; oy2 = 0
                else:      ox2 = 0; oy2 = j2
                _draw_line_1px(surface, x0+ox2, y0+oy2,
                               x1+ox2, y1+oy2, c, &bb)
    return _bb_to_rect(&bb, <int>points[0][0], <int>points[0][1])


def aaline(Surface surface, color, start_pos, end_pos, width=1):
    """aaline(surface, color, start_pos, end_pos, width=1) -> Rect"""
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    _wu_line(surface,
             c,
             <double>start_pos[0], <double>start_pos[1],
             <double>end_pos[0],   <double>end_pos[1],
             &bb)
    return _bb_to_rect(&bb, <int>start_pos[0], <int>start_pos[1])


def aalines(Surface surface, color, closed, points):
    """aalines(surface, color, closed, points) -> Rect"""
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    cdef int n = len(points)
    if n < 2:
        raise ValueError("len(points) < 2")
    cdef int i
    cdef double x0, y0, x1, y1
    x0 = <double>points[0][0]; y0 = <double>points[0][1]
    for i in range(1, n):
        x1 = <double>points[i][0]; y1 = <double>points[i][1]
        _wu_line(surface, c, x0, y0, x1, y1, &bb)
        x0 = x1; y0 = y1
    if closed and n > 1:
        x1 = <double>points[0][0]; y1 = <double>points[0][1]
        _wu_line(surface, c, x0, y0, x1, y1, &bb)
    return _bb_to_rect(&bb, <int>points[0][0], <int>points[0][1])


def rect(Surface surface, color, rect, width=0,
         border_radius=-1,
         border_top_left_radius=-1,
         border_top_right_radius=-1,
         border_bottom_left_radius=-1,
         border_bottom_right_radius=-1):
    """rect(surface, color, rect, width=0, border_radius=-1,
            border_top_left_radius=-1, border_top_right_radius=-1,
            border_bottom_left_radius=-1, border_bottom_right_radius=-1) -> Rect"""
    cdef int rx, ry, rw, rh
    if isinstance(rect, (tuple, list)):
        rx = <int>rect[0]; ry = <int>rect[1]
        rw = <int>rect[2]; rh = <int>rect[3]
    else:
        rx = rect.x; ry = rect.y; rw = rect.w; rh = rect.h
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    cdef int w = <int>width
    if w < 0 or rw <= 0 or rh <= 0:
        return _bb_to_rect(&bb, rx, ry)

    cdef int br = <int>border_radius
    cdef int tl = <int>border_top_left_radius
    cdef int tr = <int>border_top_right_radius
    cdef int bl = <int>border_bottom_left_radius
    cdef int brr = <int>border_bottom_right_radius
    if tl < 0: tl = br
    if tr < 0: tr = br
    if bl < 0: bl = br
    if brr < 0: brr = br
    # без скруглений (быстрый путь)
    cdef int tw, th, maxr, cx, cy, r, dx, dy
    if br < 1 and tl < 1 and tr < 1 and bl < 1 and brr < 1:
        if w == 0:
            _fill_rect(surface, rx, ry, rw, rh, c, &bb)
        else:
            tw = w if w < rw else rw
            th = w if w < rh else rh
            _fill_rect(surface, rx, ry, rw, th, c, &bb)
            _fill_rect(surface, rx, ry + rh - th, rw, th, c, &bb)
            _fill_rect(surface, rx, ry + th, tw, rh - 2*th, c, &bb)
            _fill_rect(surface, rx + rw - tw, ry + th, tw, rh - 2*th, c, &bb)
        return _bb_to_rect(&bb, rx, ry)
    # скруглённый прямоугольник
    maxr = rw // 2
    if rh // 2 < maxr: maxr = rh // 2
    if tl  > maxr: tl  = maxr
    if tr  > maxr: tr  = maxr
    if bl  > maxr: bl  = maxr
    if brr > maxr: brr = maxr

    if w == 0:
        _fill_rect(surface, rx + tl, ry, rw - tl - tr, rh, c, &bb) # центральная полоса
        _fill_rect(surface, rx, ry + tl, tl, rh - tl - bl, c, &bb)          # боковые полосы
        _fill_rect(surface, rx + rw - tr, ry + tr, tr, rh - tr - brr, c, &bb)
        r = tl; cx = rx + tl; cy = ry + tl
        for dy in range(-r, 0):
            for dx in range(-r, 0):
                if dx*dx + dy*dy <= r*r:
                    _put_px(surface, cx+dx, cy+dy, c)
        r = tr; cx = rx + rw - tr; cy = ry + tr
        for dy in range(-r, 0):
            for dx in range(0, r):
                if dx*dx + dy*dy <= r*r:
                    _put_px(surface, cx+dx, cy+dy, c)
        r = bl; cx = rx + bl; cy = ry + rh - bl
        for dy in range(0, r):
            for dx in range(-r, 0):
                if dx*dx + dy*dy <= r*r:
                    _put_px(surface, cx+dx, cy+dy, c)
        r = brr; cx = rx + rw - brr; cy = ry + rh - brr
        for dy in range(0, r):
            for dx in range(0, r):
                if dx*dx + dy*dy <= r*r:
                    _put_px(surface, cx+dx, cy+dy, c)
    else:
        _fill_rect(surface, rx + tl, ry, rw - tl - tr, w, c, &bb)
        _fill_rect(surface, rx + bl, ry + rh - w, rw - bl - brr, w, c, &bb)
        _fill_rect(surface, rx, ry + tl, w, rh - tl - bl, c, &bb)
        _fill_rect(surface, rx + rw - w, ry + tr, w, rh - tr - brr, c, &bb)
        _draw_circle_arc(surface, rx + tl, ry + tl, tl, 90, 180, w, c, &bb)
        _draw_circle_arc(surface, rx + rw - tr, ry + tr, tr, 0, 90, w, c, &bb)
        _draw_circle_arc(surface, rx + bl, ry + rh - bl, bl, 180, 270, w, c, &bb)
        _draw_circle_arc(surface, rx + rw - brr, ry + rh - brr, brr, 270, 360, w, c, &bb)
    return _bb_to_rect(&bb, rx, ry)


cdef inline void _circle_points(Surface s, int cx, int cy, int x, int y,
                                uint32_t color, int width, _BB* bb) noexcept:
    cdef int i, j, px, py
    cdef int half = width // 2
    for i in range(-half, width - half):
        for j in range(-half, width - half):
            px = cx + x + i; py = cy + y + j
            _put_px(s, px, py, color); _bb_upd(bb, px, py)
            px = cx - x + i; py = cy + y + j
            _put_px(s, px, py, color); _bb_upd(bb, px, py)
            px = cx + x + i; py = cy - y + j
            _put_px(s, px, py, color); _bb_upd(bb, px, py)
            px = cx - x + i; py = cy - y + j
            _put_px(s, px, py, color); _bb_upd(bb, px, py)
            px = cx + y + i; py = cy + x + j
            _put_px(s, px, py, color); _bb_upd(bb, px, py)
            px = cx - y + i; py = cy + x + j
            _put_px(s, px, py, color); _bb_upd(bb, px, py)
            px = cx + y + i; py = cy - x + j
            _put_px(s, px, py, color); _bb_upd(bb, px, py)
            px = cx - y + i; py = cy - x + j
            _put_px(s, px, py, color); _bb_upd(bb, px, py)


def circle(Surface surface, color, center, radius, width=0,
           draw_top_right=False, draw_top_left=False,
           draw_bottom_left=False, draw_bottom_right=False):
    """circle(surface, color, center, radius, width=0,
              draw_top_right=False, draw_top_left=False,
              draw_bottom_left=False, draw_bottom_right=False) -> Rect"""
    cdef int cx = <int>center[0], cy = <int>center[1]
    cdef int r = <int>radius
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    if r < 1:
        return _bb_to_rect(&bb, cx, cy)
    cdef int w = <int>width
    cdef int x = r, y = 0, err = 0
    while x >= y:
        if w == 0:
            _fill_rect(surface, cx - x, cy + y, 2*x + 1, 1, c, &bb)
            _fill_rect(surface, cx - x, cy - y, 2*x + 1, 1, c, &bb)
            _fill_rect(surface, cx - y, cy + x, 2*y + 1, 1, c, &bb)
            _fill_rect(surface, cx - y, cy - x, 2*y + 1, 1, c, &bb)
        else:
            _circle_points(surface, cx, cy, x, y, c, w, &bb)
        y += 1
        err += 1 + 2*y
        if 2*(err - x) + 1 > 0:
            x -= 1
            err += 1 - 2*x
    return _bb_to_rect(&bb, cx, cy)


cdef inline void _wu_circle_pt(Surface s, int x, int y,
                               uint32_t color, _BB* bb) noexcept:
    _blend_px(s, x, y, color, 255)
    _bb_upd(bb, x, y)


cdef void _wu_circle(Surface s, int cx, int cy, double r,
                     uint32_t color, _BB* bb) noexcept:
    cdef int x = <int>r
    cdef int y = 0
    cdef double d = 1.0 - r
    while x >= y:
        _wu_circle_pt(s, cx + x, cy + y, color, bb)
        _wu_circle_pt(s, cx + y, cy + x, color, bb)
        _wu_circle_pt(s, cx - y, cy + x, color, bb)
        _wu_circle_pt(s, cx - x, cy + y, color, bb)
        _wu_circle_pt(s, cx - x, cy - y, color, bb)
        _wu_circle_pt(s, cx - y, cy - x, color, bb)
        _wu_circle_pt(s, cx + y, cy - x, color, bb)
        _wu_circle_pt(s, cx + x, cy - y, color, bb)
        y += 1
        if d < 0:
            d += 2*y + 1
        else:
            x -= 1
            d += 2*(y - x) + 1


def aacircle(Surface surface, color, center, radius, width=0,
             draw_top_right=False, draw_top_left=False,
             draw_bottom_left=False, draw_bottom_right=False):
    """aacircle(surface, color, center, radius, width=0, ...) -> Rect"""
    cdef int cx = <int>center[0], cy = <int>center[1]
    cdef double r = <double>radius
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    if r < 1:
        return _bb_to_rect(&bb, cx, cy)
    _wu_circle(surface, cx, cy, r, c, &bb)
    return _bb_to_rect(&bb, cx, cy)


def ellipse(Surface surface, color, rect, width=0):
    """ellipse(surface, color, rect, width=0) -> Rect"""
    cdef int rx, ry, rw, rh
    if isinstance(rect, (tuple, list)):
        rx = <int>rect[0]; ry = <int>rect[1]
        rw = <int>rect[2]; rh = <int>rect[3]
    else:
        rx = rect.x; ry = rect.y; rw = rect.w; rh = rect.h
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    cdef int w = <int>width
    if w < 0 or rw <= 0 or rh <= 0:
        return _bb_to_rect(&bb, rx, ry)
    cdef double cx = rx + rw * 0.5
    cdef double cy = ry + rh * 0.5
    cdef double ax = rw * 0.5
    cdef double ay = rh * 0.5
    cdef int steps = <int>(rw + rh)
    if steps < 64: steps = 64
    cdef int i, ix, iy, x1
    cdef double a, px, py
    if w == 0:
        for iy in range(ry, ry + rh):
            py = (iy - cy) / ay
            if py < -1.0 or py > 1.0: continue
            px = ax * sqrt(1.0 - py*py)
            ix = <int>(cx - px)
            x1 = <int>(cx + px)
            _fill_rect(surface, ix, iy, x1 - ix + 1, 1, c, &bb)
    else:
        for i in range(steps):
            a = 2.0 * M_PI * i / steps
            ix = <int>(cx + ax * cos(a))
            iy = <int>(cy + ay * sin(a))
            _put_px(surface, ix, iy, c)
            _bb_upd(&bb, ix, iy)
    return _bb_to_rect(&bb, rx, ry)


def arc(Surface surface, color, rect, start_angle, stop_angle, width=1):
    """arc(surface, color, rect, start_angle, stop_angle, width=1) -> Rect"""
    cdef int rx, ry, rw, rh
    if isinstance(rect, (tuple, list)):
        rx = <int>rect[0]; ry = <int>rect[1]
        rw = <int>rect[2]; rh = <int>rect[3]
    else:
        rx = rect.x; ry = rect.y; rw = rect.w; rh = rect.h
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    cdef int w = <int>width
    if w <= 0 or rw <= 0 or rh <= 0:
        return _bb_to_rect(&bb, rx, ry)
    cdef double cx = rx + rw * 0.5
    cdef double cy = ry + rh * 0.5
    cdef double ax = rw * 0.5
    cdef double ay = rh * 0.5
    cdef double a0 = <double>start_angle
    cdef double a1 = <double>stop_angle
    if a0 > a1:
        a1 += 2.0 * M_PI
    if a0 == a1:
        return _bb_to_rect(&bb, rx, ry)
    cdef int steps = <int>(rw + rh)
    if steps < 64: steps = 64
    cdef int i, j, ix, iy
    cdef double a
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        ix = <int>(cx + ax * cos(a))
        iy = <int>(cy + ay * sin(a))
        for j in range(w):
            _put_px(surface, ix, iy + j, c)
            _bb_upd(&bb, ix, iy + j)
    return _bb_to_rect(&bb, rx, ry)


def polygon(Surface surface, color, points, width=0):
    """polygon(surface, color, points, width=0) -> Rect"""
    cdef int n = len(points)
    if n < 3:
        raise ValueError("len(points) < 3")
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    cdef int w = <int>width
    if w < 0:
        return _bb_to_rect(&bb, <int>points[0][0], <int>points[0][1])

    cdef int i, j, k, x0, y0, x1, y1
    cdef int miny = 0x7fffffff, maxy = -1
    cdef int y, cnt, xint
    cdef int* xs = NULL
    # контур
    x0 = <int>points[0][0]; y0 = <int>points[0][1]
    for i in range(1, n):
        x1 = <int>points[i][0]; y1 = <int>points[i][1]
        _draw_line_1px(surface, x0, y0, x1, y1, c, &bb)
        x0 = x1; y0 = y1
    x1 = <int>points[0][0]; y1 = <int>points[0][1]
    _draw_line_1px(surface, x0, y0, x1, y1, c, &bb)

    if w == 0:
        for i in range(n):
            y0 = <int>points[i][1]
            if y0 < miny: miny = y0
            if y0 > maxy: maxy = y0
        if miny < 0: miny = 0
        if maxy >= surface._h: maxy = surface._h - 1
        xs = <int*>malloc(n * sizeof(int))
        if xs == NULL:
            return _bb_to_rect(&bb, <int>points[0][0], <int>points[0][1])
        for y in range(miny, maxy + 1):
            cnt = 0
            for i in range(n):
                x0 = <int>points[i][0]; y0 = <int>points[i][1]
                x1 = <int>points[(i+1) % n][0]
                y1 = <int>points[(i+1) % n][1]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xint = x0 + (y - y0) * (x1 - x0) // (y1 - y0)
                    xs[cnt] = xint; cnt += 1
            for k in range(1, cnt): # сортировка вставками
                xint = xs[k]
                j = k - 1
                while j >= 0 and xs[j] > xint:
                    xs[j+1] = xs[j]; j -= 1
                xs[j+1] = xint
            k = 0
            while k + 1 < cnt:
                _fill_rect(surface, xs[k], y, xs[k+1] - xs[k] + 1, 1, c, &bb)
                k += 2
        free(xs)
    return _bb_to_rect(&bb, <int>points[0][0], <int>points[0][1])


def flood_fill(Surface surface, color, start_pos):
    """flood_fill(surface, color, start_pos) -> Rect"""
    cdef int sx = <int>start_pos[0], sy = <int>start_pos[1]
    cdef uint32_t c = _map_color(surface, color)
    cdef _BB bb
    _bb_init(&bb)
    if not (0 <= sx < surface._w and 0 <= sy < surface._h):
        return _bb_to_rect(&bb, sx, sy)

    cdef uint32_t old = _get_px(surface, sx, sy)
    if old == c:
        return _bb_to_rect(&bb, sx, sy)

    cdef int w = surface._w
    cdef int h = surface._h
    cdef int pitch = surface._pitch_u32
    cdef uint32_t* px = surface._px

    cdef int cap = w * h
    if cap > (1 << 20): cap = 1 << 20
    cdef int* stack = <int*>malloc(cap * 2 * sizeof(int))
    if stack == NULL:
        return _bb_to_rect(&bb, sx, sy)
    cdef int sp = 0
    stack[0] = sx; stack[1] = sy; sp = 1

    cdef int x, y, xl, xr, i
    cdef int* newstack
    while sp > 0:
        sp -= 1
        x = stack[sp*2]; y = stack[sp*2+1]
        if px[y*pitch + x] != old:
            continue
        xl = x
        while xl > 0 and px[y*pitch + xl - 1] == old:
            xl -= 1
        xr = x
        while xr < w - 1 and px[y*pitch + xr + 1] == old:
            xr += 1
        for i in range(xl, xr + 1):
            px[y*pitch + i] = c
        _bb_upd(&bb, xl, y)
        _bb_upd(&bb, xr, y)
        if y > 0:
            for i in range(xl, xr + 1):
                if px[(y-1)*pitch + i] == old:
                    if sp >= cap:
                        cap *= 2
                        newstack = <int*>realloc(stack, cap * 2 * sizeof(int))
                        if newstack == NULL:
                            free(stack)
                            return _bb_to_rect(&bb, sx, sy)
                        stack = newstack
                    stack[sp*2] = i; stack[sp*2+1] = y - 1; sp += 1
        if y < h - 1:
            for i in range(xl, xr + 1):
                if px[(y+1)*pitch + i] == old:
                    if sp >= cap:
                        cap *= 2
                        newstack = <int*>realloc(stack, cap * 2 * sizeof(int))
                        if newstack == NULL:
                            free(stack)
                            return _bb_to_rect(&bb, sx, sy)
                        stack = newstack
                    stack[sp*2] = i; stack[sp*2+1] = y + 1; sp += 1

    free(stack)
    return _bb_to_rect(&bb, sx, sy)