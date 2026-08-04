class ProgressBarCalc:
    _is_quantity: bool = False
    _quantity_main: int = 100
    _quantity: int = 0
    _percent: float = 0.0 # от 0 до 100
    _pixel_progress: int = 0

    _left_top: tuple[int, int]
    _width_height: tuple[int, int]

    def __init__(self, tuple[int, int] left_top, tuple[int, int] width_height) -> None:
        self._left_top = left_top
        self._width_height = width_height

    def update_progress(self) -> None:
        if self._percent > 100:
            self._percent = 100.0
        elif self._percent < 0:
            self._percent = 0

        if self._is_quantity:
            if self._quantity_main <= 0:
                self._quantity_main = 100
        
            if self._quantity > self._quantity_main:
                self._quantity = self._quantity_main
            elif self._quantity < 0:
                self._quantity = 0

            if self._quantity == 0:
                self._percent = 0.0
            else:
                self._percent = (self._quantity / self._quantity_main) * 100.0
        
        if self._width_height[0] > self._width_height[1]:
            self._pixel_progress = (self._percent/100)*self.width
        else:
            self._pixel_progress = (self._percent/100)*self.height

    def math_quantity(self) -> None:
        if self._is_quantity:
            self._quantity = int(self._quantity_main * (self._percent / 100))

    def set_pixel(self, int pixel) -> None: # без ограничений
        self._pixel_progress = pixel
    def get_pixel(self) -> int:
        return self._pixel_progress

    def set_percent(self, float percent) -> None:
        self._percent = percent
        self.update_progress()
    def get_percent(self, ) -> float:
        return self._percent
    def add_percent(self, float percent) -> None:
        self.set_percent(self.get_percent()+percent)

    def set_quantity_main(self, int quantity) -> None:
        self._is_quantity = True
        self._quantity_main = quantity
        self.update_progress()
    def get_quantity_main(self) -> int:
        return self._quantity_main
    def add_quantity_main(self, quantity: int) -> None:
        self._is_quantity = True
        self._quantity_main += quantity
        self.update_progress()

    def get_quantity(self) -> int:
        return self._quantity
    def set_quantity(self, quantity: int) -> None:
        self._is_quantity = True
        self._quantity = quantity
        self.update_progress()
    def add_quantity(self, quantity: int) -> None:
        self._is_quantity = True
        self._quantity += quantity
        self.update_progress()
    def clear_quantity(self) -> None:
        self._is_quantity = True
        self._quantity = 0
        self.update_progress()
    def del_quantity(self) -> None:
        self._quantity = 0
        self._quantity_main = 100
        self._is_quantity = False
        self.update_progress()
    
    @property
    def left(self) -> int:
        return self._left_top[0]
    @left.setter
    def left(self, int left) -> None:
        self._left_top = (left, self._left_top[1])

    @property
    def top(self) -> int:
        return self._left_top[1]
    @top.setter
    def top(self, int top) -> None:
        self._left_top = (self._left_top[0], top)
    
    @property
    def left_top(self) -> tuple[int, int]:
        return self._left_top
    @left_top.setter
    def left_top(self, tuple[int, int] left_top) -> None:
        self._left_top = left_top

    @property
    def width(self) -> int:
        return self._width_height[0]
    @width.setter
    def width(self, int width) -> None:
        self._width_height = (width, self._width_height[1])

    @property
    def height(self) -> int:
        return self._width_height[1]
    @height.setter
    def height(self, int height) -> None:
        self._width_height = (self._width_height[0], height)
    
    @property
    def width_height(self) -> tuple[int, int]:
        return self._width_height
    @width_height.setter
    def width_height(self, tuple[int, int] width_height) -> None:
        self._width_height = width_height
    
    
