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


static PyObject *
pysoundio_create(PyObject *self, PyObject *args);
static PyObject *
pysoundio_destroy(PyObject *self, PyObject *args);
static PyObject *
pysoundio_connect(PyObject *self, PyObject *args);
static PyObject *
pysoundio_flush(PyObject *self, PyObject *args);
static PyObject *
pysoundio_strerror(PyObject *self, PyObject *args);


static PyObject *
pysoundio_get_output_device_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio_get_input_device_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio_default_input_device_index(PyObject *self, PyObject *args);
static PyObject *
pysoundio_default_output_device_index(PyObject *self, PyObject *args);
static PyObject *
pysoundio_get_input_device(PyObject *self, PyObject *args);
static PyObject *
pysoundio_get_output_device(PyObject *self, PyObject *args);
static PyObject *
pysoundio_device_unref(PyObject *self, PyObject *args);
static PyObject *
pysoundio_device_supports_sample_rate(PyObject *self, PyObject *args);
static PyObject *
pysoundio_device_sort_channel_layouts(PyObject *self, PyObject *args);


static PyObject *
pysoundio_channel_layout_get_default(PyObject *self, PyObject *args);
static PyObject *
pysoundio_instream_create(PyObject *self, PyObject *args);
static PyObject *
pysoundio_instream_destroy(PyObject *self, PyObject *args);
static PyObject *
pysoundio_instream_open(PyObject *self, PyObject *args);
static PyObject *
pysoundio_instream_start(PyObject *self, PyObject *args);


static PyObject *
pysoundio_ring_buffer_create(PyObject *self, PyObject *args);
static PyObject *
pysoundio_ring_buffer_fill_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio_ring_buffer_read_ptr(PyObject *self, PyObject *args);
static PyObject *
pysoundio_ring_buffer_advance_read_ptr(PyObject *self, PyObject *args);
static PyObject *
pysoundio_ring_buffer_write_ptr(PyObject *self, PyObject *args);
static PyObject *
pysoundio_ring_buffer_free_count(PyObject *self, PyObject *args);
static PyObject *
pysoundio_ring_buffer_advance_write_ptr(PyObject *self, PyObject *args);


#endif