"""
Play and Record Sound in Python using libsoundio

libsoundio is a C library for cross-platform audio input and output.
It is suitable for real-time and consumer software.
-> https://libsound.io
"""
import ctypes as _ctypes
import platform as _platform

from . import _libsoundio
from .exceptions import PySoundIoError
from .structures import (
    soundio_overflow_callback,
    soundio_read_callback,
    RecordContext,
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
_libsoundio.soundio_backend_count.argtypes = [_ctypes.POINTER(SoundIo)]
_libsoundio.soundio_backend_count.restype = _ctypes.c_int
_libsoundio.soundio_backend_name.argtypes = [_ctypes.c_uint]
_libsoundio.soundio_backend_name.restype = _ctypes.c_char_p
_libsoundio.soundio_best_matching_channel_layout.argtypes = [
    _ctypes.POINTER(SoundIoChannelLayout), _ctypes.c_int,
    _ctypes.POINTER(SoundIoChannelLayout), _ctypes.c_int,
]
_libsoundio.soundio_connect.argtypes = [_ctypes.POINTER(SoundIo)]
_libsoundio.soundio_connect.restype = _ctypes.c_int
_libsoundio.soundio_connect_backend.argtypes = [_ctypes.POINTER(SoundIo), _ctypes.c_uint]
_libsoundio.soundio_connect_backend.restype = _ctypes.c_int
_libsoundio.soundio_create.restype = _ctypes.POINTER(SoundIo)
_libsoundio.soundio_ring_buffer_create.argtypes = [
    _ctypes.POINTER(SoundIo), _ctypes.c_int
]
_libsoundio.soundio_ring_buffer_create.restype = _ctypes.POINTER(SoundIoRingBuffer)
_libsoundio.soundio_default_input_device_index.argtypes = [_ctypes.POINTER(SoundIo)]
_libsoundio.soundio_default_input_device_index.restype = _ctypes.c_int
_libsoundio.soundio_default_output_device_index.argtypes = [_ctypes.POINTER(SoundIo)]
_libsoundio.soundio_default_output_device_index.restype = _ctypes.c_int
_libsoundio.soundio_device_sort_channel_layouts.argtypes = [_ctypes.POINTER(SoundIoDevice)]
_libsoundio.soundio_device_supports_sample_rate.argtypes = [
    _ctypes.POINTER(SoundIoDevice), _ctypes.c_int
]
_libsoundio.soundio_device_supports_sample_rate.restype = _ctypes.c_bool
_libsoundio.soundio_device_supports_format.argtypes = [
    _ctypes.POINTER(SoundIoDevice), _ctypes.c_uint
]
_libsoundio.soundio_device_supports_format.restype = _ctypes.c_bool
_libsoundio.soundio_device_unref.argtypes = [_ctypes.POINTER(SoundIoDevice)]
_libsoundio.soundio_disconnect.argtypes = [_ctypes.POINTER(SoundIo)]
_libsoundio.soundio_format_string.argtypes = [_ctypes.c_uint]
_libsoundio.soundio_format_string.restype = _ctypes.c_char_p
_libsoundio.soundio_flush_events.argtypes = [_ctypes.POINTER(SoundIo)]
_libsoundio.soundio_get_input_device.argtypes = [_ctypes.POINTER(SoundIo), _ctypes.c_int]
_libsoundio.soundio_get_input_device.restype = _ctypes.POINTER(SoundIoDevice)
_libsoundio.soundio_get_output_device.argtypes = [_ctypes.POINTER(SoundIo), _ctypes.c_int]
_libsoundio.soundio_get_output_device.restype = _ctypes.POINTER(SoundIoDevice)
_libsoundio.soundio_instream_begin_read.argtypes = [
    _ctypes.POINTER(SoundIoInStream), _ctypes.POINTER(_ctypes.POINTER(SoundIoChannelArea)),
    _ctypes.POINTER(_ctypes.c_int)
]
_libsoundio.soundio_instream_begin_read.restype = _ctypes.c_int
_libsoundio.soundio_instream_create.argtypes = [_ctypes.POINTER(SoundIoDevice)]
_libsoundio.soundio_instream_create.restype = _ctypes.POINTER(SoundIoInStream)
_libsoundio.soundio_instream_destroy.argtypes = [_ctypes.POINTER(SoundIoInStream)]
_libsoundio.soundio_instream_end_read.argtypes = [_ctypes.POINTER(SoundIoInStream)]
_libsoundio.soundio_instream_end_read.restype = _ctypes.c_int
_libsoundio.soundio_instream_get_latency.argtypes = [
    _ctypes.POINTER(SoundIoInStream), _ctypes.POINTER(_ctypes.c_double)
]
_libsoundio.soundio_instream_get_latency.restype = _ctypes.c_int
_libsoundio.soundio_instream_open.argtypes = [_ctypes.POINTER(SoundIoInStream)]
_libsoundio.soundio_instream_open.restype = _ctypes.c_int
_libsoundio.soundio_instream_pause.argtypes = [_ctypes.POINTER(SoundIoInStream), _ctypes.c_bool]
_libsoundio.soundio_instream_pause.restype = _ctypes.c_int
_libsoundio.soundio_instream_start.argtypes = [_ctypes.POINTER(SoundIoInStream)]
_libsoundio.soundio_instream_start.restype = _ctypes.c_int
_libsoundio.soundio_ring_buffer_advance_write_ptr.argtypes = [
    _ctypes.POINTER(SoundIoRingBuffer), _ctypes.c_int
]
_libsoundio.soundio_ring_buffer_free_count.argtypes = [_ctypes.POINTER(SoundIoRingBuffer)]
_libsoundio.soundio_ring_buffer_free_count.restype = _ctypes.c_int
_libsoundio.soundio_ring_buffer_read_ptr.argtypes = [_ctypes.POINTER(SoundIoRingBuffer)]
_libsoundio.soundio_ring_buffer_read_ptr.restype = _ctypes.c_char_p
_libsoundio.soundio_ring_buffer_write_ptr.argtypes = [_ctypes.POINTER(SoundIoRingBuffer)]
_libsoundio.soundio_ring_buffer_write_ptr.restype = _ctypes.c_char_p
_libsoundio.soundio_strerror.argtypes = [_ctypes.c_int]
_libsoundio.soundio_strerror.restype = _ctypes.c_char_p
_libsoundio.soundio_version_string.restype = _ctypes.c_char_p


class PySoundIo(object):

    def __init__(self, backend=None):
        self.instream = None
        self.outstream = None
        self.input_device = None
        self.output_device = None
        self.ring_buffer = None
        self.ctx = RecordContext()

        self.backend = backend
        self._soundio = _libsoundio.soundio_create()
        if self._soundio is None:
            raise PySoundIoError('Out of memory')
        if backend:
            self._call(_libsoundio.soundio_connect_backend, self._soundio, backend)
        else:
            self._call(_libsoundio.soundio_connect, self._soundio)

        self._flush()

    @property
    def version(self):
        """ Return version string """
        return _libsoundio.soundio_version_string().decode()

    def close(self):
        """ Close libsoundio connection """
        if self.instream:
            _libsoundio.soundio_instream_destroy(self.instream)
        if self.input_device:
            _libsoundio.soundio_device_unref(self.input_device)
        if self._soundio:
            _libsoundio.soundio_destroy(self._soundio)

    def _flush(self):
        """ Flush events """
        _libsoundio.soundio_flush_events(self._soundio)

    def _call(self, fn, *args, **kwargs):
        """ Call libsoundio function and check error codes """
        rc = fn(*args, **kwargs)
        if rc != 0:
            err = _libsoundio.soundio_strerror(rc)
            raise PySoundIoError(err.decode())

    def list_devices(self):
        """ Return a list of available devices """
        output_count = _libsoundio.soundio_output_device_count(self._soundio)
        input_count = _libsoundio.soundio_input_device_count(self._soundio)

        default_output = _libsoundio.soundio_default_output_device_index(self._soundio)
        default_input = _libsoundio.soundio_default_input_device_index(self._soundio)

        print('--------Input Devices--------')
        for i in range(0, input_count):
            device = _libsoundio.soundio_get_input_device(self._soundio, i)
            self.print_device(device, default_input == i)
            _libsoundio.soundio_device_unref(device)

        print('--------Output Devices--------')
        for i in range(0, output_count):
            device = _libsoundio.soundio_get_output_device(self._soundio, i)
            self.print_device(device, default_output == i)
            _libsoundio.soundio_device_unref(device)

        print('%d devices found' % (input_count + output_count))

    def print_device(self, device, is_default=False):
        """ Print device information """
        print('%s' % device.contents.id)
        print('%s is_raw=%s' % (device.contents.name, device.contents.is_raw))

    def get_default_input_device(self):
        """ Returns default input device """
        device_index = _libsoundio.soundio_default_input_device_index(self._soundio)
        self.input_device = self.get_input_device(device_index)

    def get_input_device(self, device_id):
        """ Return an input device """
        device = _libsoundio.soundio_get_input_device(self._soundio, device_id)
        if not device:
            raise PySoundIoError('Input device %d not available' % device_id)
        if device.contents.probe_error:
            raise PySoundIoError('Unable to probe input device: %s' % (
                _libsoundio.soundio_strerror(device.contents.probe_error)))
        return device

    def get_outut_device(self, device_id):
        """ Return an outut device """
        device = _libsoundio.soundio_get_outut_device(self._soundio, device_id)
        if not device:
            raise PySoundIoError('Output device %d not available' % device_id)
        if device.contents.probe_error:
            raise PySoundIoError('Unable to probe output device: %s' % (
                _libsoundio.soundio_strerror(device.contents.probe_error)))
        return device

    def supports_sample_rate(self, device, rate):
        """ Check the sample rate is supported by the selected device """
        return _libsoundio.soundio_device_supports_sample_rate(device, rate)

    def supports_format(self, device, format):
        """ Check the format is supported by the selected device """
        return _libsoundio.soundio_device_supports_format(device, format)

    def sort_channel_layouts(self, device):
        """ Sorts channel layouts by channel count, descending """
        _libsoundio.soundio_device_sort_channel_layouts(device)

    def create_input_stream(self, device, format, rate, read_callback, overflow_callback):
        """ Allocates memory and sets defaults """
        self.instream = _libsoundio.soundio_instream_create(device)
        if not self.instream:
            raise PySoundIoError('Could not create input stream')

        self.instream.contents.format = format
        self.instream.contents.sample_rate = rate
        self.instream.contents.read_callback = soundio_read_callback(read_callback)
        self.instream.contents.overflow_callback = soundio_overflow_callback(overflow_callback)

        self._call(_libsoundio.soundio_instream_open, self.instream)
        return self.instream

    def create_ring_buffer(self, stream):
        """ Create ring buffer """
        ring_buffer_duration_seconds = 30
        capacity = ring_buffer_duration_seconds * stream.contents.sample_rate * 8
        print(stream.contents.format)
        print(stream.contents.sample_rate)
        print(stream.contents.bytes_per_frame)
        print(stream.contents.bytes_per_sample)
        self.ring_buffer = _libsoundio.soundio_ring_buffer_create(self._soundio, int(capacity))
        if not self.ring_buffer:
            raise PySoundIoError('Failed to create ring buffer')
        # _libsoundio.soundio_ring_buffer_read_ptr(self.ring_buffer)
        return self.ring_buffer

    def start_input_stream(self, instream):
        """ Start an input stream running """
        self._call(_libsoundio.soundio_instream_start, instream)

    def read_callback(instream, frame_count_min, frame_count_max):
        """ Internal read callback """
        _libsoundio.soundio_ring_buffer_write_ptr(self.ring_buffer)

        areas = _ctypes.POINTER(SoundIoChannelArea)
        free_bytes = _libsoundio.soundio_ring_buffer_free_count(self.ring_buffer)
        free_count = free_bytes / instream.contents.bytes_per_frame
        if free_count < frame_count_min:
            raise PySoundIoError('Ring buffer overflow')

        write_frames = min(free_count, frame_count_max)
        frames_left = write_frames

        while True:
            frame_count = frames_left
            self._call(_libsoundio.soundio_instream_begin_read,
                       instream,
                       _ctypes.byref(areas),
                       _ctypes.byref(frame_count))
            if not frame_count:
                break
            if not areas:
                _ctypes.memset(write_ptr, 0, frame_count * instream.contents.bytes_per_frame)
            else:
                for frame in range(0, frame_count):
                    for ch in range(ch, instream.contents.layout.channel_count):
                        _ctypes.memmove(write_ptr, areas[ch].ptr, instream.contents.bytes_per_sample)
                        areas[ch].ptr += areas[ch].step
                        write_ptr += instream.contents.bytes_per_sample

            self._call(_libsoundio.soundio_instream_end_read(instream))
            frames_left -= frame_count
            if frames_left <= 0:
                break

        advance_bytes = write_frames * instream.contents.bytes_per_frame
        _libsoundio.soundio_ring_buffer_advance_write_ptr(self.ring_buffer, advance_bytes)

    def overflow_callback(self, instream):
        """ Overflow callback """
        pass

    def start_stream(self, rate, format):
        self.get_default_input_device()
        print('Input Device: %s' % self.input_device.contents.name.decode())
        self.sort_channel_layouts(self.input_device)
        if not self.supports_sample_rate(self.input_device, rate):
            raise PySoundIoError('Invalid sample rate: %d' % rate)
        if not self.supports_format(self.input_device, format):
            raise PySoundIoError('Cannot find a valid format')
        self.create_input_stream(
            device=self.input_device,
            format=format,
            rate=rate,
            read_callback=self.read_callback,
            overflow_callback=self.overflow_callback
        )
        print('%s %dHz %s interleaved' %
            (self.instream.contents.layout.name.decode(), rate,
            _libsoundio.soundio_format_string(format).decode()))
        self.create_ring_buffer(self.instream)
        self.start_input_stream(self.instream)
        self._flush()


