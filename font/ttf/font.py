from PyForge.easel import CoreObject
from .table import FontDirectory, head, maxp, loca, glyf, cmap, hhea, hmtx
from math import ceil

class Font(CoreObject):
    # таблица
    _head: head | None = None
    _maxp: maxp | None = None
    _loca: loca | None = None
    _glyf: glyf | None = None
    _cmap: cmap | None = None
    _hhea: hhea | None = None
    _hmtx: hmtx | None = None
    _data: bytes | None = None   # кэш сырых байтов файла

    file: str | None = None

    sfntVersion: int = 0x00010000   # 0x00010000 — TrueType, 'OTTO' — CFF/OpenType
    numTables: int                  # Сколько таблиц в файле
    searchRange: int                # 2^floor(log2(numTables)) × 16
    entrySelector: int              # log2(searchRange / 16)
    rangeShift: int                 # numTables × 16 − searchRange

    tableRecord: dict[FontDirectory]        # 16*numTables

    def __init__(self, file: str | None = None):
        if file: self.load(file)

    def load(self, file: str):
        with open(file, 'r+b') as f:
            data = f.read()

        # 0x0000 : 0x000C
        self.sfntVersion =      int.from_bytes(data[0x00 : 0x04])
        self.numTables =        int.from_bytes(data[0x04 : 0x06])
        self.searchRange =      int.from_bytes(data[0x06 : 0x08])
        self.entrySelector =    int.from_bytes(data[0x08 : 0x0A])
        self.rangeShift =       int.from_bytes(data[0x0A : 0x0C])

        # 0x000C : 0x000C + 16*numTables
        cesh = data[0x000C : 0x000C + 16*self.numTables]
        tableRecord: list[bytes] = [cesh[i:i + 16] for i in range(0, len(cesh), 16)]
        tableRecord: list[FontDirectory] = [FontDirectory(i[:0x04].decode('ASCII'), int.from_bytes(i[0x04:0x08]), int.from_bytes(i[0x08:0x0C]), int.from_bytes(i[0x0C:0x0C+4])) for i in tableRecord]
        self.tableRecord = {i.tag: i for i in tableRecord}

        if "head" in self.tableRecord:
            heads: FontDirectory = self.tableRecord["head"]
            self._head = head._from(data[heads.offset : heads.offset+heads.length])

        if "maxp" in self.tableRecord:
            maxps: FontDirectory = self.tableRecord["head"]
            self._maxp = head._from(data[maxps.offset : maxps.offset+maxps.length])

        if "hhea" in self.tableRecord:
            hheas: FontDirectory = self.tableRecord["hhea"]
            self._hhea = hhea._from(data[hheas.offset : hheas.offset + hheas.length])

        if "cmap" in self.tableRecord:
            cmaps: FontDirectory = self.tableRecord["cmap"]
            self._cmap = cmap._from(data[cmaps.offset : cmaps.offset + cmaps.length])

        if "loca" in self.tableRecord:
            locas: FontDirectory = self.tableRecord["loca"]
            self._loca = loca._from(
                data[locas.offset : locas.offset + locas.length],
                self._maxp.numGlyphs,
                self._head.indexToLocFormat,
            )

        if "hmtx" in self.tableRecord:
            hmtxs: FontDirectory = self.tableRecord["hmtx"]
            self._hmtx = hmtx._from(
                data[hmtxs.offset : hmtxs.offset + hmtxs.length],
                self._hhea.numberOfHMetrics,
                self._maxp.numGlyphs,
            )

        if "glyf" in self.tableRecord:
            glyfs: FontDirectory = self.tableRecord["glyf"]
            self._glyf = glyf._from(
                data[glyfs.offset : glyfs.offset + glyfs.length],
                self._loca.offsets,
                self._maxp.numGlyphs,
            )
        
        self.file = file

if __name__ == "__main__":
    #print(int.from_bytes((0xFF).to_bytes()))
    f = Font("minecraft.ttf")
    print(f.sfntVersion, f.numTables, f.searchRange, f.entrySelector, f.rangeShift)
    
    print(f.tableRecord["head"].tabl)
