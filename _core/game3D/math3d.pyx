# math3d.pyx
# Исправленная версия со всеми объявлениями cdef в начале функций

from libc.math cimport sqrt, cos, sin, tan, pi

def degrees_to_radians(int deg):
    # из градуса в радиант
    return deg * pi / 180.0

def radians_to_degrees(float deg):
    # из радианта в градус
    return int((deg / pi) * 180)

# 1. Базовые структуры (с массивами)

cdef struct Vec2:
    float v[2]

cdef struct Vec3:
    float v[3]

cdef struct Vec4:
    float v[4]

cdef struct Mat4:
    float m[16]          # column-major

cdef struct Quat:
    float q[4]           # x, y, z, w

cdef struct FrustumPlanes:
    Vec4 planes[6]       # left, right, bottom, top, near, far

# 2. Вспомогательные конструкторы

cdef inline Vec2 vec2(float x, float y):
    cdef Vec2 r
    r.v[0] = x; r.v[1] = y
    return r

cdef inline Vec3 vec3(float x, float y, float z):
    cdef Vec3 r
    r.v[0] = x; r.v[1] = y; r.v[2] = z
    return r

cdef inline Vec4 vec4(float x, float y, float z, float w):
    cdef Vec4 r
    r.v[0] = x; r.v[1] = y; r.v[2] = z; r.v[3] = w
    return r

cdef inline Quat quat(float x, float y, float z, float w):
    cdef Quat r
    r.q[0] = x; r.q[1] = y; r.q[2] = z; r.q[3] = w
    return r

# 3. Векторные операции

cdef inline Vec2 vec2_add(Vec2 a, Vec2 b):
    return vec2(a.v[0] + b.v[0], a.v[1] + b.v[1])

cdef inline Vec2 vec2_sub(Vec2 a, Vec2 b):
    return vec2(a.v[0] - b.v[0], a.v[1] - b.v[1])

cdef inline Vec2 vec2_mul(Vec2 v, float s):
    return vec2(v.v[0] * s, v.v[1] * s)

cdef inline float vec2_dot(Vec2 a, Vec2 b):
    return a.v[0] * b.v[0] + a.v[1] * b.v[1]

cdef inline float vec2_len(Vec2 v):
    return sqrt(v.v[0] * v.v[0] + v.v[1] * v.v[1])

cdef inline Vec2 vec2_normalize(Vec2 v):
    cdef float l = vec2_len(v)
    if l == 0: return vec2(0, 0)
    return vec2(v.v[0] / l, v.v[1] / l)


cdef inline Vec3 vec3_add(Vec3 a, Vec3 b):
    return vec3(a.v[0] + b.v[0], a.v[1] + b.v[1], a.v[2] + b.v[2])

cdef inline Vec3 vec3_sub(Vec3 a, Vec3 b):
    return vec3(a.v[0] - b.v[0], a.v[1] - b.v[1], a.v[2] - b.v[2])

cdef inline Vec3 vec3_mul(Vec3 v, float s):
    return vec3(v.v[0] * s, v.v[1] * s, v.v[2] * s)

cdef inline float vec3_dot(Vec3 a, Vec3 b):
    return a.v[0] * b.v[0] + a.v[1] * b.v[1] + a.v[2] * b.v[2]

cdef inline Vec3 vec3_cross(Vec3 a, Vec3 b):
    return vec3(a.v[1] * b.v[2] - a.v[2] * b.v[1],
                a.v[2] * b.v[0] - a.v[0] * b.v[2],
                a.v[0] * b.v[1] - a.v[1] * b.v[0])

cdef inline float vec3_len(Vec3 v):
    return sqrt(v.v[0] * v.v[0] + v.v[1] * v.v[1] + v.v[2] * v.v[2])

cdef inline Vec3 vec3_normalize(Vec3 v):
    cdef float l = vec3_len(v)
    if l == 0: return vec3(0, 0, 0)
    return vec3(v.v[0] / l, v.v[1] / l, v.v[2] / l)


cdef inline Vec4 vec4_add(Vec4 a, Vec4 b):
    return vec4(a.v[0] + b.v[0], a.v[1] + b.v[1], a.v[2] + b.v[2], a.v[3] + b.v[3])

