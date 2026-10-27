import glob
from setuptools import setup, Extension, find_namespace_packages
from Cython.Build import cythonize



def build_extensions():
    sources = glob.glob("**/*.pyx", recursive=True)
    extensions = []
    for src in sources:
        module_name = "PyForge." + src[:-4].replace("\\", "/").replace("/", ".")
        extensions.append(Extension(module_name, [src], include_dirs=["."]))
    return extensions


def main():
    subpackages = find_namespace_packages(where=".", include=["*"])
    packages = ["PyForge"] + ["PyForge." + p for p in subpackages]

    setup(
        name="PyForge",
        version="0.1.0",
        packages=packages,
        package_dir={"PyForge": "."}, 
        ext_modules=cythonize(
            build_extensions(),
            language_level=3,
            annotate=True,
            force=True,
        ),
        python_requires=">=3.12",
        zip_safe=False,
    )


if __name__ == "__main__":
    main()

    