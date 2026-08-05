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