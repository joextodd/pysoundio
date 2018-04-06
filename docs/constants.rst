Backends
--------

===================================  ===============================================================
Value                                Backend Description
===================================  ===============================================================
pysoundio.SoundIoBackendJack         JACK Audio
pysoundio.SoundIoBackendPulseAudio   Pulse Audio
pysoundio.SoundIoBackendAlsa         ALSA Audio
pysoundio.SoundIoBackendCoreAudio    Core Audio
pysoundio.SoundIoBackendWasapi       WASAPI Audio
pysoundio.SoundIoBackendDummy        Dummy backend
===================================  ===============================================================


Formats
-------

=================================  ====================================================================
Value                              Format Description
=================================  ====================================================================
pysoundio.SoundIoFormatS8          Signed 8 bit
pysoundio.SoundIoFormatU8          Unsigned 8 bit
pysoundio.SoundIoFormatS16LE       Signed 16 bit Little Endian
pysoundio.SoundIoFormatS16BE       Signed 16 bit Big Endian
pysoundio.SoundIoFormatU16LE       Unsigned 16 bit Little Endian
pysoundio.SoundIoFormatU16BE       Unsigned 16 bit Little Endian
pysoundio.SoundIoFormatS24LE       Signed 24 bit Little Endian using low three bytes in 32-bit word
pysoundio.SoundIoFormatS24BE       Signed 24 bit Big Endian using low three bytes in 32-bit word
pysoundio.SoundIoFormatU24LE       Unsigned 24 bit Little Endian using low three bytes in 32-bit word
pysoundio.SoundIoFormatU24BE       Unsigned 24 bit Big Endian using low three bytes in 32-bit word
pysoundio.SoundIoFormatS32LE       Signed 32 bit Little Endian
pysoundio.SoundIoFormatS32BE       Signed 32 bit Big Endian
pysoundio.SoundIoFormatU32LE       Unsigned 32 bit Little Endian
pysoundio.SoundIoFormatU32BE       Unsigned 32 bit Big Endian
pysoundio.SoundIoFormatFloat32LE   Float 32 bit Little Endian, Range -1.0 to 1.0
pysoundio.SoundIoFormatFloat32BE   Float 32 bit Big Endian, Range -1.0 to 1.0
pysoundio.SoundIoFormatFloat64LE   Float 64 bit Little Endian, Range -1.0 to 1.0
pysoundio.SoundIoFormatFloat64BE   Float 64 bit Big Endian, Range -1.0 to 1.0
=================================  ====================================================================
