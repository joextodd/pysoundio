PySoundIo
=========

.. image:: https://travis-ci.org/joextodd/pysoundio.svg?branch=master
    :target: https://travis-ci.org/joextodd/pysoundio
.. image:: https://readthedocs.org/projects/pysoundio/badge/?version=latest
    :target: http://pysoundio.readthedocs.io/en/latest/?badge=latest


A simple Pythonic interface for `libsoundio <http://libsound.io>`_.

libsoundio is a robust, cross-platform solution for real-time audio. It performs
no buffering or processing on your behalf, instead exposing the raw power of the
underlying backend.


Dependencies
------------

* macOS ::

    brew install libsoundio

* Ubuntu / Debian ::

    apt-get install libsoundio-dev

Ubuntu distributions link to an older version of libsoundio,
so to use the latest version you will need to install from `source. <http://libsound.io/#releases>`_.


Installation
------------

Once you have installed the dependencies, you can use pip to download
and install the latest release with a single command. ::

    pip install pysoundio

or from source ::

    python setup.py install


Examples
--------

See examples directory.

Some of the examples require `pysoundfile <https://pysoundfile.readthedocs.io/en/0.9.0/>`_ ::

    pip install pysoundfile

on Linux machines you will need to install libsndfile ::

    apt-get install libsndfile


Testing
-------

To run the test suite. ::

    python setup.py test

