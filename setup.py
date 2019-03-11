"""
PySoundIo

A robust, cross-platform solution for real-time audio.
"""
import os
import re
import platform
import shutil
from setuptools import setup, Extension

vstr = open('pysoundio/__init__.py', 'r').read()
regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
version = re.search(regex, vstr, re.M)

if platform.system() == 'Windows':
    windows_path = os.path.join('C:', os.sep, 'ProgramData', 'libsoundio')
    library_path = os.path.join(windows_path,
        'x86_64' if platform.machine().endswith('64') else 'i686')
    include_dirs = ['./pysoundio', windows_path]
    library_dirs = [library_path]
    shutil.copyfile(os.path.join(library_path, 'libsoundio.dll.a'),
                    os.path.join(library_path, 'soundio.lib'))
else:
    include_dirs = ['./pysoundio', '/usr/local/include']
    library_dirs = ['/usr/local/lib']

soundio = Extension('_soundiox',
                    sources=['pysoundio/_soundiox.c'],
                    include_dirs=include_dirs,
                    library_dirs=library_dirs,
                    libraries=['soundio'])

setup(
    name='pysoundio',
    version=version.group(1),
    description='Python wrapper for libsoundio',
    long_description='A robust, cross-platform solution for real-time audio',
    license='MIT',
    author='Joe Todd',
    author_email='joextodd@gmail.com',
    url='http://pysoundio.readthedocs.io/en/latest/',
    download_url='https://github.com/joextodd/pysoundio/archive/' + version.group(1) + '.tar.gz',
    include_package_data=True,
    packages=['pysoundio'],
    ext_modules=[soundio],
    test_suite='tests',
    keywords=['audio', 'sound', 'stream'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License'
    ],
)
