# cython: language_level=3

from .font cimport Font
from .table cimport glyph

cdef list  _quad_bezier(tuple p0, tuple p1, tuple p2, int steps=*)
cdef list  _contour_to_polygon(list points, int steps=*)
cdef list  _split_contours(glyph g)
cdef list  _to_pixels(list polygons, double scale,
                      double offset_x, double offset_y)
cdef bint  _point_in_polygons(double px, double py, list polygons)
cdef object _rasterize(list polygons, int width, int height,
                       tuple color, int ss=*)
cdef tuple _render_glyph_uncached(Font font, int glyph_id,
                                  int size_px, tuple color, int ss)
cdef void  _trim_cache()
cdef int   _get_advance(Font font, int glyph_id, int size_px) except -1

# модульные переменные кеша
cdef dict _glyph_cache
cdef int  _glyph_cache_limit
cdef list _glyph_cache_lru


# публичный API
cpdef tuple render_glyph(Font font, int glyph_id, int size_px,
                         tuple color, int ss=*)

cpdef tuple render_text(Font font, str text, int size_px, tuple color,
                        int ss=*, int tracking=*)