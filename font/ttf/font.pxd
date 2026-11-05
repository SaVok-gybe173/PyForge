from .table cimport FontDirectory, head, maxp, loca, glyf, cmap, hhea, hmtx, name

cdef class Font:
    # таблицы
    cdef public head _head
    cdef public maxp _maxp
    cdef public loca _loca
    cdef public glyf _glyf
    cdef public cmap _cmap
    cdef public hhea _hhea
    cdef public hmtx _hmtx
    cdef public name _name
    cdef public bytes _data   # кэш сырых байтов файла

    cdef public str file

    cdef public long long sfntVersion           # 0x00010000 — TrueType, 'OTTO' — CFF/OpenType
    cdef public int numTables                   # Сколько таблиц в файле
    cdef public int searchRange                 # 2^floor(log2(numTables)) × 16
    cdef public int entrySelector               # log2(searchRange / 16)
    cdef public int rangeShift                  # numTables × 16 − searchRange

    cdef public dict tableRecord                # dict[FontDirectory] 16*numTables

    cpdef void load(self, str file)
