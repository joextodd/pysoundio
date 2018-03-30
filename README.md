# pysoundio

[![Build Status](https://travis-ci.org/joextodd/pysoundio.svg?branch=master)](https://travis-ci.org/joextodd/pysoundio)

A simple Pythonic interface to libsoundio.

libsoundio is a robust, cross-platform solution for real-time audio. It performs
no buffering or processing on your behalf, instead exposing the raw power of the
underlying backend.

See [libsoundio](libsound.io)


## Dependencies

### macOS

    brew install libsoundio

### Ubuntu / Debian

    apt-get install libsoundio-dev


## Installation

Install from PyPi

    pip install pysoundio

or from source

    python setup.py install


## Tests

    python setup.py test


## Examples

See examples directory.

Some of the examples require [pysoundfile](https://pysoundfile.readthedocs.io/en/0.9.0/)


    pip install pysoundfile

on Linux machines you will need to install libsndfile

    apt-get install libsndfile

