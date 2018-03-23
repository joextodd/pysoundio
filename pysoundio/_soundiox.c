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
        pysoundio_create, METH_VARARGS,
        "create soundio struct"
    },
    {
        "destroy",
        pysoundio_destroy, METH_VARARGS,
        "destroy soundio struct"
    },
    {
        "connect",
        pysoundio_connect, METH_VARARGS,
        "connect to the default backend"
    },
    {
        "flush",
        pysoundio_flush, METH_VARARGS,
        "atomically update information for all connected devices"
    },
    {
        "strerror",
        pysoundio_strerror, METH_VARARGS,
        "get a string representation of a SoundIoError."
    },
    {
        "get_output_device_count",
        pysoundio_get_output_device_count, METH_VARARGS,
        "get output device count"
    },
    {
        "get_input_device_count",
        pysoundio_get_input_device_count, METH_VARARGS,
        "get input device count"
    },
    {
        "default_input_device_index",
        pysoundio_default_input_device_index, METH_VARARGS,
        "get default input device index"
    },
    {
        "default_output_device_index",
        pysoundio_default_output_device_index, METH_VARARGS,
        "get default output device index"
    },
    {
        "get_input_device",
        pysoundio_get_input_device, METH_VARARGS,
        "get input device"
    },
    {
        "get_output_device",
        pysoundio_get_output_device, METH_VARARGS,
        "get output device"
    },
    {
        "device_unref",
        pysoundio_device_unref, METH_VARARGS,
        "clean up device"
    },
    {
        "device_supports_sample_rate",
        pysoundio_device_supports_sample_rate, METH_VARARGS,
        "check is sample rate is supported by device"
    },
    {
        "device_sort_channel_layouts",
        pysoundio_device_sort_channel_layouts, METH_VARARGS,
        "sorts channel layouts by channel count, descending."
    },
    {
        "channel_layout_get_default",
        pysoundio_channel_layout_get_default, METH_VARARGS,
        "get the default builtin channel layout"
    },
    {
        "instream_create",
        pysoundio_instream_create, METH_VARARGS,
        "allocates memory for input stream"
    },
    {
        "instream_destroy",
        pysoundio_instream_destroy, METH_VARARGS,
        "cleans up input stream"
    },
    {
        "instream_open",
        pysoundio_instream_open, METH_VARARGS,
        "open input stream"
    },
    {
        "instream_start",
        pysoundio_instream_start, METH_VARARGS,
        "start input stream"
    },
    {
        "ring_buffer_create",
        pysoundio_ring_buffer_create, METH_VARARGS,
        "create ring buffer"
    },
    {
        "ring_buffer_fill_count",
        pysoundio_ring_buffer_fill_count, METH_VARARGS,
        "how many bytes of the buffer is used, ready for reading"
    },
    {
        "ring_buffer_read_ptr",
        pysoundio_ring_buffer_read_ptr, METH_VARARGS,
        "get pointer to read from buffer"
    },
    {
        "ring_buffer_advance_read_ptr",
        pysoundio_ring_buffer_advance_read_ptr, METH_VARARGS,
        "advance read pointer"
    },
    {
        "ring_buffer_write_ptr",
        pysoundio_ring_buffer_write_ptr, METH_VARARGS,
        "get pointer to write to buffer"
    },
    {
        "ring_buffer_free_count",
        pysoundio_ring_buffer_free_count, METH_VARARGS,
        "how many bytes of the buffer is free, ready for writing"
    },
    {
        "soundio_ring_buffer_advance_write_ptr",
        pysoundio_ring_buffer_advance_write_ptr, METH_VARARGS,
        "advance write pointer"
    },


    {NULL, NULL, 0, NULL}
};

static PyObject *PySoundIoError;
struct RecordContext {
    struct SoundIoRingBuffer *ring_buffer;
};
struct RecordContext rc;

static int min_int(int a, int b) {
    return (a < b) ? a : b;
}


