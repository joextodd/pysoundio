"""
pysoundio.py

Play and Record Sound in Python using libsoundio

libsoundio is a C library for cross-platform audio input and output.
It is suitable for real-time and consumer software.
-> https://libsound.io

TODO:
    - More device statistics
    - Move streams to own class
    - Fix memory leaks
    - Publish
    - Docs
    - TravisCI
    - play, record functions
"""
import logging
import threading

import ctypes as _ctypes
from .constants import (
    DEFAULT_RING_BUFFER_DURATION,
    PRIORITISED_FORMATS,
    PRIORITISED_SAMPLE_RATES,
)
from .structures import (
    SoundIoErrorCallback,
    SoundIoOverflowCallback,
    SoundIoReadCallback,
    SoundIoUnderflowCallback,
    SoundIoWriteCallback,
    SoundIoDevice,
    SoundIoInStream,
    SoundIoOutStream,
    SoundIoChannelLayout,
)
import _soundiox as soundio

LOGGER = logging.getLogger(__name__)


class PySoundIoError(Exception):
    pass


class _InputProcessingThread(threading.Thread):

    def __init__(self, parent, *args, **kwargs):
        self.buffer = parent.input_buffer
        self.callback = parent.read_callback
        self.bytes_per_frame = parent.input_bytes_per_frame
        super(_InputProcessingThread, self).__init__(*args, **kwargs)

    def run(self):
        """ Callback with data """
        fill_bytes = soundio.ring_buffer_fill_count(self.buffer)
        read_buf = soundio.ring_buffer_read_ptr(self.buffer)
        if self.callback:
            self.callback(data=read_buf, length=fill_bytes / self.bytes_per_frame)
        soundio.ring_buffer_advance_read_ptr(self.buffer, fill_bytes)


class _OutputProcessingThread(threading.Thread):

    def __init__(self, parent, block_size, *args, **kwargs):
        self.buffer = parent.output_buffer
        self.callback = parent.write_callback
        self.bytes_per_frame = parent.output_bytes_per_frame
        self.block_size = block_size
        super(_OutputProcessingThread, self).__init__(*args, **kwargs)

    def run(self):
        """ Callback to fill data """
        data = bytearray(b'' * self.block_size * self.bytes_per_frame)
        free_bytes = soundio.ring_buffer_free_count(self.buffer)
        if self.callback and free_bytes >= len(data):
            self.callback(data=data, length=self.block_size)
        soundio.ring_buffer_write_ptr(self.buffer, data, len(data))
        soundio.ring_buffer_advance_write_ptr(self.buffer, len(data))


