from setuptools import setup
from Cython.Build import cythonize

setup(
    name='calculation_progress',
    ext_modules=cythonize("calculation_progress.pyx"),
)