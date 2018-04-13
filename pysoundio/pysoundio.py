"""
pysoundio.py

Play and Record Sound in Python using libsoundio

libsoundio is a C library for cross-platform audio input and output.
It is suitable for real-time and consumer software.

"""
import logging
import threading

import ctypes as _ctypes
from .constants import (
    DEFAULT_RING_BUFFER_DURATION,
    PRIORITISED_FORMATS,
    PRIORITISED_SAMPLE_RATES,
    SoundIoFormat
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
    SoundIoSampleRateRange
)
import _soundiox as soundio

LOGGER = logging.getLogger(__name__)


class PySoundIoError(Exception):
    pass


class _InputProcessingThread(threading.Thread):

    def __init__(self, parent, *args, **kwargs):
        self.buffer = parent.input['buffer']
        self.callback = parent.input['read_callback']
        self.bytes_per_frame = parent.input['bytes_per_frame']
        super(_InputProcessingThread, self).__init__(*args, **kwargs)

    def run(self):
        """ Callback with data """
        fill_bytes = soundio.ring_buffer_fill_count(self.buffer)
        read_buf = soundio.ring_buffer_read_ptr(self.buffer)
        if self.callback and fill_bytes:
            self.callback(data=read_buf, length=fill_bytes / self.bytes_per_frame)
        soundio.ring_buffer_advance_read_ptr(self.buffer, fill_bytes)


class _OutputProcessingThread(threading.Thread):

    def __init__(self, parent, block_size, *args, **kwargs):
        self.buffer = parent.output['buffer']
        self.callback = parent.output['write_callback']
        self.bytes_per_frame = parent.output['bytes_per_frame']
        self.block_size = block_size
        super(_OutputProcessingThread, self).__init__(*args, **kwargs)

    def run(self):
        """ Callback to fill data """
        data = bytearray(b'\x00' * self.block_size * self.bytes_per_frame)
        free_bytes = soundio.ring_buffer_free_count(self.buffer)
        if self.callback and free_bytes >= len(data):
            self.callback(data=data, length=self.block_size)
        soundio.ring_buffer_write_ptr(self.buffer, data, len(data))
        soundio.ring_buffer_advance_write_ptr(self.buffer, len(data))


