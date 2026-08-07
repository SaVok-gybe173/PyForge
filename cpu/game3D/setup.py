from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy
import os

# Корень проекта
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Путь к папке, где лежит rect.pxd
rect_dir = os.path.join(root_dir, "PyForge", "_core", "game3D")

ext = Extension(
    "camera",
    sources=["camera.pyx"],
    include_dirs=[numpy.get_include(), rect_dir]   # <-- добавляем папку с rect.pxd
)

setup(
    ext_modules=cythonize([ext], compiler_directives={'language_level': 3}),
    zip_safe=False,
)