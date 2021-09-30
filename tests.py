import pytest
import leven_cython, leven_python
import time
from main import get_closest_packages_cython, get_closest_packages_python

packages = []
with open('data/data.txt') as file:
    for line in file:
        packages.append(line.strip())

def test_levenshtein():
    s1 = 'numpy'
    s2 = 'numpa'

    dist = leven_cython.levenshtein(s1, s2)
    print(dist)
    assert dist is not None


def test_levenshtein_cython_time():
    start_time = time.time()
    closest_packages = get_closest_packages_cython('numpy', packages)
    print(closest_packages)
    processing_time = time.time() - start_time
    print(f'Processing time: {time.time() - start_time}')
    assert processing_time < 0.5


def test_levenshtein_python_time():
    start_time = time.time()
    closest_packages = get_closest_packages_python('numpy', packages)
    print(closest_packages)
    processing_time = time.time() - start_time
    print(f'Processing time: {time.time() - start_time}')
    assert processing_time < 0.5


"""def test_levenshtein_list():
    l = ['bumpy', 'dumpy', 'gnumpy', 'gumpy', 'humpy', 'jumpy', 'Lumpy', 'ncmpy', 'nempy', 'nlmpy', 'nsmpy', 'nump5y', 
    'numphy', 'numpsy', 'numpy', 'numpy1', 'numpyx', 'numspy', 'nupy', 'nutpy', 'nuvpy', 'pnumpy', 'pumpy', 'rnumpy', 
    'snumpy', 'sumpy', 'umpy', 'unumpy', 'wumpy', 'xnumpy', 'random phrase 1', 'random phrase 2', 'xyzabc']
    s = 'numpy'
    results = leven_cython_list.levenshtein_list(l, s)
    assert results == ['bumpy', 'dumpy', 'gnumpy', 'gumpy', 'humpy', 'jumpy', 'Lumpy', 'ncmpy', 'nempy', 'nlmpy', 'nsmpy',
                       'nump5y', 'numphy', 'numpsy', 'numpy', 'numpy1', 'numpyx', 'numspy', 'nupy', 'nutpy', 'nuvpy',
                       'pnumpy', 'pumpy', 'rnumpy', 'snumpy', 'sumpy', 'umpy', 'unumpy', 'wumpy', 'xnumpy']"""

"""def test_levenshtein_list():
    l = ['random phrase 1', 'random phrase 2', 'xyzabc']
    s = 'numpy'
    results = leven_cython_list.levenshtein_list(l, s)
    assert results == []"""