class PySoundIo(object):

    def __init__(self, backend=None):
        self.backend = backend

        self.input_device = None
        self.output_device = None
        self.input_stream = None
        self.output_stream = None
        self.input_buffer = None
        self.output_buffer = None
        self.read_callback = None
        self.write_callback = None

        self._soundio = soundio.create()
        if backend:
            self._call(soundio.connect_backend, self._soundio, backend)
        else:
            self._call(soundio.connect, self._soundio)
        self.flush()

    @property
    def version(self):
        """
        Return version string for libsoundio
        """
        return soundio.version_string()

    def close(self):
        """
        Clean up allocated memory
        Close libsoundio connections
        """
        if self.input_stream:
            soundio.instream_destroy(self.input_stream)
        if self.output_stream:
            soundio.outstream_destroy(self.output_stream)
        if self.input_buffer:
            soundio.ring_buffer_destroy(self.input_buffer)
        if self.output_buffer:
            soundio.ring_buffer_destroy(self.output_buffer)
        if self.input_device:
            soundio.device_unref(self.input_device)
        if self.output_device:
            soundio.device_unref(self.output_device)
        if self._soundio:
            soundio.destroy(self._soundio)

    def flush(self):
        """
        Atomically update information for all connected devices.
        """
        soundio.flush(self._soundio)

    @property
    def backend_count(self):
        return soundio.backend_count(self._soundio)

    def _call(self, fn, *args, **kwargs):
        """
        Call libsoundio function and check error codes.

        Raises:
            PySoundIoError with libsoundio error message
        """
        rc = fn(*args, **kwargs)
        if rc != 0:
            err = soundio.strerror(rc)
            raise PySoundIoError(err)

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
        device_id = soundio.default_input_device_index(self._soundio)
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
        self.input_device = soundio.get_input_device(self._soundio, device_id)
        if not self.input_device:
            raise PySoundIoError('Input device %d not available' % device_id)
        pydevice = _ctypes.cast(self.input_device, _ctypes.POINTER(SoundIoDevice))
        if pydevice.contents.probe_error:
            raise PySoundIoError('Unable to probe input device: %s' % (
                soundio.strerror(pydevice.contents.probe_error)))
        return self.input_device

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
        device_id = soundio.default_output_device_index(self._soundio)
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
        self.output_device = soundio.get_output_device(self._soundio, device_id)
        if not self.output_device:
            raise PySoundIoError('Output device %d not available' % device_id)
        pydevice = _ctypes.cast(self.output_device, _ctypes.POINTER(SoundIoDevice))
        if pydevice.contents.probe_error:
            raise PySoundIoError('Unable to probe output device: %s' % (
                soundio.strerror(pydevice.contents.probe_error)))
        return self.output_device

    def list_devices(self):
        """
        Return a list of available devices
        """
        output_count = soundio.get_output_device_count(self._soundio)
        input_count = soundio.get_input_device_count(self._soundio)

        default_output = soundio.default_output_device_index(self._soundio)
        default_input = soundio.default_input_device_index(self._soundio)

        input_devices = []
        output_devices = []

        for i in range(0, input_count):
            device = soundio.get_input_device(self._soundio, i)
            pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
            input_devices.append({
                'id': pydevice.contents.id.decode(), 'name': pydevice.contents.name.decode(),
                'is_raw': pydevice.contents.is_raw, 'is_default': default_input == i
                # TODO: Add more parameters
            })
            soundio.device_unref(device)

        for i in range(0, output_count):
            device = soundio.get_output_device(self._soundio, i)
            pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
            output_devices.append({
                'id': pydevice.contents.id.decode(), 'name': pydevice.contents.name.decode(),
                'is_raw': pydevice.contents.is_raw, 'is_default': default_output == i
                # TODO: Add more parameters
            })
            soundio.device_unref(device)

        LOGGER.info('%d devices found' % (input_count + output_count))
        return (input_devices, output_devices)

    def print_devices(self):
        """ Print device information """
        input_devices, output_devices = self.list_devices()
        for device in input_devices:
            print('%s' % device.contents.id)
            print('%s is_raw=%s' % (device.contents.name, device.contents.is_raw))
        for device in output_devices:
            print('%s' % device.contents.id)
            print('%s is_raw=%s' % (device.contents.name, device.contents.is_raw))

    def supports_sample_rate(self, device, rate):
        """
        Check the sample rate is supported by the selected device.

        Args:
            device (SoundIoDevice): The device object
            rate (int): The sample rate

        Returns:
            bool: True if sample rate is supported for this device
        """
        return soundio.device_supports_sample_rate(device, rate) > 0

    def get_default_sample_rate(self, device):
        for sample_rate in PRIORITISED_SAMPLE_RATES:
            if self.supports_sample_rate(device, sample_rate):
                self.sample_rate = sample_rate
                break
        if not self.sample_rate:
            pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
            self.sample_rate = device.contents.sample_rates.contents.max

    def supports_format(self, device, format):
        """
        Check the format is supported by the selected device.

        Args:
            device (SoundIoDevice): The device object
            format (int): The format from enum -

        Returns:
            bool: True if the format is supported for this device
        """
        return soundio.device_supports_format(device, format) > 0

    def get_default_format(self, device):
        for dtype in PRIORITISED_FORMATS:
            if self.supports_format(device, dtype):
                self.format = dtype
                break
        if self.format == soundio.SoundIoFormatInvalid:
            pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
            self.format = pydevice.formats.contents

    def sort_channel_layouts(self, device):
        """
        Sorts channel layouts by channel count, descending

        Args:
            device (SoundIoDevice): The device object
        """
        soundio.device_sort_channel_layouts(device)

    def _get_default_layout(self, channels):
        """
        Get default builtin channel layout for the given number of channels

        Args:
            channels (int): The desired number of channels, mono or stereo

        Returns: SoundIoChannelLayout
        """
        return soundio.channel_layout_get_default(channels)

    def get_bytes_per_frame(self, device, channels):
        return soundio.get_bytes_per_frame(device, channels)

    def get_bytes_per_sample(self, device):
        return soundio.get_bytes_per_sample(device)

    def get_bytes_per_frame(self, device, channels, sample_rate):
        return soundio.get_bytes_per_second(device, channels, sample_rate)

    def _create_input_ring_buffer(self, capacity):
        """
        Creates ring buffer with the capacity to hold 10 seconds of data,
        by default.

        Args:
            stream (SoundIoInstream/SoundIoOutStream): The stream object
            duration (int): The duration of the ring buffer in secs

        Raises:
            PySoundIoError if memory could not be allocated
        """
        self.input_buffer = soundio.input_ring_buffer_create(self._soundio, capacity)
        if not self.input_buffer:
            raise PySoundIoError('Failed to create ring buffer')
        return self.input_buffer

    def _create_output_ring_buffer(self, capacity):
        """
        Creates ring buffer with the capacity to hold 10 seconds of data,
        by default.

        Args:
            stream (SoundIoInstream/SoundIoOutStream): The stream object
            duration (int): The duration of the ring buffer in secs

        Raises:
            PySoundIoError if memory could not be allocated
        """
        self.output_buffer = soundio.output_ring_buffer_create(self._soundio, capacity)
        if not self.output_buffer:
            raise PySoundIoError('Failed to create ring buffer')
        return self.output_buffer

    def _create_input_stream(self):
        """
        Allocates memory and sets defaults for input stream

        Returns: SoundIoInStream instream object

        Raises:
            PySoundIoError if memory could not be allocated
        """
        self.input_stream = soundio.instream_create(self.input_device)
        if not self.input_stream:
            raise PySoundIoError('Could not create input stream')

        pyinstream = _ctypes.cast(self.input_stream, _ctypes.POINTER(SoundIoInStream))
        soundio.set_read_callback(self._read_callback)

        layout = self._get_default_layout(self.channels)
        pylayout = _ctypes.cast(layout, _ctypes.POINTER(SoundIoChannelLayout))
        pyinstream.contents.layout = pylayout.contents

        pyinstream.contents.format = self.format
        pyinstream.contents.sample_rate = self.sample_rate
        if self.block_size:
            pyinstream.contents.software_latency = float(self.block_size) / self.sample_rate

        return self.input_stream

    def _open_input_stream(self):
        """
        Open an input stream..

        Raises:
            PySoundIoError if there is an error starting stream.
        """
        self._call(soundio.instream_open, self.input_stream)
        pystream = _ctypes.cast(self.input_stream, _ctypes.POINTER(SoundIoInStream))

    def _start_input_stream(self):
        """
        Start an input stream running.

        Raises:
            PySoundIoError if there is an error starting stream.
        """
        self._call(soundio.instream_start, self.input_stream)

    def get_input_latency(self, out_latency):
        return soundio.instream_get_latency(self.input_stream, out_latency)

    def _read_callback(self):
        """
        Internal read callback.
        """
        _InputProcessingThread(parent=self).start()

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

    def start_input_stream(self, device_id=None,
                           sample_rate=None, dtype=None,
                           block_size=None, channels=None,
                           read_callback=None):
        """
        Creates input stream, and sets parameters. Then allocates
        a ring buffer and starts the stream.
        """
        self.sample_rate = sample_rate
        self.format = dtype
        self.block_size = block_size
        self.channels = channels
        self.read_callback = read_callback

        if device_id:
            self.input_device = self.get_input_device(device_id)
        else:
            self.input_device = self.get_default_input_device()

        pydevice = _ctypes.cast(self.input_device, _ctypes.POINTER(SoundIoDevice))
        LOGGER.info('Input Device: %s' % pydevice.contents.name.decode())
        self.sort_channel_layouts(self.input_device)

        if self.sample_rate:
            if not self.supports_sample_rate(self.input_device, self.sample_rate):
                raise PySoundIoError('Invalid sample rate: %d' % self.sample_rate)
        else:
            self.get_default_sample_rate(self.input_device)

        if self.format:
            if not self.supports_format(self.input_device, self.format):
                raise PySoundIoError('Invalid format: %s interleaved' %
                                    (soundio.format_string(self.format)))
        else:
            self.get_default_format(self.input_device)

        self._create_input_stream()
        self._open_input_stream()
        pystream = _ctypes.cast(self.input_stream, _ctypes.POINTER(SoundIoInStream))
        self.input_bytes_per_frame = pystream.contents.bytes_per_frame
        capacity = (DEFAULT_RING_BUFFER_DURATION *
                    pystream.contents.sample_rate * pystream.contents.bytes_per_frame)
        self._create_input_ring_buffer(capacity)
        self._start_input_stream()
        self.flush()

    def _create_output_stream(self):
        """
        Allocates memory and sets defaults for output stream

        Returns: SoundIoInStream instream object

        Raises:
            PySoundIoError if memory could not be allocated
        """
        self.output_stream = soundio.outstream_create(self.output_device)
        if not self.output_stream:
            raise PySoundIoError('Could not create output stream')

        pystream = _ctypes.cast(self.output_stream, _ctypes.POINTER(SoundIoOutStream))
        soundio.set_write_callback(self._write_callback)

        layout = self._get_default_layout(self.channels)
        pylayout = _ctypes.cast(layout, _ctypes.POINTER(SoundIoChannelLayout))
        pystream.contents.layout = pylayout.contents

        pystream.contents.format = self.format
        pystream.contents.sample_rate = self.sample_rate
        if self.block_size:
            pystream.contents.software_latency = float(self.block_size) / self.sample_rate

        return self.output_stream

    def _open_output_stream(self):
        """
        Open an output stream.
        Calculate actual block size here.

        Raises:
            PySoundIoError if there is an error starting stream.
        """
        self._call(soundio.outstream_open, self.output_stream)
        pystream = _ctypes.cast(self.output_stream, _ctypes.POINTER(SoundIoOutStream))
        self.block_size = int(pystream.contents.software_latency / self.sample_rate)

    def _start_output_stream(self):
        """
        Start an output stream running.

        Raises:
            PySoundIoError if there is an error starting stream.
        """
        self._call(soundio.outstream_start, self.output_stream)

    def _write_callback(self, size):
        """
        Internal write callback.
        """
        _OutputProcessingThread(parent=self, block_size=size).start()

    def _underflow_callback(self, stream):
        """
        Internal underflow callback, which calls the external
        underflow callback if defined.
        """
        if self.underflow_callback:
            self.underflow_callback(stream)

    def _clear_output_buffer(self):
        if self.output_buffer:
            soundio.ring_buffer_clear(self.output_buffer)

    def get_output_latency(self, out_latency):
        return soundio.instream_get_latency(self.output_stream, out_latency)

    def start_output_stream(self, device_id=None,
                            sample_rate=None, dtype=None,
                            block_size=None, channels=None,
                            write_callback=None):
        """
        Creates output stream, and sets parameters. Then allocates
        a ring buffer and starts the stream.
        """
        self.sample_rate = sample_rate
        self.format = dtype
        self.block_size = block_size
        self.channels = channels
        self.write_callback = write_callback

        if device_id:
            self.output_device = self.get_output_device(device_id)
        else:
            self.output_device = self.get_default_output_device()

        pydevice = _ctypes.cast(self.output_device, _ctypes.POINTER(SoundIoDevice))
        LOGGER.info('Input Device: %s' % pydevice.contents.name.decode())
        self.sort_channel_layouts(self.output_device)

        if self.sample_rate:
            if not self.supports_sample_rate(self.output_device, self.sample_rate):
                raise PySoundIoError('Invalid sample rate: %d' % self.sample_rate)
        else:
            self.get_default_sample_rate(self.output_device)

        if self.format:
            if not self.supports_format(self.output_device, self.format):
                raise PySoundIoError('Invalid format: %s interleaved' %
                                    (soundio.format_string(self.format)))
        else:
            self.get_default_format(self.output_device)

        self._create_output_stream()
        self._open_output_stream()
        pystream = _ctypes.cast(self.output_stream, _ctypes.POINTER(SoundIoOutStream))
        self.output_bytes_per_frame = pystream.contents.bytes_per_frame
        capacity = (DEFAULT_RING_BUFFER_DURATION *
                    pystream.contents.sample_rate * pystream.contents.bytes_per_frame)
        # if self.block_size is None:
            # self.block_size = pystream.contents.software_latency * self.sample_rate
        # print(self.block_size)
        self._create_output_ring_buffer(capacity)
        self._clear_output_buffer()
        self._start_output_stream()
        self.flush()


