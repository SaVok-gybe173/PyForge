"""
Ниже dataclasses для всех таблиц, которые нужны для рендера. 
Каждое поле снабжено комментарием: что это и зачем оно. 
В конце - зачем вообще нужен сам файл шрифта.

"""

cimport cython

@cython.dataclasses.dataclass
cdef class FontDirectory:
    pass


@cython.dataclasses.dataclass
cdef class head: # заголовок шрифта
    @staticmethod
    cdef head _from(bytes datahead):
        return head(
                int.from_bytes(datahead[0x00 : 0x04], "big"),
                int.from_bytes(datahead[0x04 : 0x08], "big"),
                int.from_bytes(datahead[0x08 : 0x0C], "big"),
                int.from_bytes(datahead[0x0C : 0x10], "big"),
                int.from_bytes(datahead[0x10 : 0x12], "big"),
                int.from_bytes(datahead[0x12 : 0x14], "big"),
                int.from_bytes(datahead[0x14 : 0x1C], "big", signed=True),
                int.from_bytes(datahead[0x1C : 0x24], "big", signed=True),
                int.from_bytes(datahead[0x24 : 0x26], "big", signed=True),
                int.from_bytes(datahead[0x26 : 0x28], "big", signed=True),
                int.from_bytes(datahead[0x28 : 0x2A], "big", signed=True),
                int.from_bytes(datahead[0x2A : 0x2C], "big", signed=True),
                int.from_bytes(datahead[0x2C : 0x2E], "big"),
                int.from_bytes(datahead[0x2E : 0x30], "big"),
                int.from_bytes(datahead[0x30 : 0x32], "big", signed=True),
                int.from_bytes(datahead[0x32 : 0x34], "big", signed=True),
                int.from_bytes(datahead[0x34 : 0x36], "big", signed=True),
            )

    cdef bytes _to(self):
        return (
            self.version.to_bytes(4) +
            self.fontRevision.to_bytes(4) +
            self.checkSumAdjustment.to_bytes(4) +
            self.magicNumber.to_bytes(4) +
            self.flags.to_bytes(2) +
            self.unitsPerEm.to_bytes(2) +
            self.created.to_bytes(8) +
            self.modified.to_bytes(8) +
            self.xMin.to_bytes(2) +
            self.yMin.to_bytes(2) +
            self.xMax.to_bytes(2) +
            self.yMax.to_bytes(2) +
            self.macStyle.to_bytes(2) +
            self.lowestRecPPEM.to_bytes(2) +
            self.fontDirectionHint.to_bytes(2) +
            self.indexToLocFormat.to_bytes(2) + 
            self.glyphDataFormat.to_bytes(2)
        )


@cython.dataclasses.dataclass
cdef class maxp: # максимумы
    @staticmethod
    cdef maxp _from(bytes datamaxp):
        return maxp(
            int.from_bytes(datamaxp[0x00 : 0x04], "big"),
            int.from_bytes(datamaxp[0x04 : 0x06], "big"),
            int.from_bytes(datamaxp[0x06 : 0x08], "big"),
            int.from_bytes(datamaxp[0x08 : 0x0A], "big"),
            int.from_bytes(datamaxp[0x0A : 0x0C], "big"),
            int.from_bytes(datamaxp[0x0C : 0x0E], "big"),
            int.from_bytes(datamaxp[0x0E : 0x10], "big"),
            int.from_bytes(datamaxp[0x10 : 0x12], "big"),
            int.from_bytes(datamaxp[0x12 : 0x14], "big"),
            int.from_bytes(datamaxp[0x14 : 0x16], "big"),
            int.from_bytes(datamaxp[0x16 : 0x18], "big"),
            int.from_bytes(datamaxp[0x18 : 0x1A], "big"),
            int.from_bytes(datamaxp[0x1A : 0x1C], "big"),
            int.from_bytes(datamaxp[0x1C : 0x1E], "big"),
            int.from_bytes(datamaxp[0x1E : 0x20], "big"),
        )

