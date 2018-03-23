"""
pysoundio.py

Play and Record Sound in Python using libsoundio

libsoundio is a C library for cross-platform audio input and output.
It is suitable for real-time and consumer software.
-> https://libsound.io

TODO:
    - Listening demo
    - Check through all function, structure definitions
    - Bring back ring buffer without affecting CPU
    - Store ring buffer in userdata
    - Add enums to constants
    - Autoset formats and sample rates if not specified
    - Tests
    - TravisCI
    - Docs
"""
import math
import time
import struct
import logging
import threading
import multiprocessing

import array as ar
import ctypes as _ctypes
import platform as _platform

from . import _lib
from .constants import DEFAULT_RING_BUFFER_DURATION
from ._structures import (
    SoundIoErrorCallback,
    SoundIoOverflowCallback,
    SoundIoReadCallback,
    SoundIoUnderflowCallback,
    SoundIoWriteCallback,
    SoundIo,
    SoundIoChannelArea,
    SoundIoChannelLayout,
    SoundIoDevice,
    SoundIoInStream,
    SoundIoOutStream,
    SoundIoRingBuffer,
)

LOGGER = logging.getLogger(__name__)


class PySoundIoError(Exception):
    pass


class PySoundIo(object):

    def __init__(self, backend=None):
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
        """
        Return version string
        """
        return _lib.soundio_version_string().decode()

    def close(self):
        """
        Close libsoundio connection
        """
        if self._soundio:
            _lib.soundio_destroy(self._soundio)

    def _flush(self):
        """
        Atomically update information for all connected devices.
        """
        _lib.soundio_flush_events(self._soundio)

    def _call(self, fn, *args, **kwargs):
        """
        Call libsoundio function and check error codes.

        Raises:
            PySoundIoError with libsoundio error message
        """
        rc = fn(*args, **kwargs)
        if rc != 0:
            err = _lib.soundio_strerror(rc)
            raise PySoundIoError(err.decode())

    def list_devices(self):
        """
        Return a list of available devices
        """
        output_count = _lib.soundio_output_device_count(self._soundio)
        input_count = _lib.soundio_input_device_count(self._soundio)

        default_output = _lib.soundio_default_output_device_index(self._soundio)
        default_input = _lib.soundio_default_input_device_index(self._soundio)

        input_devices = []
        output_devices = []

        for i in range(0, input_count):
            device = _lib.soundio_get_input_device(self._soundio, i)
            input_devices.append({
                'id': device.contents.id, 'name': device.contents.name,
                'is_raw': device.contents.is_raw, 'is_default': default_input == i
                # TODO: Add more parameters
            })
            self.print_device(device, default_input == i)
            _lib.soundio_device_unref(device)

        for i in range(0, output_count):
            device = _lib.soundio_get_output_device(self._soundio, i)
            output_devices.append({
                'id': device.contents.id, 'name': device.contents.name,
                'is_raw': device.contents.is_raw, 'is_default': default_input == i
                # TODO: Add more parameters
            })
            self.print_device(device, default_output == i)
            _lib.soundio_device_unref(device)

        LOGGER.info('%d devices found' % (input_count + output_count))
        return (input_devices, output_devices)

    def print_device(self, device, is_default=False):
        """ Print device information """
        LOGGER.info('%s' % device.contents.id)
        LOGGER.info('%s is_raw=%s' % (device.contents.name, device.contents.is_raw))


