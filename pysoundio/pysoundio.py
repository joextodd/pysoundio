"""
Play and Record Sound in Python using libsoundio

libsoundio is a C library for cross-platform audio input and output.
It is suitable for real-time and consumer software.
-> https://libsound.io
"""
import ctypes as _ctypes
import platform as _platform

from . import _lib
from .exceptions import PySoundIoError
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


class PySoundIo(object):

    def __init__(self, backend=None):
        self.instream = None
        self.outstream = None
        self.input_device = None
        self.output_device = None
        self.ring_buffer = None

        self.backend = backend
        self._soundio = _lib.soundio_create()
        if self._soundio is None:
            raise PySoundIoError('Out of memory')
        if backend:
            self._call(_lib.soundio_connect_backend, self._soundio, backend)
        else:
            self._call(_lib.soundio_connect, self._soundio)

        self._flush()

    @property
    def version(self):
        """ Return version string """
        return _lib.soundio_version_string().decode()

    def close(self):
        """ Close libsoundio connection """
        if self.instream:
            _lib.soundio_instream_destroy(self.instream)
        if self.input_device:
            _lib.soundio_device_unref(self.input_device)
        if self._soundio:
            _lib.soundio_destroy(self._soundio)

    def _flush(self):
        """ Flush events """
        _lib.soundio_flush_events(self._soundio)

    def _call(self, fn, *args, **kwargs):
        """ Call libsoundio function and check error codes """
        rc = fn(*args, **kwargs)
        if rc != 0:
            err = _lib.soundio_strerror(rc)
            raise PySoundIoError(err.decode())

    def list_devices(self):
        """ Return a list of available devices """
        output_count = _lib.soundio_output_device_count(self._soundio)
        input_count = _lib.soundio_input_device_count(self._soundio)

        default_output = _lib.soundio_default_output_device_index(self._soundio)
        default_input = _lib.soundio_default_input_device_index(self._soundio)

        print('--------Input Devices--------')
        for i in range(0, input_count):
            device = _lib.soundio_get_input_device(self._soundio, i)
            self.print_device(device, default_input == i)
            _lib.soundio_device_unref(device)

        print('--------Output Devices--------')
        for i in range(0, output_count):
            device = _lib.soundio_get_output_device(self._soundio, i)
            self.print_device(device, default_output == i)
            _lib.soundio_device_unref(device)

        print('%d devices found' % (input_count + output_count))

    def print_device(self, device, is_default=False):
        """ Print device information """
        print('%s' % device.contents.id)
        print('%s is_raw=%s' % (device.contents.name, device.contents.is_raw))

    def get_default_input_device(self):
        """ Returns default input device """
        device_index = _lib.soundio_default_input_device_index(self._soundio)
        return self.get_input_device(device_index)

    def get_input_device(self, device_id):
        """ Return an input device """
        input_device = _lib.soundio_get_input_device(self._soundio, device_id)
        if not input_device:
            raise PySoundIoError('Input device %d not available' % device_id)
        if input_device.contents.probe_error:
            raise PySoundIoError('Unable to probe input device: %s' % (
                _lib.soundio_strerror(device.contents.probe_error)))
        return input_device

    def get_output_device(self, device_id):
        """ Return an outut device """
        output_device = _lib.soundio_get_output_device(self._soundio, device_id)
        if not output_device:
            raise PySoundIoError('Output device %d not available' % device_id)
        if output_device.contents.probe_error:
            raise PySoundIoError('Unable to probe output device: %s' % (
                _lib.soundio_strerror(device.contents.probe_error)))
        return output_device

    def supports_sample_rate(self, device, rate):
        """ Check the sample rate is supported by the selected device """
        return _lib.soundio_device_supports_sample_rate(device, rate)

    def supports_format(self, device, format):
        """ Check the format is supported by the selected device """
        return _lib.soundio_device_supports_format(device, format)

    def sort_channel_layouts(self, device):
        """ Sorts channel layouts by channel count, descending """
        _lib.soundio_device_sort_channel_layouts(device)

    def _create_input_stream(self, device, format, rate,
                             read_callback, overflow_callback,
                             error_callback):
        """ Allocates memory and sets defaults """
        instream = _lib.soundio_instream_create(device)
        if not instream:
            raise PySoundIoError('Could not create input stream')

        layout = _lib.soundio_channel_layout_get_default(2)  # TODO:  Get / set mono / stereo
        instream.contents.layout = layout.contents

        instream.contents.format = format
        instream.contents.sample_rate = rate
        instream.contents.read_callback = soundio_read_callback(read_callback)
        instream.contents.overflow_callback = soundio_overflow_callback(overflow_callback)
        instream.contents.error_callback = soundio_error_callback(error_callback)

        self._call(_lib.soundio_instream_open, instream)
        return instream

    def _create_ring_buffer(self, stream):
        """ Create ring buffer """
        ring_buffer_duration_seconds = 10
        capacity = ring_buffer_duration_seconds * stream.contents.sample_rate * stream.contents.bytes_per_frame
        ring_buffer = _lib.soundio_ring_buffer_create(self._soundio, int(capacity))
        if not ring_buffer:
            raise PySoundIoError('Failed to create ring buffer')
        return ring_buffer

    def _start_input_stream(self, instream):
        """ Start an input stream running """
        self._call(_lib.soundio_instream_start, instream)

    def _read_callback(self, instream, frame_count_min, frame_count_max):
        """ Internal read callback """
        instream = _ctypes.cast(instream, _ctypes.POINTER(SoundIoInStream))
        _lib.soundio_ring_buffer_write_ptr(self.ring_buffer)

        areas = _ctypes.POINTER(SoundIoChannelArea)()
        write_ptr = _lib.soundio_ring_buffer_write_ptr(self.ring_buffer)
        free_bytes = _lib.soundio_ring_buffer_free_count(self.ring_buffer)
        free_count = int(free_bytes / instream.contents.bytes_per_frame)
        if free_count < frame_count_min:
            raise PySoundIoError('Ring buffer overflow')

        write_frames = min(free_count, frame_count_max)
        frames_left = write_frames

        while True:
            frame_count = frames_left
            self._call(_lib.soundio_instream_begin_read,
                       instream,
                       _ctypes.byref(areas),
                       _ctypes.byref(_ctypes.c_int(frame_count)))
            if not frame_count:
                break
            if not areas:
                _ctypes.memset(write_ptr, 0, frame_count * instream.contents.bytes_per_frame)
            else:
                for frame in range(0, frame_count):
                    for ch in range(0, instream.contents.layout.channel_count):
                        _ctypes.memmove(write_ptr, areas[ch].ptr, instream.contents.bytes_per_sample)

                        a_ptr = _ctypes.cast(_ctypes.pointer(areas[ch].ptr), _ctypes.POINTER(_ctypes.c_void_p))
                        a_ptr.contents.value += areas[ch].step

                        w_ptr = _ctypes.cast(_ctypes.pointer(write_ptr), _ctypes.POINTER(_ctypes.c_void_p))
                        w_ptr.contents.value += instream.contents.bytes_per_sample

            self._call(_lib.soundio_instream_end_read, instream)
            frames_left -= frame_count
            if frames_left <= 0:
                break

        advance_bytes = write_frames * instream.contents.bytes_per_frame
        _lib.soundio_ring_buffer_advance_write_ptr(self.ring_buffer, advance_bytes)

    def _overflow_callback(self, instream):
        """ Overflow callback """
        pass

    def _error_callback(self, stream, err):
        """ Error callback """
        print('ERROR: %d' % err)

    def start_stream(self, rate, format):
        """ Start input stream """
        self.input_device = self.get_default_input_device()
        print('Input Device: %s' % self.input_device.contents.name.decode())

        self.sort_channel_layouts(self.input_device)
        if not self.supports_sample_rate(self.input_device, rate):
            raise PySoundIoError('Invalid sample rate: %d' % rate)

        if not self.supports_format(self.input_device, format):
            raise PySoundIoError('Cannot find a valid format')

        self.instream = self._create_input_stream(
            device=self.input_device,
            format=format,
            rate=rate,
            read_callback=self._read_callback,
            overflow_callback=self._overflow_callback,
            error_callback=self._error_callback
        )

        print('%s %dHz %s interleaved' %
            (self.instream.contents.layout.name.decode(), rate,
            _lib.soundio_format_string(format).decode()))

        self.ring_buffer = self._create_ring_buffer(self.instream)
        self._start_input_stream(self.instream)
        self._flush()