class _BaseStream(object):

    def __init__(self, soundio, channels=None,
                 sample_rate=None, format=None, block_size=None,
                 callback=None):
        self._soundio = soundio
        self.channels = channels
        self.sample_rate = sample_rate
        self.format = format
        self.block_size = block_size
        self.callback = callback
        self.buffer = None

    def close(self):
        if self.buffer:
            soundio.ring_buffer_destroy(self.buffer)

    def _create_ring_buffer(self, capacity):
        """
        Creates ring buffer with the capacity to hold 10 seconds of data,
        by default.

        Args:
            stream (SoundIoInstream/SoundIoOutStream): The stream object
            duration (int): The duration of the ring buffer in secs

        Raises:
            PySoundIoError if memory could not be allocated
        """
        self.buffer = soundio.ring_buffer_create(self._soundio._soundio, capacity)
        if not self.buffer:
            raise PySoundIoError('Failed to create ring buffer')
        return self.buffer


class InputStream(_BaseStream):
    """
    Input Stream
    """
    def __init__(self, soundio, device_id=None,
                 channels=None, sample_rate=None, format=None, block_size=None,
                 callback=None, overflow_callback=None, error_callback=None):
        self._soundio = soundio
        self.channels = channels
        self.sample_rate = sample_rate
        self.format = format
        self.block_size = block_size
        self.callback = callback
        self.overflow_callback = overflow_callback
        self.error_callback = error_callback
        self.stream = None
        self.buffer = None

        if device_id:
            self.device_id = device_id
            self.device = self.get_input_device(self.device_id)
        else:
            self.device = self._soundio.get_default_input_device()

        pydevice = _ctypes.cast(self.device, _ctypes.POINTER(SoundIoDevice))
        LOGGER.info('Input Device: %s' % pydevice.contents.name.decode())

        self._soundio.sort_channel_layouts(self.device)

        if not self._soundio.supports_sample_rate(self.device, self.sample_rate):
            raise PySoundIoError('Invalid sample rate: %d' % self.sample_rate)

        if not self._soundio.supports_format(self.device, self.format):
            raise PySoundIoError('Invalid format: %s interleaved' %
            (soundio.format_string(self.format)))

    def close(self):
        """
        Close input stream and pysoundio connection.
        """
        if self.buffer:
            soundio.ring_buffer_destroy(self.buffer)
        if self.stream:
            soundio.instream_destroy(self.stream)
        if self.device:
            soundio.device_unref(self.device)


