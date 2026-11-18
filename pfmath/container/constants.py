AUTO        = None
CENTER      = (0.5, 0.5)
TOP_LEFT    = (0.0, 0.0)
BOTTOM_RIGHT= (1.0, 1.0)

# resize flags для Container
NATURAL = 0
FILL_W  = 1 << 0
FILL_H  = 1 << 1
FILL    = FILL_W | FILL_H
STRETCH = FILL          # алиас для обратной совместимости

ALIGN_START   = 1 << 0
ALIGN_CENTER  = 1 << 1
ALIGN_END     = 1 << 2
ALIGN_STRETCH = 1 << 3
ALIGN_MASK    = ALIGN_START | ALIGN_CENTER | ALIGN_END | ALIGN_STRETCH