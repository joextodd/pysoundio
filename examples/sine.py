"""
sine.py

Play a sine wave over the default output device.
Supports specifying backend, device, sample rate, block size.

"""
import array as ar
import argparse
import math
import struct
import time

import _soundiox as soundio
from pysoundio import (
    PySoundIo,
    SoundIoFormatFloat32LE,
    SoundIoOutStream,
)


class Player(object):

    def __init__(self, freq=None, backend=None, output_device=None,
                 sample_rate=None, block_size=None):
        self.pysoundio = PySoundIo(backend=None)

        self.freq = float(freq)
        self.seconds_offset = 0.0
        self.radians_per_second = self.freq * 2.0 * math.pi
        self.seconds_per_frame = 1.0 / sample_rate

        self.pysoundio.start_output_stream(
            device_id=output_device,
            channels=1,
            sample_rate=sample_rate,
            block_size=block_size,
            dtype=SoundIoFormatFloat32LE,
            write_callback=self.callback
        )

    def close(self):
        self.pysoundio.close()

    def callback(self, data, length):
        indata = ar.array('f', [0] * length)
        for i in range(0, length):
            indata[i] = math.sin(
                (self.seconds_offset + i * self.seconds_per_frame) * self.radians_per_second)
        data[:] = indata.tostring()
        self.seconds_offset += self.seconds_per_frame * length


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PySoundIo sine wave output example',
        epilog='Play a sine wave over the default output device'
    )
    parser.add_argument('--freq', default=442.0, help='Note frequency (optional)')
    parser.add_argument('--backend', help='Backend to use (optional)')
    parser.add_argument('--blocksize', type=int, help='Block size (optional)')
    parser.add_argument('--rate', type=int, default=44100, help='Sample rate (optional)')
    parser.add_argument('--device', type=int, help='Output device id (optional)')
    args = parser.parse_args()

    player = Player(args.freq, args.backend, args.device, args.rate, args.blocksize)
    print('Playing...')
    print('CTRL-C to exit')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting...')

    player.close()
