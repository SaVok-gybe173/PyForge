from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["math3d.pyx", "rect.pyx"],
                          compiler_directives={'language_level': 3})
)