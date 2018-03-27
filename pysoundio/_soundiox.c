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

#include <Python.h>
#include <soundio/soundio.h>
#include "_soundiox.h"


/************************************************************
 * Python Methods
 ************************************************************/

static PyMethodDef soundio_methods[] = {

    {
        "create",
        pysoundio__create, METH_VARARGS,
        "create soundio struct"
    },
    {
        "destroy",
        pysoundio__destroy, METH_VARARGS,
        "destroy soundio struct"
    },
    {
        "connect",
        pysoundio__connect, METH_VARARGS,
        "connect to the default backend"
    },
    {
        "connect_backend",
        pysoundio__connect_backend, METH_VARARGS,
        "connect to a specific backend"
    },
    {
        "flush",
        pysoundio__flush, METH_VARARGS,
        "atomically update information for all connected devices"
    },
    {
        "strerror",
        pysoundio__strerror, METH_VARARGS,
        "get a string representation of a SoundIoError."
    },
    {
        "version_string",
        pysoundio__version_string, METH_VARARGS,
        "get version string"
    },
    {
        "format_string",
        pysoundio__format_string, METH_VARARGS,
        "get string representation of format"
    },
    {
        "get_output_device_count",
        pysoundio__get_output_device_count, METH_VARARGS,
        "get output device count"
    },
    {
        "get_input_device_count",
        pysoundio__get_input_device_count, METH_VARARGS,
        "get input device count"
    },
    {
        "default_input_device_index",
        pysoundio__default_input_device_index, METH_VARARGS,
        "get default input device index"
    },
    {
        "default_output_device_index",
        pysoundio__default_output_device_index, METH_VARARGS,
        "get default output device index"
    },
    {
        "get_input_device",
        pysoundio__get_input_device, METH_VARARGS,
        "get input device"
    },
    {
        "get_output_device",
        pysoundio__get_output_device, METH_VARARGS,
        "get output device"
    },
    {
        "device_unref",
        pysoundio__device_unref, METH_VARARGS,
        "clean up device"
    },
    {
        "device_supports_sample_rate",
        pysoundio__device_supports_sample_rate, METH_VARARGS,
        "check if sample rate is supported by device"
    },
    {
        "device_supports_format",
        pysoundio__device_supports_format, METH_VARARGS,
        "check if format is supported by device"
    },
    {
        "device_sort_channel_layouts",
        pysoundio__device_sort_channel_layouts, METH_VARARGS,
        "sorts channel layouts by channel count, descending."
    },
    {
        "channel_layout_get_default",
        pysoundio__channel_layout_get_default, METH_VARARGS,
        "get the default builtin channel layout"
    },
    {
        "set_read_callback",
        pysoundio__set_read_callback, METH_VARARGS,
        "set read callback"
    },
    {
        "instream_create",
        pysoundio__instream_create, METH_VARARGS,
        "allocates memory for input stream"
    },
    {
        "instream_destroy",
        pysoundio__instream_destroy, METH_VARARGS,
        "cleans up input stream"
    },
    {
        "instream_open",
        pysoundio__instream_open, METH_VARARGS,
        "open input stream"
    },
    {
        "instream_start",
        pysoundio__instream_start, METH_VARARGS,
        "start input stream"
    },
    {
        "set_write_callback",
        pysoundio__set_write_callback, METH_VARARGS,
        "set write callback"
    },
    {
        "outstream_create",
        pysoundio__outstream_create, METH_VARARGS,
        "allocates memory for output stream"
    },
    {
        "outstream_destroy",
        pysoundio__outstream_destroy, METH_VARARGS,
        "cleans up output stream"
    },
    {
        "outstream_open",
        pysoundio__outstream_open, METH_VARARGS,
        "open output stream"
    },
    {
        "outstream_start",
        pysoundio__outstream_start, METH_VARARGS,
        "start output stream"
    },
    {
        "input_ring_buffer_create",
        pysoundio__input_ring_buffer_create, METH_VARARGS,
        "create input ring buffer"
    },
    {
        "output_ring_buffer_create",
        pysoundio__output_ring_buffer_create, METH_VARARGS,
        "create output ring buffer"
    },
    {
        "ring_buffer_destroy",
        pysoundio__ring_buffer_destroy, METH_VARARGS,
        "destroy ring buffer"
    },
    {
        "ring_buffer_fill_count",
        pysoundio__ring_buffer_fill_count, METH_VARARGS,
        "how many bytes of the buffer is used, ready for reading"
    },
    {
        "ring_buffer_read_ptr",
        pysoundio__ring_buffer_read_ptr, METH_VARARGS,
        "get pointer to read from buffer"
    },
    {
        "ring_buffer_advance_read_ptr",
        pysoundio__ring_buffer_advance_read_ptr, METH_VARARGS,
        "advance read pointer"
    },
    {
        "ring_buffer_write_ptr",
        pysoundio__ring_buffer_write_ptr, METH_VARARGS,
        "get pointer to write to buffer"
    },
    {
        "ring_buffer_free_count",
        pysoundio__ring_buffer_free_count, METH_VARARGS,
        "how many bytes of the buffer is free, ready for writing"
    },
    {
        "ring_buffer_advance_write_ptr",
        pysoundio__ring_buffer_advance_write_ptr, METH_VARARGS,
        "advance write pointer"
    },


    {NULL, NULL, 0, NULL}
};