class PySoundIo(object):

    def __init__(self, backend=None):
        """
        Initialise PySoundIo.
        Connect to a specific backend, or the default.

        Parameters
        ----------
        backend: (SoundIoBackend) see `Backends`_. (optional)
        """
        self.backend = backend
        self.testing = False

        self.input = {'device': None, 'stream': None, 'buffer': None, 'read_callback': None}
        self.output = {'device': None, 'stream': None, 'buffer': None, 'write_callback': None}

        self._soundio = soundio.create()
        if backend:
            soundio.connect_backend(backend)
        else:
            soundio.connect()
        self.flush()

    def close(self):
        """
        Clean up allocated memory
        Close libsoundio connections
        """
        if self.input['stream']:
            soundio.instream_destroy()
            self.input['stream'] = None
        if self.output['stream']:
            soundio.outstream_destroy()
            self.output['stream'] = None
        if self.input['buffer']:
            soundio.ring_buffer_destroy(self.input['buffer'])
            self.input['buffer'] = None
        if self.output['buffer']:
            soundio.ring_buffer_destroy(self.output['buffer'])
            self.output['buffer'] = None
        if self.input['device']:
            soundio.device_unref(self.input['device'])
            self.input['device'] = None
        if self.output['device']:
            soundio.device_unref(self.output['device'])
            self.output['device'] = None
        if self._soundio:
            soundio.disconnect()
            soundio.destroy()
            self._soundio = None

    def flush(self):
        """
        Atomically update information for all connected devices.
        """
        soundio.flush()

    @property
    def backend_count(self):
        """
        Returns the number of available backends.
        """
        return soundio.backend_count()

    def get_default_input_device(self):
        """
        Returns default input device

        Returns
        -------
        PySoundIoDevice input device

        Raises
        ------
        PySoundIoError if the input device is not available
        """
        device_id = soundio.default_input_device_index()
        return self.get_input_device(device_id)

    def get_input_device(self, device_id):
        """
        Return an input device by index

        Parameters
        ----------
        device_id: (int) input device index

        Returns
        -------
        PySoundIoDevice input device

        Raises
        ------
        PySoundIoError if an invalid device id is used, or device is unavailable
        """
        if device_id < 0 or device_id > soundio.get_input_device_count():
            raise PySoundIoError('Invalid input device id')
        self.input['device'] = soundio.get_input_device(device_id)
        return self.input['device']

    def get_default_output_device(self):
        """
        Returns default output device

        Returns
        -------
        PySoundIoDevice output device

        Raises
        ------
        PySoundIoError if the output device is not available
        """
        device_id = soundio.default_output_device_index()
        return self.get_output_device(device_id)

    def get_output_device(self, device_id):
        """
        Return an output device by index

        Parameters
        ----------
        device_id: (int) output device index

        Returns
        -------
        PySoundIoDevice output device

        Raises
        ------
        PySoundIoError if an invalid device id is used, or device is unavailable
        """
        if device_id < 0 or device_id > soundio.get_output_device_count():
            raise PySoundIoError('Invalid output device id')
        self.output['device'] = soundio.get_output_device(device_id)
        return self.output['device']

    def list_devices(self):
        """
        Return a list of available devices

        Returns
        -------
        (list)(dict) containing information on available input / output devices.
        """
        output_count = soundio.get_output_device_count()
        input_count = soundio.get_input_device_count()

        default_output = soundio.default_output_device_index()
        default_input = soundio.default_input_device_index()

        input_devices = []
        output_devices = []

        for i in range(0, input_count):
            device = soundio.get_input_device(i)
            pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
            input_devices.append({
                'id': pydevice.contents.id.decode(), 'name': pydevice.contents.name.decode(),
                'is_raw': pydevice.contents.is_raw, 'is_default': default_input == i,
                'sample_rates': self.get_sample_rates(device),
                'formats': self.get_formats(device),
                'layouts': self.get_layouts(device),
                'software_latency_min': pydevice.contents.software_latency_min,
                'software_latency_max': pydevice.contents.software_latency_max,
                'software_latency_current': pydevice.contents.software_latency_current
            })
            soundio.device_unref(device)

        for i in range(0, output_count):
            device = soundio.get_output_device(i)
            pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
            output_devices.append({
                'id': pydevice.contents.id.decode(), 'name': pydevice.contents.name.decode(),
                'is_raw': pydevice.contents.is_raw, 'is_default': default_output == i,
                'sample_rates': self.get_sample_rates(device),
                'formats': self.get_formats(device),
                'layouts': self.get_layouts(device),
                'software_latency_min': pydevice.contents.software_latency_min,
                'software_latency_max': pydevice.contents.software_latency_max,
                'software_latency_current': pydevice.contents.software_latency_current
            })
            soundio.device_unref(device)

        LOGGER.info('%d devices found' % (input_count + output_count))
        return (input_devices, output_devices)

    def get_layouts(self, device):
        """
        Return a list of available layouts for a device

        Parameters
        ----------
        device: (SoundIoDevice) device object

        Returns
        -------
        (dict) Dictionary of available channel layouts for a device
        """
        pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
        current = pydevice.contents.current_layout
        layouts = {
            'current': {'name': current.name.decode() if current.name else 'None'},
            'available': []
        }
        for l in range(0, pydevice.contents.layout_count):
            layouts['available'].append({
                'name': (pydevice.contents.layouts[l].name.decode() if
                    pydevice.contents.layouts[l].name else 'None'),
                'channel_count': pydevice.contents.layouts[l].channel_count
            })
        return layouts

    def get_sample_rates(self, device):
        """
        Return a list of available sample rates for a device

        Parameters
        ----------
        device: (SoundIoDevice) device object

        Returns
        -------
        (dict) Dictionary of available sample rates for a device
        """
        pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
        sample_rates = {'current': pydevice.contents.sample_rate_current, 'available': []}
        for s in range(0, pydevice.contents.sample_rate_count):
            sample_rates['available'].append({
                'min': pydevice.contents.sample_rates[s].min,
                'max': pydevice.contents.sample_rates[s].max
            })
        return sample_rates

    def get_formats(self, device):
        """
        Return a list of available formats for a device

        Parameters
        ----------
        device: (SoundIoDevice) device object

        Returns
        -------
        (dict) Dictionary of available formats for a device
        """
        pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
        formats = {'current': pydevice.contents.current_format, 'available': []}
        for r in range(0, pydevice.contents.format_count):
            formats['available'].append(SoundIoFormat[pydevice.contents.formats[r]])
        return formats

    def supports_sample_rate(self, device, rate):
        """
        Check the sample rate is supported by the selected device.

        Parameters
        ----------
        device: (SoundIoDevice) device object
        rate (int): sample rate

        Returns
        -------
        (bool) True if sample rate is supported for this device
        """
        return soundio.device_supports_sample_rate(device, rate) > 0

    def get_default_sample_rate(self, device):
        """
        Get the best sample rate.

        Parameters
        ----------
        device: (SoundIoDevice) device object

        Returns
        -------
        (int) The best available sample rate
        """
        sample_rate = None
        for rate in PRIORITISED_SAMPLE_RATES:
            if self.supports_sample_rate(device, rate):
                sample_rate = rate
                break
        if not sample_rate:
            pydevice = _ctypes.cast(device, _ctypes.POINTER(SoundIoDevice))
            sample_rate = pydevice.contents.sample_rates.contents.max
        return sample_rate

    def supports_format(self, device, format):
        """
        Check the format is supported by the selected device.

        Parameters
        ----------
        device: (SoundIoDevice) device object
        format: (SoundIoFormat) see `Formats`_.

        Returns
        -------
        (bool) True if the format is supported for this device
        """
        return soundio.device_supports_format(device, format) > 0

    def get_default_format(self, device):
        """
        Get the best format value.

        Parameters
        ----------
        device: (SoundIoDevice) device object

        Returns
        ------
        (SoundIoFormat) The best available format
        """
        dtype = soundio.SoundIoFormatInvalid
        for fmt in PRIORITISED_FORMATS:
            if self.supports_format(device, fmt):
                dtype = fmt
                break
        if dtype == soundio.SoundIoFormatInvalid:
            raise PySoundIoError('Incompatible sample formats')
        return dtype

    def sort_channel_layouts(self, device):
        """
        Sorts channel layouts by channel count, descending

        Parameters
        ----------
        device: (SoundIoDevice) device object
        """
        soundio.device_sort_channel_layouts(device)

    def _get_default_layout(self, channels):
        """
        Get default builtin channel layout for the given number of channels

        Parameters
        ----------
        channels: (int) desired number of channels
        """
        return soundio.channel_layout_get_default(channels)

    def get_bytes_per_frame(self, device, channels):
        """
        Get the number of bytes per frame

        Parameters
        ----------
        device: (PySoundIoDevice) device
        channels: (int) number of channels

        Returns
        -------
        (int) number of bytes per frame
        """
        return soundio.get_bytes_per_frame(device, channels)

    def get_bytes_per_sample(self, device):
        """
        Get the number of bytes per sample

        Parameters
        ----------
        device: (PySoundIoDevice) device

        Returns
        -------
        (int) number of bytes per sample
        """
        return soundio.get_bytes_per_sample(device)

    def get_bytes_per_second(self, device, channels, sample_rate):
        """
        Get the number of bytes per second

        Parameters
        ----------
        device: (PySoundIoDevice) device
        channels (int) number of channels
        sample_rate (int) sample rate

        Returns
        -------
        (int) number of bytes per second
        """
        return soundio.get_bytes_per_second(device, channels, sample_rate)

    def _create_input_ring_buffer(self, capacity):
        """
        Creates ring buffer with the capacity to hold 30 seconds of data,
        by default.
        """
        self.input['buffer'] = soundio.input_ring_buffer_create(capacity)
        return self.input['buffer']

    def _create_output_ring_buffer(self, capacity):
        """
        Creates ring buffer with the capacity to hold 30 seconds of data,
        by default.
        """
        self.output['buffer'] = soundio.output_ring_buffer_create(capacity)
        return self.output['buffer']

    def _create_input_stream(self):
        """
        Allocates memory and sets defaults for input stream
        """
        self.input['stream'] = soundio.instream_create(self.input['device'])

        pyinstream = _ctypes.cast(self.input['stream'], _ctypes.POINTER(SoundIoInStream))
        soundio.set_read_callbacks(self._read_callback, self._overflow_callback)

        layout = self._get_default_layout(self.input['channels'])
        pylayout = _ctypes.cast(layout, _ctypes.POINTER(SoundIoChannelLayout))
        pyinstream.contents.layout = pylayout.contents

        pyinstream.contents.format = self.input['format']
        pyinstream.contents.sample_rate = self.input['sample_rate']
        if self.input['block_size']:
            pyinstream.contents.software_latency = float(self.input['block_size']) / self.input['sample_rate']

        return self.input['stream']

    def _open_input_stream(self):
        """
        Open an input stream.
        """
        soundio.instream_open()

    def _start_input_stream(self):
        """
        Start an input stream running.
        """
        soundio.instream_start()

    def pause_input_stream(self, pause):
        """
        Pause input stream

        Parameters
        ----------
        pause: (bool) True to pause, False to unpause
        """
        soundio.instream_pause(pause)

    def get_input_latency(self, out_latency):
        """
        Obtain the number of seconds that the next frame of sound
        being captured will take to arrive in the buffer,
        plus the amount of time that is represented in the buffer.

        Parameters
        ----------
        out_latency: (int) output latency in seconds
        """
        return soundio.instream_get_latency(out_latency)

    def _read_callback(self):
        """
        Internal read callback.
        """
        _InputProcessingThread(parent=self).start()

    def _overflow_callback(self):
        """
        Internal overflow callback, which calls the external
        overflow callback if defined.
        """
        if self.input['overflow_callback']:
            self.input['overflow_callback']()

    def start_input_stream(self, device_id=None,
                           sample_rate=None, dtype=None,
                           block_size=None, channels=None,
                           read_callback=None, overflow_callback=None):
        """
        Creates input stream, and sets parameters. Then allocates
        a ring buffer and starts the stream.

        The read callback is called in an audio processing thread,
        when a block of data is read from the microphone. Data is
        passed from the ring buffer to the callback to process.

        Parameters
        ----------
        device_id: (int) input device id
        sample_rate: (int) desired sample rate (optional)
        dtype: (SoundIoFormat) desired format, see `Formats`_. (optional)
        block_size: (int) desired block size (optional)
        channels: (int) number of channels [1: mono, 2: stereo] (optional)
        read_callback: (fn) function to call with data, the function must have
                        the arguments data and length. See record example
        overflow_callback: (fn) function to call if data is not being read fast enough

        Raises
        ------
        PySoundIoError if any invalid parameters are used

        Notes
        -----
        An example read callback

        .. code-block:: python
            :linenos:

            def read_callback(data, length):
                wav.write(data)

        Overflow callback example

        .. code-block:: python
            :linenos:

            def overflow_callback():
                print('buffer overflow')
        """
        self.input['sample_rate'] = sample_rate
        self.input['format'] = dtype
        self.input['block_size'] = block_size
        self.input['channels'] = channels
        self.input['read_callback'] = read_callback
        self.input['overflow_callback'] = overflow_callback

        if device_id is not None:
            self.input['device'] = self.get_input_device(device_id)
        else:
            self.input['device'] = self.get_default_input_device()

        pydevice = _ctypes.cast(self.input['device'], _ctypes.POINTER(SoundIoDevice))
        LOGGER.info('Input Device: %s' % pydevice.contents.name.decode())
        self.sort_channel_layouts(self.input['device'])

        if self.input['sample_rate']:
            if not self.supports_sample_rate(self.input['device'], self.input['sample_rate']):
                raise PySoundIoError('Invalid sample rate: %d' % self.input['sample_rate'])
        else:
            self.input['sample_rate'] = self.get_default_sample_rate(self.input['device'])

        if self.input['format']:
            if not self.supports_format(self.input['device'], self.input['format']):
                raise PySoundIoError('Invalid format: %s interleaved' %
                                     (soundio.format_string(self.input['format'])))
        else:
            self.input['format'] = self.get_default_format(self.input['device'])

        self._create_input_stream()
        self._open_input_stream()
        pystream = _ctypes.cast(self.input['stream'], _ctypes.POINTER(SoundIoInStream))
        self.input['bytes_per_frame'] = pystream.contents.bytes_per_frame
        capacity = (DEFAULT_RING_BUFFER_DURATION *
                    pystream.contents.sample_rate * pystream.contents.bytes_per_frame)
        self._create_input_ring_buffer(capacity)
        self._start_input_stream()
        self.flush()

    def _create_output_stream(self):
        """
        Allocates memory and sets defaults for output stream
        """
        self.output['stream'] = soundio.outstream_create(self.output['device'])

        pystream = _ctypes.cast(self.output['stream'], _ctypes.POINTER(SoundIoOutStream))
        if not self.testing:
            soundio.set_write_callbacks(self._write_callback, self._underflow_callback)

        layout = self._get_default_layout(self.output['channels'])
        pylayout = _ctypes.cast(layout, _ctypes.POINTER(SoundIoChannelLayout))
        pystream.contents.layout = pylayout.contents

        pystream.contents.format = self.output['format']
        pystream.contents.sample_rate = self.output['sample_rate']
        if self.output['block_size']:
            pystream.contents.software_latency = float(self.output['block_size']) / self.output['sample_rate']

        return self.output['stream']

    def _open_output_stream(self):
        """
        Open an output stream.
        """
        soundio.outstream_open()
        pystream = _ctypes.cast(self.output['stream'], _ctypes.POINTER(SoundIoOutStream))
        self.output['block_size'] = int(pystream.contents.software_latency / self.output['sample_rate'])

    def _start_output_stream(self):
        """
        Start an output stream running.
        """
        soundio.outstream_start()

    def pause_output_stream(self, pause):
        """
        Pause output stream

        Parameters
        ----------
        pause: (bool) True to pause, False to unpause
        """
        soundio.outstream_pause(pause)

    def _write_callback(self, size):
        """
        Internal write callback.
        """
        _OutputProcessingThread(parent=self, block_size=size).start()

    def _underflow_callback(self):
        """
        Internal underflow callback, which calls the external
        underflow callback if defined.
        """
        if self.output['underflow_callback']:
            self.output['underflow_callback']()

    def _clear_output_buffer(self):
        """
        Clear the output buffer
        """
        if self.output['buffer']:
            soundio.ring_buffer_clear(self.output['buffer'])

    def get_output_latency(self, out_latency):
        """
        Obtain the total number of seconds that the next frame written
        will take to become audible.

        Parameters
        ----------
        out_latency: (int) output latency in seconds
        """
        return soundio.outstream_get_latency(out_latency)

    def start_output_stream(self, device_id=None,
                            sample_rate=None, dtype=None,
                            block_size=None, channels=None,
                            write_callback=None, underflow_callback=None):
        """
        Creates output stream, and sets parameters. Then allocates
        a ring buffer and starts the stream.

        The write callback is called in an audio processing thread,
        when a block of data should be passed to the speakers. Data is
        added to the ring buffer to process.

        Parameters
        ----------
        device_id: (int) output device id
        sample_rate: (int) desired sample rate (optional)
        dtype: (SoundIoFormat) desired format, see `Formats`_. (optional)
        block_size: (int) desired block size (optional)
        channels: (int) number of channels [1: mono, 2: stereo] (optional)
        write_callback: (fn) function to call with data, the function must have
                        the arguments data and length.
        underflow_callback: (fn) function to call if data is not being written fast enough

        Raises
        ------
        PySoundIoError if any invalid parameters are used

        Notes
        -----
        An example write callback

        .. code-block:: python
            :linenos:

            def write_callback(data, length):
                outdata = ar.array('f', [0] * length)
                for value in outdata:
                    outdata = 1.0
                data[:] = outdata.tostring()

        Underflow callback example

        .. code-block:: python
            :linenos:

            def underflow_callback():
                print('buffer underflow')
        """
        self.output['sample_rate'] = sample_rate
        self.output['format'] = dtype
        self.output['block_size'] = block_size
        self.output['channels'] = channels
        self.output['write_callback'] = write_callback
        self.output['underflow_callback'] = underflow_callback

        if device_id is not None:
            self.output['device'] = self.get_output_device(device_id)
        else:
            self.output['device'] = self.get_default_output_device()

        pydevice = _ctypes.cast(self.output['device'], _ctypes.POINTER(SoundIoDevice))
        LOGGER.info('Input Device: %s' % pydevice.contents.name.decode())
        self.sort_channel_layouts(self.output['device'])

        if self.output['sample_rate']:
            if not self.supports_sample_rate(self.output['device'], self.output['sample_rate']):
                raise PySoundIoError('Invalid sample rate: %d' % self.output['sample_rate'])
        else:
            self.output['sample_rate'] = self.get_default_sample_rate(self.output['device'])

        if self.output['format']:
            if not self.supports_format(self.output['device'], self.output['format']):
                raise PySoundIoError('Invalid format: %s interleaved' %
                                     (soundio.format_string(self.output['format'])))
        else:
            self.output['format'] = self.get_default_format(self.output['device'])

        self._create_output_stream()
        self._open_output_stream()
        pystream = _ctypes.cast(self.output['stream'], _ctypes.POINTER(SoundIoOutStream))
        self.output['bytes_per_frame'] = pystream.contents.bytes_per_frame
        capacity = (DEFAULT_RING_BUFFER_DURATION *
                    pystream.contents.sample_rate * pystream.contents.bytes_per_frame)
        self._create_output_ring_buffer(capacity)
        self._clear_output_buffer()
        self._start_output_stream()
        self.flush()
