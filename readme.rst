.. this file is kept in the docs\source directory and COPIED to the project root directory.
.. DO NOT edit the copy in the project root directory.

glance (timing utility)
=======================

Simple to use package that keeps track of various functions execution times. Ala timeit, but in your code.
Useful utility as a


Installation
============

.. code-block:: console

    pip install glance-times

Simple Example
==============

.. code:: python

    from glance import Glance

    gl = Glance()

    @gl.watch
    def func_a():
        # some functionality.