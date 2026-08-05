# math3d.pyi
# Интерфейс модуля для статической типизации и документации.
# Все матрицы представлены кортежами из 16 чисел (float) в столбцовом порядке (column-major).

from typing import Tuple

def degrees_to_radians(deg: int): ...
    # из градуса в радиант

def radians_to_degrees(deg: float): ...
    # из радианта в градус


# ----------------------------------------------------------------------
# Базовые операции с матрицами
# ----------------------------------------------------------------------

def identity_matrix() -> Tuple[float, ...]:
    """
    Возвращает единичную матрицу 4x4 как кортеж из 16 чисел.
    """
    ...

def multiply_matrices(A: Tuple[float, ...], B: Tuple[float, ...]) -> Tuple[float, ...]:
    """
    Умножает две матрицы 4x4 (A * B). Каждая матрица – кортеж из 16 чисел.
    Возвращает результирующую матрицу.
    """
    ...

# ----------------------------------------------------------------------
# Матрицы трансформаций
# ----------------------------------------------------------------------

def translation(tx: float, ty: float, tz: float) -> Tuple[float, ...]:
    """
    Создаёт матрицу переноса на вектор (tx, ty, tz).
    """
    ...

def scaling(sx: float, sy: float, sz: float) -> Tuple[float, ...]:
    """
    Создаёт матрицу масштабирования с коэффициентами (sx, sy, sz).
    """
    ...

def rotation_x(angle: float) -> Tuple[float, ...]:
    """
    Создаёт матрицу поворота вокруг оси X на угол (в радианах).
    """
    ...

def rotation_y(angle: float) -> Tuple[float, ...]:
    """
    Создаёт матрицу поворота вокруг оси Y на угол (в радианах).
    """
    ...

def rotation_z(angle: float) -> Tuple[float, ...]:
    """
    Создаёт матрицу поворота вокруг оси Z на угол (в радианах).
    """
    ...

# ----------------------------------------------------------------------
# Матрица вида и проекции
# ----------------------------------------------------------------------

def look_at(eye_x: float, eye_y: float, eye_z: float,
            target_x: float, target_y: float, target_z: float,
            up_x: float, up_y: float, up_z: float) -> Tuple[float, ...]:
    """
    Создаёт матрицу вида (камера), направленную из точки eye на target,
    с вектором up. Возвращает матрицу 4x4.
    """
    ...

def perspective(fov: float, aspect: float, near: float, far: float) -> Tuple[float, ...]:
    """
    Создаёт матрицу перспективной проекции.
    :param fov: угол обзора по вертикали в радианах.
    :param aspect: отношение ширины к высоте (width/height).
    :param near: расстояние до ближней плоскости отсечения.
    :param far: расстояние до дальней плоскости отсечения.
    """
    ...

def orthographic(left: float, right: float, bottom: float, top: float,
                 near: float, far: float) -> Tuple[float, ...]:
    """
    Создаёт матрицу ортографической проекции.
    """
    ...

# ----------------------------------------------------------------------
# Кватернионы (экспортируемые функции)
# ----------------------------------------------------------------------

def quat_identity() -> Tuple[float, float, float, float]:
    """
    Возвращает единичный кватернион (0, 0, 0, 1) как кортеж (x, y, z, w).
    """
    ...

def quat_from_euler(pitch: float, yaw: float, roll: float) -> Tuple[float, float, float, float]:
    """
    Создаёт кватернион из углов Эйлера (порядок XYZ) в радианах.
    Возвращает кортеж (x, y, z, w).
    """
    ...

def quat_to_matrix(q: Tuple[float, float, float, float]) -> Tuple[float, ...]:
    """
    Преобразует кватернион (x, y, z, w) в матрицу вращения 4x4.
    """
    ...

def quat_multiply(q1: Tuple[float, float, float, float],
                  q2: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    """
    Умножает два кватерниона (композиция вращений).
    """
    ...

def quat_conjugate(q: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    """
    Возвращает сопряжённый кватернион.
    """
    ...

def quat_normalize(q: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    """
    Нормализует кватернион (делает единичную длину).
    """
    ...

# ----------------------------------------------------------------------
# Преобразование координат
# ----------------------------------------------------------------------

def world_to_screen(mvp: Tuple[float, ...],
                    x: float, y: float, z: float,
                    viewport_width: int, viewport_height: int) -> Tuple[float, float, float]:
    """
    Преобразует мировую точку (x, y, z) в экранные координаты.
    :param mvp: матрица вида-проекции (MVP).
    :param viewport_width, viewport_height: размеры окна вывода.
    :return: кортеж (screen_x, screen_y, depth) – где screen_x, screen_y в пикселях,
             depth в диапазоне [0, 1].
    """
    ...

# ----------------------------------------------------------------------
# Отсечение (Frustum culling)
# ----------------------------------------------------------------------

def extract_frustum_planes(mvp: Tuple[float, ...]) -> Tuple[Tuple[float, float, float, float], ...]:
    """
    Извлекает 6 плоскостей frustum из матрицы MVP (вида-проекции).
    Возвращает кортеж из 6 плоскостей, каждая задана уравнением (a, b, c, d)
    где a*x + b*y + c*z + d = 0. Плоскости нормализованы.
    """
    ...

def point_in_frustum(planes: Tuple[Tuple[float, float, float, float], ...],
                     x: float, y: float, z: float) -> bool:
    """
    Проверяет, находится ли точка (x, y, z) внутри frustum.
    planes – результат extract_frustum_planes.
    """
    ...

def sphere_in_frustum(planes: Tuple[Tuple[float, float, float, float], ...],
                      cx: float, cy: float, cz: float, radius: float) -> bool:
    """
    Проверяет, пересекает ли сфера с центром (cx, cy, cz) и радиусом radius
    frustum (true – видима хотя бы частично).
    """
    ...