cdef inline Vec4 vec4_mul(Vec4 v, float s):
    return vec4(v.v[0] * s, v.v[1] * s, v.v[2] * s, v.v[3] * s)

cdef inline Vec4 vec3_to_vec4(Vec3 v, float w):
    return vec4(v.v[0], v.v[1], v.v[2], w)

# 4. Матрицы 4x4

cdef inline Mat4 mat4_identity():
    cdef Mat4 M
    cdef int i
    for i in range(16): M.m[i] = 0.0
    M.m[0] = M.m[5] = M.m[10] = M.m[15] = 1.0
    return M

cdef inline Mat4 mat4_mul(Mat4 A, Mat4 B):
    cdef Mat4 C
    cdef int i, j, k
    for i in range(4):
        for j in range(4):
            C.m[i*4 + j] = 0.0
            for k in range(4):
                C.m[i*4 + j] += A.m[i*4 + k] * B.m[k*4 + j]
    return C

cdef inline Vec4 mat4_mul_vec4(Mat4 M, Vec4 v):
    cdef Vec4 r
    r.v[0] = M.m[0]*v.v[0] + M.m[4]*v.v[1] + M.m[8]*v.v[2] + M.m[12]*v.v[3]
    r.v[1] = M.m[1]*v.v[0] + M.m[5]*v.v[1] + M.m[9]*v.v[2] + M.m[13]*v.v[3]
    r.v[2] = M.m[2]*v.v[0] + M.m[6]*v.v[1] + M.m[10]*v.v[2] + M.m[14]*v.v[3]
    r.v[3] = M.m[3]*v.v[0] + M.m[7]*v.v[1] + M.m[11]*v.v[2] + M.m[15]*v.v[3]
    return r


cdef inline Mat4 mat4_translation(Vec3 t):
    cdef Mat4 M = mat4_identity()
    M.m[12] = t.v[0]
    M.m[13] = t.v[1]
    M.m[14] = t.v[2]
    return M

cdef inline Mat4 mat4_scale(Vec3 s):
    cdef Mat4 M = mat4_identity()
    M.m[0] = s.v[0]
    M.m[5] = s.v[1]
    M.m[10] = s.v[2]
    return M

cdef inline Mat4 mat4_rotation_x(float angle):
    cdef float c = cos(angle), s = sin(angle)
    cdef Mat4 M = mat4_identity()
    M.m[5] = c; M.m[9] = -s
    M.m[6] = s; M.m[10] = c
    return M

cdef inline Mat4 mat4_rotation_y(float angle):
    cdef float c = cos(angle), s = sin(angle)
    cdef Mat4 M = mat4_identity()
    M.m[0] = c; M.m[8] = s
    M.m[2] = -s; M.m[10] = c
    return M

cdef inline Mat4 mat4_rotation_z(float angle):
    cdef float c = cos(angle), s = sin(angle)
    cdef Mat4 M = mat4_identity()
    M.m[0] = c; M.m[4] = -s
    M.m[1] = s; M.m[5] = c
    return M


cdef inline Mat4 mat4_look_at(Vec3 eye, Vec3 target, Vec3 up):
    cdef Vec3 f = vec3_normalize(vec3_sub(target, eye))
    cdef Vec3 s = vec3_normalize(vec3_cross(f, up))
    cdef Vec3 u = vec3_cross(s, f)
    cdef Mat4 M = mat4_identity()
    M.m[0] = s.v[0]; M.m[4] = s.v[1]; M.m[8] = s.v[2]; M.m[12] = -vec3_dot(s, eye)
    M.m[1] = u.v[0]; M.m[5] = u.v[1]; M.m[9] = u.v[2]; M.m[13] = -vec3_dot(u, eye)
    M.m[2] = -f.v[0]; M.m[6] = -f.v[1]; M.m[10] = -f.v[2]; M.m[14] = vec3_dot(f, eye)
    return M


