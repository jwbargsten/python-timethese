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

ired of writing the same code again and again when comparing the runtime of
more than one function? `timethese` helps with this type of micro-benchmarking.
It basically runs timeit (or actually repeat) on multiple functions and spits
out a report.

In one sentence: timethese is timeit for multiple functions with better reporting

* Free software: MIT License

Installation
============

::

    pip install timethese

You can also install the in-development version with::

    pip install https://github.com/jwbargsten/python-timethese/archive/master.zip


Usage
=====

Microbenchmark
--------------

`timethese` has a 3 step approach:

1. define the functions you want to compare
2. feed them to cmpthese as list or dict (see below)
3. format the results, aka pretty print

Let's have a look::

      from timethese import cmpthese, pprint_cmp, timethese

      xs = range(10)


      # 1. DEFINE FUNCTIONS

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


      # 2. FEED THE FUNCTIONS TO CMPTHESE

      # AS DICT:

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


      # OR AS LIST:

      cmp_res_list = cmpthese(
          10000, [map_hex, list_compr_hex, map_lambda, map_lambda_fn, list_compr_nofn,], repeat=3,
      )

      # 3. PRETTY PRINT THE RESULTS

      print(pprint_cmp(cmp_res_dict))
      print(pprint_cmp(cmp_res_list))

What do you get if you run this?

Depending on the runtime of the supplied functions, either rate (unit: 1/s) or
the seconds per iteration (s/iter) are shown.

For dict something like:
.. code-block::


                            Rate  list_compr_nofn  map_hex  map_lambda  map_lambda_fn  list_compr_hex
      list_compr_nofn  1385057/s                .      43%         47%            48%             88%
              map_hex   969501/s             -30%        .          3%             4%             31%
           map_lambda   940257/s             -32%      -3%           .             1%             27%
        map_lambda_fn   935508/s             -32%      -4%         -1%              .             27%
       list_compr_hex   738367/s             -47%     -24%        -21%           -21%               .

For list something like:
.. code-block::

                              Rate  4.list_compr_nofn  0.map_hex  2.map_lambda  3.map_lambda_fn  1.list_compr_hex
      4.list_compr_nofn  1360009/s                  .        31%           42%              46%               78%
              0.map_hex  1037581/s               -24%          .            9%              11%               36%
           2.map_lambda   955513/s               -30%        -8%             .               2%               25%
        3.map_lambda_fn   933666/s               -31%       -10%           -2%                .               22%
       1.list_compr_hex   763397/s               -44%       -26%          -20%             -18%                 .


(the function names are taken from `fn.__name__` and prefixed with the list index.)

Timing
------

`timethese` also has the function `timethese`, which is used by `cmpthese`
internally. To get the timings directly, you can run::

      from timethese import cmpthese, pprint_cmp, timethese

      xs = range(10)


      # 1. DEFINE FUNCTIONS

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


      # 2. FEED THE FUNCTIONS TO CMPTHESE

      # AS DICT:

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

Timing functions with decorators
--------------------------------
`timethese` also provides decorators to time single functions::

     import time
     import timethese

     @timethese.print_time
     def calculate_something():
         time.sleep(1)

     calculate_something()

Four decorators are provided, 2 for normal stuff

* ``timethese.print_time``
* ``timethese.log_time(logger, level=logging.INFO)``

and 2 for pandas dataframes (they also print the shape of the resulting dataframe).
Useful when using ``df.pipe(...)``

* ``timethese.log_time_df(logger, level=logging.INFO)``
* ``timethese.print_time_df``

See the function documentation in the source code for better examples.

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
