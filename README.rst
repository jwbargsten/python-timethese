========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-timethese/badge/?style=flat
    :target: https://readthedocs.org/projects/python-timethese
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/jwbargsten/python-timethese.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jwbargsten/python-timethese

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/jwbargsten/python-timethese?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/jwbargsten/python-timethese

.. |requires| image:: https://requires.io/github/jwbargsten/python-timethese/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/jwbargsten/python-timethese/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/jwbargsten/python-timethese/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/jwbargsten/python-timethese

.. |version| image:: https://img.shields.io/pypi/v/timethese.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/timethese

.. |wheel| image:: https://img.shields.io/pypi/wheel/timethese.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/timethese

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/timethese.svg
    :alt: Supported versions
    :target: https://pypi.org/project/timethese

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/timethese.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/timethese

.. |commits-since| image:: https://img.shields.io/github/commits-since/jwbargsten/python-timethese/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/jwbargsten/python-timethese/compare/v0.0.1...master



.. end-badges

timeit for multiple functions with better reporting

* Free software: BSD 2-Clause License

Installation
============

::

    pip install timethese

You can also install the in-development version with::

    pip install https://github.com/jwbargsten/python-timethese/archive/master.zip


Documentation
=============


https://python-timethese.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