cdef inline Mat4 mat4_inverse(Mat4 M):
    cdef Mat4 inv = mat4_identity()
    cdef float a[16], b[16]
    cdef int i, j, k
    cdef float pivot, factor
    for i in range(16):
        a[i] = M.m[i]
        b[i] = inv.m[i]
    for i in range(4):
        pivot = a[i*4 + i]
        if pivot == 0:
            for j in range(i+1, 4):
                if a[j*4 + i] != 0:
                    for k in range(4):
                        a[i*4 + k], a[j*4 + k] = a[j*4 + k], a[i*4 + k]
                        b[i*4 + k], b[j*4 + k] = b[j*4 + k], b[i*4 + k]
                    pivot = a[i*4 + i]
                    break
        for j in range(4):
            a[i*4 + j] /= pivot
            b[i*4 + j] /= pivot
        for j in range(4):
            if j == i: continue
            factor = a[j*4 + i]
            for k in range(4):
                a[j*4 + k] -= factor * a[i*4 + k]
                b[j*4 + k] -= factor * b[i*4 + k]
    for i in range(16):
        inv.m[i] = b[i]
    return inv

# 5. Кватернионы

cdef inline Quat quat_identity():
    return quat(0, 0, 0, 1)

cdef inline Quat quat_mul(Quat q1, Quat q2):
    return quat(
        q1.q[3]*q2.q[0] + q1.q[0]*q2.q[3] + q1.q[1]*q2.q[2] - q1.q[2]*q2.q[1],
        q1.q[3]*q2.q[1] - q1.q[0]*q2.q[2] + q1.q[1]*q2.q[3] + q1.q[2]*q2.q[0],
        q1.q[3]*q2.q[2] + q1.q[0]*q2.q[1] - q1.q[1]*q2.q[0] + q1.q[2]*q2.q[3],
        q1.q[3]*q2.q[3] - q1.q[0]*q2.q[0] - q1.q[1]*q2.q[1] - q1.q[2]*q2.q[2]
    )

cdef inline Quat quat_conjugate(Quat q):
    return quat(-q.q[0], -q.q[1], -q.q[2], q.q[3])

cdef inline float quat_norm(Quat q):
    return sqrt(q.q[0]*q.q[0] + q.q[1]*q.q[1] + q.q[2]*q.q[2] + q.q[3]*q.q[3])

cdef inline Quat quat_normalize(Quat q):
    cdef float n = quat_norm(q)
    if n == 0: return quat_identity()
    return quat(q.q[0]/n, q.q[1]/n, q.q[2]/n, q.q[3]/n)

cdef inline Quat quat_from_euler(float pitch, float yaw, float roll):
    cdef float cy = cos(yaw*0.5), sy = sin(yaw*0.5)
    cdef float cp = cos(pitch*0.5), sp = sin(pitch*0.5)
    cdef float cr = cos(roll*0.5), sr = sin(roll*0.5)
    return quat(
        sr*cp*cy - cr*sp*sy,
        cr*sp*cy + sr*cp*sy,
        cr*cp*sy - sr*sp*cy,
        cr*cp*cy + sr*sp*sy
    )

cdef inline Mat4 quat_to_mat4(Quat q):
    cdef float xx = q.q[0]*q.q[0], yy = q.q[1]*q.q[1], zz = q.q[2]*q.q[2]
    cdef float xy = q.q[0]*q.q[1], xz = q.q[0]*q.q[2], yz = q.q[1]*q.q[2]
    cdef float wx = q.q[3]*q.q[0], wy = q.q[3]*q.q[1], wz = q.q[3]*q.q[2]
    cdef Mat4 M = mat4_identity()
    M.m[0] = 1 - 2*(yy + zz)
    M.m[4] = 2*(xy - wz)
    M.m[8] = 2*(xz + wy)
    M.m[1] = 2*(xy + wz)
    M.m[5] = 1 - 2*(xx + zz)
    M.m[9] = 2*(yz - wx)
    M.m[2] = 2*(xz - wy)
    M.m[6] = 2*(yz + wx)
    M.m[10] = 1 - 2*(xx + yy)
    return M

# 6. Функции проекций

