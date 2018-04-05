"""
test_pysoundio.py

PySoundIo Test Suite
"""
import unittest
import pysoundio
import _soundiox


class TestPySoundIo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sio = pysoundio.PySoundIo(
            backend=pysoundio.SoundIoBackendDummy)

    @classmethod
    def tearDownClass(cls):
        cls.sio.close()

    def setUp(self):
        self.sio = pysoundio.PySoundIo(
            backend=pysoundio.SoundIoBackendDummy)
        self.sio.channels = 2
        self.sio.sample_rate = 44100
        self.sio.format = pysoundio.SoundIoFormatFloat32LE
        self.sio.block_size = None
        self.sio.testing = True

        self.callback_called = False
        self.error_callback_called = False

    # - Device API

    def test_backend_count(self):
        self.assertIsInstance(self.sio.backend_count, int)

    def test_get_default_input_device(self):
        self.assertIsNotNone(self.sio.get_default_input_device())

    def test_get_input_device(self):
        self.assertIsNotNone(self.sio.get_input_device(0))

    def test_invalid_input_device(self):
        with self.assertRaises(pysoundio.PySoundIoError):
            self.sio.get_input_device(100)

    def test_get_default_output_device(self):
        self.assertIsNotNone(self.sio.get_default_output_device())

    def test_get_output_device(self):
        self.assertIsNotNone(self.sio.get_output_device(0))

    def test_invalid_output_device(self):
        with self.assertRaises(pysoundio.PySoundIoError):
            self.sio.get_output_device(100)

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

    def test_get_default_sample_rate(self):
        device = self.sio.get_input_device(0)
        self.assertIsInstance(self.sio.get_default_sample_rate(device), int)

    def test_supports_format(self):
        device = self.sio.get_input_device(0)
        self.assertTrue(self.sio.supports_format(device, pysoundio.SoundIoFormatFloat32LE))

    def test_get_default_format(self):
        device = self.sio.get_input_device(0)
        self.assertIsInstance(self.sio.get_default_format(device), int)

    def test_get_default_layout(self):
        self.assertIsNotNone(self.sio._get_default_layout(2))

    def test_bytes_per_frame(self):
        self.assertEqual(self.sio.get_bytes_per_frame(
            pysoundio.SoundIoFormatFloat32LE, 2), 8)

    def test_bytes_per_sample(self):
        self.assertEqual(self.sio.get_bytes_per_sample(
            pysoundio.SoundIoFormatFloat32LE), 4)

    def test_bytes_per_second(self):
        self.assertEqual(self.sio.get_bytes_per_second(
            pysoundio.SoundIoFormatFloat32LE, 1, 44100), 176400)

    # - Input Stream API

    def fill_input_buffer(self):
        data = bytearray(b'\x00' * 4096 * 8)
        _soundiox.ring_buffer_write_ptr(self.sio.input_buffer, data, len(data))
        _soundiox.ring_buffer_advance_write_ptr(self.sio.input_buffer, len(data))

    def test__create_input_ring_buffer(self):
        capacity = 44100 * 8
        self.assertIsNotNone(self.sio._create_input_ring_buffer(capacity))

    def test__create_input_stream(self):
        self.sio.get_default_input_device()
        stream = self.sio._create_input_stream()
        self.assertIsNotNone(stream)

    def test__create_input_stream_blocksize(self):
        self.sio.block_size = 4096
        self.sio.get_default_input_device()
        stream = self.sio._create_input_stream()
        self.assertIsNotNone(stream)

    def test_get_input_latency(self):
        self.sio.start_input_stream(
            sample_rate=44100,
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2)
        self.fill_input_buffer()
        self.assertIsInstance(self.sio.get_input_latency(0.2), int)

    def overflow_callback(self, stream):
        self.callback_called = True

    def error_callback(self, stream, err):
        self.error_callback_called = True

    def test_overflow_callback(self):
        self.sio.overflow_callback = self.overflow_callback
        self.sio._overflow_callback(None)
        self.assertTrue(self.callback_called)

    def test_error_callback(self):
        self.sio.error_callback = self.error_callback
        self.sio._error_callback(None, None)
        self.assertTrue(self.error_callback_called)

    def test_start_input_stream(self):
        self.sio.start_input_stream(
            sample_rate=44100,
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2)
        self.fill_input_buffer()
        self.assertIsNotNone(self.sio.input_stream)

    def test_pause_input_stream(self):
        self.sio.start_input_stream(
            sample_rate=44100,
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2)
        self.fill_input_buffer()
        self.sio.pause_input_stream(True)

    def test_start_input_stream_device(self):
        self.sio.start_input_stream(
            device_id=0,
            sample_rate=44100,
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2)
        self.fill_input_buffer()
        self.assertIsNotNone(self.sio.input_stream)

    def test_start_input_invalid_rate(self):
        with self.assertRaises(pysoundio.PySoundIoError):
            self.sio.start_input_stream(
                sample_rate=10000000,
                dtype=pysoundio.SoundIoFormatFloat32LE,
                channels=2)

    def test_start_input_default_rate(self):
        self.sio.start_input_stream(
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2)
        self.fill_input_buffer()
        self.assertIsNotNone(self.sio.input_stream)
        self.assertIsInstance(self.sio.sample_rate, int)

    def test_start_input_invalid_format(self):
        with self.assertRaises(pysoundio.PySoundIoError):
            self.sio.start_input_stream(
                sample_rate=44100,
                dtype=50,
                channels=2)

    def test_start_input_default_format(self):
        self.sio.start_input_stream(
            sample_rate=44100,
            channels=2)
        self.fill_input_buffer()
        self.assertIsNotNone(self.sio.input_stream)
        self.assertIsInstance(self.sio.format, int)

    # -- Output Stream API

    def test__create_output_ring_buffer(self):
        capacity = 44100 * 8
        self.assertIsNotNone(self.sio._create_output_ring_buffer(capacity))

    def test__create_output_stream(self):
        self.sio.get_default_output_device()
        stream = self.sio._create_output_stream()
        self.assertIsNotNone(stream)

    def test__create_output_stream_blocksize(self):
        self.sio.block_size = 4096
        self.sio.get_default_output_device()
        stream = self.sio._create_output_stream()
        self.assertIsNotNone(stream)

    def test__open_output_stream(self):
        self.sio.get_default_output_device()
        self.sio._create_output_stream()
        self.sio._open_output_stream()
        self.assertIsNotNone(self.sio.block_size)

    def test_clear_output_buffer(self):
        capacity = 44100 * 8
        self.assertIsNotNone(self.sio._create_output_ring_buffer(capacity))
        self.sio._clear_output_buffer()

    def underflow_callback(self, stream):
        self.callback_called = True

    def test_underflow_callback(self):
        self.sio.underflow_callback = self.underflow_callback
        self.sio._underflow_callback(None)
        self.assertTrue(self.callback_called)

    def test_get_output_latency(self):
        self.sio.start_output_stream(
            sample_rate=44100,
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2)
        self.assertIsInstance(self.sio.get_output_latency(0.2), int)

    # def test_pause_output_stream(self):
    #     self.sio.start_output_stream(
    #         sample_rate=44100,
    #         dtype=pysoundio.SoundIoFormatFloat32LE,
    #         channels=2)
    #     self.sio.pause_output_stream(True)

    def test_start_output_stream(self):
        self.sio.start_output_stream(
            sample_rate=44100,
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2)
        self.assertIsNotNone(self.sio.output_stream)

    def test_start_output_stream_device(self):
        self.sio.start_output_stream(
            device_id=0,
            sample_rate=44100,
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2)
        self.assertIsNotNone(self.sio.output_stream)

    def test_start_output_invalid_rate(self):
        with self.assertRaises(pysoundio.PySoundIoError):
            self.sio.start_output_stream(
                sample_rate=10000000,
                dtype=pysoundio.SoundIoFormatFloat32LE,
                channels=2)

    def test_start_output_default_rate(self):
        self.sio.start_output_stream(
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2)
        self.assertIsNotNone(self.sio.output_stream)
        self.assertIsInstance(self.sio.sample_rate, int)

    def test_start_output_invalid_format(self):
        with self.assertRaises(pysoundio.PySoundIoError):
            self.sio.start_output_stream(
                sample_rate=44100,
                dtype=50,
                channels=2)

    def test_start_output_default_format(self):
        self.sio.start_output_stream(
            sample_rate=44100,
            channels=2)
        self.assertIsNotNone(self.sio.output_stream)
        self.assertIsInstance(self.sio.format, int)


