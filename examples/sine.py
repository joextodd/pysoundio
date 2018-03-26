"""
sine.py

Play a sine wave over the default output device.
Supports specifying backend, device, sample rate, block size.

"""
import argparse
import time

from pysoundio import (
    PySoundIo,
    SoundIoFormatFloat32LE,
)


class Player(object):

    def __init__(self, backend=None, output_device=None,
                 sample_rate=None, block_size=None, channels=None):
        self.pysoundio = PySoundIo(backend=None)
        self.pysoundio.start_output_stream(
            device_id=output_device,
            channels=channels,
            sample_rate=sample_rate,
            block_size=block_size,
            format=SoundIoFormatFloat32LE,
            write_callback=self.callback
        )

    def close(self):
        self.pysoundio.close()

    def callback(self, data, length):
        pass



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