cdef inline Mat4 mat4_perspective(float fov_rad, float aspect, float near, float far):
    cdef float tan_half_fov = tan(fov_rad / 2.0)
    cdef Mat4 M = mat4_identity()
    M.m[0] = 1.0 / (aspect * tan_half_fov)
    M.m[5] = 1.0 / tan_half_fov
    M.m[10] = -(far + near) / (far - near)
    M.m[11] = -1.0
    M.m[14] = -(2.0 * far * near) / (far - near)
    M.m[15] = 0.0
    return M

cdef inline Mat4 mat4_ortho(float left, float right, float bottom, float top, float near, float far):
    cdef Mat4 M = mat4_identity()
    M.m[0] = 2.0 / (right - left)
    M.m[5] = 2.0 / (top - bottom)
    M.m[10] = -2.0 / (far - near)
    M.m[12] = -(right + left) / (right - left)
    M.m[13] = -(top + bottom) / (top - bottom)
    M.m[14] = -(far + near) / (far - near)
    return M

# 7. Отсечение (Frustum Culling)

cdef inline FrustumPlanes frustum_from_matrix(Mat4 MVP):
    cdef FrustumPlanes fp
    cdef float *m = MVP.m
    cdef int i
    cdef float norm_len
    fp.planes[0] = vec4(m[3] + m[0], m[7] + m[4], m[11] + m[8], m[15] + m[12]) # Левая
    fp.planes[1] = vec4(m[3] - m[0], m[7] - m[4], m[11] - m[8], m[15] - m[12]) # Правая
    fp.planes[2] = vec4(m[3] + m[1], m[7] + m[5], m[11] + m[9], m[15] + m[13]) # Нижняя
    fp.planes[3] = vec4(m[3] - m[1], m[7] - m[5], m[11] - m[9], m[15] - m[13]) # Верхняя
    fp.planes[4] = vec4(m[3] + m[2], m[7] + m[6], m[11] + m[10], m[15] + m[14]) # Ближняя
    fp.planes[5] = vec4(m[3] - m[2], m[7] - m[6], m[11] - m[10], m[15] - m[14]) # Дальняя
    # Нормализация всех плоскостей
    for i in range(6):
        norm_len = sqrt(fp.planes[i].v[0]*fp.planes[i].v[0] +
                        fp.planes[i].v[1]*fp.planes[i].v[1] +
                        fp.planes[i].v[2]*fp.planes[i].v[2])
        fp.planes[i].v[0] /= norm_len
        fp.planes[i].v[1] /= norm_len
        fp.planes[i].v[2] /= norm_len
        fp.planes[i].v[3] /= norm_len
    return fp

cdef inline bint is_point_in_frustum(FrustumPlanes fp, Vec3 point):
    cdef int i
    for i in range(6):
        if (fp.planes[i].v[0] * point.v[0] +
            fp.planes[i].v[1] * point.v[1] +
            fp.planes[i].v[2] * point.v[2] +
            fp.planes[i].v[3] < 0):
            return False
    return True

cdef inline bint is_sphere_in_frustum(FrustumPlanes fp, Vec3 center, float radius):
    cdef int i
    for i in range(6):
        if (fp.planes[i].v[0] * center.v[0] +
            fp.planes[i].v[1] * center.v[1] +
            fp.planes[i].v[2] * center.v[2] +
            fp.planes[i].v[3] < -radius):
            return False
    return True

# 8. Преобразование координат (мировые -> экранные)

cdef inline Vec3 world_to_screen(Mat4 MVP, Vec3 world_point,
                                 int viewport_width, int viewport_height):
    cdef Vec4 clip = mat4_mul_vec4(MVP, vec3_to_vec4(world_point, 1.0))
    cdef Vec3 ndc
    cdef Vec3 screen
    ndc.v[0] = clip.v[0] / clip.v[3]
    ndc.v[1] = clip.v[1] / clip.v[3]
    ndc.v[2] = clip.v[2] / clip.v[3]
    screen.v[0] = (ndc.v[0] + 1.0) * 0.5 * viewport_width
    screen.v[1] = (1.0 - ndc.v[1]) * 0.5 * viewport_height
    screen.v[2] = (ndc.v[2] + 1.0) * 0.5
    return screen