import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_here_real = os.path.normcase(os.path.realpath(_here))


def _is_project_path(p):
    """True, если p указывает на корень проекта или его подкаталог."""
    if not p:
        return True
    try:
        p_real = os.path.normcase(os.path.realpath(p))
    except OSError:
        return False
    return p_real == _here_real or p_real.startswith(_here_real + os.sep)


# Убираем корень проекта и всё под ним, чтобы math/, time.pyx, font/ и т.п.
# не перекрывали stdlib и site-packages при импорте build/setuptools/wheel.
sys.path = [p for p in sys.path if not _is_project_path(p)]

import glob
import shutil

from setuptools import setup, Extension, find_namespace_packages
from Cython.Build import cythonize
import numpy


STAGE_DIR = os.path.join(_here, "PyForge")
STAGE_EXTS = (".py", ".pyx", ".pxd", ".pyi")
SKIP_DIRS = {
    ".git", ".github", "build", "dist", "wheelhouse", "__pycache__",
    ".venv", "venv", "env", ".env", ".tox", ".nox", ".idea", ".vscode",
    "node_modules", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "PyForge",
}


def _stage_package():
    """Копирует весь исходный код в PyForge/, чтобы wheel получился как
    site-packages/PyForge/... — с импортами вида `import PyForge.cpu`."""
    if os.path.exists(STAGE_DIR):
        shutil.rmtree(STAGE_DIR, ignore_errors=True)
    os.makedirs(STAGE_DIR, exist_ok=True)

    for root, dirs, files in os.walk(_here):
        dirs[:] = [
            d for d in dirs
            if d not in SKIP_DIRS
            and not d.endswith(".egg-info")
            and not d.startswith(".")
        ]
        rel = os.path.relpath(root, _here)
        for f in files:
            if not f.endswith(STAGE_EXTS):
                continue
            src = os.path.join(root, f)
            dst = (
                os.path.join(STAGE_DIR, f)
                if rel == "."
                else os.path.join(STAGE_DIR, rel, f)
            )
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)


def _cleanup():
    shutil.rmtree(STAGE_DIR, ignore_errors=True)


def _build_extensions():
    """Extension'ы из staged .pyx: PyForge.cpu.game3D.camera и т.п."""
    sources = glob.glob(os.path.join(STAGE_DIR, "**", "*.pyx"), recursive=True)
    extensions = []
    for src in sources:
        rel = os.path.relpath(src, STAGE_DIR)
        module_name = "PyForge." + rel[:-4].replace(os.sep, ".").replace("/", ".")
        extensions.append(
            Extension(
                module_name,
                [os.path.relpath(src, _here)],
                include_dirs=[numpy.get_include(), STAGE_DIR, _here],
            )
        )
    return extensions


def main():
    os.chdir(_here)
    _stage_package()
    try:
        subpackages = find_namespace_packages(where=STAGE_DIR, include=["*"])
        packages = ["PyForge"] + ["PyForge." + p for p in subpackages]

        setup(
    name="PyForge",
    version="0.1.0",
    packages=packages,
    package_dir={"": "."},
    include_package_data=False,
    ext_modules=cythonize(
        _build_extensions(),
        language_level=3,
        annotate=False,
        include_path=[_here, STAGE_DIR],
    ),
    python_requires=">=3.12",
    zip_safe=False,
    script_args=["bdist_wheel", "--dist-dir", "dist"],
)
    finally:
        _cleanup()


if __name__ == "__main__":
    main()
