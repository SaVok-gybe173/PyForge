import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
print(sys.path)

from PyForge._core.game3D.rect import Rect3D
from PyForge._core.game3D.obj import load

import math
import pygame as pg

verts = [
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1]
]
idxs = [
    [0, 1, 2],
    [2, 3, 0]
]

cube = Rect3D(verts, idxs)
ds = Rect3D(verts, idxs)


cube.rotate(math.pi, math.pi, math.pi)
print(Rect3D.__dict__)
print(cube.colliderect(ds))

cube.offset(10, 1, 10)

verts = cube.get_vertices()
for i in range(verts.shape[0]):
    x, y, z = verts[i,0], verts[i,1], verts[i,2]
    print(x, y, z)


obgect = Rect3D(*load("obj/maps/map1.obj"))
obgect.offset(10, 1, 10)

verts = obgect.get_vertices()
for i in range(verts.shape[0]):
    x, y, z = verts[i,0], verts[i,1], verts[i,2]
    print(x, y, z)