static PyObject *PySoundIoError;

struct RecordContext {
    struct SoundIoRingBuffer *input_buffer;
    struct SoundIoRingBuffer *output_buffer;

    PyObject *read_callback;
    PyObject *write_callback;
};
struct RecordContext rc;

static int min_int(int a, int b) {
    return (a < b) ? a : b;
}

#if PY_MAJOR_VERSION==2
#define FORMAT_DATA_READ_ID     "s#"
#define FORMAT_DATA_WRITE_ID    "Osi"
#else
#define FORMAT_DATA_READ_ID     "y#"
#define FORMAT_DATA_WRITE_ID    "Oyi"
#endif


/*************************************************************
 * Initialisation
 *************************************************************/

static PyObject *
pysoundio__create(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    struct SoundIo *soundio = soundio_create();
    if (!soundio) {
        PyErr_SetString(PySoundIoError, "Out of memory");
        return NULL;
    }

    // Py_XINCREF(soundio);
    return PyLong_FromVoidPtr(soundio);
}

static PyObject *
pysoundio__destroy(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    soundio_destroy(soundio);
    // Py_XDECREF(soundio);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio__connect(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    int err = soundio_connect(soundio);
    if (err) {
        PyErr_SetString(PySoundIoError, soundio_strerror(err));
        return NULL;
    }
    // Py_DECREF(soundio);
    return Py_BuildValue("i", err);
}

static PyObject *
pysoundio__connect_backend(PyObject *self, PyObject *args)
{
    PyObject *data;
    uint8_t backend;

    if (!PyArg_ParseTuple(args, "Ob", &data, &backend))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    int err = soundio_connect_backend(soundio, backend);
    if (err) {
        PyErr_SetString(PySoundIoError, soundio_strerror(err));
        return NULL;
    }
    // Py_DECREF(soundio);
    return Py_BuildValue("i", err);
}

static PyObject *
pysoundio__flush(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    soundio_flush_events(soundio);
    // Py_DECREF(soundio);
    Py_RETURN_NONE;
}

/*************************************************************
 * Debugging
 *************************************************************/

static PyObject *
pysoundio__version_string(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    const char *version = soundio_version_string();
    return Py_BuildValue("s", version);
}

static PyObject *
pysoundio__strerror(PyObject *self, PyObject *args)
{
    int error;

    if (!PyArg_ParseTuple(args, "i", &error))
        return NULL;

    const char *message = soundio_strerror(error);
    return Py_BuildValue("s", message);
}

