# cython: language_level=3
# cython: boundscheck=False
# cython: cdivision=True
# cython: initializedcheck=False
# cython: nonecheck=False

from libc.math cimport ceil

from .font cimport Font
from .table cimport glyph
from ...easel.surface cimport Surface
from ...easel.surface import SRCALPHA


cdef list _quad_bezier(tuple p0, tuple p1, tuple p2, int steps=16):
    cdef list result = []
    cdef int s
    cdef double t, mt
    for s in range(1, steps + 1):
        t = s / <double>steps
        mt = 1.0 - t
        result.append(( mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0], mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1],))
    return result


cdef list _contour_to_polygon(tuple points, int steps=16):
    if not points: return []

    start_idx = next((i for i, (_, _, on) in enumerate(points) if on), None)
    if start_idx is None:
        px = (points[-1][0] + points[0][0]) / 2
        py = (points[-1][1] + points[0][1]) / 2
        pts = [(px, py, True)] + list(points)
        start_idx = 0
    else:
        pts = list(points)

    ordered = pts[start_idx:] + pts[:start_idx]
    ordered.append(ordered[0])

    expanded = [ordered[0]]
    cdef int i
    for i in range(1, len(ordered)):
        p, prev = ordered[i], expanded[-1]
        if not prev[2] and not p[2]:
            expanded.append((
                (prev[0] + p[0]) / 2,
                (prev[1] + p[1]) / 2,
                True,
            ))
        expanded.append(p)

    cdef list polygon = []
    i = 0
    while i < len(expanded) - 1:
        p0 = expanded[i]
        p1 = expanded[i + 1]

        if p1[2]:
            polygon.append((p0[0], p0[1]))
            i += 1
        elif i + 2 < len(expanded):
            p2 = expanded[i + 2]
            polygon.append((p0[0], p0[1]))
            polygon.extend(_quad_bezier(p0, p1, p2, steps))
            i += 2
        else:
            i += 1

    if len(polygon) >= 2 and polygon[-1] == polygon[0]:
        polygon.pop()
    return polygon


cdef list _split_contours(glyph g):
    cdef list contours = []
    cdef int prev_end = -1
    cdef list pts
    cdef int i, end
    for end in g.endPtsOfContours:
        pts = []
        for i in range(prev_end + 1, end + 1):
            pts.append((
                g.xCoordinates[i],
                g.yCoordinates[i],
                bool(g.flags[i] & 0x01),
            ))
        contours.append(pts)
        prev_end = end
    return contours


cdef list _to_pixels(list polygons, double scale,
                     double offset_x, double offset_y):
    return [
        [
            (x * scale + offset_x, -y * scale + offset_y)
            for (x, y) in poly
        ]
        for poly in polygons
    ]


# supersampling

cdef bint _point_in_polygons(double px, double py, list polygons):
    cdef bint inside = False
    cdef int n, i
    cdef double x1, y1, x2, y2, xint
    for poly in polygons:
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            if (y1 > py) != (y2 > py):
                xint = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
                if px < xint:
                    inside = not inside
    return inside


cdef object _rasterize(list polygons, int width, int height,
                       tuple color, int ss=4):
    cdef object surf = Surface((width, height), flags=SRCALPHA)
    surf.fill((0, 0, 0, 0))

    r, g, b = color
    cdef double step = 1.0 / ss
    cdef int total = ss * ss
    cdef int py, px, sy, sx, hits, alpha
    cdef double fx, fy

    for py in range(height):
        for px in range(width):
            hits = 0
            for sy in range(ss):
                for sx in range(ss):
                    fx = px + (sx + 0.5) * step
                    fy = py + (sy + 0.5) * step
                    if _point_in_polygons(fx, fy, polygons):
                        hits += 1
            if hits:
                alpha = <int>(255 * hits / total)
                surf.set_at((px, py), (r, g, b, alpha))

    return surf


# Низкоуровневый рендер одного глифа

cdef tuple _render_glyph_uncached(Font font, int glyph_id, int size_px,
                                  tuple color, int ss):
    cdef glyph g = font._glyf.glyphs[glyph_id]
    if g is None:
        return ()

    cdef list contours = _split_contours(g)
    if not contours:
        return ()

    cdef list polygons = []
    cdef list poly
    cdef tuple c
    for c in contours:
        poly = _contour_to_polygon(c)
        if len(poly) >= 3:
            polygons.append(poly)
    if not polygons:
        return ()

    cdef float scale = size_px / font._head.unitsPerEm
    cdef int x_min = g.xMin
    cdef int y_min = g.yMin
    cdef int x_max = g.xMax
    cdef int y_max = g.yMax

    cdef int width  = <int>(ceil((x_max - x_min) * scale) + 2)
    cdef int height = <int>(ceil((y_max - y_min) * scale) + 2)

    cdef float offset_x = <float>(-x_min * scale + 1)
    cdef float offset_y = <float>(y_max * scale + 1)

    cdef list polygons_px = _to_pixels(polygons, scale, offset_x, offset_y)

    cdef object surface = _rasterize(polygons_px, width, height, color, ss)
    return (surface, offset_x, offset_y)


