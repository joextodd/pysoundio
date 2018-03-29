"""
test_soundiox.py

C API Test Suite
"""
import ctypes
import unittest
import pysoundio


class TestInitialisation(unittest.TestCase):

    def setUp(self):
        self.s = pysoundio.create()

    def tearDown(self):
        pysoundio.destroy(self.s)

    def test_connect(self):
        self.assertEqual(
            pysoundio.connect_backend(self.s, pysoundio.SoundIoBackendDummy), 0)

    def test_version(self):
        self.assertIsInstance(pysoundio.version_string(), str)

    def test_format_string(self):
        self.assertEqual(
            pysoundio.format_string(pysoundio.SoundIoFormatFloat32LE),
            'float 32-bit LE'
        )

    def test_backend_count(self):
        self.assertIsInstance(pysoundio.backend_count(self.s), int)


class TestDeviceAPI(unittest.TestCase):

    def setUp(self):
        self.device = None
        self.s = pysoundio.create()
        pysoundio.connect_backend(self.s, pysoundio.SoundIoBackendDummy)
        pysoundio.flush(self.s)

    def tearDown(self):
        if self.device:
            pysoundio.device_unref(self.device)
        pysoundio.destroy(self.s)

    def test_get_input_device_count(self):
        self.assertNotEqual(pysoundio.get_input_device_count(self.s), -1)

    def test_get_output_device_count(self):
        self.assertNotEqual(pysoundio.get_output_device_count(self.s), -1)

    def test_default_input_device_index(self):
        self.assertNotEqual(pysoundio.default_input_device_index(self.s), -1)

    def test_default_output_device_index(self):
        self.assertNotEqual(pysoundio.default_output_device_index(self.s), -1)

    def test_get_input_device(self):
        default_index = pysoundio.default_input_device_index(self.s)
        self.device = pysoundio.get_input_device(self.s, default_index)
        self.assertIsNotNone(self.device)

    def test_get_output_device(self):
        default_index = pysoundio.default_output_device_index(self.s)
        self.device = pysoundio.get_output_device(self.s, default_index)
        self.assertIsNotNone(self.device)

    def test_device_supports_sample_rate(self):
        default_index = pysoundio.default_output_device_index(self.s)
        self.device = pysoundio.get_output_device(self.s, default_index)
        self.assertIsNotNone(pysoundio.device_supports_sample_rate(self.device, 44100))

    def test_device_supports_format(self):
        default_index = pysoundio.default_output_device_index(self.s)
        self.device = pysoundio.get_output_device(self.s, default_index)
        self.assertIsNotNone(pysoundio.device_supports_format(
            self.device, pysoundio.SoundIoFormatFloat32LE))

    def test_device_sort_channel_layouts(self):
        default_index = pysoundio.default_output_device_index(self.s)
        self.device = pysoundio.get_output_device(self.s, default_index)
        pysoundio.device_sort_channel_layouts(self.device)

    def test_channel_layout_get_default(self):
        self.assertIsNotNone(pysoundio.channel_layout_get_default(2))

    def test_channel_layout_detect_builtin(self):
        layout = pysoundio.channel_layout_get_default(2)
        self.assertTrue(pysoundio.channel_layout_detect_builtin(layout))

    def test_channel_layout_equal(self):
        layout = pysoundio.channel_layout_get_default(2)
        self.assertTrue(pysoundio.channel_layout_equal(layout, layout))

    def test_channel_layout_find_channel(self):
        layout = pysoundio.channel_layout_get_default(2)
        self.assertIsInstance(pysoundio.channel_layout_find_channel(layout, 0), int)

    def test_channel_layout_get_builtin(self):
        self.assertIsNotNone(pysoundio.channel_layout_get_builtin(0))

    def test_force_device_scan(self):
        pysoundio.force_device_scan(self.s)

    def test_bytes_per_frame(self):
        self.assertEqual(pysoundio.get_bytes_per_frame(
            pysoundio.SoundIoFormatFloat32LE, 2), 8)

    def test_bytes_per_sample(self):
        self.assertEqual(pysoundio.get_bytes_per_sample(
            pysoundio.SoundIoFormatFloat32LE), 4)

    def test_bytes_per_second(self):
        self.assertEqual(pysoundio.get_bytes_per_second(
            pysoundio.SoundIoFormatFloat32LE, 1, 44100), 176400)