class _BaseStream(PySoundIo):

    def __init__(self, backend=None, device_id=None,
                 channels=None, sample_rate=None, format=None, block_size=None,
                 callback=None, error_callback=None):

        self.backend = backend
        self.channels = channels
        self.sample_rate = sample_rate
        self.format = format
        self.block_size = block_size
        self.callback = callback
        self.error_callback = error_callback

        self.stream = None
        self.buffer = None

        super(_BaseStream, self).__init__(backend)

    def close(self):
        """
        Clean up and close libsoundio connection
        """
        if self.device:
            _lib.soundio_device_unref(self.device)
        super(_BaseStream, self).close()

    def supports_sample_rate(self, device, rate):
        """
        Check the sample rate is supported by the selected device.

        Args:
            device (SoundIoDevice): The device object
            rate (int): The sample rate

        Returns:
            bool: True if sample rate is supported for this device
        """
        return _lib.soundio_device_supports_sample_rate(device, rate)

    def supports_format(self, device, format):
        """
        Check the format is supported by the selected device.

        Args:
            device (SoundIoDevice): The device object
            format (int): The format from enum -

        Returns:
            bool: True if the format is supported for this device
        """
        return _lib.soundio_device_supports_format(device, format)

    def sort_channel_layouts(self, device):
        """
        Sorts channel layouts by channel count, descending

        Args:
            device (SoundIoDevice): The device object
        """
        _lib.soundio_device_sort_channel_layouts(device)

    def _get_default_layout(self, channels):
        """
        Get default builtin channel layout for the given number of channels

        Args:
            channels (int): The desired number of channels, mono or stereo

        Returns: SoundIoChannelLayout
        """
        return _lib.soundio_channel_layout_get_default(channels)

    def _create_ring_buffer(self, stream, duration=DEFAULT_RING_BUFFER_DURATION):
        """
        Creates ring buffer with the capacity to hold 10 seconds of data,
        by default.

        Args:
            stream (SoundIoInstream/SoundIoOutStream): The stream object
            duration (int): The duration of the ring buffer in secs

        Raises:
            PySoundIoError if memory could not be allocated
        """
        capacity = duration * stream.contents.sample_rate * stream.contents.bytes_per_frame
        ring_buffer = _lib.soundio_ring_buffer_create(self._soundio, int(capacity))
        if not ring_buffer:
            raise PySoundIoError('Failed to create ring buffer')
        return ring_buffer


class _InputProcessingThread(threading.Thread):

    def __init__(self, parent, instream,
                 frame_count_min, frame_count_max,
                 *args, **kwargs):
        self._call = parent._call
        self.callback = parent.callback
        self.instream = instream
        self.frame_count_min = frame_count_min
        self.frame_count_max = frame_count_max
        super(_InputProcessingThread, self).__init__(*args, **kwargs)
        self.start()

    def run(self):
        """
        Retrieve data from input stream structure and pass to callback
        """
        instream = _ctypes.cast(self.instream, _ctypes.POINTER(SoundIoInStream))
        areas = _ctypes.POINTER(SoundIoChannelArea)()

        data = bytearray()
        frame_count = self.frame_count_max
        frames_left = self.frame_count_max
        bytes_per_sample = instream.contents.bytes_per_sample

        while frames_left:
            self._call(_lib.soundio_instream_begin_read,
                           instream,
                           _ctypes.byref(areas),
                           _ctypes.byref(_ctypes.c_int(frame_count)))

            for frame in range(0, frame_count * bytes_per_sample, bytes_per_sample):
                for ch in range(0, instream.contents.layout.channel_count):
                    data.extend(areas[ch].ptr[frame:frame + bytes_per_sample])

            self._call(_lib.soundio_instream_end_read, instream)
            frames_left -= frame_count

        if self.callback:
            self.callback(bytes(data), frame_count)


