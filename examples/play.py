"""
play.py

Stream a wav file to the default output device.
Supports specifying backend, device and block size.

Requires pysoundfile
    pip install pysoundfile

http://pysoundfile.readthedocs.io/
"""
import argparse
import struct
import time

import soundfile as sf
from pysoundio import (
    PySoundIo,
    SoundIoFormatFloat32LE,
    SoundIoOutStream,
)


class Player(object):

    def __init__(self, infile, backend=None, output_device=None, block_size=None):

        data, rate = sf.read(
            infile,
            dtype='float32',
            always_2d=True
        )
        self.data = [d[0] for d in data]
        self.block_size = block_size

        self.pysoundio = PySoundIo(backend=None)
        self.pysoundio.start_output_stream(
            device_id=output_device,
            channels=1,
            sample_rate=rate,
            block_size=self.block_size,
            dtype=SoundIoFormatFloat32LE,
            write_callback=self.callback
        )
        self.cb = 0
        self.total_blocks = len(self.data)
        self.timer = self.total_blocks / float(rate)

    def close(self):
        self.pysoundio.close()

    def callback(self, data, length):
        dlen = (self.block_size if
                self.cb + self.block_size <= self.total_blocks else
                self.total_blocks - self.cb)
        data[:] = struct.pack('%sf' % dlen, *self.data[self.cb:self.cb + dlen])
        self.cb += dlen


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PySoundIo audio player example',
        epilog='Play a wav file over the default output device'
    )
    parser.add_argument('infile', help='WAV output file name')
    parser.add_argument('--backend', type=int, help='Backend to use (optional)')
    parser.add_argument('--blocksize', type=int, default=4096, help='Block size (optional)')
    parser.add_argument('--device', type=int, help='Output device id (optional)')
    args = parser.parse_args()

    player = Player(args.infile, args.backend, args.device, args.blocksize)
    print('Playing...')
    print('CTRL-C to exit')

    try:
        time.sleep(player.timer)
    except KeyboardInterrupt:
        print('Exiting...')

    player.close()
