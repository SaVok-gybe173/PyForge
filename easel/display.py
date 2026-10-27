_size = (0, 0)

def set_window_size(size):
    global _size
    _size = size

def get_window_size() -> tuple[int, int]:
    global _size
    return _size