class InputStream(_BaseStream):
    """
    Input Stream
    """
    def __init__(self, backend=None, device_id=None,
                 channels=None, sample_rate=None, format=None, block_size=None,
                 callback=None, overflow_callback=None, error_callback=None):
        self.overflow_callback = overflow_callback
        super(InputStream, self).__init__(
            backend, device_id, channels, sample_rate, format, block_size,
            callback, error_callback
        )
        if device_id:
            self.device_id = device_id
            self.device = self.get_input_device(self.device_id)
        else:
            self.device = self.get_default_input_device()

        LOGGER.info('Input Device: %s' % self.device.contents.name.decode())

        self.sort_channel_layouts(self.device)
        if not self.supports_sample_rate(self.device, self.sample_rate):
            raise PySoundIoError('Invalid sample rate: %d' % self.sample_rate)

        if not self.supports_format(self.device, self.format):
            raise PySoundIoError('Invalid format: %s interleaved' %
            (_lib.soundio_format_string(self.format).decode()))

    def close(self):
        """
        Close input stream and pysoundio connection.
        """
        if self.stream:
            _lib.soundio_instream_destroy(self.stream)
        super(InputStream, self).close()

    def get_default_input_device(self):
        """
        Returns default input device

        Args:
            device_id (int): Device index

        Returns:
            PySoundIoDevice input device

        Raises:
            PySoundIoError if the input device is not available
        """
        device_id = _lib.soundio_default_input_device_index(self._soundio)
        return self.get_input_device(device_id)

    def get_input_device(self, device_id):
        """
        Return an input device by index

        Args:
            device_id (int): Device index

        Returns:
            PySoundIoDevice input device

        Raises:
            PySoundIoError if the input device is not available
        """
        device = _lib.soundio_get_input_device(self._soundio, device_id)
        if not device:
            raise PySoundIoError('Input device %d not available' % device_id)
        if device.contents.probe_error:
            raise PySoundIoError('Unable to probe input device: %s' % (
                _lib.soundio_strerror(device.contents.probe_error)))
        return device

    def _create_input_stream(self):
        """
        Allocates memory and sets defaults for input stream

        Returns: SoundIoInStream instream object

        Raises:
            PySoundIoError if memory could not be allocated
        """
        instream = _lib.soundio_instream_create(self.device)
        if not instream:
            raise PySoundIoError('Could not create input stream')

        layout = self._get_default_layout(self.channels)
        instream.contents.layout = layout.contents

        instream.contents.format = self.format
        instream.contents.sample_rate = self.sample_rate
        if self.block_size:
            instream.contents.software_latency = float(self.block_size) / self.sample_rate

        instream.contents.read_callback = SoundIoReadCallback(self._read_callback)
        instream.contents.overflow_callback = SoundIoOverflowCallback(self._overflow_callback)
        instream.contents.error_callback = SoundIoErrorCallback(self._error_callback)

        self._call(_lib.soundio_instream_open, instream)
        return instream

    def _start_input_stream(self, instream):
        """
        Start an input stream running.

        Raises:
            PySoundIoError if there is an error starting stream.
        """
        self._call(_lib.soundio_instream_start, instream)

    def _read_callback(self, instream, frame_count_min, frame_count_max):
        """
        Internal read callback.
        """
        self.thread = _InputProcessingThread(
            parent=self,
            instream=instream,
            frame_count_min=frame_count_min,
            frame_count_max=frame_count_max
        )

        # write_ptr = _lib.soundio_ring_buffer_write_ptr(self.ring_buffer)
        # free_bytes = _lib.soundio_ring_buffer_free_count(self.ring_buffer)
        # free_count = int(free_bytes / instream.contents.bytes_per_frame)
        # if free_count < frame_count_min:
        #     raise PySoundIoError('Ring buffer overflow')

        # write_frames = min(free_count, frame_count_max)
        # frames_left = write_frames

        # t1 = time.time()

        # while True:
        #     frame_count = frames_left
        #     if not frame_count:
        #         break
        #     self._call(_lib.soundio_instream_begin_read,
        #                instream,
        #                _ctypes.byref(areas),
        #                _ctypes.byref(_ctypes.c_int(frame_count)))
        #     if not areas:
        #         _ctypes.memset(write_ptr, 0, frame_count * instream.contents.bytes_per_frame)
        #     else:
        #         for frame in range(0, frame_count):
        #             for ch in range(0, instream.contents.layout.channel_count):
        #                 _ctypes.memmove(write_ptr, areas[ch].ptr, instream.contents.bytes_per_sample)

        #                 a_ptr = _ctypes.cast(_ctypes.pointer(areas[ch].ptr), _ctypes.POINTER(_ctypes.c_void_p))
        #                 a_ptr.contents.value += areas[ch].step

        #                 w_ptr = _ctypes.cast(_ctypes.pointer(write_ptr), _ctypes.POINTER(_ctypes.c_void_p))
        #                 w_ptr.contents.value += instream.contents.bytes_per_sample

        #     self._call(_lib.soundio_instream_end_read, instream)
        #     frames_left -= frame_count
        #     if frames_left <= 0:
        #         break

        # print(int((time.time() - t1) * 1000000))
        # advance_bytes = write_frames * instream.contents.bytes_per_frame
        # _lib.soundio_ring_buffer_advance_write_ptr(self.ring_buffer, advance_bytes)

    def _overflow_callback(self, stream):
        """
        Internal overflow callback, which calls the external
        overflow callback if defined.
        """
        if self.overflow_callback:
            self.overflow_callback(stream)

    def _error_callback(self, stream, err):
        """
        Internal error callback, which calls the external
        error callback if defined.
        """
        if self.error_callback:
            self.error_callback(stream, err)

    def start_stream(self):
        """
        Start input stream.
        Set up instream object and the ring buffer.
        """
        self.stream = self._create_input_stream()

        LOGGER.info('%s %dHz %s interleaved' %
            (self.stream.contents.layout.name.decode(), self.sample_rate,
            _lib.soundio_format_string(self.format).decode()))

        self.ring_buffer = self._create_ring_buffer(self.stream)
        self._start_input_stream(self.stream)
        self._flush()

    # Temporary

    def write_data_to_file(self, fptr):
        """ Read data from ring buffer and write to file """
        fill_bytes = _lib.soundio_ring_buffer_fill_count(self.ring_buffer)
        read_buf = _lib.soundio_ring_buffer_read_ptr(self.ring_buffer)

        for i in range(0, fill_bytes):
            fptr.write(read_buf.contents)
            buf_ptr = _ctypes.cast(_ctypes.pointer(read_buf), _ctypes.POINTER(_ctypes.c_void_p))
            buf_ptr.contents.value += 1

        _lib.soundio_ring_buffer_advance_read_ptr(self.ring_buffer, fill_bytes)


