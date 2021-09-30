# typosquatting
A demo for exploring PyPI package names

Typosquatting is the act of creating software packages with names that mimic popular package names. A study (Speed Meyers and Tozer, 2020) found 40 such typosquatting attacks against PyPI users between 2017 and 2020.

There are nearly 329,000 PyPI packages as at 30/September/2021. This demo project allows a user to enter a PyPI package name, and the summaries of any projects with closely related names will be displayed. Closely related names are detected by finding those package names within a Levenshtein edit distance of 1.

The Levenshtein algorithm is implemented using Cython, resulting in calculation times that are 2.3 times faster than the pure Python equivalent. In order to compile the Cython file you may have to run the following command:

    python .\setup.py build_ext --inplace

Requests to PyPI for summary texts are handled using asyncio, allowing multiple requests to be sent concurrently. The summary texts from PyPI are parsed from the index page of each package using the Beautiful Soup library.

References:
Speed Meyers, J. and Tozer, B. (2020) "Bewear! Python Typosquatting Is About More Than Typos", In-Q-Tel, Inc., 28 September 2020. Available at https://www.iqt.org/bewear-python-typosquatting-is-about- more-than-typos/ (Accessed 30 September 2021).