class TestInputProcessing(unittest.TestCase):

    def setUp(self):
        self.sio = pysoundio.PySoundIo(
            backend=pysoundio.SoundIoBackendDummy)
        self.callback_called = False

    def tearDown(self):
        self.sio.close()

    def callback(self, data, length):
        self.callback_called = True

    def test_read_callback(self):
        self.sio.start_input_stream(
            sample_rate=44100,
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2,
            block_size=4096,
            read_callback=self.callback)
        self.assertIsNotNone(self.sio.input_stream)

        data = bytearray(b'\x00' * 4096 * 8)
        _soundiox.ring_buffer_write_ptr(self.sio.input_buffer, data, len(data))
        _soundiox.ring_buffer_advance_write_ptr(self.sio.input_buffer, len(data))

        thread = pysoundio.pysoundio._InputProcessingThread(parent=self.sio)
        thread.run()
        self.assertTrue(self.callback_called)


class TestOutputProcessing(unittest.TestCase):

    def setUp(self):
        self.sio = pysoundio.PySoundIo(
            backend=pysoundio.SoundIoBackendDummy)
        self.sio.testing = True
        self.callback_called = False

    def callback(self, data, length):
        self.callback_called = True

    def test_write_callback(self):
        self.sio.start_output_stream(
            sample_rate=44100,
            dtype=pysoundio.SoundIoFormatFloat32LE,
            channels=2,
            block_size=4096,
            write_callback=self.callback)
        self.assertIsNotNone(self.sio.output_stream)
        thread = pysoundio.pysoundio._OutputProcessingThread(parent=self.sio, block_size=4096)
        thread.run()
        self.assertTrue(self.callback_called)
