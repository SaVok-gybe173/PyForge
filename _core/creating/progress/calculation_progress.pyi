
class  ProgressBarCalc:
    _is_quantity: bool
    _quantity_main: int
    _quantity: int
    _percent: float # от 0 до 100
    _pixel_progress: int

    _left_top: tuple[int, int]
    _width_height: tuple[int, int]

    def __init__(self,  left_top: tuple[int, int], width_height: tuple[int, int]) -> None: ...

    def update_progress(self) -> None: ...
    def math_quantity(self) -> None: ...

    def set_pixel(self, pixel: int) -> None: ... # установка прогресс в пикселей
    def get_pixel(self) -> int: ... # получение текущего расположения


    def set_percent(self, percent: float): ... # установка процента
    def get_percent(self, ) -> float: ... # получение процента
    def add_percent(self, percent: float): ... # добавление процента
    
    def set_quantity_main(self, quantity: int): ... # добавление кочичества
    def get_quantity_main(self, quantity: int): ... # возвращает максимальное количество
    def add_quantity_main(self, quantity: int): ... # добавляет к основному количество
    
    def get_quantity(self) -> int: ... # возвращает текущие количество
    def set_quantity(self, quantity: int): ... # устанавливает количество
    def add_quantity(self, quantity: int): ... # добавляет к прогресу
    def clear_quantity(self): ... # очищает прогресс
    def del_quantity(self): ... # удаляет прогресс

    @property
    def left(self) -> int: ...
    @left.setter
    def left(self, left: int) -> None: ...
    @property
    def top(self) -> int: ...
    @top.setter
    def top(self, top: int) -> None: ...
    
    @property
    def left_top(self) -> tuple[int, int]: ...
    @left_top.setter
    def left_top(self, left_top: tuple[int, int]) -> None: ...

    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, width: int) -> None: ...

    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, height: int) -> None: ...
    
    @property
    def width_height(self) -> tuple[int, int]: ... 
    @width_height.setter
    def width_height(self, width_height: tuple[int, int]) -> None: ...
    