static PyObject *
pysoundio__format_string(PyObject *self, PyObject *args)
{
    uint8_t format;

    if (!PyArg_ParseTuple(args, "b", &format))
        return NULL;

    const char *format_string = soundio_format_string(format);
    return Py_BuildValue("s", format_string);
}


/*************************************************************
 * Device API
 *************************************************************/

static PyObject *
pysoundio__get_output_device_count(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);
    int output_count = soundio_output_device_count(soundio);

    // Py_DECREF(soundio);
    return Py_BuildValue("i", output_count);
}

static PyObject *
pysoundio__get_input_device_count(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);
    int input_count = soundio_input_device_count(soundio);

    // Py_DECREF(soundio);
    return Py_BuildValue("i", input_count);
}

static PyObject *
pysoundio__default_input_device_index(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);
    int input_index = soundio_default_input_device_index(soundio);

    // Py_DECREF(soundio);
    return Py_BuildValue("i", input_index);
}

static PyObject *
pysoundio__default_output_device_index(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);
    int output_index = soundio_default_output_device_index(soundio);

    // Py_DECREF(soundio);
    return Py_BuildValue("i", output_index);
}

static PyObject *
pysoundio__get_input_device(PyObject *self, PyObject *args)
{
    PyObject *data;
    int device_index;

    if (!PyArg_ParseTuple(args, "Oi", &data, &device_index))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);
    struct SoundIoDevice *device = soundio_get_input_device(soundio, device_index);

    if (device->probe_error) {
        PyErr_SetString(PySoundIoError, "Unable to probe device\n");
        return NULL;
    }

    // Py_DECREF(soundio);
    return PyLong_FromVoidPtr(device);
}

static PyObject *
pysoundio__get_output_device(PyObject *self, PyObject *args)
{
    PyObject *data;
    int device_index;

    if (!PyArg_ParseTuple(args, "Oi", &data, &device_index))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);
    struct SoundIoDevice *device = soundio_get_output_device(soundio, device_index);

    if (device->probe_error) {
        PyErr_SetString(PySoundIoError, "Unable to probe device\n");
        return NULL;
    }

    // Py_DECREF(soundio);
    return PyLong_FromVoidPtr(device);
}

