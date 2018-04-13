"""
constants.py

Constants and enumerations.
"""

from _soundiox import (
    SoundIoBackendNone, SoundIoBackendJack, SoundIoBackendPulseAudio,
    SoundIoBackendAlsa, SoundIoBackendCoreAudio, SoundIoBackendWasapi,
    SoundIoBackendDummy,
    SoundIoFormatS8, SoundIoFormatU8, SoundIoFormatS16LE,
    SoundIoFormatS16BE, SoundIoFormatU16LE, SoundIoFormatU16BE,
    SoundIoFormatS24LE, SoundIoFormatS24BE, SoundIoFormatU24LE,
    SoundIoFormatU24BE, SoundIoFormatS32LE, SoundIoFormatS32BE,
    SoundIoFormatU32LE, SoundIoFormatU32BE,
    SoundIoFormatFloat32LE, SoundIoFormatFloat32BE, SoundIoFormatFloat64LE,
    SoundIoFormatFloat64BE, SoundIoFormatInvalid
)

DEFAULT_RING_BUFFER_DURATION = 30  # secs

SoundIoBackend = {
    SoundIoBackendNone: 'SoundIoBackendNone',
    SoundIoBackendJack: 'SoundIoBackendJack',
    SoundIoBackendPulseAudio: 'SoundIoBackendPulseAudio',
    SoundIoBackendAlsa: 'SoundIoBackendAlsa',
    SoundIoBackendCoreAudio: 'SoundIoBackendCoreAudio',
    SoundIoBackendWasapi: 'SoundIoBackendWasapi',
    SoundIoBackendDummy: 'SoundIoBackendDummy',
}

SoundIoFormat = {
    SoundIoFormatS8: 'SoundIoFormatS8',
    SoundIoFormatU8: 'SoundIoFormatU8',
    SoundIoFormatS16LE: 'SoundIoFormatS16LE',
    SoundIoFormatS16BE: 'SoundIoFormatS16BE',
    SoundIoFormatU16LE: 'SoundIoFormatU16LE',
    SoundIoFormatU16BE: 'SoundIoFormatU16BE',
    SoundIoFormatS24LE: 'SoundIoFormatS24LE',
    SoundIoFormatS24BE: 'SoundIoFormatS24BE',
    SoundIoFormatU24LE: 'SoundIoFormatU24LE',
    SoundIoFormatU24BE: 'SoundIoFormatU24BE',
    SoundIoFormatS32LE: 'SoundIoFormatS32LE',
    SoundIoFormatS32BE: 'SoundIoFormatS32BE',
    SoundIoFormatU32LE: 'SoundIoFormatU32LE',
    SoundIoFormatU32BE: 'SoundIoFormatU32BE',
    SoundIoFormatFloat32LE: 'SoundIoFormatFloat32LE',
    SoundIoFormatFloat32BE: 'SoundIoFormatFloat32BE',
    SoundIoFormatFloat64LE: 'SoundIoFormatFloat64LE',
    SoundIoFormatFloat64BE: 'SoundIoFormatFloat64BE',
    SoundIoFormatInvalid: 'SoundIoFormatInvalid'
}

PRIORITISED_FORMATS = [
    SoundIoFormatFloat32LE,
    SoundIoFormatFloat32BE,
    SoundIoFormatS32LE,
    SoundIoFormatS32BE,
    SoundIoFormatS24LE,
    SoundIoFormatS24BE,
    SoundIoFormatS16LE,
    SoundIoFormatS16BE,
    SoundIoFormatFloat64LE,
    SoundIoFormatFloat64BE,
    SoundIoFormatU32LE,
    SoundIoFormatU32BE,
    SoundIoFormatU24LE,
    SoundIoFormatU24BE,
    SoundIoFormatU16LE,
    SoundIoFormatU16BE,
    SoundIoFormatS8,
    SoundIoFormatU8,
    SoundIoFormatInvalid,
]

PRIORITISED_SAMPLE_RATES = [
    48000,
    44100,
    96000,
    24000,
    0,
]

ARRAY_FORMATS = {
    SoundIoFormatS8: 'b',
    SoundIoFormatU8: 'B',
    SoundIoFormatS16LE: 'h',
    SoundIoFormatS16BE: 'h',
    SoundIoFormatU16LE: 'H',
    SoundIoFormatU16BE: 'H',
    SoundIoFormatS24LE: None,
    SoundIoFormatS24BE: None,
    SoundIoFormatU24LE: None,
    SoundIoFormatU24BE: None,
    SoundIoFormatS32LE: 'l',
    SoundIoFormatS32BE: 'l',
    SoundIoFormatU32LE: 'L',
    SoundIoFormatU32BE: 'L',
    SoundIoFormatFloat32LE: 'f',
    SoundIoFormatFloat32BE: 'f',
    SoundIoFormatFloat64LE: 'd',
    SoundIoFormatFloat64BE: 'd'
}

SOUNDFILE_FORMATS = {
    SoundIoFormatS8: None,
    SoundIoFormatU8: None,
    SoundIoFormatS16LE: 'int16',
    SoundIoFormatS16BE: 'int16',
    SoundIoFormatU16LE: None,
    SoundIoFormatU16BE: None,
    SoundIoFormatS24LE: None,
    SoundIoFormatS24BE: None,
    SoundIoFormatU24LE: None,
    SoundIoFormatU24BE: None,
    SoundIoFormatS32LE: 'int32',
    SoundIoFormatS32BE: 'int32',
    SoundIoFormatU32LE: None,
    SoundIoFormatU32BE: None,
    SoundIoFormatFloat32LE: 'float32',
    SoundIoFormatFloat32BE: 'float32',
    SoundIoFormatFloat64LE: 'float64',
    SoundIoFormatFloat64BE: 'float64'
}