from .table cimport FontDirectory, head, maxp, loca, glyf, cmap, hhea, hmtx, name

cdef class Font:
    def __cinit__(self):
        self.sfntVersion = 0x00010000

    def __init__(self, file: str | None = None):
        if isinstance(file, str): self.load(<str>file)

    cpdef tuple layout(self, str text, double font_size, double start_x):
        """
        Возвращает (xs, widths, gids):
          xs     - list[float], x начала каждого символа, len == len(text)
          widths - list[float], advance ширина каждого символа, len == len(text)
          gids   - list[int],   glyph id каждого символа
        """
        cdef double scale = font_size / self._head.unitsPerEm
        cdef list aw = self._hmtx.advanceWidth
        cdef Py_ssize_t n = len(aw)
        cdef Py_ssize_t i
        cdef int gid
        cdef double x = start_x

        cdef list xs = []
        cdef list widths = []
        cdef list gids = []
        cdef double w

        for i in range(len(text)):
            gid = self._cmap.lookup(ord(text[i]))
            if 0 <= gid < n:
                w = aw[gid] * scale
            else:
                gid = 0
                w = 0.0
            xs.append(x)
            widths.append(w)
            gids.append(gid)
            x += w

        return xs, widths, gids

    cpdef void load(self, str file):
        cdef bytes data
        with open(file, 'r+b') as f:
            data = f.read()

        # 0x0000 : 0x000C
        self.sfntVersion =      int.from_bytes(data[0x00 : 0x04], "big")
        self.numTables =        int.from_bytes(data[0x04 : 0x06], "big")
        self.searchRange =      int.from_bytes(data[0x06 : 0x08], "big")
        self.entrySelector =    int.from_bytes(data[0x08 : 0x0A], "big")
        self.rangeShift =       int.from_bytes(data[0x0A : 0x0C], "big")

        # 0x000C : 0x000C + 16*numTables
        cdef Py_ssize_t need = 0x000C + 16 * self.numTables
        if len(data) < need:
            raise ValueError(f"Font too short: need {need}, got {len(data)}")

        cdef bytes table_dir = data[0x000C:need]
        cdef list[FontDirectory] tableRecord = [
            FontDirectory(
                table_dir[i:i + 4].decode('ASCII'),
                int.from_bytes(table_dir[i + 4:i + 8], 'big'),
                int.from_bytes(table_dir[i + 8:i + 12], 'big'),
                int.from_bytes(table_dir[i + 12:i + 16], 'big'),
            )
            for i in range(0, len(table_dir), 16)
        ]
        self.tableRecord = {i.tag: i for i in tableRecord}

        cdef FontDirectory heads 
        cdef FontDirectory maxps 
        cdef FontDirectory hheas 
        cdef FontDirectory cmaps 
        cdef FontDirectory locas 
        cdef FontDirectory hmtxs 
        cdef FontDirectory glyfs 
        cdef FontDirectory names

        if "head" in self.tableRecord:
            heads = self.tableRecord["head"]
            self._head = head._from(data[heads.offset : heads.offset+heads.length])

        if "maxp" in self.tableRecord:
            maxps: FontDirectory = self.tableRecord["maxp"]  
            self._maxp = maxp._from(data[maxps.offset : maxps.offset + maxps.length])

        if "hhea" in self.tableRecord:
            hheas = self.tableRecord["hhea"]
            self._hhea = hhea._from(data[hheas.offset : hheas.offset + hheas.length])

        if "cmap" in self.tableRecord:
            cmaps = self.tableRecord["cmap"]
            self._cmap = cmap._from(data[cmaps.offset : cmaps.offset + cmaps.length])

        if "loca" in self.tableRecord:
            locas = self.tableRecord["loca"]
            self._loca = loca._from(
                data[locas.offset : locas.offset + locas.length],
                self._maxp.numGlyphs,
                self._head.indexToLocFormat,
            )

        if "hmtx" in self.tableRecord:
            hmtxs = self.tableRecord["hmtx"]
            self._hmtx = hmtx._from(
                data[hmtxs.offset : hmtxs.offset + hmtxs.length],
                self._hhea.numberOfHMetrics,
                self._maxp.numGlyphs,
            )

        if "glyf" in self.tableRecord:
            glyfs = self.tableRecord["glyf"]
            self._glyf = glyf._from(
                data[glyfs.offset : glyfs.offset + glyfs.length],
                self._loca.offsets,
                self._maxp.numGlyphs,
            )

        if "name" in self.tableRecord:
            names = self.tableRecord["name"]
            self._name = name._from(
                data[names.offset : names.offset + names.length]
            )
        
        self.file = file