static PyObject *
pysoundio__device_unref(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoDevice *device = PyLong_AsVoidPtr(data);

    soundio_device_unref(device);
    // Py_XDECREF(device);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio__device_supports_sample_rate(PyObject *self, PyObject *args)
{
    PyObject *data;
    int sample_rate;

    if (!PyArg_ParseTuple(args, "Oi", &data, &sample_rate))
        return NULL;

    struct SoundIoDevice *device = PyLong_AsVoidPtr(data);
    bool supported = soundio_device_supports_sample_rate(device, sample_rate);

    return Py_BuildValue("i", (int)supported);
}

static PyObject *
pysoundio__device_supports_format(PyObject *self, PyObject *args)
{
    PyObject *data;
    int format;

    if (!PyArg_ParseTuple(args, "Oi", &data, &format))
        return NULL;

    struct SoundIoDevice *device = PyLong_AsVoidPtr(data);
    bool supported = soundio_device_supports_format(device, format);

    return Py_BuildValue("i", (int)supported);
}

static PyObject *
pysoundio__device_sort_channel_layouts(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoDevice *device = PyLong_AsVoidPtr(data);
    soundio_device_sort_channel_layouts(device);

    Py_RETURN_NONE;
}

static PyObject *
pysoundio__channel_layout_get_default(PyObject *self, PyObject *args)
{
    int channel_count;

    if (!PyArg_ParseTuple(args, "i", &channel_count))
        return NULL;

    const struct SoundIoChannelLayout *layout = soundio_channel_layout_get_default(channel_count);
    return PyLong_FromVoidPtr((void *)layout);
}


/*************************************************************
 * Input Stream API
 *************************************************************/

static void
read_callback(struct SoundIoInStream *instream, int frame_count_min, int frame_count_max)
{
    struct RecordContext *rc = instream->userdata;
    struct SoundIoChannelArea *areas;
    int err;

    if (!rc->input_buffer)
        return;

    char *write_ptr = soundio_ring_buffer_write_ptr(rc->input_buffer);
    int free_bytes = soundio_ring_buffer_free_count(rc->input_buffer);

    int free_count = free_bytes / instream->bytes_per_frame;

    if (free_count < frame_count_min) {
        fprintf(stderr, "ring buffer overflow\n");
        exit(1);
    }
    int write_frames = min_int(free_count, frame_count_max);
    int frames_left = write_frames;

    for (;;) {
        int frame_count = frames_left;
        if ((err = soundio_instream_begin_read(instream, &areas, &frame_count))) {
            fprintf(stderr, "begin read error: %s", soundio_strerror(err));
            exit(1);
        }
        if (!frame_count)
            break;
        if (!areas) {
            // Due to an overflow there is a hole. Fill the ring buffer with
            // silence for the size of the hole.
            memset(write_ptr, 0, frame_count * instream->bytes_per_frame);
        } else {
            for (int frame = 0; frame < frame_count; frame += 1) {
                for (int ch = 0; ch < instream->layout.channel_count; ch += 1) {
                    memcpy(write_ptr, areas[ch].ptr, instream->bytes_per_sample);
                    areas[ch].ptr += areas[ch].step;
                    write_ptr += instream->bytes_per_sample;
                }
            }
        }
        if ((err = soundio_instream_end_read(instream))) {
            fprintf(stderr, "end read error: %s", soundio_strerror(err));
            exit(1);
        }
        frames_left -= frame_count;
        if (frames_left <= 0)
            break;
    }

    int advance_bytes = write_frames * instream->bytes_per_frame;
    soundio_ring_buffer_advance_write_ptr(rc->input_buffer, advance_bytes);

    PyGILState_STATE state = PyGILState_Ensure();

    if (rc->read_callback) {
        PyObject *result = PyObject_CallObject(rc->read_callback, NULL);
        Py_XDECREF(result);
    }

    PyGILState_Release(state);
}

static void
overflow_callback(struct SoundIoInStream *instream)
{
    static int count = 0;
    count++;
}

static PyObject *
pysoundio__set_read_callback(PyObject *self, PyObject *args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O", &temp)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        Py_XINCREF(temp);
        Py_XDECREF(rc.read_callback);
        rc.read_callback = temp;
        Py_RETURN_NONE;
    }
    return result;
}

static PyObject *
pysoundio__instream_create(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoDevice *device = PyLong_AsVoidPtr(data);
    struct SoundIoInStream *instream = soundio_instream_create(device);

    instream->read_callback = read_callback;
    instream->overflow_callback = overflow_callback;
    instream->userdata = &rc;

    if (!instream) {
        PyErr_SetString(PySoundIoError, "Out of memory");
        return NULL;
    }

    // Py_XINCREF(instream);
    return PyLong_FromVoidPtr(instream);
}

static PyObject *
pysoundio__instream_destroy(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoInStream *instream = PyLong_AsVoidPtr(data);

    soundio_instream_destroy(instream);
    // Py_XDECREF(instream);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio__instream_open(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoInStream *instream = PyLong_AsVoidPtr(data);

    int err = soundio_instream_open(instream);
    if (err) {
        PyErr_SetString(PySoundIoError, soundio_strerror(err));
        return NULL;
    }

    return Py_BuildValue("i", err);
}

static PyObject *
pysoundio__instream_start(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoInStream *instream = PyLong_AsVoidPtr(data);

    int err = soundio_instream_start(instream);
    if (err) {
        PyErr_SetString(PySoundIoError, soundio_strerror(err));
        return NULL;
    }
    return Py_BuildValue("i", err);
}


/*************************************************************
 * Output Stream API
 *************************************************************/

static PyObject *
pysoundio__set_write_callback(PyObject *self, PyObject *args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O", &temp)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        Py_XINCREF(temp);
        Py_XDECREF(rc.write_callback);
        rc.write_callback = temp;
        Py_RETURN_NONE;
    }
    return result;
}

