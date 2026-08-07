cdef class Rect3D:
    cdef float[:, :] vertices
    cdef int[:, :] indices
    cdef float[:, :] normals
    cdef float[:, :] uvs
    cdef float[:, :] colors

    cpdef float[:, :] get_vertices(self)
    cpdef int[:, :] get_indices(self)