"""
devices.py

List the available input and output devices on the system and their properties.
"""
import argparse

from pysoundio import PySoundIo


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PySoundIo list devices example',
        epilog='List the available input and output devices'
    )
    parser.add_argument('--backend', help='Backend to use (optional)')
    args = parser.parse_args()

    pysoundio = PySoundIo(backend=args.backend)
    input_devices, output_devices = pysoundio.list_devices()
    print('\n------ Input Devices ------')
    for i, device in enumerate(input_devices):
        msg = '* ' if device['is_default'] else '  '
        msg += str(i) + ' - ' + device['name']
        print(msg)

    print('\n------ Output Devices ------')
    for i, device in enumerate(output_devices):
        msg = '* ' if device['is_default'] else '  '
        msg += str(i) + ' - ' + device['name']
        print(msg)

    print("")
    pysoundio.close()
