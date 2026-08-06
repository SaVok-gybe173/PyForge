from math3d cimport *
import numpy as np

cdef class Rect3D:
    cdef float[:, :] vertices
    cdef int[:, :] indices
    cdef float[:, :] normals
    cdef float[:, :] uvs
    cdef float[:, :] colors

    def __init__(self, vertices_list, indices_list, normals_list=None, uvs_list=None, colors_list=None):
        self.vertices = np.array(vertices_list, dtype=np.float32)

        self.indices = np.array(indices_list, dtype=np.int32)
        if normals_list is not None:
            self.normals = np.array(normals_list, dtype=np.float32)
        if uvs_list is not None:
            self.uvs = np.array(uvs_list, dtype=np.float32)
        if colors_list is not None:
            self.colors = np.array(colors_list, dtype=np.float32)

    def rotate(self, float ax, float ay, float az):
        cdef Mat4 rot = mat4_rotation_x(ax)
        rot = mat4_mul(mat4_rotation_y(ay), rot)
        rot = mat4_mul(mat4_rotation_z(az), rot)
        cdef int i
        cdef Vec4 v
        for i in range(self.vertices.shape[0]):
            v = vec3_to_vec4(vec3(self.vertices[i,0], self.vertices[i,1], self.vertices[i,2]), 1.0)
            v = mat4_mul_vec4(rot, v)
            self.vertices[i,0] = v.v[0] / v.v[3]
            self.vertices[i,1] = v.v[1] / v.v[3]
            self.vertices[i,2] = v.v[2] / v.v[3]

    def offset(self, int x, int y, int z):
        for i in range(self.vertices.shape[0]):
            self.vertices[i,0] = self.vertices[i, 0] + x
            self.vertices[i,1] = self.vertices[i, 1] + y
            self.vertices[i,2] = self.vertices[i, 2] + z

    def get_aabb(self):
        """Возвращает ограничивающий параллелепипед (AABB) текущих вершин."""
        cdef int i
        cdef float minx, maxx, miny, maxy, minz, maxz
        minx = maxx = self.vertices[0,0]
        miny = maxy = self.vertices[0,1]
        minz = maxz = self.vertices[0,2]
        for i in range(1, self.vertices.shape[0]):
            if self.vertices[i,0] < minx: minx = self.vertices[i,0]
            elif self.vertices[i,0] > maxx: maxx = self.vertices[i,0]
            if self.vertices[i,1] < miny: miny = self.vertices[i,1]
            elif self.vertices[i,1] > maxy: maxy = self.vertices[i,1]
            if self.vertices[i,2] < minz: minz = self.vertices[i,2]
            elif self.vertices[i,2] > maxz: maxz = self.vertices[i,2]
        return (minx, maxx, miny, maxy, minz, maxz)

    def collidepoint(self, float x, float y, float z):
        """Проверяет, находится ли точка (x,y,z) внутри AABB объекта."""
        aabb = self.get_aabb()
        return (aabb[0] <= x <= aabb[1] and
                aabb[2] <= y <= aabb[3] and
                aabb[4] <= z <= aabb[5])

    def colliderect(self, Rect3D other):
        """Проверяет пересечение AABB текущего объекта с другим объектом."""
        a = self.get_aabb()
        b = other.get_aabb()
        return (a[0] < b[1] and a[1] > b[0] and
                a[2] < b[3] and a[3] > b[2] and
                a[4] < b[5] and a[5] > b[4])

    def get_vertices(self):
        return self.vertices
    def set_vertices(self, vertices_list):
        self.vertices = np.array(vertices_list, dtype=np.float32)
    