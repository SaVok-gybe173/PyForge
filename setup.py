import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p or '.') != _here]

import glob
import shutil

from setuptools import setup, Extension, find_namespace_packages
from Cython.Build import cythonize
import numpy


def _copy_pxd_to_pyforge():
    """Копирует .pxd в PyForge/, чтобы Cython нашёл их по имени модуля PyForge.*"""
    dst_root = os.path.join(_here, "PyForge")
    if os.path.exists(dst_root):
        shutil.rmtree(dst_root, ignore_errors=True)
    for root, dirs, files in os.walk(_here):
        # не заходим в служебные папки
        dirs[:] = [d for d in dirs if d not in {".git", "build", "dist", "wheelhouse", "__pycache__", ".venv", "venv"}]
        for f in files:
            if f.endswith(".pxd"):
                src = os.path.join(root, f)
                rel = os.path.relpath(src, _here)
                dst = os.path.join(dst_root, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)


def _cleanup():
    shutil.rmtree(os.path.join(_here, "PyForge"), ignore_errors=True)


def build_extensions():
    sources = [
        s for s in glob.glob("**/*.pyx", recursive=True)
        if not s.startswith("PyForge" + os.sep) and not s.startswith("PyForge/")
    ]
    extensions = []
    for src in sources:
        module_name = "PyForge." + src[:-4].replace("\\", "/").replace("/", ".")
        extensions.append(
            Extension(
                module_name,
                [src],
                include_dirs=[numpy.get_include(), "."],
            )
        )
    return extensions


def main():
    _copy_pxd_to_pyforge()
    try:
        subpackages = find_namespace_packages(
            where=".",
            include=["*"],
            exclude=["PyForge", "PyForge.*", "build*", "dist*", "wheelhouse*", "tests*", "examples*"],
        )
        packages = ["PyForge"] + ["PyForge." + p for p in subpackages]

        setup(
            name="PyForge",
            version="0.1.0",
            packages=packages,
            package_dir={"PyForge": "."},
            include_package_data=False,
            exclude_package_data={"": ["*.c", "*.html", "*.pyx", "*.pxd"]},
            ext_modules=cythonize(
                build_extensions(),
                language_level=3,
                annotate=False,
                force=True,
                include_path=["..", "."],
            ),
            python_requires=">=3.12",
            zip_safe=False,
        )
    finally:
        _cleanup()


if __name__ == "__main__":
    main()
