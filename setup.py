"""
PySoundIo setup.py

"""
import re
from setuptools import setup, Extension

vstr = open('pysoundio/__init__.py', 'r').read()
regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
version = re.search(regex, vstr, re.M)

soundio = Extension('_soundio',
                    sources=['pysoundio/_soundiomodule.c'],
                    libraries=['soundio'])

setup(
    name='pysoundio',
    version=version.group(1),
    description='Python wrapper for libsoundio',
    long_description='A robust, cross-platform solution for real-time audio in Python',
    license='MIT',
    author='Joe Todd',
    author_email='joextodd@gmail.com',
    url='libsound.io',
    packages=['pysoundio'],
    ext_modules=[soundio],
    keywords=('audio', 'sound', 'stream')
)