"""
sine.py

Play a sine wave over the default output device.
Supports specifying backend, device, sample rate, block size.

"""
import argparse
import ctypes
import time

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
        self.pysoundio.channels = channels
        self.pysoundio.sample_rate = sample_rate
        self.pysoundio.format = SoundIoFormatFloat32LE
        self.pysoundio.block_size = block_size

        set_write_callback(self.callback)
        self.pysoundio.get_default_output_device()
        stream = self.pysoundio._create_output_stream()
        self.pysoundio._open_output_stream()
        pystream = ctypes.cast(stream, ctypes.POINTER(SoundIoOutStream))
        self.output_bytes_per_frame = pystream.contents.bytes_per_frame
        capacity = (30 *
            pystream.contents.sample_rate * pystream.contents.bytes_per_frame)
        self.pysoundio._create_output_ring_buffer(capacity)
        self.pysoundio._start_output_stream()

        # self.pysoundio.start_output_stream(
        #     device_id=output_device,
        #     channels=channels,
        #     sample_rate=sample_rate,
        #     block_size=block_size,
        #     format=SoundIoFormatFloat32LE,
        #     write_callback=self.callback
        # )

    def close(self):
        self.pysoundio.close()

    def callback(self, data, length):
        print('hello')



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