class OutputStream(_BaseStream):
    """
    Output Stream
    """
    def __init__(self, soundio, device_id=None,
                 channels=None, sample_rate=None, format=None, block_size=None,
                 callback=None, underflow_callback=None, error_callback=None):
        self._soundio = soundio
        self.channels = channels
        self.sample_rate = sample_rate
        self.format = format
        self.block_size = block_size
        self.callback = callback
        self.underflow_callback = underflow_callback
        self.error_callback = error_callback

        self.stream = None
        self.buffer = None

        if device_id:
            self.device_id = device_id
            self.device = self._soundio.get_output_device(self.device_id)
        else:
            self.device = self._soundio.get_default_output_device()

        pydevice = _ctypes.cast(self.device, _ctypes.POINTER(SoundIoDevice))
        LOGGER.info('Output Device: %s' % pydevice.contents.name.decode())

        self._soundio.sort_channel_layouts(self.device)
        if not self._soundio.supports_sample_rate(self.device, self.sample_rate):
            raise PySoundIoError('Invalid sample rate: %d' % self.sample_rate)

        if not self._soundio.supports_format(self.device, self.format):
            raise PySoundIoError('Invalid format: %s interleaved' %
            (soundio.format_string(self.format)))

    def close(self):
        """
        Close output stream and pysoundio connection.
        """
        if self.buffer:
            soundio.ring_buffer_destroy(self.buffer)
        if self.stream:
            soundio.outstream_destroy(self.stream)
        if self.device:
            soundio.device_unref(self.device)
