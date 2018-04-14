"""
devices.py

List the available input and output devices on the system and their properties.
"""
import argparse

from pysoundio import PySoundIo
from pysoundio.constants import SoundIoFormat


def print_devices(devices):
    for i, device in enumerate(devices):
        msg = '* ' if device['is_default'] else '  '
        msg += str(i) + ' - ' + device['name']
        print(msg)
        print('\tsample rate:')
        print('\t default: {}Hz'.format(device['sample_rates']['current']))
        print('\t available: {}'.format(
            ', '.join([str(d['max']) + 'Hz' for d in device['sample_rates']['available']])))
        print('\tformat: {}'.format(
            ', '.join([str(d) for d in device['formats']['available']])))
        print('\tlayouts: {}'.format(device['layouts']['current']['name']))
        print('\t available: {}'.format(
            ', '.join([str(d['name']) for d in device['layouts']['available']])))
        print('\tsoftware latency:')
        print('\t min: {}s, max: {}s, current: {}s'.format(
            round(device['software_latency_min'], 4),
            round(device['software_latency_max'], 4),
            round(device['software_latency_current'], 4)))
        print("")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PySoundIo list devices example',
        epilog='List the available input and output devices'
    )
    parser.add_argument('--backend', type=int, help='Backend to use (optional)')
    args = parser.parse_args()

    pysoundio = PySoundIo(backend=args.backend)
    input_devices, output_devices = pysoundio.list_devices()
    print('\n' + '-' * 20 + ' Input Devices ' + '-' * 20 + '\n')
    print_devices(input_devices)

    print('\n' + '-' * 20 + ' Output Devices ' + '-' * 20 + '\n')
    print_devices(output_devices)

    pysoundio.close()