class TestInputStreamAPI(unittest.TestCase):

    def setUp(self):
        self.instream = None
        self.s = pysoundio.create()
        pysoundio.connect_backend(self.s, pysoundio.SoundIoBackendDummy)
        pysoundio.flush(self.s)
        default_index = pysoundio.default_input_device_index(self.s)
        self.device = pysoundio.get_input_device(self.s, default_index)
        self.buffer = pysoundio.input_ring_buffer_create(self.s, 44100 * 8)

    def tearDown(self):
        if self.instream:
            pysoundio.instream_destroy(self.instream)
        if self.device:
            pysoundio.device_unref(self.device)
        pysoundio.destroy(self.s)

    def callback(self):
        pass

    def setup_stream(self):
        pysoundio.set_read_callback(self.callback)
        self.instream = pysoundio.instream_create(self.device)
        instream = ctypes.cast(self.instream, ctypes.POINTER(pysoundio.SoundIoInStream))
        instream.contents.format = pysoundio.SoundIoFormatFloat32LE
        instream.contents.sample_rate = 44100

    def test_instream_create(self):
        self.assertIsNotNone(pysoundio.instream_create(self.device))

    def test_instream_open(self):
        self.setup_stream()
        self.assertEqual(pysoundio.instream_open(self.instream), 0)

    def test_instream_start(self):
        self.setup_stream()
        pysoundio.instream_open(self.instream)
        self.assertEqual(pysoundio.instream_start(self.instream), 0)

    def test_instream_get_latency(self):
        self.setup_stream()
        pysoundio.instream_open(self.instream)
        self.assertIsInstance(pysoundio.instream_get_latency(self.instream, 0.42), int)


class TestOutputStreamAPI(unittest.TestCase):

    def setUp(self):
        self.outstream = None
        self.s = pysoundio.create()
        pysoundio.connect_backend(self.s, pysoundio.SoundIoBackendDummy)
        pysoundio.flush(self.s)
        default_index = pysoundio.default_output_device_index(self.s)
        self.device = pysoundio.get_output_device(self.s, default_index)
        self.buffer = pysoundio.input_ring_buffer_create(self.s, 44100 * 8)

    def tearDown(self):
        if self.outstream:
            pysoundio.outstream_destroy(self.outstream)
        if self.device:
            pysoundio.device_unref(self.device)
        pysoundio.destroy(self.s)

    def callback(self):
        pass

    def setup_stream(self):
        self.outstream = pysoundio.outstream_create(self.device)
        pysoundio.set_write_callback(self.callback)
        outstream = ctypes.cast(self.outstream, ctypes.POINTER(pysoundio.SoundIoOutStream))
        outstream.contents.format = pysoundio.SoundIoFormatFloat32LE
        outstream.contents.sample_rate = 44100
        outstream.contents.software_latency = 0.0

    def test_outstream_create(self):
        self.assertIsNotNone(pysoundio.outstream_create(self.device))

    def test_outstream_open(self):
        self.setup_stream()
        self.assertEqual(pysoundio.outstream_open(self.outstream), 0)

    def test_outstream_start(self):
        self.setup_stream()
        pysoundio.outstream_open(self.outstream)
        self.assertEqual(pysoundio.outstream_start(self.outstream), 0)

    def test_outstream_get_latency(self):
        self.setup_stream()
        pysoundio.outstream_open(self.outstream)
        self.assertIsInstance(pysoundio.outstream_get_latency(self.outstream, 0.42), int)


class TestRingBufferAPI(unittest.TestCase):

    def setUp(self):
        self.s = pysoundio.create()
        pysoundio.connect_backend(self.s, pysoundio.SoundIoBackendDummy)
        pysoundio.flush(self.s)
        self.buffer = pysoundio.input_ring_buffer_create(self.s, 44100)

    def tearDown(self):
        if self.buffer:
            pysoundio.ring_buffer_destroy(self.buffer)
        pysoundio.destroy(self.s)

    def test_ring_buffer_fill_count(self):
        self.assertEqual(pysoundio.ring_buffer_fill_count(self.buffer), 0)

    def test_ring_buffer_read_ptr(self):
        ptr = pysoundio.ring_buffer_read_ptr(self.buffer)
        self.assertIsInstance(ptr, bytes)
        self.assertNotEqual(ptr, 0)

    def test_ring_buffer_advance_read_ptr(self):
        count = pysoundio.ring_buffer_free_count(self.buffer)
        pysoundio.ring_buffer_advance_read_ptr(self.buffer, 16)
        self.assertEqual(pysoundio.ring_buffer_free_count(self.buffer), count + 16)

    def test_ring_buffer_write_ptr(self):
        data = bytearray('\x01\x02\x03\x04'.encode())
        pysoundio.ring_buffer_write_ptr(self.buffer, data, len(data))

    def test_ring_buffer_free_count(self):
        self.assertNotEqual(pysoundio.ring_buffer_free_count(self.buffer), 0)

    def test_ring_buffer_advance_write_ptr(self):
        self.assertEqual(pysoundio.ring_buffer_fill_count(self.buffer), 0)
        pysoundio.ring_buffer_advance_write_ptr(self.buffer, 16)
        self.assertEqual(pysoundio.ring_buffer_fill_count(self.buffer), 16)

    def test_outstream_clear_buffer(self):
        pysoundio.ring_buffer_clear(self.buffer)

    def test_ring_buffer_capacity(self):
        self.assertIsInstance(pysoundio.ring_buffer_capacity(self.buffer), int)


if __name__ == '__main__':
    unittest.main()
