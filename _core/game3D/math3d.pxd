# math3d.pxd

cdef struct Vec2:
    float v[2]

cdef struct Vec3:
    float v[3]

cdef struct Vec4:
    float v[4]

cdef struct Mat4:
    float m[16]

cdef struct Quat:
    float q[4]

cdef Mat4 mat4_identity()
cdef Mat4 mat4_rotation_x(float angle)
cdef Mat4 mat4_rotation_y(float angle)
cdef Mat4 mat4_rotation_z(float angle)
cdef Mat4 mat4_mul(Mat4 A, Mat4 B)
cdef Vec4 mat4_mul_vec4(Mat4 M, Vec4 v)
cdef Vec4 vec3_to_vec4(Vec3 v, float w)
cdef Vec3 vec3(float x, float y, float z)
# при необходимости добавьте другие функции, которые используете