# pysoundio

[![Build Status](https://travis-ci.org/joextodd/pysoundio.svg?branch=master)](https://travis-ci.org/joextodd/pysoundio)

The aim of this project is to create a simple Pythonic interface to libsoundio.

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

