"""
structures.py

Implements data structures and callbacks from libsoundio
"""
import ctypes as _ctypes


soundio_read_callback = _ctypes.CFUNCTYPE(
    None,
    _ctypes.c_void_p, _ctypes.c_int, _ctypes.c_int,
)
soundio_write_callback = _ctypes.CFUNCTYPE(
    None,
    _ctypes.c_void_p, _ctypes.c_int, _ctypes.c_int,
)
soundio_overflow_callback = _ctypes.CFUNCTYPE(
    None,
    _ctypes.c_void_p
)
soundio_underflow_callback = _ctypes.CFUNCTYPE(
    None,
    _ctypes.c_void_p
)
soundio_error_callback = _ctypes.CFUNCTYPE(
    None,
    _ctypes.c_void_p, _ctypes.c_int
)

class SoundIo(_ctypes.Structure):
    """
    Forward declaration of SoundIo structure
    """
    pass


_soundio_on_devices_change = _ctypes.CFUNCTYPE(
    None,
    _ctypes.POINTER(SoundIo)
)
_soundio_on_backend_disconnect = _ctypes.CFUNCTYPE(
    None,
    _ctypes.POINTER(SoundIo), _ctypes.c_int
)
_soundio_on_events_signal = _ctypes.CFUNCTYPE(
    None,
    _ctypes.POINTER(SoundIo)
)
_soundio_emit_rtprio_warning = _ctypes.CFUNCTYPE(None)
_soundio_jack_info_callback = _ctypes.CFUNCTYPE(
    None,
    _ctypes.c_char_p
)
_soundio_jack_error_callback = _ctypes.CFUNCTYPE(
    None,
    _ctypes.c_char_p
)


SoundIo._fields_ = [
    ('userdata', _ctypes.c_void_p),
    ('on_devices_change', _soundio_on_devices_change),
    ('on_backend_disconnect', _soundio_on_backend_disconnect),
    ('on_events_signal', _soundio_on_events_signal),
    ('current_backend', _ctypes.c_uint),
    ('app_name', _ctypes.c_char_p),
    ('emit_rtprio_warning', _soundio_emit_rtprio_warning),
    ('jack_info_callback', _soundio_jack_info_callback),
    ('jack_error_callback', _soundio_jack_error_callback)
]


class SoundIoChannelArea(_ctypes.Structure):
    _fields_ = [
        ('ptr', _ctypes.POINTER(_ctypes.c_char)),
        ('step', _ctypes.c_int)
    ]


class SoundIoSampleRateRange(_ctypes.Structure):
    _fields_ = [
        ('min', _ctypes.c_int),
        ('max', _ctypes.c_int),
    ]


class SoundIoChannelLayout(_ctypes.Structure):
    _fields_ = [
        ('name', _ctypes.c_char_p),
        ('channel_count', _ctypes.c_int),
        ('channels', _ctypes.c_uint * 24)  # SOUNDIO_MAX_CHANNELS
    ]


class SoundIoDevice(_ctypes.Structure):
    _fields_ = [
        ('soundio', _ctypes.POINTER(SoundIo)),
        ('id', _ctypes.c_char_p),
        ('name', _ctypes.c_char_p),
        ('aim', _ctypes.c_uint),
        ('layouts', _ctypes.POINTER(SoundIoChannelLayout)),
        ('layout_count', _ctypes.c_int),
        ('current_layout', SoundIoChannelLayout),
        ('formats', _ctypes.POINTER(_ctypes.c_uint)),
        ('format_count', _ctypes.c_int),
        ('current_format', _ctypes.c_uint),
        ('sample_rates', _ctypes.POINTER(SoundIoSampleRateRange)),
        ('sample_rate_count', _ctypes.c_int),
        ('sample_rate_current', _ctypes.c_int),
        ('software_latency_min', _ctypes.c_double),
        ('software_latency_max', _ctypes.c_double),
        ('software_latency_current', _ctypes.c_double),
        ('is_raw', _ctypes.c_bool),
        ('ref_count', _ctypes.c_int),
        ('probe_error', _ctypes.c_int)
    ]


class SoundIoInStream(_ctypes.Structure):
    _fields_ = [
        ('device', _ctypes.POINTER(SoundIoDevice)),
        ('format', _ctypes.c_uint),
        ('sample_rate', _ctypes.c_int),
        ('layout', SoundIoChannelLayout),
        ('software_latency', _ctypes.c_double),
        ('userdata', _ctypes.c_void_p),
        ('read_callback', soundio_read_callback),
        ('overflow_callback', soundio_overflow_callback),
        ('error_callback', soundio_error_callback),
        ('name', _ctypes.c_char_p),
        ('non_terminal_hint', _ctypes.c_bool),
        ('bytes_per_frame', _ctypes.c_int),
        ('bytes_per_sample', _ctypes.c_int),
        ('layout_error', _ctypes.c_int)
    ]


class SoundIoOutStream(_ctypes.Structure):
    _fields_ = [
        ('device', _ctypes.POINTER(SoundIoDevice)),
        ('format', _ctypes.c_uint),
        ('sample_rate', _ctypes.c_int),
        ('layout', SoundIoChannelLayout),
        ('software_latency', _ctypes.c_double),
        ('userdata', _ctypes.c_void_p),
        ('write_callback', soundio_read_callback),
        ('underflow_callback', soundio_overflow_callback),
        ('error_callback', soundio_error_callback),
        ('name', _ctypes.c_char_p),
        ('non_terminal_hint', _ctypes.c_bool),
        ('bytes_per_frame', _ctypes.c_int),
        ('bytes_per_sample', _ctypes.c_int),
        ('layout_error', _ctypes.c_int)
    ]


class _SoundIoOsMirroredMemory(_ctypes.Structure):
    _fields_ = [
        ('capacity', _ctypes.c_size_t),
        ('address', _ctypes.c_char_p),
        ('priv', _ctypes.c_void_p)
    ]


class _SoundIoAtomicULong(_ctypes.Structure):
    _fields_ = [
        ('x', _ctypes.c_ulong)
    ]


class SoundIoRingBuffer(_ctypes.Structure):
    _fields_ = [
        ('mem', _SoundIoOsMirroredMemory),
        ('write_offset', _SoundIoAtomicULong),
        ('read_offset', _SoundIoAtomicULong),
        ('capacity', _ctypes.c_int)
    ]