class OutputStream(_BaseStream):
    """
    Output Stream

    """
    def __init__(self, backend=None, device_id=None,
                 channels=None, sample_rate=None, format=None, block_size=None,
                 callback=None, underflow_callback=None, error_callback=None):
        super(OutputStream, self).__init__(
            backend, device_id, channels, sample_rate, format, block_size,
            callback, error_callback
        )
        if device_id:
            self.device_id = device_id
            self.device = self.get_output_device(self.device_id)
        else:
            self.device = self.get_default_output_device()
        LOGGER.info('Output Device: %s' % self.device.contents.name.decode())

        self.underflow_callback = underflow_callback

        self.sort_channel_layouts(self.device)
        if not self.supports_sample_rate(self.device, self.sample_rate):
            raise PySoundIoError('Invalid sample rate: %d' % self.sample_rate)

        if not self.supports_format(self.device, self.format):
            raise PySoundIoError('Invalid format: %s interleaved' %
            (_lib.soundio_format_string(self.format).decode()))

        self.seconds_offset = 0

    def close(self):
        """
        Close output stream and pysoundio connection.
        """
        if self.stream:
            _lib.soundio_outstream_destroy(self.stream)
        super(OutputStream, self).close()

    def get_default_output_device(self):
        """
        Returns default output device

        Args:
            device_id (int): Device index

        Returns:
            PySoundIoDevice output device

        Raises:
            PySoundIoError if the output device is not available
        """
        device_id = _lib.soundio_default_output_device_index(self._soundio)
        return self.get_output_device(device_id)

    def get_output_device(self, device_id):
        """
        Return an output device by index

        Args:
            device_id (int): Device index

        Returns:
            PySoundIoDevice output device

        Raises:
            PySoundIoError if the output device is not available
        """
        device = _lib.soundio_get_output_device(self._soundio, device_id)
        if not device:
            raise PySoundIoError('Output device %d not available' % device_id)
        if device.contents.probe_error:
            raise PySoundIoError('Unable to probe output device: %s' % (
                _lib.soundio_strerror(device.contents.probe_error)))
        return device

    def _create_output_stream(self):
        """
        Allocates memory and sets defaults for output stream

        Returns: SoundIoOutStream outstream object

        Raises:
            PySoundIoError if memory could not be allocated
        """
        outstream = _lib.soundio_outstream_create(self.device)
        if not outstream:
            raise PySoundIoError('Could not create output stream')

        outstream.contents.format = self.format
        outstream.contents.sample_rate = self.sample_rate
        if self.block_size:
            outstream.contents.software_latency = float(self.block_size) / self.sample_rate

        outstream.contents.write_callback = SoundIoWriteCallback(self._write_callback)
        # outstream.contents.underflow_callback = SoundIoUnderflowCallback(self._underflow_callback)
        # outstream.contents.error_callback = SoundIoErrorCallback(self._error_callback)

        self._call(_lib.soundio_outstream_open, outstream)
        return outstream

    def _start_output_stream(self, outstream):
        """
        Start an output stream running.

        Raises:
            PySoundIoError if there is an error starting stream.
        """
        self._call(_lib.soundio_outstream_start, outstream)

    def _write_callback(self, outstream, frame_count_min, frame_count_max):
        """
        Internal write callback
        """
        outstream = _ctypes.cast(outstream, _ctypes.POINTER(SoundIoOutStream))
        areas = _ctypes.POINTER(SoundIoChannelArea)()

        data = bytearray()
        frame_count = frame_count_max
        frames_left = frame_count_max

        pitch = 440
        radians_per_second = pitch * 2.0 * math.pi;
        seconds_per_frame = 1.0 / self.sample_rate
        bytes_per_sample = outstream.contents.bytes_per_sample

        while frames_left:
            self._call(_lib.soundio_outstream_begin_write,
                       outstream,
                       _ctypes.byref(areas),
                       _ctypes.byref(_ctypes.c_int(frame_count)))

            for frame in range(0, frame_count * bytes_per_sample, bytes_per_sample):
                for ch in range(0, outstream.contents.layout.channel_count):
                    # TODO: make this work for all data types
                    data = struct.pack('f', math.sin(
                        (self.seconds_offset + frame * seconds_per_frame) * radians_per_second))
                    for byte in range(0, bytes_per_sample):
                        areas[ch].ptr[frame + byte] = data[byte]

            self.seconds_offset += seconds_per_frame * frame_count
            self._call(_lib.soundio_outstream_end_write, outstream)
            frames_left -= frame_count

    def _underflow_callback(self, stream):
        """
        Internal underflow callback, which calls the external
        underflow callback if defined.
        """
        if self.underflow_callback:
            self.underflow_callback(stream)

    def _error_callback(self, stream, err):
        """
        Internal error callback, which calls the external
        error callback if defined.
        """
        if self.error_callback:
            self.error_callback(stream, err)

    def start_stream(self):
        """
        Start output stream.
        Set up outstream object and the ring buffer.
        """
        self.stream = self._create_output_stream()

        LOGGER.info('%s %dHz %s interleaved' %
            (self.stream.contents.layout.name.decode(), self.sample_rate,
            _lib.soundio_format_string(self.format).decode()))

        self.ring_buffer = self._create_ring_buffer(self.stream)
        self._start_output_stream(self.stream)
        self._flush()


def list_devices():
    pass