static void
write_callback(struct SoundIoOutStream *outstream, int frame_count_min, int frame_count_max)
{
    struct RecordContext *rc = outstream->userdata;
    struct SoundIoChannelArea *areas;
    int frame_count;
    int err;

    if (!rc->output_buffer)
        return;

    char *read_ptr = soundio_ring_buffer_read_ptr(rc->output_buffer);
    int fill_bytes = soundio_ring_buffer_fill_count(rc->output_buffer);
    int fill_count = fill_bytes / outstream->bytes_per_frame;

    if (frame_count_min > fill_count) {
        // Ring buffer does not have enough data, fill with zeroes.
        for (;;) {
            if ((err = soundio_outstream_begin_write(outstream, &areas, &frame_count)))
                PyErr_SetString(PySoundIoError, soundio_strerror(err));
            if (frame_count <= 0)
                break;
            for (int frame = 0; frame < frame_count; frame += 1) {
                for (int ch = 0; ch < outstream->layout.channel_count; ch += 1) {
                    memset(areas[ch].ptr, 0, outstream->bytes_per_sample);
                    areas[ch].ptr += areas[ch].step;
                }
            }
            if ((err = soundio_outstream_end_write(outstream)))
                PyErr_SetString(PySoundIoError, soundio_strerror(err));
        }
    }

    int read_count = min_int(frame_count_max, fill_count);
    int frames_left = read_count;

    while (frames_left > 0) {
        int frame_count = frames_left;
        if ((err = soundio_outstream_begin_write(outstream, &areas, &frame_count)))
            PyErr_SetString(PySoundIoError, soundio_strerror(err));
        if (frame_count <= 0)
            break;
        for (int frame = 0; frame < frame_count; frame += 1) {
            for (int ch = 0; ch < outstream->layout.channel_count; ch += 1) {
                memcpy(areas[ch].ptr, read_ptr, outstream->bytes_per_sample);
                areas[ch].ptr += areas[ch].step;
                read_ptr += outstream->bytes_per_sample;
            }
        }
        if ((err = soundio_outstream_end_write(outstream)))
            PyErr_SetString(PySoundIoError, soundio_strerror(err));
        frames_left -= frame_count;
    }
    soundio_ring_buffer_advance_read_ptr(rc->output_buffer, read_count * outstream->bytes_per_frame);

    // PyGILState_STATE state = PyGILState_Ensure();

    // if (rc->write_callback) {
    //     PyObject *result = PyObject_CallObject(rc->write_callback, NULL);
    //     Py_XDECREF(result);
    // }

    // PyGILState_Release(state);
}


static void
underflow_callback(struct SoundIoOutStream *outstream)
{
    static int count = 0;
    count++;
}

static PyObject *
pysoundio__outstream_create(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoDevice *device = PyLong_AsVoidPtr(data);
    struct SoundIoOutStream *outstream = soundio_outstream_create(device);

    outstream->write_callback = write_callback;
    outstream->underflow_callback = underflow_callback;
    outstream->userdata = &rc;

    if (!outstream) {
        PyErr_SetString(PySoundIoError, "Out of memory");
        return NULL;
    }

    // Py_XINCREF(outstream);
    return PyLong_FromVoidPtr(outstream);
}

static PyObject *
pysoundio__outstream_destroy(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoOutStream *outstream = PyLong_AsVoidPtr(data);

    soundio_outstream_destroy(outstream);
    // Py_XDECREF(outstream);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio__outstream_open(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoOutStream *outstream = PyLong_AsVoidPtr(data);

    int err = soundio_outstream_open(outstream);
    if (err) {
        PyErr_SetString(PySoundIoError, soundio_strerror(err));
        return NULL;
    }
    return Py_BuildValue("i", err);
}

