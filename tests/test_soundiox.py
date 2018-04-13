"""
test_soundiox.py

C API Test Suite
"""
import ctypes
import unittest
import pysoundio
import _soundiox as soundio


class TestInitialisation(unittest.TestCase):

    def setUp(self):
        self.s = soundio.create()

    def tearDown(self):
        soundio.destroy()

    def test_connect(self):
        self.assertEqual(
            soundio.connect_backend(pysoundio.SoundIoBackendDummy), 0)

    def test_version(self):
        self.assertIsInstance(soundio.version_string(), str)

    def test_format_string(self):
        self.assertEqual(
            soundio.format_string(pysoundio.SoundIoFormatFloat32LE),
            'float 32-bit LE'
        )

    def test_backend_count(self):
        self.assertIsInstance(soundio.backend_count(), int)


class TestDeviceAPI(unittest.TestCase):

    def setUp(self):
        self.device = None
        self.s = soundio.create()
        soundio.connect_backend(pysoundio.SoundIoBackendDummy)
        soundio.flush()

    def tearDown(self):
        if self.device:
            soundio.device_unref(self.device)
        soundio.destroy()

    def test_get_input_device_count(self):
        self.assertNotEqual(soundio.get_input_device_count(), -1)

    def test_get_output_device_count(self):
        self.assertNotEqual(soundio.get_output_device_count(), -1)

    def test_default_input_device_index(self):
        self.assertNotEqual(soundio.default_input_device_index(), -1)

    def test_default_output_device_index(self):
        self.assertNotEqual(soundio.default_output_device_index(), -1)

    def test_get_input_device(self):
        default_index = soundio.default_input_device_index()
        self.device = soundio.get_input_device(default_index)
        self.assertIsNotNone(self.device)

    def test_get_output_device(self):
        default_index = soundio.default_output_device_index()
        self.device = soundio.get_output_device(default_index)
        self.assertIsNotNone(self.device)

    def test_device_supports_sample_rate(self):
        default_index = soundio.default_output_device_index()
        self.device = soundio.get_output_device(default_index)
        self.assertIsNotNone(soundio.device_supports_sample_rate(self.device, 44100))

    def test_device_supports_format(self):
        default_index = soundio.default_output_device_index()
        self.device = soundio.get_output_device(default_index)
        self.assertIsNotNone(soundio.device_supports_format(
            self.device, pysoundio.SoundIoFormatFloat32LE))

    def test_device_sort_channel_layouts(self):
        default_index = soundio.default_output_device_index()
        self.device = soundio.get_output_device(default_index)
        soundio.device_sort_channel_layouts(self.device)

    def test_channel_layout_get_default(self):
        self.assertIsNotNone(soundio.channel_layout_get_default(2))

    def test_channel_layout_detect_builtin(self):
        layout = soundio.channel_layout_get_default(2)
        self.assertTrue(soundio.channel_layout_detect_builtin(layout))

    def test_channel_layout_equal(self):
        layout = soundio.channel_layout_get_default(2)
        self.assertTrue(soundio.channel_layout_equal(layout, layout))

    def test_channel_layout_find_channel(self):
        layout = soundio.channel_layout_get_default(2)
        self.assertIsInstance(soundio.channel_layout_find_channel(layout, 0), int)

    def test_channel_layout_get_builtin(self):
        self.assertIsNotNone(soundio.channel_layout_get_builtin(0))

    def test_force_device_scan(self):
        soundio.force_device_scan()

    def test_bytes_per_frame(self):
        self.assertEqual(soundio.get_bytes_per_frame(
            pysoundio.SoundIoFormatFloat32LE, 2), 8)

    def test_bytes_per_sample(self):
        self.assertEqual(soundio.get_bytes_per_sample(
            pysoundio.SoundIoFormatFloat32LE), 4)

    def test_bytes_per_second(self):
        self.assertEqual(soundio.get_bytes_per_second(
            pysoundio.SoundIoFormatFloat32LE, 1, 44100), 176400)


