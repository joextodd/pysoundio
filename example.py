"""


"""

import time
from pysoundio import InputStream


if __name__ == '__main__':
    instream = InputStream(
        channels=2,
        sample_rate=44100,
        format=15
    )
    instream.start_stream()

    f = open('out.wav', 'wb')
    try:
        while True:
            time.sleep(1)
            instream.write_data_to_file(f)
    except KeyboardInterrupt:
        f.close()
        instream.close()