/*************************************************************
 * Initialisation
 *************************************************************/

static PyObject *
pysoundio_create(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    struct SoundIo *soundio = soundio_create();
    if (!soundio) {
        PyErr_SetString(PySoundIoError, "Out of memory");
        return NULL;
    }

    return PyLong_FromVoidPtr(soundio);
}

static PyObject *
pysoundio_destroy(PyObject *self, PyObject *args)
{
    PyObject *data;
    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    soundio_destroy(soundio);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio_connect(PyObject *self, PyObject *args)
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
    return Py_BuildValue("i", err);
}

static PyObject *
pysoundio_flush(PyObject *self, PyObject *args)
{
    PyObject *data;
    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    soundio_flush_events(soundio);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio_strerror(PyObject *self, PyObject *args)
{
    int error;

    if (!PyArg_ParseTuple(args, "i", &error))
        return NULL;

    const char *message = soundio_strerror(error);
    return Py_BuildValue("s", message);
}


/*************************************************************
 * Device API
 *************************************************************/

static PyObject *
pysoundio_get_output_device_count(PyObject *self, PyObject *args)
{
    PyObject *data;
    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    int output_count = soundio_output_device_count(soundio);
    return Py_BuildValue("i", output_count);
}

static PyObject *
pysoundio_get_input_device_count(PyObject *self, PyObject *args)
{
    PyObject *data;
    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    int input_count = soundio_input_device_count(soundio);
    return Py_BuildValue("i", input_count);
}

static PyObject *
pysoundio_default_input_device_index(PyObject *self, PyObject *args)
{
    PyObject *data;
    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    int input_index = soundio_default_input_device_index(soundio);
    return Py_BuildValue("i", input_index);
}

static PyObject *
pysoundio_default_output_device_index(PyObject *self, PyObject *args)
{
    PyObject *data;
    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    int output_index = soundio_default_output_device_index(soundio);
    return Py_BuildValue("i", output_index);
}

static PyObject *
pysoundio_get_input_device(PyObject *self, PyObject *args)
{
    PyObject *data;
    int device_index;

    if (!PyArg_ParseTuple(args, "Oi", &data, &device_index))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    struct SoundIoDevice *input_device = soundio_get_input_device(soundio, device_index);
    if (input_device->probe_error) {
        PyErr_SetString(PySoundIoError, "Unable to probe device: \n");
            // soundio_strerror(input_device->probe_error));
        return NULL;
    }

    return PyLong_FromVoidPtr(input_device);
}

static PyObject *
pysoundio_get_output_device(PyObject *self, PyObject *args)
{
    PyObject *data;
    int device_index;

    if (!PyArg_ParseTuple(args, "Oi", &data, &device_index))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    struct SoundIoDevice *output_device = soundio_get_output_device(soundio, device_index);
    if (output_device->probe_error) {
        PyErr_SetString(PySoundIoError, "Unable to probe device: \n");
            // soundio_strerror(output_device->probe_error));
        return NULL;
    }

    return PyLong_FromVoidPtr(output_device);
}

static PyObject *
pysoundio_device_unref(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoDevice *device = PyLong_AsVoidPtr(data);

    soundio_device_unref(device);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio_device_supports_sample_rate(PyObject *self, PyObject *args)
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
pysoundio_device_sort_channel_layouts(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoDevice *device = PyLong_AsVoidPtr(data);

    soundio_device_sort_channel_layouts(device);
    Py_RETURN_NONE;
}


/*************************************************************
 * Input Stream API
 *************************************************************/

static PyObject *
pysoundio_channel_layout_get_default(PyObject *self, PyObject *args)
{
    int channel_count;

    if (!PyArg_ParseTuple(args, "i", &channel_count))
        return NULL;

    const struct SoundIoChannelLayout *layout = soundio_channel_layout_get_default(channel_count);
    return PyLong_FromVoidPtr((void *)layout);
}

static void
read_callback(struct SoundIoInStream *instream, int frame_count_min, int frame_count_max)
{
    struct RecordContext *rc = instream->userdata;
    struct SoundIoChannelArea *areas;
    int err;

    char *write_ptr = soundio_ring_buffer_write_ptr(rc->ring_buffer);
    int free_bytes = soundio_ring_buffer_free_count(rc->ring_buffer);
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
            // fprintf(stderr, "begin read error: %s", soundio_strerror(err));
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
            exit(1);
        }
        frames_left -= frame_count;
        if (frames_left <= 0)
            break;
    }

}