static PyObject *
pysoundio__outstream_start(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoOutStream *outstream = PyLong_AsVoidPtr(data);

    int err = soundio_outstream_start(outstream);
    if (err) {
        PyErr_SetString(PySoundIoError, soundio_strerror(err));
        return NULL;
    }

    return Py_BuildValue("i", err);
}


/*************************************************************
 * Ring Buffer API
 *************************************************************/

static PyObject *
pysoundio__input_ring_buffer_create(PyObject *self, PyObject *args)
{
    PyObject *data;
    int capacity;

    if (!PyArg_ParseTuple(args, "Oi", &data, &capacity))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);
    rc.input_buffer = soundio_ring_buffer_create(soundio, capacity);
    if (!rc.input_buffer) {
        PyErr_SetString(PySoundIoError, "Out of memory");
        return NULL;
    }

    // Py_XINCREF(rc.input_buffer);
    return PyLong_FromVoidPtr(rc.input_buffer);
}

static PyObject *
pysoundio__output_ring_buffer_create(PyObject *self, PyObject *args)
{
    PyObject *data;
    int capacity;

    if (!PyArg_ParseTuple(args, "Oi", &data, &capacity))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);
    rc.output_buffer = soundio_ring_buffer_create(soundio, capacity);
    if (!rc.output_buffer) {
        PyErr_SetString(PySoundIoError, "Out of memory");
        return NULL;
    }

    // Py_DECREF(soundio);
    // Py_XINCREF(rc.output_buffer);
    return PyLong_FromVoidPtr(rc.output_buffer);
}

static PyObject *
pysoundio__ring_buffer_destroy(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);

    // Py_XDECREF(buffer);
    soundio_ring_buffer_destroy(buffer);
    Py_RETURN_NONE;
}


static PyObject *
pysoundio__ring_buffer_fill_count(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);
    int bytes = soundio_ring_buffer_fill_count(buffer);

    // Py_DECREF(buffer);
    return Py_BuildValue("i", bytes);
}

static PyObject *
pysoundio__ring_buffer_read_ptr(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);
    int fill_bytes = soundio_ring_buffer_fill_count(buffer);
    char *ptr = soundio_ring_buffer_read_ptr(buffer);

    // Py_DECREF(buffer);
    return Py_BuildValue(FORMAT_DATA_READ_ID, ptr, fill_bytes);
}

static PyObject *
pysoundio__ring_buffer_advance_read_ptr(PyObject *self, PyObject *args)
{
    PyObject *data;
    int count;

    if (!PyArg_ParseTuple(args, "Oi", &data, &count))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);
    soundio_ring_buffer_advance_read_ptr(buffer, count);

    // Py_DECREF(buffer);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio__ring_buffer_write_ptr(PyObject *self, PyObject *args)
{
    PyObject *pbuf;
    char *data;
    int length;

    if (!PyArg_ParseTuple(args, FORMAT_DATA_WRITE_ID, &pbuf, &data, &length))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(pbuf);
    char *ptr = soundio_ring_buffer_write_ptr(buffer);

    for (int i = 0; i < length; i++) {
        ptr[i] = data[i];
    }

    // Py_DECREF(buffer);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio__ring_buffer_free_count(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);
    int free_count = soundio_ring_buffer_free_count(buffer);

    // Py_DECREF(buffer);
    return Py_BuildValue("i", free_count);
}

static PyObject *
pysoundio__ring_buffer_advance_write_ptr(PyObject *self, PyObject *args)
{
    PyObject *data;
    int count;

    if (!PyArg_ParseTuple(args, "Oi", &data, &count))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);
    soundio_ring_buffer_advance_write_ptr(buffer, count);

    // Py_DECREF(buffer);
    Py_RETURN_NONE;
}



