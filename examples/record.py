"""
record.py

Stream the default input device and save to wav file.
Supports specifying backend, device, sample rate, format.

Requires pysoundfile
    pip install pysoundfile
"""
import argparse
import time

import soundfile as sf
from pysoundio import (
    PySoundIo,
    SoundIoFormatFloat32LE,
    SoundIoBackendDummy
)


class Record(object):

    def __init__(self, outfile, backend=None,
                 input_device=None,
                 sample_rate=None, format=None, channels=None):
        self.wav_file = sf.SoundFile(
            outfile, mode='w', channels=channels,
            samplerate=sample_rate)
        self.pysoundio = PySoundIo(
            backend=None,
            device_id=input_device,
            channels=channels,
            sample_rate=sample_rate,
            format=SoundIoFormatFloat32LE,
            read_callback=self.callback
        )
        self.pysoundio.get_default_input_device()
        self.pysoundio.start_input_stream()

    def close(self):
        self.pysoundio.close()
        self.wav_file.close()

    def callback(self, data, length):
        self.wav_file.buffer_write(data, dtype='float32')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PySoundIo audio record example',
        epilog='Stream the input device and save to wav file'
    )
    parser.add_argument('outfile', help='WAV output file name')
    parser.add_argument('-b', help='Backend to use (optional)')
    parser.add_argument('-f', default=SoundIoFormatFloat32LE, help='Sample format (optional)')
    parser.add_argument('-s', default=44100, help='Sample rate (optional)')
    parser.add_argument('-c', type=int, default=1, help='Mono or stereo (optional)')
    parser.add_argument('-i', help='Input device id (optional)')
    args = parser.parse_args()

    record = Record(args.outfile, args.b, args.i, args.s, args.f, args.c)

    try:
        while True:
            record.pysoundio.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    record.close()