static void overflow_callback(struct SoundIoInStream *instream) {
}

static PyObject *
pysoundio_instream_create(PyObject *self, PyObject *args)
{
    PyObject *data;
    int sample_rate;
    int format;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoDevice *device = PyLong_AsVoidPtr(data);

    // TODO: Remove from here once fixed
    soundio_device_sort_channel_layouts(device);
    struct SoundIoInStream *instream = soundio_instream_create(device);

    instream->sample_rate = 44100;
    instream->format = 15;
    instream->read_callback = read_callback;
    instream->overflow_callback = overflow_callback;
    // instream->userdata = &rc;

    return PyLong_FromVoidPtr(instream);
}

static PyObject *
pysoundio_instream_destroy(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoInStream *instream = PyLong_AsVoidPtr(data);

    soundio_instream_destroy(instream);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio_instream_open(PyObject *self, PyObject *args)
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
pysoundio_instream_start(PyObject *self, PyObject *args)
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
 * Ring Buffer API
 *************************************************************/

static PyObject *
pysoundio_ring_buffer_create(PyObject *self, PyObject *args)
{
    PyObject *data;
    int capacity;

    if (!PyArg_ParseTuple(args, "Oi", &data, &capacity))
        return NULL;

    struct SoundIo *soundio = PyLong_AsVoidPtr(data);

    struct SoundIoRingBuffer *buffer = soundio_ring_buffer_create(soundio, capacity);
    rc.ring_buffer = buffer;
    if (!buffer) {
        PyErr_SetString(PySoundIoError, "Out of memory");
        return NULL;
    }

    return PyLong_FromVoidPtr(buffer);
}

static PyObject *
pysoundio_ring_buffer_fill_count(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);

    int err = soundio_ring_buffer_fill_count(buffer);
    return Py_BuildValue("i", err);
}

static PyObject *
pysoundio_ring_buffer_read_ptr(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);

    char *ptr = soundio_ring_buffer_read_ptr(buffer);
    return Py_BuildValue("z", ptr);
}

static PyObject *
pysoundio_ring_buffer_advance_read_ptr(PyObject *self, PyObject *args)
{
    PyObject *data;
    int count;

    if (!PyArg_ParseTuple(args, "Oi", &data, &count))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);

    soundio_ring_buffer_advance_read_ptr(buffer, count);
    Py_RETURN_NONE;
}

static PyObject *
pysoundio_ring_buffer_write_ptr(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);

    char *ptr = soundio_ring_buffer_write_ptr(buffer);
    return Py_BuildValue("z", ptr);
}

static PyObject *
pysoundio_ring_buffer_free_count(PyObject *self, PyObject *args)
{
    PyObject *data;

    if (!PyArg_ParseTuple(args, "O", &data))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);

    int free_count = soundio_ring_buffer_free_count(buffer);
    return Py_BuildValue("i", free_count);
}

static PyObject *
pysoundio_ring_buffer_advance_write_ptr(PyObject *self, PyObject *args)
{
    PyObject *data;
    int count;

    if (!PyArg_ParseTuple(args, "Oi", &data, &count))
        return NULL;

    struct SoundIoRingBuffer *buffer = PyLong_AsVoidPtr(data);

    soundio_ring_buffer_advance_write_ptr(buffer, count);
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
