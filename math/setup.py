from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name="fastrect",
    version="1.0.0",
    ext_modules=cythonize(
        "rect.pyx",
        language_level=3,
        compiler_directives={
            "boundscheck": False,
            "wraparound": False,
            "cdivision": True,
            "embedsignature": True,
        },
    ),
    zip_safe=False,
)