class TestInputStreamAPI(unittest.TestCase):

    def setUp(self):
        self.instream = None
        self.s = soundio.create()
        soundio.connect_backend(pysoundio.SoundIoBackendDummy)
        soundio.flush()
        default_index = soundio.default_input_device_index()
        self.device = soundio.get_input_device(default_index)
        self.buffer = soundio.input_ring_buffer_create(44100 * 8)

    def tearDown(self):
        if self.instream:
            soundio.instream_destroy()
        if self.device:
            soundio.device_unref(self.device)
        soundio.destroy()

    def callback(self):
        pass

    def setup_stream(self):
        soundio.set_read_callbacks(self.callback, self.callback)
        self.instream = soundio.instream_create(self.device)
        instream = ctypes.cast(self.instream, ctypes.POINTER(pysoundio.SoundIoInStream))
        instream.contents.format = soundio.SoundIoFormatFloat32LE
        instream.contents.sample_rate = 44100

    def test_instream_create(self):
        self.assertIsNotNone(soundio.instream_create(self.device))

    def test_instream_open(self):
        self.setup_stream()
        self.assertEqual(soundio.instream_open(), 0)

    def test_instream_start(self):
        self.setup_stream()
        soundio.instream_open()
        self.assertEqual(soundio.instream_start(), 0)

    def test_instream_pause(self):
        self.setup_stream()
        soundio.instream_open()
        self.assertEqual(soundio.instream_pause(True), 0)

    def test_instream_get_latency(self):
        self.setup_stream()
        soundio.instream_open()
        self.assertIsInstance(soundio.instream_get_latency(0.42), int)


class TestOutputStreamAPI(unittest.TestCase):

    def setUp(self):
        self.outstream = None
        self.s = soundio.create()
        soundio.connect_backend(pysoundio.SoundIoBackendDummy)
        soundio.flush()
        default_index = soundio.default_output_device_index()
        self.device = soundio.get_output_device(default_index)
        self.buffer = soundio.input_ring_buffer_create(44100 * 8)

    def tearDown(self):
        if self.outstream:
            soundio.outstream_pause(True)
            soundio.outstream_destroy()
        if self.device:
            soundio.device_unref(self.device)
        soundio.disconnect()
        soundio.destroy()

    def setup_stream(self):
        self.outstream = soundio.outstream_create(self.device)
        outstream = ctypes.cast(self.outstream, ctypes.POINTER(pysoundio.SoundIoOutStream))
        outstream.contents.format = soundio.SoundIoFormatFloat32LE
        outstream.contents.sample_rate = 44100
        outstream.contents.software_latency = 0.0

    def test_outstream_create(self):
        self.assertIsNotNone(soundio.outstream_create(self.device))

    def test_outstream_open(self):
        self.setup_stream()
        self.assertEqual(soundio.outstream_open(), 0)

    def test_outstream_pause(self):
        self.setup_stream()
        soundio.outstream_open()
        self.assertEqual(soundio.outstream_pause(True), 0)

    def test_outstream_get_latency(self):
        self.setup_stream()
        soundio.outstream_open()
        self.assertIsInstance(soundio.outstream_get_latency(0.42), int)


class TestRingBufferAPI(unittest.TestCase):

    def setUp(self):
        self.s = soundio.create()
        soundio.connect_backend(pysoundio.SoundIoBackendDummy)
        soundio.flush()
        self.buffer = soundio.input_ring_buffer_create(44100)

        # Fill with some data for libsoundio < v1.1.0
        data = bytearray(b'' * 42)
        soundio.ring_buffer_write_ptr(self.buffer, data, len(data))
        soundio.ring_buffer_advance_write_ptr(self.buffer, 42)

    def tearDown(self):
        if self.buffer:
            soundio.ring_buffer_destroy(self.buffer)
        soundio.destroy()

    def test_ring_buffer_fill_count(self):
        self.assertEqual(soundio.ring_buffer_fill_count(self.buffer), 42)

    def test_ring_buffer_read_ptr(self):
        ptr = soundio.ring_buffer_read_ptr(self.buffer)
        self.assertIsInstance(ptr, bytes)
        self.assertNotEqual(ptr, 0)

    def test_ring_buffer_advance_read_ptr(self):
        count = soundio.ring_buffer_free_count(self.buffer)
        soundio.ring_buffer_advance_read_ptr(self.buffer, 16)
        self.assertEqual(soundio.ring_buffer_free_count(self.buffer), count + 16)

    def test_ring_buffer_write_ptr(self):
        data = bytearray('\x01\x02\x03\x04'.encode())
        soundio.ring_buffer_write_ptr(self.buffer, data, len(data))

    def test_ring_buffer_free_count(self):
        self.assertNotEqual(soundio.ring_buffer_free_count(self.buffer), 0)

    def test_ring_buffer_advance_write_ptr(self):
        self.assertEqual(soundio.ring_buffer_fill_count(self.buffer), 42)
        soundio.ring_buffer_advance_write_ptr(self.buffer, 16)
        self.assertEqual(soundio.ring_buffer_fill_count(self.buffer), 58)

    def test_ring_buffer_clear(self):
        soundio.ring_buffer_clear(self.buffer)

    def test_ring_buffer_capacity(self):
        self.assertIsInstance(soundio.ring_buffer_capacity(self.buffer), int)


if __name__ == '__main__':
    unittest.main()
