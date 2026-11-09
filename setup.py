import os
import sys
# Убираем корень проекта из sys.path, чтобы папка math/ не затеняла стандартный модуль
_here = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p or '.') != _here]

import glob
import shutil

from setuptools import setup, Extension, find_namespace_packages
from Cython.Build import cythonize
import numpy


def _create_pyforge_link():
    """Создаёт PyForge -> . чтобы Cython нашёл .pxd по пути PyForge/..."""
    link = os.path.join(_here, "PyForge")
    if os.path.exists(link):
        return
    try:
        os.symlink(".", link)  # Linux / macOS
    except (OSError, NotImplementedError):
        # Windows: симлинки требуют прав — копируем .pxd файлы
        os.makedirs(link, exist_ok=True)
        for root, _, files in os.walk(_here):
            if "PyForge" in root.split(os.sep):
                continue
            for f in files:
                if f.endswith(".pxd"):
                    src = os.path.join(root, f)
                    rel = os.path.relpath(src, _here)
                    dst = os.path.join(link, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)


def _cleanup_pyforge_link():
    """Удаляет временный симлинк/папку после сборки."""
    link = os.path.join(_here, "PyForge")
    if os.path.islink(link):
        os.unlink(link)
    elif os.path.isdir(link):
        shutil.rmtree(link, ignore_errors=True)


def build_extensions():
    sources = glob.glob("**/*.pyx", recursive=True)
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
    _create_pyforge_link()

    try:
        subpackages = find_namespace_packages(
            where=".",
            include=["*"],
            exclude=[
                "PyForge", "PyForge.*",       # временный симлинк
                "build*", "dist*", "wheelhouse*",
                "tests*", "examples*", "docs*",
            ],
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
        _cleanup_pyforge_link()


if __name__ == "__main__":
    main()
