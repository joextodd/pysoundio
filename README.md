# pysoundio

The aim of this project is to create a simple Pythonic interface to libsoundio.

libsoundio is a robust, cross-platform solution for real-time audio. It performs
no buffering or processing on your behalf, instead exposing the raw power of the
underlying backend.

See [libsoundio](libsound.io)


## Installation

On macOS

    `brew install libsoundio`

For Linux and Windows head to libsound.io and compile from source

Then install pysoundio

    `python setup.py install`