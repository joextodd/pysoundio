"""
test_pysoundio.py

PySoundIo Test Suite
"""
import ctypes
import unittest
import pysoundio


class TestPySoundIo(unittest.TestCase):

    def setUp(self):
        self.sio = pysoundio.PySoundIo(
            backend=pysoundio.SoundIoBackendDummy,
            sample_rate=44100, format=pysoundio.SoundIoFormatFloat32LE,
            channels=2)

    def tearDown(self):
        self.sio.close()

    def test_version(self):
        self.assertIsInstance(self.sio.version, str)

    def test_get_default_input_device(self):
        self.assertIsNotNone(self.sio.get_default_input_device())

    def test_get_input_device(self):
        self.assertIsNotNone(self.sio.get_input_device(0))

    def test_get_default_output_device(self):
        self.assertIsNotNone(self.sio.get_default_output_device())

    def test_get_output_device(self):
        self.assertIsNotNone(self.sio.get_output_device(0))

    def test_list_devices(self):
        input_devices, output_devices = self.sio.list_devices()
        self.assertIsInstance(input_devices, list)
        self.assertIsInstance(output_devices, list)
        self.assertTrue(len(input_devices) > 0)
        self.assertTrue(len(output_devices) > 0)
        self.assertIsInstance(input_devices[0], dict)
        self.assertIsInstance(output_devices[0], dict)
        self.assertIn('id', input_devices[0])
        self.assertIn('name', input_devices[0])
        self.assertIn('is_raw', input_devices[0])
        self.assertIn('id', output_devices[0])
        self.assertIn('name', output_devices[0])
        self.assertIn('is_raw', output_devices[0])

    def test_supports_sample_rate(self):
        device = self.sio.get_input_device(0)
        self.assertTrue(self.sio.supports_sample_rate(device, 44100))

    def test_supports_format(self):
        device = self.sio.get_input_device(0)
        self.assertTrue(self.sio.supports_format(device, pysoundio.SoundIoFormatFloat32LE))

    def test_get_default_layout(self):
        self.assertIsNotNone(self.sio._get_default_layout(2))

    def test_create_input_ring_buffer(self):
        capacity = 44100 * 8
        self.assertIsNotNone(self.sio._create_input_ring_buffer(capacity))

    def test_create_input_stream(self):
        self.sio.get_default_input_device()
        stream = self.sio._create_input_stream()
        self.assertIsNotNone(stream)

    def test_open_input_stream(self):
        self.sio.get_default_input_device()
        stream = self.sio._create_input_stream()
        self.sio._open_input_stream()

    def test_start_input_stream(self):
        self.sio.get_default_input_device()
        stream = self.sio._create_input_stream()
        self.sio._open_input_stream()
        self.sio._start_input_stream()

    def test_create_output_stream(self):
        self.sio.get_default_output_device()
        stream = self.sio._create_output_stream()
        self.assertIsNotNone(stream)

    def test_open_output_stream(self):
        self.sio.get_default_output_device()
        stream = self.sio._create_output_stream()
        self.sio._open_output_stream()

    # def test_start_output_stream(self):
    #     self.sio.get_default_output_device()
    #     stream = self.sio._create_output_stream()
    #     self.sio._open_output_stream()
    #     self.sio._start_output_stream()


# class TestInputStream(unittest.TestCase):

#     def setUp(self):
#         self.sio = pysoundio.PySoundIo(
#             backend=pysoundio.SoundIoBackendDummy)
#         self.stream = pysoundio.InputStream(
#             self.sio, channels=2, sample_rate=44100,
#             format=pysoundio.SoundIoFormatFloat32LE)

#     def tearDown(self):
#         self.stream.close()
#         self.sio.close()

#     def test_create_ring_buffer(self):
#         capacity = 44100 * 8
#         self.assertIsNotNone(self.stream._create_ring_buffer(capacity))

    # def test_create_input_stream(self):
    #     self.stream._create_input_stream()
    #     self.assertIsNotNone(self.stream.stream)

#     def test_start_stream(self):
#         pass
#         # input_stream = pysoundio.instream_create(self.stream.device)
#         # instream = ctypes.cast(input_stream, ctypes.POINTER(pysoundio.SoundIoInStream))
#         # instream.contents.format = pysoundio.SoundIoFormatFloat32LE
#         # instream.contents.sample_rate = 44100
#         # pysoundio.instream_open(input_stream)
#         # capacity = 44100 * 30 * 8
#         # input_buffer = pysoundio.ring_buffer_create(self.sio._soundio, capacity)
#         # pysoundio.instream_start(input_stream)
#         # self.assertIsNotNone(self.stream.start_stream())


# class TestOutputStream(unittest.TestCase):

#     def setUp(self):
#         self.sio = pysoundio.PySoundIo(
#             backend=pysoundio.SoundIoBackendDummy)
#         self.stream = pysoundio.OutputStream(
#             self.sio, channels=2, sample_rate=44100,
#             format=pysoundio.SoundIoFormatFloat32LE,
#             block_size=4096)

#     def tearDown(self):
#         self.stream.close()
#         self.sio.close()

#     def test_create_ring_buffer(self):
#         capacity = 44100 * 8
#         self.assertIsNotNone(self.stream._create_ring_buffer(capacity))

    # def test_create_output_stream(self):
    #     self.stream._create_output_stream()
    #     self.assertIsNotNone(self.stream.stream)

#     # def test_start_stream(self):
#         # self.stream.start_stream()