@cython.dataclasses.dataclass
cdef class loca: # индекс местоположений глифов
    @staticmethod
    cdef loca _from(bytes data, int num_glyphs, int index_to_loc_format):
        cdef int count = num_glyphs + 1
        cdef list offsets = []
        cdef int i
        cdef int raw

        if index_to_loc_format == 0:
            if len(data) < count * 2:
                raise ValueError("loca: недостаточно байт для короткого формата")
            for i in range(count):
                offsets.append(int.from_bytes(data[i*2 : i*2 + 2], "big") * 2)
        elif index_to_loc_format == 1:
            if len(data) < count * 4:
                raise ValueError("loca: недостаточно байт для длинного формата")
            for i in range(count):
                offsets.append(int.from_bytes(data[i*4 : i*4 + 4], "big"))
        else:
            raise ValueError(f"loca: неизвестный index_to_loc_format = {index_to_loc_format}")
        return loca(offsets)

cdef class glyph:
    @staticmethod
    cdef glyph _from(bytes data):
        cdef glyph g = glyph()
        cdef int n_contours = int.from_bytes(data[0x00:0x02], "big", signed=True)
        cdef int pos

        if n_contours < 0: return None

        g.numberOfContours = n_contours
        g.xMin = int.from_bytes(data[0x02:0x04], "big", signed=True)
        g.yMin = int.from_bytes(data[0x04:0x06], "big", signed=True)
        g.xMax = int.from_bytes(data[0x06:0x08], "big", signed=True)
        g.yMax = int.from_bytes(data[0x08:0x0A], "big", signed=True)
        g.endPtsOfContours = []
        for ci in range(n_contours):
            off = 0x0A + 2 * ci
            g.endPtsOfContours.append(
                int.from_bytes(data[off:off + 2], "big")
            )
        cdef int num_points = g.endPtsOfContours[-1] + 1
        pos = 0x0A + 2 * n_contours
        cdef int instr_len = int.from_bytes(data[pos:pos + 2], "big")
        pos += 2 + instr_len
        g.flags = []
        cdef int flag, repeat
        while len(g.flags) < num_points:
            flag = data[pos]; pos += 1
            g.flags.append(flag)
            if flag & 0x08:                      # Repeat
                repeat = data[pos]; pos += 1
                g.flags.extend([flag] * repeat)
        g.xCoordinates = []
        cdef int x = 0, dx
        for flag in g.flags:
            if flag & 0x02:                      # x-Short: 1 байт
                dx = data[pos]; pos += 1
                if not (flag & 0x10):
                    dx = -dx
            else:
                if flag & 0x10:                  # Same X
                    dx = 0
                else:
                    dx = int.from_bytes(data[pos:pos + 2], "big", signed=True)
                    pos += 2
            x += dx
            g.xCoordinates.append(x)
        g.yCoordinates = []
        cdef int y = 0, dy
        for flag in g.flags:
            if flag & 0x04:                      # y-Short
                dy = data[pos]; pos += 1
                if not (flag & 0x20):
                    dy = -dy
            else:
                if flag & 0x20:                  # Same Y
                    dy = 0
                else:
                    dy = int.from_bytes(data[pos:pos + 2], "big", signed=True)
                    pos += 2
            y += dy
            g.yCoordinates.append(y)

        return g

@cython.dataclasses.dataclass
cdef class glyf: # контуры глифов
    @staticmethod
    cdef glyf _from(bytes data, list loca_offsets, int num_glyphs):
        cdef list glyphs = []
        cdef int i, start, end
        cdef glyph g

        for i in range(num_glyphs):
            start = loca_offsets[i]
            end   = loca_offsets[i + 1]
            if start == end:
                glyphs.append(None)
                continue
            g = glyph._from(data[start:end])
            glyphs.append(g)
        return  glyf(glyphs)

@cython.dataclasses.dataclass
cdef class EncodingRecords:
    pass

