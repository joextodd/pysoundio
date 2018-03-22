import time
from pysoundio import PySoundIo


if __name__ == '__main__':
    soundio = PySoundIo()
    print(soundio.version)
    # soundio.list_devices()
    soundio.start_stream(rate=44100, format=15)

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        soundio.close()