#if PY_MAJOR_VERSION >= 3
#define ERROR_INIT NULL
#else
#define ERROR_INIT /**/
#endif

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "_soundiox",
  NULL,
  -1,
  soundio_methods,
  NULL,
  NULL,
  NULL,
  NULL
};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit__soundiox(void)
#else
init_soundiox(void)
#endif
{
    PyObject* m;

    PyEval_InitThreads();

#if PY_MAJOR_VERSION >= 3
    m = PyModule_Create(&moduledef);
#else
    m = Py_InitModule("_soundiox", soundio_methods);
#endif

    // Errors
    PySoundIoError = PyErr_NewException("pysoundio.error", NULL, NULL);
    Py_INCREF(PySoundIoError);
    PyModule_AddObject(m, "error", PySoundIoError);

    // Constants
    PyModule_AddIntMacro(m, SOUNDIO_MAX_CHANNELS);

    // SoundIoError
    PyModule_AddIntMacro(m, SoundIoErrorNone);
    PyModule_AddIntMacro(m, SoundIoErrorNoMem);
    PyModule_AddIntMacro(m, SoundIoErrorInitAudioBackend);
    PyModule_AddIntMacro(m, SoundIoErrorSystemResources);
    PyModule_AddIntMacro(m, SoundIoErrorOpeningDevice);
    PyModule_AddIntMacro(m, SoundIoErrorNoSuchDevice);
    PyModule_AddIntMacro(m, SoundIoErrorInvalid);
    PyModule_AddIntMacro(m, SoundIoErrorBackendUnavailable);
    PyModule_AddIntMacro(m, SoundIoErrorStreaming);
    PyModule_AddIntMacro(m, SoundIoErrorIncompatibleDevice);
    PyModule_AddIntMacro(m, SoundIoErrorNoSuchClient);
    PyModule_AddIntMacro(m, SoundIoErrorIncompatibleBackend);
    PyModule_AddIntMacro(m, SoundIoErrorBackendDisconnected);
    PyModule_AddIntMacro(m, SoundIoErrorInterrupted);
    PyModule_AddIntMacro(m, SoundIoErrorUnderflow);
    PyModule_AddIntMacro(m, SoundIoErrorEncodingString);

    // SoundIoChannelId
    PyModule_AddIntMacro(m, SoundIoChannelIdInvalid);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontLeft);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontRight);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdLfe);
    PyModule_AddIntMacro(m, SoundIoChannelIdBackLeft);
    PyModule_AddIntMacro(m, SoundIoChannelIdBackRight);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontLeftCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontRightCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdBackCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdSideLeft);
    PyModule_AddIntMacro(m, SoundIoChannelIdSideRight);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopFrontLeft);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopFrontCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopFrontRight);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopBackLeft);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopBackCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopBackRight);
    PyModule_AddIntMacro(m, SoundIoChannelIdBackLeftCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdBackRightCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontLeftWide);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontRightWide);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontLeftHigh);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontCenterHigh);
    PyModule_AddIntMacro(m, SoundIoChannelIdFrontRightHigh);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopFrontLeftCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopFrontRightCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopSideLeft);
    PyModule_AddIntMacro(m, SoundIoChannelIdTopSideRight);
    PyModule_AddIntMacro(m, SoundIoChannelIdLeftLfe);
    PyModule_AddIntMacro(m, SoundIoChannelIdRightLfe);
    PyModule_AddIntMacro(m, SoundIoChannelIdLfe2);
    PyModule_AddIntMacro(m, SoundIoChannelIdBottomCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdBottomLeftCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdBottomRightCenter);
    PyModule_AddIntMacro(m, SoundIoChannelIdMsMid);
    PyModule_AddIntMacro(m, SoundIoChannelIdMsSide);
    PyModule_AddIntMacro(m, SoundIoChannelIdAmbisonicW);
    PyModule_AddIntMacro(m, SoundIoChannelIdAmbisonicX);
    PyModule_AddIntMacro(m, SoundIoChannelIdAmbisonicY);
    PyModule_AddIntMacro(m, SoundIoChannelIdAmbisonicZ);
    PyModule_AddIntMacro(m, SoundIoChannelIdXyX);
    PyModule_AddIntMacro(m, SoundIoChannelIdXyY);
    PyModule_AddIntMacro(m, SoundIoChannelIdHeadphonesLeft);
    PyModule_AddIntMacro(m, SoundIoChannelIdHeadphonesRight);
    PyModule_AddIntMacro(m, SoundIoChannelIdClickTrack);
    PyModule_AddIntMacro(m, SoundIoChannelIdForeignLanguage);
    PyModule_AddIntMacro(m, SoundIoChannelIdHearingImpaired);
    PyModule_AddIntMacro(m, SoundIoChannelIdNarration);
    PyModule_AddIntMacro(m, SoundIoChannelIdHaptic);
    PyModule_AddIntMacro(m, SoundIoChannelIdDialogCentricMix);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux0);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux1);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux2);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux3);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux4);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux5);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux6);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux7);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux8);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux9);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux10);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux11);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux12);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux13);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux14);
    PyModule_AddIntMacro(m, SoundIoChannelIdAux15);


    // SoundIoChannelLayoutId
    PyModule_AddIntMacro(m, SoundIoChannelLayoutIdMono);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutIdStereo);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId2Point1);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId3Point0);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId3Point0Back);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId3Point1);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId4Point0);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutIdQuad);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutIdQuadSide);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId4Point1);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId5Point0Back);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId5Point0Side);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId5Point1);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId5Point1Back);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId6Point0Side);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId6Point0Front);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutIdHexagonal);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId6Point1);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId6Point1Back);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId6Point1Front);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId7Point0);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId7Point0Front);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId7Point1);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId7Point1Wide);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutId7Point1WideBack);
    PyModule_AddIntMacro(m, SoundIoChannelLayoutIdOctagonal);


    // SoundIoBackend
    PyModule_AddIntMacro(m, SoundIoBackendNone);
    PyModule_AddIntMacro(m, SoundIoBackendJack);
    PyModule_AddIntMacro(m, SoundIoBackendPulseAudio);
    PyModule_AddIntMacro(m, SoundIoBackendAlsa);
    PyModule_AddIntMacro(m, SoundIoBackendCoreAudio);
    PyModule_AddIntMacro(m, SoundIoBackendWasapi);
    PyModule_AddIntMacro(m, SoundIoBackendDummy);


    // SoundIoDeviceAim
    PyModule_AddIntMacro(m, SoundIoDeviceAimInput);
    PyModule_AddIntMacro(m, SoundIoDeviceAimOutput);

    // SoundIoFormat
    PyModule_AddIntMacro(m, SoundIoFormatInvalid);
    PyModule_AddIntMacro(m, SoundIoFormatS8);
    PyModule_AddIntMacro(m, SoundIoFormatU8);
    PyModule_AddIntMacro(m, SoundIoFormatS16LE);
    PyModule_AddIntMacro(m, SoundIoFormatS16BE);
    PyModule_AddIntMacro(m, SoundIoFormatU16LE);
    PyModule_AddIntMacro(m, SoundIoFormatU16BE);
    PyModule_AddIntMacro(m, SoundIoFormatS24LE);
    PyModule_AddIntMacro(m, SoundIoFormatS24BE);
    PyModule_AddIntMacro(m, SoundIoFormatU24LE);
    PyModule_AddIntMacro(m, SoundIoFormatU24BE);
    PyModule_AddIntMacro(m, SoundIoFormatS32LE);
    PyModule_AddIntMacro(m, SoundIoFormatS32BE);
    PyModule_AddIntMacro(m, SoundIoFormatU32LE);
    PyModule_AddIntMacro(m, SoundIoFormatU32BE);
    PyModule_AddIntMacro(m, SoundIoFormatFloat32LE);
    PyModule_AddIntMacro(m, SoundIoFormatFloat32BE);
    PyModule_AddIntMacro(m, SoundIoFormatFloat64LE);
    PyModule_AddIntMacro(m, SoundIoFormatFloat64BE);


#if PY_MAJOR_VERSION >= 3
    return m;
#endif
}