@cython.dataclasses.dataclass
cdef class Format4:
    @property
    def segCount(self):
        return self.segCountX2 // 2

    cpdef int lookup(self, int char_code):
        cdef int seg_count = <int>self.segCount
        cdef int i, gid, idx

        for i in range(seg_count):
            if self.startCode[i] <= char_code <= self.endCode[i]:
                if self.idRangeOffset[i] == 0:
                    gid = (char_code + self.idDelta[i]) & 0xFFFF
                else:
                    idx = (self.idRangeOffset[i] // 2 + (char_code - self.startCode[i]) - (seg_count - i))
                    if 0 <= idx < len(self.glyphIdArray):
                        gid = self.glyphIdArray[idx]
                        if gid != 0:
                            gid = (gid + self.idDelta[i]) & 0xFFFF
                    else:
                        gid = 0
                return gid if gid != 0 else 0
        return 0

    @staticmethod
    cdef Format4 _parse_format4(bytes sub, int cmap_offset):
        cdef int fmt           = int.from_bytes(sub[0x00:0x02], "big")
        cdef int length        = int.from_bytes(sub[0x02:0x04], "big")
        cdef int language      = int.from_bytes(sub[0x04:0x06], "big")
        cdef int segCountX2    = int.from_bytes(sub[0x06:0x08], "big")
        cdef int searchRange   = int.from_bytes(sub[0x08:0x0A], "big")
        cdef int entrySelector = int.from_bytes(sub[0x0A:0x0C], "big")
        cdef int rangeShift    = int.from_bytes(sub[0x0C:0x0E], "big")
        cdef int seg_count     = <int>(segCountX2//2)

        cdef list end_code = []
        cdef list start_code = []
        cdef list id_delta = []
        cdef list id_range_offset = []
        cdef list glyph_id_array = []

        cdef int gia_base = 0x10 + 8 * seg_count
        cdef int pos = gia_base
        cdef int iro_base = 0x10 + 6 * seg_count
        cdef int id_base = 0x10 + 4 * seg_count
        cdef int sc_base = 0x10 + 2 * seg_count
        cdef int reserved_pad_off = 0x0E + 2 * seg_count
        cdef int reserved_pad = int.from_bytes(sub[reserved_pad_off:reserved_pad_off + 2], "big")
        cdef int off
        cdef int i

        for i in range(seg_count):
            off = 0x0E + 2 * i
            end_code.append(int.from_bytes(sub[off:off + 2], "big"))

        for i in range(seg_count):
            off = sc_base + 2 * i
            start_code.append(int.from_bytes(sub[off:off + 2], "big"))

        for i in range(seg_count):
            off = id_base + 2 * i
            id_delta.append(int.from_bytes(sub[off:off + 2], "big", signed=True))

        for i in range(seg_count):
            off = iro_base + 2 * i
            id_range_offset.append(int.from_bytes(sub[off:off + 2], "big"))
    
        while pos + 2 <= length:
            glyph_id_array.append(int.from_bytes(sub[pos:pos + 2], "big"))
            pos += 2

        return Format4(offset=cmap_offset, format=fmt, length=length, language=language, segCountX2=segCountX2, searchRange=searchRange, entrySelector=entrySelector, rangeShift=rangeShift, endCode=end_code, reservedPad=reserved_pad, startCode=start_code, idDelta=id_delta, idRangeOffset=id_range_offset, glyphIdArray=glyph_id_array, )

@cython.dataclasses.dataclass
cdef class cmap: # сопоставление символов и глифов
    cpdef int lookup(self, int char_code):
        cdef EncodingRecords rec
        cdef Format4 f4

        for rec in self.encodingRecords:
            if rec.platformID == 3 and rec.encodingID == 1:
                for f4 in self.format4:
                    if f4.offset == rec.subtableOffset:
                        return f4.lookup(char_code)
        for rec in self.encodingRecords:
            if rec.platformID == 0:
                for f4 in self.format4:
                    if f4.offset == rec.subtableOffset:
                        return f4.lookup(char_code)
        if self.format4: return self.format4[0].lookup(char_code)
        return 0


    @staticmethod
    cdef cmap _from(bytes data):
        cdef int version   = int.from_bytes(data[0x00:0x02], "big")
        cdef int numTables = int.from_bytes(data[0x02:0x04], "big")

        cdef list records = []
        cdef list format4_list = []
        cdef set seen_offsets = set()

        cdef int base, i
        cdef int platform_id, encoding_id, offset

        for i in range(numTables):
            base = 0x04 + 8 * i
            platform_id = int.from_bytes(data[base  : base+2], "big")
            encoding_id = int.from_bytes(data[base+2: base+4], "big")
            offset      = int.from_bytes(data[base+4: base+8], "big")
            records.append(EncodingRecords(platform_id, encoding_id, offset))
            if offset in seen_offsets: continue
            seen_offsets.add(offset)
            if offset + 2 > len(data): continue
            if int.from_bytes(data[offset:offset + 2], "big") == 4:
                format4_list.append(Format4._parse_format4(data[offset:], offset))
        return cmap(version, numTables, records, format4_list)

@cython.dataclasses.dataclass
cdef class hhea: # горизонтальный заголовок
    @staticmethod
    cdef hhea _from(bytes data):
        return hhea(int.from_bytes(data[0x00:0x04], "big"),
                    int.from_bytes(data[0x04:0x06], "big", signed=True),
                    int.from_bytes(data[0x06:0x08], "big", signed=True),
                    int.from_bytes(data[0x08:0x0A], "big", signed=True),
                    int.from_bytes(data[0x0A:0x0C], "big"),
                    int.from_bytes(data[0x0C:0x0E], "big", signed=True),
                    int.from_bytes(data[0x0E:0x10], "big", signed=True),
                    int.from_bytes(data[0x10:0x12], "big", signed=True),
                    int.from_bytes(data[0x12:0x14], "big", signed=True),
                    int.from_bytes(data[0x14:0x16], "big", signed=True),
                    int.from_bytes(data[0x16:0x18], "big", signed=True),
                    int.from_bytes(data[0x18:0x20], "big", signed=True),
                    int.from_bytes(data[0x20:0x22], "big", signed=True),
                    int.from_bytes(data[0x22:0x24], "big"))

@cython.dataclasses.dataclass
cdef class hmtx: # горизонтальные метрики
    @staticmethod
    cdef hmtx _from(bytes data, int number_of_h_metrics, int num_glyphs):
        cdef int N = number_of_h_metrics
        cdef list advances = []
        cdef list lsbs = []
        cdef int i, off
        cdef int last_advance = 0
        for i in range(N):
            off = 4 * i
            if off + 4 > len(data): break
            advance = int.from_bytes(data[off    : off + 2], 'big')
            lsb     = int.from_bytes(data[off + 2: off + 4], 'big', signed=True)
            advances.append(advance)
            lsbs.append(lsb)
            last_advance = advance

        cdef int extra_base = 4 * N
        for i in range(N, num_glyphs):
            off = extra_base + 2 * (i - N)
            lsb = 0 if off + 2 > len(data) else  int.from_bytes(data[off: off + 2], 'big', signed=True)
            advances.append(last_advance)
            lsbs.append(lsb)

        return hmtx(advances, lsbs)

@cython.dataclasses.dataclass
cdef class NameRecord:
    pass

@cython.dataclasses.dataclass
cdef class name: # имена
    def get(self, int name_id, str default = None):
        """Быстрый доступ по nameID. Вернёт первую найденную строку."""
        return self.by_name_id.get(name_id, default)
    @staticmethod
    cdef name _from(bytes data):
        cdef int fmt      = int.from_bytes(data[0x00:0x02], "big")
        cdef int cnt      = int.from_bytes(data[0x02:0x04], "big")
        cdef int str_off  = int.from_bytes(data[0x04:0x06], "big")

        cdef list records = []
        cdef dict by_id   = {}
        cdef int i, base, pid, eid, lid, nid, ln, off, start, end
        cdef bytes raw
        cdef str text
        cdef NameRecord rec

        for i in range(cnt):
            base = 0x06 + 12 * i
            pid = int.from_bytes(data[base    : base + 2], "big")
            eid = int.from_bytes(data[base + 2: base + 4], "big")
            lid = int.from_bytes(data[base + 4: base + 6], "big")
            nid = int.from_bytes(data[base + 6: base + 8], "big")
            ln  = int.from_bytes(data[base + 8: base + 10], "big")
            off = int.from_bytes(data[base + 10: base + 12], "big")

            start = str_off + off
            end   = start + ln
            if end > len(data):
                continue
            raw = data[start:end]
            if pid == 0 or pid == 3:
                # Unicode / Windows -> UTF-16BE
                try:
                    text = raw.decode('utf-16-be')
                except UnicodeDecodeError:
                    text = ''
            elif pid == 1:
                try:
                    text = raw.decode('latin-1')
                except UnicodeDecodeError:
                    text = ''
            else:
                text = ''

            rec = NameRecord(pid, eid, lid, nid, ln, off, text)
            records.append(rec)
            if text and nid not in by_id:
                by_id[nid] = text
            elif text and pid == 3 and eid == 1:
                by_id[nid] = text
        return name(fmt, cnt, str_off, records, by_id)

@cython.dataclasses.dataclass
cdef class post: # PostScript-информация
    @staticmethod
    cdef post _from(bytes data):
        return post(int.from_bytes(data[0x00:0x04], "big"),
                    int.from_bytes(data[0x04:0x08], "big"),
                    int.from_bytes(data[0x08:0x0A], "big", signed=True),
                    int.from_bytes(data[0x0A:0x0C], "big", signed=True),
                    int.from_bytes(data[0x0C:0x10], "big"),
                    int.from_bytes(data[0x10:0x14], "big"),
                    int.from_bytes(data[0x14:0x18], "big"),
                    int.from_bytes(data[0x18:0x1C], "big"),
                    int.from_bytes(data[0x1C:0x20], "big"))

# Опциональные, но почти всегда присутствуют

@cython.dataclasses.dataclass
cdef class OSH2: # OS/2 (H = F+2) - метрики для Windows
    """
    Смещение    Размер	Тип	        Имя
    0x00	    2	    uint16	    version
    0x02	    2	    int16	    xAvgCharWidth
    0x04	    2	    uint16	    usWeightClass
    0x06	    2	    uint16	    usWidthClass
    0x08	    2	    uint16	    fsType
    0x0A	    2	    int16	    ySubscriptXSize
    0x0C	    2	    int16	    ySubscriptYSize
    0x0E	    2	    int16	    ySubscriptXOffset
    0x10	    2	    int16	    ySubscriptYOffset
    0x12	    2	    int16	    ySuperscriptXSize
    0x14	    2	    int16	    ySuperscriptYSize
    0x16	    2	    int16	    ySuperscriptXOffset
    0x18	    2	    int16	    ySuperscriptYOffset
    0x1A	    2	    int16	    yStrikeoutSize
    0x1C	    2	    int16	    yStrikeoutPosition
    0x1E	    2	    int16	    sFamilyClass
    0x20	    10	    uint8[10]	panose
    0x2A	    4	    uint32	    ulUnicodeRange1
    0x2E	    4	    uint32	    ulUnicodeRange2
    0x32	    4	    uint32	    ulUnicodeRange3
    0x36	    4	    uint32	    ulUnicodeRange4
    0x3A	    4	    -	        achVendID (4 символа)
    0x3E	    2	    uint16	    fsSelection
    0x40	    2	    uint16	    usFirstCharIndex
    0x42	    2	    uint16	    usLastCharIndex
    0x44	    2	    int16	    sTypoAscender
    0x46	    2	    int16	    sTypoDescender
    0x48	    2	    int16	    sTypoLineGap
    0x4A	    2	    uint16	    usWinAscent
    0x4C	    2	    uint16	    usWinDescent

    Дальше зависит от version:
    v0 - конец (78 байт)
    v1 - добавляются ulCodePageRange1 (0x4E), ulCodePageRange2 (0x52) → 86 байт
    v2 - добавляются sxHeight (0x56), sCapHeight (0x58), usDefaultChar (0x5A), usBreakChar (0x5C), usMaxContext (0x5E) → 96 байт
    v3 - как v2 (не несёт новых полей)
    v4 - + usLowerOpticalPointSize (0x60), usUpperOpticalPointSize (0x62) → 100 байт
    """

    @staticmethod
    def _from(data: bytes) -> "OSH2":
        """
        Зачем нужна: без неё Windows не признаёт шрифт «полноценным» и не использует в некоторых местах.

        Что внутри:
            usWeightcdef class - 400 (normal), 700 (bold).
            usWidthcdef class - 1..9, 5 = normal.
            fsSelection - italic, bold, regular.
            sTypoAscender / sTypoDescender / sTypoLineGap - альтернативные метрики строки.
            usWinAscent / usWinDescent - метрики для Windows.
            ulUnicodeRange1..4 - какие блоки Unicode поддерживаются.
            panose - классификация стиля (для подбора похожих шрифтов).

        Кто использует: 
            Windows для выбора шрифта, для позиционирования. 
            Для своего рендера не обязательна - метрики можно взять из hhea.
        """
        return OSH2()

@cython.dataclasses.dataclass
cdef class kern: # кернинг
    @staticmethod
    def _from(data: bytes) -> "kern":
        """
        Зачем нужна: 
            попарные сдвиги между глифами. 
            Например, AV в большинстве шрифтов сближаются, потому что «A» и «V» можно подвинуть друг к другу.

        Что внутри: 
            таблица пар (left_glyph, right_glyph) → value. 
            value прибавляется к advanceWidth левого глифа при рендере.

        Кто использует: 
            рендер - для качественной типографики. 
            Без неё буквы стоят «по сетке», но всё равно читаемо. 

        """

@cython.dataclasses.dataclass
cdef class GPOS: # OpenType-позиционирование
    @staticmethod
    def _from(data: bytes) -> "GPOS":
        """
        Зачем нужна: 
            современная замена kern. 
            Умеет не только попарный кернинг, но и сложное позиционирование: 
                диакритика (например, «й» = «и» + breve), марки, курсивные наклоны.

        Что внутри: 
            сложная система lookup-таблиц с бинарным форматом. 
            Гораздо сложнее kern.

        Кто использует: 
            cовременные шрифты с качественной типографикой.
        """

@cython.dataclasses.dataclass
cdef class GSUB: # OpenType-подстановки
    @staticmethod
    def _from(data: bytes) -> "GSUB":
        """
        Зачем нужна: 
            замены глифов. Лигатуры (fi → ﬁ), альтернативные формы, маленькие заглавные и т.д.

        Что внутри: 
            похоже на GPOS - lookup-таблицы.

        Кто использует: 
            продвинутая типографика.
        """

@cython.dataclasses.dataclass
cdef class GDEF: # классы глифов
    @staticmethod
    def _from(data: bytes) -> "GDEF":
        """
        Зачем нужна: 
            вспомогательная для GPOS и GSUB. 
            Размечает глифы на категории: базовые, марки, лигатуры.

        Что внутри: 
            массив классов глифов и таблица атрибутов.

        Кто использует: 
            только GPOS/GSUB. Самостоятельного значения не имеет.
        """

# Опциональные, для хинтинга
#
# Хинтинг - это подсказки рендереру, как правильно округлять глифы при мелких размерах. 
# Реализовать его очень сложно (это интерпретатор байт-кода). 

@cython.dataclasses.dataclass
cdef class cvt: # Control Values Table
    @staticmethod
    def _from(data: bytes) -> "cvt":
        """
        Зачем нужна: 
            массив «опорных» вертикальных и горизонтальных значений (высоты штрихов, положение baseline). 
            Хинтинг-программа использует их как эталоны.

        Что внутри: 
            массив int16
        """    

@cython.dataclasses.dataclass
cdef class fpgm: #  Font Program
    @staticmethod
    def _from(data: bytes) -> "fpgm":
        """
        Зачем нужна: 
            байт-код, который выполняется один раз при загрузке шрифта. 
            Определяет вспомогательные функции, настраивает переменные для хинтинга.

        Что внутри: 
            байт-код для виртуальной машины TrueType.
        """

@cython.dataclasses.dataclass
cdef class prep: # Pre-Program
    @staticmethod
    def _from(data: bytes) -> "prep":
        """
        Зачем нужна: 
            байт-код, который выполняется при каждом размере шрифта. 
            Настраивает control values под конкретный ppem (пикселей на em).

        Что внутри: 
            байт-код.
        """
@cython.dataclasses.dataclass
cdef class gasp:
    @staticmethod
    def _from(data: bytes) -> "gasp":
        """
        Зачем нужна: 
            говорит рендереру, для каких размеров применять хинтинг, для каких - сглаживание.

        Что внутри: 
            массив пар (размер, флаги). 

        Флаги: 
            применять ли grid-fitting, применять ли сглаживание.

        Кто использует: 
            системный рендерер.
        """

# Опциональные, специальные

@cython.dataclasses.dataclass
cdef class DSIG: # цифровая подпись
    @staticmethod
    def _from(data: bytes) -> "DSIG":
        """
        Зачем нужна: 
            подтверждает, что шрифт не был изменён после выпуска. 
            Криптографическая подпись.

        Что внутри: 
            записи с форматом, длиной и смещением подписи. 
            Сами подписи - отдельные блоки данных.

        Кто использует: 
            системы проверки легитимности шрифта.
        """

@cython.dataclasses.dataclass
cdef class hdmx:
    @staticmethod
    def _from(data: bytes) -> "hdmx": # Horizontal Device Metrics
        """
        Зачем нужна: 
            заранее посчитанные ширины глифов для конкретных ppem. 
            Ускоряет рендеринг на старых системах.

        Что внутри: 
            для каждого размера - массив ширин.

        Кто использует: 
            старые Windows. 
            Современный рендер обходится.
        """

@cython.dataclasses.dataclass
cdef class LTSH: # Linear Threshold
    @staticmethod
    def _from(data: bytes) -> "LTSH":
        """
        Зачем нужна: 
            говорит, с какого размера глиф можно рендерить «линейно», без хинтинга.

        Что внутри: 
            массив порогов на каждый глиф.

        Кто использует: 
            вместе с хинтингом.
        """

@cython.dataclasses.dataclass
cdef class VDMX: #  Vertical Device Metrics
    @staticmethod
    def _from(data: bytes) -> "VDMX":
        """
        Зачем нужна: 
            заранее посчитанные вертикальные метрики для конкретных размеров. 
            Нужна для правильного межстрочного расстояния на малых размерах.

        Что внутри: 
            сложная структура из групп размеров и значений.

        Кто использует: 
            Windows для вертикального позиционирования.
        """

@cython.dataclasses.dataclass
cdef class ttcf: # TTC / ttcf - TrueType Collection
    @staticmethod
    def _from(data: bytes) -> "ttcf":
        """
        Зачем нужна: 
            позволяет в одном файле хранить несколько шрифтов, 
            разделяющих общие таблицы (например, Regular, Bold, Italic - все используют один glyf, но разные hmtx и head).

        Что внутри: 
            список offset до Font Directory каждого шрифта.

        Кто использует: 
            системы для экономии места. 
        Для парсера: 
            если видишь sfntVersion = 'ttcf', значит файл - коллекция, и работать надо чуть иначе.
        """
@cython.dataclasses.dataclass
cdef class EBLC: # EBLC / EBDT - встроенные bitmap-глифы
    @staticmethod
    def _from(data: bytes) -> "EBLC":
        """
        Зачем нужна: 
            шрифт может содержать готовые картинки глифов для мелких размеров (не контуры, а пиксели). 
            Рендерер тогда просто берёт картинку, не растеризует.

        Что внутри: 
            метрики (EBLC) и сами битмапы (EBDT) или их сжатые варианты (EBSC, CBDT, CBLC).

        Кто использует: 
            рендереры для повышения чёткости на малых размерах. 
        """

@cython.dataclasses.dataclass
cdef class SVG: # SVG-глифы
    @staticmethod
    def _from(data: bytes) -> "SVG":
        """
        Зачем нужна: 
            глифы описываются как SVG. 
            Полезно для цветных и сложных шрифтов (иконки, эмодзи).

        Что внутри: 
            таблица с SVG-документами для глифов.

        Кто использует: 
            современные браузеры для цветных шрифтов.
        """
@cython.dataclasses.dataclass
cdef class COLR: # COLR / CPAL - цветные глифы
    @staticmethod
    def _from(data: bytes) -> "COLR":
        """
        Зачем нужна: 
            для эмодзи и иконок. 
            COLR описывает, как собрать цветной глиф из слоёв, CPAL - палитру цветов.

        Что внутри: 
            слоистые описания + цвета.

        Кто использует: 
            рендерер эмодзи.
        """

#   Минимум для базового рендера текста:
#   Таблица	    Зачем
#   head	    unitsPerEm, indexToLocFormat
#   maxp	    numGlyphs
#   loca	    границы глифов
#   glyf	    контуры
#   cmap	    символ → glyph_id
#   hhea	    numberOfHMetrics, метрики строки
#   hmtx	    ширины глифов
#
#   Добавь потом, для качества:
#   Таблица	    Что даёт
#   kern	    попарный кернинг
#   OS/2	    альтернативные метрики, вес/стиль
#
#   Игнорируй полностью:
#   Таблица	                    Почему
#   cvt, fpgm, prep, gasp, LTSH	хинтинг - очень сложно, не критично
#   GPOS, GSUB, GDEF	        продвинутая типографика
#   DSIG, hdmx, VDMX	        служебные
#   name, post	                метаданные
#   EBLC, EBDT, SVG, COLR	    спец-случаи (bitmap, цветные)