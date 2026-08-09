from rect cimport Rect3D
import pygame

cdef class Camera:
    cdef float pos_x, pos_y, pos_z
    cdef float rot_x, rot_y, rot_z
    cdef int fov
    cdef int width, height
    cdef list rects
    cdef tuple color_line

    def __init__(self, list rects, int fov=90, int width=800, int height=600):
        self.rects = rects
        self.fov = fov
        self.width = width
        self.height = height
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0
        self.color_line = (255, 255, 255)

    def set_position(self, float x, float y, float z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

    def translate(self, float dx, float dy, float dz):
        self.pos_x += dx
        self.pos_y += dy
        self.pos_z += dz

    def set_rotation(self, float ax, float ay, float az):
        self.rot_x = ax
        self.rot_y = ay
        self.rot_z = az

    def rotate(self, float ax, float ay, float az):
        self.rot_x += ax
        self.rot_y += ay
        self.rot_z += az

    def set_color_line(self, int r, int g, int b):
        self.color_line = (r, g, b)

    def get_color_line(self) -> tuple[int, int, int]:
        return self.color_line

    cdef tuple _project_point(self, float x, float y, float z):
        cdef float wz = z - self.pos_z
        cdef float factor = self.fov / (self.fov + wz)
        if wz + self.fov > 0:
            px = (x - self.pos_x) * -factor
            py = (y - self.pos_y) * factor
            screen_x = (px + 1) * self.width / 2
            screen_y = (1 - py) * self.height / 2
            return (screen_x, screen_y, wz) 
        else:
            return None

    def draw_vertices(self, scene):
        cdef Rect3D rect
        cdef int i, j
        cdef float[:, :] verts
        cdef int[:, :] idxs
        cdef tuple p1, p2, p3
        cdef int n

        for rect in self.rects:
            verts = rect.get_vertices()
            idxs = rect.get_indices()
            n = idxs.shape[1]

            projected = []
            for i in range(verts.shape[0]):
                p = self._project_point(verts[i, 0], verts[i, 1], verts[i, 2])
                projected.append(p)

            if n == 2:
                for j in range(idxs.shape[0]):
                    p1 = projected[idxs[j, 0]]
                    p2 = projected[idxs[j, 1]]
                    if p1 is not None and p2 is not None:
                        pygame.draw.line(
                            scene,
                            self.color_line,
                            (int(p1[0]), int(p1[1])),
                            (int(p2[0]), int(p2[1])),
                            1
                        )
            elif n == 3:
                for j in range(idxs.shape[0]):
                    p1 = projected[idxs[j, 0]]
                    p2 = projected[idxs[j, 1]]
                    p3 = projected[idxs[j, 2]]
                    if p1 is not None and p2 is not None and p3 is not None:
                        pygame.draw.line(
                            scene,
                            self.color_line,
                            (int(p1[0]), int(p1[1])),
                            (int(p2[0]), int(p2[1])),
                            1
                        )
                        pygame.draw.line(
                            scene,
                            self.color_line,
                            (int(p2[0]), int(p2[1])),
                            (int(p3[0]), int(p3[1])),
                            1
                        )
                        pygame.draw.line(
                            scene,
                            self.color_line,
                            (int(p3[0]), int(p3[1])),
                            (int(p1[0]), int(p1[1])),
                            1
                        )

    def draw_solid(self, scene, color=(255, 255, 255)):
        """
        Рисует все объекты залитыми треугольниками одного цвета.
        Сортирует треугольники по глубине (painter's algorithm).
        """
        cdef Rect3D rect
        cdef float[:, :] verts
        cdef int[:, :] idxs
        cdef list triangles = []
        cdef int i, j
        cdef tuple p1, p2, p3
        cdef float depth

        for rect in self.rects:
            verts = rect.get_vertices()
            idxs = rect.get_indices()
            if idxs.shape[1] != 3:
                continue   
            for j in range(idxs.shape[0]):
                i1 = idxs[j, 0]
                i2 = idxs[j, 1]
                i3 = idxs[j, 2]
                p1 = self._project_point(verts[i1,0], verts[i1,1], verts[i1,2])
                p2 = self._project_point(verts[i2,0], verts[i2,1], verts[i2,2])
                p3 = self._project_point(verts[i3,0], verts[i3,1], verts[i3,2])
                if p1 is not None and p2 is not None and p3 is not None:
                    depth = (p1[2] + p2[2] + p3[2]) / 3.0
                    pts = [(p1[0], p1[1]), (p2[0], p2[1]), (p3[0], p3[1])]
                    triangles.append((depth, pts))
        triangles.sort(key=lambda t: t[0], reverse=True)
        for depth, pts in triangles:
            pts_int = [(int(x), int(y)) for x, y in pts]
            pygame.draw.polygon(scene, color, pts_int)