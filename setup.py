import glob
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize


def build_extensions():
    sources = glob.glob("PyForge/**/*.pyx", recursive=True)
    return [
        Extension(
            src[:-4].replace("\\", "/").replace("/", "."),
            [src],
        )
        for src in sources
    ]


def main():
    setup(
        name="PyForge",
        version="0.1.0",
        packages=find_packages(),
        ext_modules=cythonize(
            build_extensions(),
            language_level=3,
            annotate=True,
            force=True,
        ),
    )


if __name__ == "__main__":
    main()