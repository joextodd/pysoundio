"""
play.py

Stream the default input device and save to wav file.
Supports specifying backend, device.

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
    set_write_callback
)


class Player(object):

    def __init__(self, infile, backend=None, output_device=None):

        self.data, rate = sf.read(infile)
        self.pysoundio = PySoundIo(backend=None)
        self.pysoundio.start_output_stream(
            device_id=output_device,
            channels=1,
            sample_rate=rate,
            block_size=4096,
            dtype=SoundIoFormatFloat32LE,
            write_callback=self.callback
        )
        self.current_block = 0
        self.total_blocks = int(len(self.data) / 4096)

    def close(self):
        self.pysoundio.close()

    def callback(self, data, length):
        current = self.current_block * 4096
        data[:] = struct.pack('%sf' % 4096, *self.data[current:current + 4096])
        self.current_block += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PySoundIo audio player example',
        epilog='Play a wav file over the default output device'
    )
    parser.add_argument('infile', help='WAV output file name')
    parser.add_argument('--backend', help='Backend to use (optional)')
    parser.add_argument('--blocksize', help='Block size (optional)')
    parser.add_argument('--rate', default=44100, help='Sample rate (optional)')
    parser.add_argument('--channels', type=int, default=2, help='Mono or stereo (optional)')
    parser.add_argument('--device', help='Output device id (optional)')
    args = parser.parse_args()

    player = Player(args.infile, args.backend, args.device)
    print('Playing...')

    print(player.current_block)
    print(player.total_blocks)
    while player.current_block <= player.total_blocks:
        pass

    player.close()
