from setuptools import setup
from Cython.Build import cythonize

setup(
    name='calculations',
    ext_modules=cythonize("calculations.pyx"),
    packages=['listing']
)