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
import _soundiox as soundio
from pysoundio import (
    PySoundIo,
    SoundIoFormatFloat32LE,
    SoundIoBackendDummy,
    SoundIoOutStream,
    set_write_callback,
    SoundIoFormatU8
)


class Player(object):

    def __init__(self, backend=None, output_device=None,
                 sample_rate=None, block_size=None, channels=None):
        self.pysoundio = PySoundIo(backend=None)

        self.pitch = 440.0
        self.seconds_offset = 0.0
        self.radians_per_second = self.pitch * 2.0 * math.pi
        self.seconds_per_frame = 1.0 / sample_rate

        self.wav_file = open('out.wav', 'wb')

        self.pysoundio.start_output_stream(
            device_id=output_device,
            channels=1,
            sample_rate=44100,
            block_size=4096,
            dtype=SoundIoFormatFloat32LE,
            write_callback=self.callback
        )

    def close(self):
        self.wav_file.close()
        self.pysoundio.close()

    def callback(self, data, length):
        indata = ar.array('f', [0] * 4096)
        # indata = [0.0] * 4096
        for i in range(0, length):
            # indata[i] = 1.0
            indata[i] = math.sin((self.seconds_offset + i * self.seconds_per_frame) * self.radians_per_second)
        struct.pack_into('<%sf' % 4096, data, 0, *indata)
        # data[:] = indata.tostring()
        # self.wav_file.write(data)
        self.seconds_offset += self.seconds_per_frame * length

        soundio.ring_buffer_write_ptr(self.pysoundio.output_buffer, data, len(data))
        soundio.ring_buffer_advance_write_ptr(self.pysoundio.output_buffer, len(data))

        read_buf = soundio.ring_buffer_read_ptr(self.pysoundio.output_buffer)
        print(read_buf)
        # print('data')
        # print(data)
        self.wav_file.write(read_buf)


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
