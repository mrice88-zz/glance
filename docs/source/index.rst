Welcome to glance's documentation!
==================================

Glance is a package that allows one to mark a function for timing, and keep tabs on what's going on in your code.

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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Package Contents
=================

.. automodule:: glance

Glance
==============

.. autoclass:: Glance
    :members:

Watch
==============

.. autoclass:: Watch
    :members:

Watch
==============

.. autoclass:: Look
    :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