# LRU кеш отрендеренных глифов

cdef dict _glyph_cache = {}
cdef int  _glyph_cache_limit = 2048
cdef list _glyph_cache_lru = []


def clear_glyph_cache():
    """Полностью очистить кеш отрендеренных глифов."""
    _glyph_cache.clear()
    del _glyph_cache_lru[:]


def set_glyph_cache_limit(int limit):
    """Установить максимальное число кешируемых глифов."""
    global _glyph_cache_limit
    _glyph_cache_limit = limit if limit > 0 else 1
    _trim_cache()


cdef void _trim_cache():
    cdef int excess = len(_glyph_cache) - _glyph_cache_limit
    cdef tuple key
    while excess > 0 and _glyph_cache_lru:
        key = _glyph_cache_lru.pop(0)
        _glyph_cache.pop(key, None)
        excess -= 1


cpdef tuple render_glyph(Font font, int glyph_id, int size_px,
                         tuple color, int ss=4):
    """
    Отрендерить глиф с кешированием.
    Возвращает (Surface, offset_x, offset_y) или () для пустого глифа.
    """
    cdef tuple key = (id(font), glyph_id, size_px, color, ss)
    cdef tuple cached = _glyph_cache.get(key)

    if cached is not None:
        try:
            _glyph_cache_lru.remove(key)
        except ValueError:
            pass
        _glyph_cache_lru.append(key)
        return cached

    cdef tuple result = _render_glyph_uncached(font, glyph_id, size_px, color, ss)

    if len(_glyph_cache) >= _glyph_cache_limit:
        _trim_cache()

    _glyph_cache[key] = result
    _glyph_cache_lru.append(key)
    return result


# Метрики и рендер строки

cdef int _get_advance(Font font, int glyph_id, int size_px) except -1:
    cdef glyph g = font._glyf.glyphs[glyph_id]
    if g is None:
        return 0
    return <int>ceil(g.advanceWidth * size_px / font._head.unitsPerEm)


cpdef tuple render_text(Font font, str text, int size_px, tuple color,
                        int ss=4, int tracking=0):
    """
    Отрендерить строку в единую Surface.
    Возвращает (Surface, baseline_y) либо (None, 0).
    """
    cdef list glyphs = []
    cdef int x = 0
    cdef int min_x = 0, min_y = 0, max_x = 0, max_y = 0
    cdef int i, gid, adv, w, h, gx, gy
    cdef tuple rendered, cmap
    cdef object surf
    cdef bint first = True

    cmap = font._cmap
    for i in range(len(text)):
        gid = cmap.get(ord(text[i]), 0)
        if gid == 0 and text[i] != ' ':
            continue

        rendered = render_glyph(font, gid, size_px, color, ss)
        adv = _get_advance(font, gid, size_px)

        if rendered:
            surf = rendered[0]
            gx = int(x + rendered[1])
            gy = int(-rendered[2])
            w = surf.width
            h = surf.height
            if first:
                min_x, min_y, max_x, max_y = gx, gy, gx + w, gy + h
                first = False
            else:
                if gx < min_x:         min_x = gx
                if gy < min_y:         min_y = gy
                if gx + w > max_x:     max_x = gx + w
                if gy + h > max_y:     max_y = gy + h

        glyphs.append((gid, x, rendered))
        x += adv + tracking

    if first:
        return (None, 0)

    cdef int surf_w = max_x - min_x
    cdef int surf_h = max_y - min_y
    cdef object out = Surface((surf_w, surf_h), flags=SRCALPHA)
    out.fill((0, 0, 0, 0))

    cdef int px, py, gx_px, gy_px, s_w, s_h
    cdef tuple pix
    for (gid, x, rendered) in glyphs:
        if not rendered:
            continue
        surf = rendered[0]
        gx_px = int(x + rendered[1]) - min_x
        gy_px = int(-rendered[2]) - min_y
        s_w = surf.width
        s_h = surf.height
        for py in range(s_h):
            for px in range(s_w):
                pix = surf.get_at((px, py))
                if pix[3]:
                    out.set_at((gx_px + px, gy_px + py), pix)

    return (out, -min_y)