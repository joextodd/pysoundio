"""
example.py

Stream the default input device over the default output device.
Supports specifying device and backend to use.
"""
import argparse
import time

from pysoundio import (
    InputStream,
    OutputStream,
    SoundIoFormatFloat32LE
)

def read_callback(data, length):
    pass

def write_callback(data, length):
    pass


def main(backend,
         input_device, output_device,
         sample_rate, format, channels):

    instream = InputStream(
        device_id=input_device,
        channels=channels,
        sample_rate=sample_rate,
        format=SoundIoFormatFloat32LE,
        block_size=4096,
        callback=read_callback
    )
    instream.start_stream()

    outstream = OutputStream(
        device_id=output_device,
        channels=channels,
        sample_rate=sample_rate,
        format=SoundIoFormatFloat32LE,
        block_size=4096,
        callback=write_callback
    )
    outstream.start_stream()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            pass

    instream.close()
    outstream.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PySoundIo audio stream example',
        epilog='Stream the input device over the output device'
    )
    parser.add_argument('-b', help='Backend to use (optional)')
    parser.add_argument('-f', default=SoundIoFormatFloat32LE, help='Sample format (optional)')
    parser.add_argument('-s', default=44100, help='Sample rate (optional)')
    parser.add_argument('-c', type=int, default=1, help='Mono or stereo (optional)')
    parser.add_argument('-i', help='Input device id (optional)')
    parser.add_argument('-o', help='Output device id (optional)')
    args = parser.parse_args()

    main(args.b, args.i, args.o, args.s, args.f, args.c)