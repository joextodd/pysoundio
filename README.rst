PySoundIo
=========

.. image:: https://travis-ci.org/joextodd/pysoundio.svg?branch=master
    :target: https://travis-ci.org/joextodd/pysoundio
.. image:: https://coveralls.io/repos/github/joextodd/pysoundio/badge.svg
    :target: https://coveralls.io/github/joextodd/pysoundio
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
so to use the latest version you will need to install from `source <http://libsound.io/#releases>`_.


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

* macOS ::

    brew install libsndfile

* Ubuntu / Debian ::

    apt-get install libsndfile1


:download:`devices.py <../examples/devices.py>`

List the available input and output devices on the system and their properties. ::

    python devices.py


:download:`record.py <../examples/record.py>`

Records data from microphone and saves to a wav file.
Supports specifying backend, device, sample rate, block size. ::

    python record.py out.wav --device 0 --rate 44100


:download:`play.py <../examples/play.py>`

Plays a wav file through the speakers.
Supports specifying backend, device, block size. ::

    python play.py in.wav --device 0


:download:`sine.py <../examples/sine.py>`

Plays a sine wave through the speakers.
Supports specifying backend, device, sample rate, block size. ::

    python sine.py --freq 442


Testing
-------

To run the test suite. ::

    python setup.py test

