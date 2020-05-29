========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|

.. |travis| image:: https://api.travis-ci.org/jwbargsten/python-timethese.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jwbargsten/python-timethese

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


.. end-badges

timeit for multiple functions with better reporting

* Free software: MIT License

Installation
============

::

    pip install timethese

You can also install the in-development version with::

    pip install https://github.com/jwbargsten/python-timethese/archive/master.zip


Usage
=====

To use TimeThese in a project::

      from timethese import cmpthese, pprint_cmp, timethese

      xs = range(10)


      def map_hex():
          list(map(hex, xs))


      def list_compr_hex():
          list([hex(x) for x in xs])


      def map_lambda():
          list(map(lambda x: x + 2, xs))


      def map_lambda_fn():
          fn = lambda x: x + 2
          list(map(fn, xs))


      def list_compr_nofn():
          list([x + 2 for x in xs])


      cmp_res_dict = cmpthese(
          10000,
          {
              "map_hex": map_hex,
              "list_compr_hex": list_compr_hex,
              "map_lambda": map_lambda,
              "map_lambda_fn": map_lambda_fn,
              "list_compr_nofn": list_compr_nofn,
          },
          repeat=3,
      )

      print(pprint_cmp(cmp_res_dict))


      cmp_res_list = cmpthese(
          10000, [map_hex, list_compr_hex, map_lambda, map_lambda_fn, list_compr_nofn,], repeat=3,
      )

      print(pprint_cmp(cmp_res_list))


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
