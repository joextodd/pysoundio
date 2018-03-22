#include <Python.h>
#include <soundio/soundio.h>

#if PY_MAJOR_VERSION >= 3
#define ERROR_INIT NULL
#else
#define ERROR_INIT /**/
#endif

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "_soundio",
  NULL,
  -1,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL
};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit__soundio(void)
#else
init_soundio(void)
#endif
{
  PyObject* m;

  PyEval_InitThreads();

#if PY_MAJOR_VERSION >= 3
  m = PyModule_Create(&moduledef);
#else
  m = Py_InitModule("_soundio", NULL);
#endif

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