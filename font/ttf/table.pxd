cimport cython

@cython.dataclasses.dataclass
cdef class FontDirectory:
    cdef public str tag         # 4 байта, 4 символа ASCII
    cdef public int checkSum    # 4 байта, uint32
    cdef public int offset      # 4 байта, uint32
    cdef public int length      # 4 байта, uint32

@cython.dataclasses.dataclass
cdef class head:                        # заголовок шрифта
    cdef public int version             # 0x00010000
    cdef public int fontRevision        # 0x00010000
    cdef public int checkSumAdjustment  
    cdef public int magicNumber         # 0x5F0F3CF5
    cdef public int flags   
    cdef public int unitsPerEm          # 1024 или 2048 (иногда 1000, 2000)
    cdef public int created
    cdef public int modified
    cdef public int xMin
    cdef public int yMin
    cdef public int xMax
    cdef public int yMax
    cdef public int macStyle
    cdef public int lowestRecPPEM
    cdef public int fontDirectionHint
    cdef public int indexToLocFormat   # 0 или 1
    cdef public int glyphDataFormat    # 0
    @staticmethod
    cdef head _from(bytes datahead)
    cdef bytes _to(self)

@cython.dataclasses.dataclass
cdef class maxp: #максимумы
    cdef public int version
    cdef public int numGlyphs
    cdef public int maxPoints
    cdef public int maxContours
    cdef public int maxCompositePoints
    cdef public int maxCompositeContours
    cdef public int maxZones
    cdef public int maxTwilightPoints
    cdef public int maxStorage
    cdef public int maxFunctionDefs
    cdef public int maxInstructionDefs
    cdef public int maxStackElements
    cdef public int maxSizeOfInstructions
    cdef public int maxComponentElements
    cdef public int maxComponentDepth
    @staticmethod
    cdef maxp _from(bytes datamaxp)

@cython.dataclasses.dataclass
cdef class loca:
    cdef public list offsets
    @staticmethod
    cdef loca _from(bytes data, int num_glyphs, int index_to_loc_format)

cdef class glyph:
    cdef public int numberOfContours
    cdef public int xMin
    cdef public int yMin
    cdef public int xMax
    cdef public int yMax
    cdef public list endPtsOfContours   # [int, ...] - конец каждого контура
    cdef public list xCoordinates       # [int, ...] - все X-координаты
    cdef public list yCoordinates       # [int, ...] - все Y-координаты
    cdef public list flags              # [int, ...] - биты on_curve и т.д.
    @staticmethod
    cdef glyph _from(bytes data)

@cython.dataclasses.dataclass
cdef class glyf:
    cdef public list glyphs         # list[glyph | None]
    @staticmethod
    cdef glyf _from(bytes data, list loca_offsets, int num_glyphs)

@cython.dataclasses.dataclass
cdef class EncodingRecords:
    cdef public int platformID
    cdef public int encodingID
    cdef public int subtableOffset

@cython.dataclasses.dataclass
cdef class Format4:
    cdef public int offset              # позиция подтаблицы внутри cmap (для приоритета)
    cdef public int format
    cdef public int length
    cdef public int language
    cdef public int segCountX2
    cdef public int searchRange
    cdef public int entrySelector
    cdef public int rangeShift
    cdef public list endCode            # list[int], длина = segCount
    cdef public int reservedPad
    cdef public list startCode          # list[int], длина = segCount
    cdef public list idDelta            # list[int], длина = segCount (signed)
    cdef public list idRangeOffset      # list[int], длина = segCount
    cdef public list glyphIdArray       # list[int]
    cpdef int lookup(self, int char_code)
    @staticmethod
    cdef Format4 _parse_format4(bytes sub, int cmap_offset)

@cython.dataclasses.dataclass
cdef class cmap:
    cdef public int version
    cdef public int numTables
    cdef public list encodingRecords    # list[EncodingRecords]
    cdef public list format4            # list[Format4] - все Format 4 в cmap
    cpdef int lookup(self, int char_code)
    @staticmethod
    cdef cmap _from(bytes data)

@cython.dataclasses.dataclass
cdef class hhea:
    cdef int version
    cdef int ascender
    cdef int descender
    cdef int lineGap
    cdef int advanceWidthMax
    cdef int minLeftSideBearing
    cdef int minRightSideBearing
    cdef int xMaxExtent
    cdef int caretSlopeRise
    cdef int caretSlopeRun
    cdef int caretOffset
    cdef int reserved
    cdef int metricDataFormat
    cdef int numberOfHMetrics
    @staticmethod
    cdef hhea _from(data: bytes)

@cython.dataclasses.dataclass
cdef class hmtx:
    cdef public list advanceWidth       # list[int], длина = numGlyphs
    cdef public list leftSideBearing    # list[int], длина = numGlyphs
    @staticmethod
    cdef hmtx _from(bytes data, int number_of_h_metrics, int num_glyphs)

@cython.dataclasses.dataclass
cdef class NameRecord:
    cdef public int platform_id
    cdef public int encoding_id
    cdef public int language_id
    cdef public int name_id
    cdef public int length
    cdef public int offset
    cdef public str text          # уже декодированная строка

@cython.dataclasses.dataclass
cdef class name:
    cdef public int format
    cdef public int count
    cdef public int string_offset
    cdef public list records          # list[NameRecord]
    cdef public dict by_name_id       # {nameID: str}, только (3,1) и (0,*) - для удобства
    @staticmethod
    cdef name _from(bytes data)

@cython.dataclasses.dataclass
cdef class post:
    cdef public int version
    cdef public int italicAngle
    cdef public int underlinePosition
    cdef public int underlineThickness
    cdef public int isFixedPitch
    cdef public int minMemType42
    cdef public int maxMemType42
    cdef public int minMemType1
    cdef public int maxMemType1
    cdef public bytes tail
    @staticmethod
    cdef post _from(bytes data)

@cython.dataclasses.dataclass
cdef class OSH2: pass

@cython.dataclasses.dataclass
cdef class kern: pass

@cython.dataclasses.dataclass
cdef class GPOS: pass

@cython.dataclasses.dataclass
cdef class GSUB: pass

@cython.dataclasses.dataclass
cdef class GDEF: pass

@cython.dataclasses.dataclass
cdef class cvt: pass

@cython.dataclasses.dataclass
cdef class fpgm: pass

@cython.dataclasses.dataclass
cdef class prep: pass

@cython.dataclasses.dataclass
cdef class gasp: pass

@cython.dataclasses.dataclass
cdef class DSIG: pass

@cython.dataclasses.dataclass
cdef class hdmx: pass

@cython.dataclasses.dataclass
cdef class LTSH: pass

@cython.dataclasses.dataclass
cdef class VDMX: pass

@cython.dataclasses.dataclass
cdef class ttcf: pass

@cython.dataclasses.dataclass
cdef class EBLC: pass

@cython.dataclasses.dataclass
cdef class SVG: pass

@cython.dataclasses.dataclass
cdef class COLR: pass