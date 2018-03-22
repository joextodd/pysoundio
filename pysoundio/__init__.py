#
# MIT License
#
# Copyright (c) 2018 Joe Todd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ctypes as _ctypes
from ctypes.util import find_library as _find_library

__version__ = '0.0.1'


_libname = _find_library('libsoundio')
if _libname is None:
    raise OSError('libsoundio not found')
else:
    _lib = _ctypes.CDLL(_libname)


from .structures import (
    soundio_error_callback,
    soundio_overflow_callback,
    soundio_read_callback,
    SoundIo,
    SoundIoChannelArea,
    SoundIoChannelLayout,
    SoundIoDevice,
    SoundIoInStream,
    SoundIoRingBuffer,
)


# ------------------------------------------------------------------------
# Symbol bindings
# ------------------------------------------------------------------------
_lib.soundio_backend_count.argtypes = [_ctypes.POINTER(SoundIo)]
_lib.soundio_backend_count.restype = _ctypes.c_int
_lib.soundio_backend_name.argtypes = [_ctypes.c_uint]
_lib.soundio_backend_name.restype = _ctypes.c_char_p
_lib.soundio_best_matching_channel_layout.argtypes = [
    _ctypes.POINTER(SoundIoChannelLayout), _ctypes.c_int,
    _ctypes.POINTER(SoundIoChannelLayout), _ctypes.c_int,
]
_lib.soundio_connect.argtypes = [_ctypes.POINTER(SoundIo)]
_lib.soundio_connect.restype = _ctypes.c_int
_lib.soundio_connect_backend.argtypes = [_ctypes.POINTER(SoundIo), _ctypes.c_uint]
_lib.soundio_connect_backend.restype = _ctypes.c_int
_lib.soundio_create.restype = _ctypes.POINTER(SoundIo)
_lib.soundio_ring_buffer_create.argtypes = [
    _ctypes.POINTER(SoundIo), _ctypes.c_int
]
_lib.soundio_ring_buffer_create.restype = _ctypes.POINTER(SoundIoRingBuffer)
_lib.soundio_default_input_device_index.argtypes = [_ctypes.POINTER(SoundIo)]
_lib.soundio_default_input_device_index.restype = _ctypes.c_int
_lib.soundio_default_output_device_index.argtypes = [_ctypes.POINTER(SoundIo)]
_lib.soundio_default_output_device_index.restype = _ctypes.c_int
_lib.soundio_device_sort_channel_layouts.argtypes = [_ctypes.POINTER(SoundIoDevice)]
_lib.soundio_device_supports_sample_rate.argtypes = [
    _ctypes.POINTER(SoundIoDevice), _ctypes.c_int
]
_lib.soundio_device_supports_sample_rate.restype = _ctypes.c_bool
_lib.soundio_device_supports_format.argtypes = [
    _ctypes.POINTER(SoundIoDevice), _ctypes.c_uint
]
_lib.soundio_device_supports_format.restype = _ctypes.c_bool
_lib.soundio_device_unref.argtypes = [_ctypes.POINTER(SoundIoDevice)]
_lib.soundio_disconnect.argtypes = [_ctypes.POINTER(SoundIo)]
_lib.soundio_format_string.argtypes = [_ctypes.c_uint]
_lib.soundio_format_string.restype = _ctypes.c_char_p
_lib.soundio_flush_events.argtypes = [_ctypes.POINTER(SoundIo)]
_lib.soundio_get_bytes_per_sample.argtypes = [_ctypes.c_uint]
_lib.soundio_get_bytes_per_sample.restype = _ctypes.c_int
_lib.soundio_channel_layout_get_default.argtypes = [_ctypes.c_int]
_lib.soundio_channel_layout_get_default.restype = _ctypes.POINTER(SoundIoChannelLayout)
_lib.soundio_get_input_device.argtypes = [_ctypes.POINTER(SoundIo), _ctypes.c_int]
_lib.soundio_get_input_device.restype = _ctypes.POINTER(SoundIoDevice)
_lib.soundio_get_output_device.argtypes = [_ctypes.POINTER(SoundIo), _ctypes.c_int]
_lib.soundio_get_output_device.restype = _ctypes.POINTER(SoundIoDevice)
_lib.soundio_instream_begin_read.argtypes = [
    _ctypes.POINTER(SoundIoInStream), _ctypes.POINTER(_ctypes.POINTER(SoundIoChannelArea)),
    _ctypes.POINTER(_ctypes.c_int)
]
_lib.soundio_instream_begin_read.restype = _ctypes.c_int
_lib.soundio_instream_create.argtypes = [_ctypes.POINTER(SoundIoDevice)]
_lib.soundio_instream_create.restype = _ctypes.POINTER(SoundIoInStream)
_lib.soundio_instream_destroy.argtypes = [_ctypes.POINTER(SoundIoInStream)]
_lib.soundio_instream_end_read.argtypes = [_ctypes.POINTER(SoundIoInStream)]
_lib.soundio_instream_end_read.restype = _ctypes.c_int
_lib.soundio_instream_get_latency.argtypes = [
    _ctypes.POINTER(SoundIoInStream), _ctypes.POINTER(_ctypes.c_double)
]
_lib.soundio_instream_get_latency.restype = _ctypes.c_int
_lib.soundio_instream_open.argtypes = [_ctypes.POINTER(SoundIoInStream)]
_lib.soundio_instream_open.restype = _ctypes.c_int
_lib.soundio_instream_pause.argtypes = [_ctypes.POINTER(SoundIoInStream), _ctypes.c_bool]
_lib.soundio_instream_pause.restype = _ctypes.c_int
_lib.soundio_instream_start.argtypes = [_ctypes.POINTER(SoundIoInStream)]
_lib.soundio_instream_start.restype = _ctypes.c_int
_lib.soundio_ring_buffer_advance_write_ptr.argtypes = [
    _ctypes.POINTER(SoundIoRingBuffer), _ctypes.c_int
]
_lib.soundio_ring_buffer_free_count.argtypes = [_ctypes.POINTER(SoundIoRingBuffer)]
_lib.soundio_ring_buffer_free_count.restype = _ctypes.c_int
_lib.soundio_ring_buffer_read_ptr.argtypes = [_ctypes.POINTER(SoundIoRingBuffer)]
_lib.soundio_ring_buffer_read_ptr.restype = _ctypes.c_char_p
_lib.soundio_ring_buffer_write_ptr.argtypes = [_ctypes.POINTER(SoundIoRingBuffer)]
_lib.soundio_ring_buffer_write_ptr.restype = _ctypes.POINTER(_ctypes.c_int8)
_lib.soundio_strerror.argtypes = [_ctypes.c_int]
_lib.soundio_strerror.restype = _ctypes.c_char_p
_lib.soundio_version_string.restype = _ctypes.c_char_p


from .pysoundio import PySoundIo
