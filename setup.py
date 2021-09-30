from setuptools import setup
from Cython.Build import cythonize

setup(
    name='levenshtein',
    ext_modules=cythonize("leven_cython.pyx"),
    zip_safe=False,
)