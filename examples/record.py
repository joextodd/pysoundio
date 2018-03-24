"""
record.py

Stream the default input device and save to wav file.
Supports specifying backend, device, sample rate, format, blocksize.

Requires pysoundfile
    pip install pysoundfile
"""
import argparse
import time

import soundfile as sf
from pysoundio import (
    PySoundIo,
    SoundIoFormatFloat32LE
)


class Record(object):

    def __init__(self, outfile, backend=None,
                 input_device=None, output_device=None,
                 sample_rate=None, format=None, channels=None):
        self.pysoundio = PySoundIo(backend=backend)
        self.instream = self.pysoundio.start_input_stream(
            device_id=input_device,
            channels=channels,
            sample_rate=sample_rate,
            format=SoundIoFormatFloat32LE,
            callback=self.callback
        )
        self.wav_file = sf.SoundFile(
            outfile, mode='w', channels=channels,
            samplerate=sample_rate)

    def close(self):
        self.wav_file.close()
        self.instream.close()
        self.pysoundio.close()

    def callback(self, data, length):
        pass
        # self.wav_file.buffer_write(data, dtype='f')


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
    parser.add_argument('-o', help='Output device id (optional)')
    args = parser.parse_args()

    record = Record(args.outfile, args.b, args.i, args.o, args.s, args.f, args.c)

    while True:
        try:
            record.pysoundio.flush()
            time.sleep(1)
        except KeyboardInterrupt:
            pass

    record.close()