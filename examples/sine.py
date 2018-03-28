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

import soundfile as sf
from pysoundio import (
    PySoundIo,
    SoundIoFormatFloat32LE,
    SoundIoOutStream,
    set_write_callback
)


class Player(object):

    def __init__(self, backend=None, output_device=None,
                 sample_rate=None, block_size=None, channels=None):
        self.pysoundio = PySoundIo(backend=None)

        self.pysoundio.start_output_stream(
            device_id=output_device,
            channels=1,
            sample_rate=44100,
            block_size=4096,
            fmt=SoundIoFormatFloat32LE,
            write_callback=self.callback
        )
        self.wav_file = sf.SoundFile(
            'out.wav', mode='w', channels=1,
            samplerate=sample_rate
        )

        self.pitch = 440.0
        self.seconds_offset = 0.0
        self.radians_per_second = self.pitch * 2.0 * math.pi
        self.seconds_per_frame = 1.0 / sample_rate

    def close(self):
        self.pysoundio.close()
        self.wav_file.close()

    def callback(self, data, length):
        indata = ar.array('f', [0.0] * length)
        for i in range(0, length):
            indata[i] = math.sin((self.seconds_offset + i * self.seconds_per_frame) * self.radians_per_second)
        # struct.pack('<f', data, 0, indata)
        data[:] = indata.tostring()
        self.wav_file.buffer_write(indata, dtype='float32')
        self.seconds_offset += self.seconds_per_frame * length


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PySoundIo sine wave output example',
        epilog='Play a sine wave over the default output device'
    )
    parser.add_argument('--backend', help='Backend to use (optional)')
    parser.add_argument('--blocksize', help='Block size (optional)')
    parser.add_argument('--rate', default=44100, help='Sample rate (optional)')
    parser.add_argument('--channels', type=int, default=2, help='Mono or stereo (optional)')
    parser.add_argument('--device', help='Output device id (optional)')
    args = parser.parse_args()

    player = Player(args.backend, args.device, args.rate, args.blocksize, args.channels)
    print('Playing...')
    print('CTRL-C to exit')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting...')

    player.close()
