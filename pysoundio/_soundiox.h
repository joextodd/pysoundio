/**
 * Copyright (c) 2018 Joe Todd
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#ifndef __SOUNDIOX_H__
#define __SOUNDIOX_H__

/**
 * Initialisation
 */
static PyObject *
pysoundio__create(PyObject *self, PyObject *args);
static PyObject *
pysoundio__destroy(PyObject *self, PyObject *args);
static PyObject *
pysoundio__connect(PyObject *self, PyObject *args);
static PyObject *
pysoundio__disconnect(PyObject *self, PyObject *args);
static PyObject *
pysoundio__connect_backend(PyObject *self, PyObject *args);
static PyObject *
pysoundio__backend_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio__flush(PyObject *self, PyObject *args);
static PyObject *
pysoundio__wait_events(PyObject *self, PyObject *args);
static PyObject *
pysoundio__wakeup(PyObject *self, PyObject *args);

/**
 * Debugging
 */
static PyObject *
pysoundio__strerror(PyObject *self, PyObject *args);
static PyObject *
pysoundio__version_string(PyObject *self, PyObject *args);
static PyObject *
pysoundio__format_string(PyObject *self, PyObject *args);
static PyObject *
pysoundio__get_channel_name(PyObject *self, PyObject *args);

/**
 * Device API
 */
static PyObject *
pysoundio__get_output_device_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio__get_input_device_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio__default_input_device_index(PyObject *self, PyObject *args);
static PyObject *
pysoundio__default_output_device_index(PyObject *self, PyObject *args);
static PyObject *
pysoundio__get_input_device(PyObject *self, PyObject *args);
static PyObject *
pysoundio__get_output_device(PyObject *self, PyObject *args);
static PyObject *
pysoundio__device_unref(PyObject *self, PyObject *args);
static PyObject *
pysoundio__device_supports_sample_rate(PyObject *self, PyObject *args);
static PyObject *
pysoundio__device_supports_format(PyObject *self, PyObject *args);
static PyObject *
pysoundio__device_sort_channel_layouts(PyObject *self, PyObject *args);
static PyObject *
pysoundio__channel_layout_get_default(PyObject *self, PyObject *args);
static PyObject *
pysoundio__best_matching_channel_layout(PyObject *self, PyObject *args);
static PyObject *
pysoundio__channel_layout_builtin_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio__channel_layout_detect_builtin(PyObject *self, PyObject *args);
static PyObject *
pysoundio__channel_layout_equal(PyObject *self, PyObject *args);
static PyObject *
pysoundio__channel_layout_find_channel(PyObject *self, PyObject *args);
static PyObject *
pysoundio__channel_layout_get_builtin(PyObject *self, PyObject *args);
static PyObject *
pysoundio__force_device_scan(PyObject *self, PyObject *args);
static PyObject *
pysoundio__get_bytes_per_frame(PyObject *self, PyObject *args);
static PyObject *
pysoundio__get_bytes_per_sample(PyObject *self, PyObject *args);
static PyObject *
pysoundio__get_bytes_per_second(PyObject *self, PyObject *args);

/**
 * Input Stream API
 */
static PyObject *
pysoundio__set_read_callbacks(PyObject *self, PyObject *args);
static PyObject *
pysoundio__instream_create(PyObject *self, PyObject *args);
static PyObject *
pysoundio__instream_destroy(PyObject *self, PyObject *args);
static PyObject *
pysoundio__instream_open(PyObject *self, PyObject *args);
static PyObject *
pysoundio__instream_start(PyObject *self, PyObject *args);
static PyObject *
pysoundio__instream_pause(PyObject *self, PyObject *args);
static PyObject *
pysoundio__instream_get_latency(PyObject *self, PyObject *args);

/**
 * Output Stream API
 */
static PyObject *
pysoundio__set_write_callbacks(PyObject *self, PyObject *args);
static PyObject *
pysoundio__outstream_create(PyObject *self, PyObject *args);
static PyObject *
pysoundio__outstream_destroy(PyObject *self, PyObject *args);
static PyObject *
pysoundio__outstream_open(PyObject *self, PyObject *args);
static PyObject *
pysoundio__outstream_start(PyObject *self, PyObject *args);
static PyObject *
pysoundio__outstream_pause(PyObject *self, PyObject *args);
static PyObject *
pysoundio__outstream_clear_buffer(PyObject *self, PyObject *args);
static PyObject *
pysoundio__outstream_get_latency(PyObject *self, PyObject *args);

/**
 * Ring Buffer API
 */
static PyObject *
pysoundio__input_ring_buffer_create(PyObject *self, PyObject *args);
static PyObject *
pysoundio__output_ring_buffer_create(PyObject *self, PyObject *args);
static PyObject *
pysoundio__ring_buffer_destroy(PyObject *self, PyObject *args);
static PyObject *
pysoundio__ring_buffer_fill_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio__ring_buffer_read_ptr(PyObject *self, PyObject *args);
static PyObject *
pysoundio__ring_buffer_advance_read_ptr(PyObject *self, PyObject *args);
static PyObject *
pysoundio__ring_buffer_write_ptr(PyObject *self, PyObject *args);
static PyObject *
pysoundio__ring_buffer_free_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio__ring_buffer_advance_write_ptr(PyObject *self, PyObject *args);
static PyObject *
pysoundio__ring_buffer_clear(PyObject *self, PyObject *args);
static PyObject *
pysoundio__ring_buffer_capacity(PyObject *self, PyObject *args);


#endif
