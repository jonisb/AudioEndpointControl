# -*- coding: utf-8 -*-
# TODO: Missing module docstring (missing-docstring)

from __future__ import print_function, unicode_literals, absolute_import

from ctypes import POINTER as _POINTER
from functools import partial as _partial
from _ctypes import COMError
from win32api import FormatMessage

from comtypes import CoCreateInstance, CLSCTX_INPROC_SERVER, CLSCTX_ALL, GUID

from .MMConstants import (
    Render, Console, DEVICE_STATE_ACTIVE, PKEY_Device_FriendlyName, STGM_READ
)
try:
    # Try to import local .MMDeviceAPILib for Python 2.6 compability
    from .MMDeviceAPILib import (
        MMDeviceEnumerator as _MMDeviceEnumerator,
        IMMDeviceEnumerator as _IMMDeviceEnumerator,
        IMMNotificationClient
    )
except ImportError:
    # Use comtypes to generate MMDeviceAPILib (Python 2.7+))
    from comtypes.client import GetModule
    GetModule("mmdeviceapi.tlb")
    from comtypes.gen.MMDeviceAPILib import (
        MMDeviceEnumerator as _MMDeviceEnumerator,
        IMMDeviceEnumerator as _IMMDeviceEnumerator,
        IMMNotificationClient
    )
from .Notifications import CAudioEndpointVolumeCallback, CMMNotificationClient
from .EndpointvolumeAPI import IAudioEndpointVolume as _IAudioEndpointVolume, IID_IAudioEndpointVolume
from .PolicyConfigAPI import CLSID_CPolicyConfigVistaClient, IPolicyConfigVista

__version__ = '0.1a2'

_CLSID_MMDeviceEnumerator = _MMDeviceEnumerator._reg_clsid_


def _GetValue(value):
    # Need to do this in a function as comtypes seems to
    # have a problem if it's in a class.

    # Types for vt defined here:
    # https://msdn.microsoft.com/en-us/library/windows/desktop/aa380072%28v=vs.85%29.aspx
    if value.vt == 0:
        return None
    elif value.vt == 31:
        return value.__MIDL____MIDL_itf_mmdeviceapi_0003_00850001.pwszVal
    return value.__MIDL____MIDL_itf_mmdeviceapi_0003_00850001.cVal


class AudioVolume(object):
    """Wrapper for volume related methods."""
    def __init__(self, endpoint, IAudioEndpointVolume, EventContext=None):
        self.callback = None
        self.endpoint = endpoint
        self.IAudioEndpointVolume = IAudioEndpointVolume
        self.EventContext = EventContext

    def GetChannelCount(self):
        """Gets a count of the channels in the audio stream."""
        return self.IAudioEndpointVolume.GetChannelCount()

    def __len__(self):
        return self.GetChannelCount()

    def Get(self, nChannel=0, Scalar=True):
        """
        When Scalar=True: Gets the master volume level, expressed as
        (default)         a normalized, audio-tapered value.

        When Scalar=False: Gets the master volume level of the
                           audio stream, in decibels.

        When Scalar=True: Gets the normalized, audio-tapered volume
        (default)         level of the specified channel of the audio stream.

        When Scalar=False: Gets the volume level, in decibels, of the
                           specified channel in the audio stream.
        """
        if nChannel == 0:
            if Scalar:
                return self.IAudioEndpointVolume.GetMasterVolumeLevelScalar()
            else:
                return self.IAudioEndpointVolume.GetMasterVolumeLevel()

        if Scalar:
            return self.IAudioEndpointVolume.GetChannelVolumeLevelScalar(
                nChannel
            )

        return self.IAudioEndpointVolume.GetChannelVolumeLevel(nChannel)

    def Set(self, fLevelDB, nChannel=0, Scalar=True):
        """
        When Scalar=True: Sets the master volume level, expressed as
        (default)         a normalized, audio-tapered value.

        When Scalar=False: Sets the master volume level of the
                           audio stream, in decibels.

        When Scalar=True: Sets the normalized, audio-tapered volume level of
        (default)         the specified channel in the audio stream.

        When Scalar=False: Sets the volume level, in decibels, of the
                           specified channel of the audio stream.

        """
        if type(fLevelDB) == bool:
            return self.Mute(fLevelDB)

        if nChannel == 0:
            if Scalar:
                return self.IAudioEndpointVolume.SetMasterVolumeLevelScalar(
                    fLevelDB, self.EventContext)
            else:
                return self.IAudioEndpointVolume.SetMasterVolumeLevel(
                    fLevelDB, self.EventContext)

        if Scalar:
            return self.IAudioEndpointVolume.SetChannelVolumeLevelScalar(
                nChannel-1, fLevelDB, self.EventContext)

        return self.IAudioEndpointVolume.SetChannelVolumeLevel(
            nChannel-1, fLevelDB, self.EventContext)

    def GetRange(self):
        """Gets the volume range of the audio stream, in decibels."""
        return self.IAudioEndpointVolume.GetVolumeRange()

    def StepDown(self):
        """Decreases the volume level by one step."""
        return self.IAudioEndpointVolume.VolumeStepDown(self.EventContext)

    def StepUp(self):
        """Increases the volume level by one step."""
        return self.IAudioEndpointVolume.VolumeStepUp(self.EventContext)

    def GetStepInfo(self):
        """Gets information about the current step in the volume range."""
        return self.IAudioEndpointVolume.GetVolumeStepInfo()

    def QueryHardwareSupport(self):
        """
        Queries the audio endpoint device for its hardware-supported functions.
        """
        return self.IAudioEndpointVolume.QueryHardwareSupport()

    def RegisterControlChangeNotify(self, callback):
        """Registers a client's notification callback interface."""
        self.callback = CAudioEndpointVolumeCallback(callback, self.endpoint)
        hr = self.IAudioEndpointVolume.RegisterControlChangeNotify(
            self.callback
        )
        if hr:
            print('RegisterControlChangeNotify', hr, FormatMessage(hr))

    def UnregisterControlChangeNotify(self):
        """
        Deletes the registration of a client's notification callback interface.
        """
        if self.callback is not None:
            hr = self.IAudioEndpointVolume.UnregisterControlChangeNotify(
                self.callback
            )
            if hr:
                print('UnregisterControlChangeNotify', hr, FormatMessage(hr))
            self.callback = None

    def __add__(self, other=1):
        for _ in range(other):
            self.StepUp()

    def __sub__(self, other=1):
        for _ in range(other):
            self.StepDown()

    def __int__(self):
        return self[0]

    def __str__(self):
        return 'Volume: {0}'.format(self[0])

    @property
    def Mute(self):  # TODO: Missing method docstring (missing-docstring)
        return bool(self.IAudioEndpointVolume.GetMute())

    @Mute.setter
    def Mute(self, bMute):
        return self.IAudioEndpointVolume.SetMute(bMute, self.EventContext)

    def __eq__(self, other):
        """Tests if two enpoint devices are the same."""
        return self.endpoint.getId() == other.endpoint.getId()

    def __ne__(self, other):
        """Tests if two enpoint devices are not the same."""
        return self.endpoint.getId() != other.endpoint.getId()

    __getitem__ = Get
    __setitem__ = _partial(Set, Scalar=True)
    __pos__ = __add__
    __neg__ = __add__


# FIX: Too many instance attributes (8/7) (too-many-instance-attributes)
class AudioEndpoint(object):
    """Wrapper for a single COM endpoint."""
    def __init__(
            self,
            endpoint,
            endpoints,
            PKEY_Device=PKEY_Device_FriendlyName,
            EventContext=None
    ):
        """Initializes an endpoint object."""
        self.endpoint = endpoint
        self.endpoints = endpoints
        self.PKEY_Device = PKEY_Device
        self.EventContext = EventContext
        self.IAudioEndpointVolume = _POINTER(_IAudioEndpointVolume)(
            endpoint.Activate(
                IID_IAudioEndpointVolume, CLSCTX_INPROC_SERVER, None
            )
        )
        self._AudioVolume = AudioVolume(
            self,
            self.IAudioEndpointVolume,
            self.EventContext
        )
        self.RegisterControlChangeNotify = self._AudioVolume.\
            RegisterControlChangeNotify
        self.UnregisterControlChangeNotify = self._AudioVolume.\
            UnregisterControlChangeNotify

    @property
    def volume(self):  # TODO: Missing method docstring (missing-docstring)
        return self._AudioVolume

    @volume.setter
    # FIX: Using type() instead of isinstance() for a typecheck.
    def volume(self, fLevelDB):
        if type(fLevelDB) == bool:
            return self._AudioVolume.SetMute(fLevelDB)
            # FIX: Instance of 'AudioVolume' has no 'SetMute' member

        return self._AudioVolume.Set(fLevelDB)

    def getName(self):
        """Return an endpoint devices FriendlyName."""
        pStore = self.endpoint.OpenPropertyStore(STGM_READ)
        return _GetValue(pStore.GetValue(self.PKEY_Device))

    def getId(self):
        """Gets a string that identifies the device."""
        return self.endpoint.GetId()

    def getState(self):
        """Gets the current state of the device."""
        return self.endpoint.GetState()

    def isDefault(self, role=Console, dataFlow=Render):
        """Return if endpoint device is default or not."""
        return self == self.endpoints.GetDefault(role, dataFlow)

    def GetVolumeRange(self):
        """Gets the volume range of the audio stream, in decibels."""
        return self.IAudioEndpointVolume.GetVolumeRange()

    def GetMasterVolumeLevel(self, Scalar=True):
        """
        When Scalar=True: Gets the master volume level, expressed as
        (default)         a normalized, audio-tapered value.

        When Scalar=False: Gets the master volume level of the
                           audio stream, in decibels.
        """
        if Scalar:
            return self.IAudioEndpointVolume.GetMasterVolumeLevelScalar()

        return self.IAudioEndpointVolume.GetMasterVolumeLevel()

    def SetMasterVolumeLevel(self, fLevelDB, Scalar=True):
        """
        When Scalar=True: Sets the master volume level, expressed as
        (default)         a normalized, audio-tapered value.

        When Scalar=False: Sets the master volume level of the
                           audio stream, in decibels.
        """
        if Scalar:
            return self.IAudioEndpointVolume.SetMasterVolumeLevelScalar(
                fLevelDB, self.EventContext
            )

        return self.IAudioEndpointVolume.SetMasterVolumeLevel(
            fLevelDB, self.EventContext
        )

    def GetChannelVolumeLevel(self, nChannel, Scalar=True):
        """
        When Scalar=True: Gets the normalized, audio-tapered volume level
        (default)         of the specified channel of the audio stream.

        When Scalar=False: Gets the volume level, in decibels, of the
                           specified channel in the audio stream.
        """
        if Scalar:
            return self.IAudioEndpointVolume.GetChannelVolumeLevelScalar(
                nChannel
            )

        return self.IAudioEndpointVolume.GetChannelVolumeLevel(nChannel)

    def SetChannelVolumeLevel(self, nChannel, fLevelDB, Scalar=True):
        """
        When Scalar=True: Sets the normalized, audio-tapered volume level
        (default)         of the specified channel in the audio stream.

        When Scalar=False: Sets the volume level, in decibels, of the
                           specified channel of the audio stream.
        """
        if Scalar:
            return self.IAudioEndpointVolume.SetChannelVolumeLevelScalar(
                nChannel, fLevelDB, self.EventContext
            )

        return self.IAudioEndpointVolume.SetChannelVolumeLevel(
            nChannel, fLevelDB, self.EventContext
        )

    def GetMute(self):
        """Gets the muting state of the audio stream."""
        return self._AudioVolume.Mute()
        # FIX: self._AudioVolume.Mute is not callable (not-callable)

    def SetMute(self, bMute):
        """Sets the muting state of the audio stream."""
        return self.IAudioEndpointVolume.SetMute(bMute, self.EventContext)

    def GetChannelCount(self):
        """Gets a count of the channels in the audio stream."""
        return len(self._AudioVolume)

    def VolumeStepDown(self):
        """Decreases the volume level by one step."""
        return self.IAudioEndpointVolume.VolumeStepDown(self.EventContext)

    def VolumeStepUp(self):
        """Increases the volume level by one step."""
        return self.IAudioEndpointVolume.VolumeStepUp(self.EventContext)

    def GetVolumeStepInfo(self):
        """Gets information about the current step in the volume range."""
        return self.IAudioEndpointVolume.GetVolumeStepInfo()

    def __eq__(self, other):
        """Tests if two enpoint devices are the same."""
        return self.getId() == other.getId()

    def __ne__(self, other):
        """Tests if two enpoint devices are not the same."""
        return self.getId() != other.getId()

    __str__ = getName


# TODO: Missing class docstring (missing-docstring)
class AudioEndpoints(object):
    def __init__(
            self,
            DEVICE_STATE=DEVICE_STATE_ACTIVE,
            PKEY_Device=PKEY_Device_FriendlyName,
            EventContext=GUID.create_new()
    ):
        self.DEVICE_STATE = DEVICE_STATE
        self.PKEY_Device = PKEY_Device
        self.EventContext = EventContext
        self.pDevEnum = CoCreateInstance(
            _CLSID_MMDeviceEnumerator,
            _IMMDeviceEnumerator,
            CLSCTX_INPROC_SERVER
        )
        self.callback = None
        self.pPolicyConfig = None

    # TODO: Missing class docstring (missing-docstring)
    def GetDefault(self, role=Console, dataFlow=Render):
        return AudioEndpoint(
            self.pDevEnum.GetDefaultAudioEndpoint(dataFlow, role),
            self,
            self.PKEY_Device,
            self.EventContext
        )

    # TODO: Missing class docstring (missing-docstring)
    def SetDefault(self, endpoint, role=Console):
        OldDefault = self.GetDefault(role)

        if not self.pPolicyConfig:
            self.pPolicyConfig = CoCreateInstance(
                CLSID_CPolicyConfigVistaClient, IPolicyConfigVista, CLSCTX_ALL)

        hr = self.pPolicyConfig.SetDefaultEndpoint(endpoint.getId(), role)
        if hr:
            print('SetDefaultEndpoint', FormatMessage(hr))
        return OldDefault

    # TODO: Missing class docstring (missing-docstring)
    def RegisterCallback(self, callback):
        self.callback = CMMNotificationClient(callback, self)
        hr = self.pDevEnum.RegisterEndpointNotificationCallback(self.callback)
        if hr:
            print(
                'RegisterEndpointNotificationCallback',
                hr,
                FormatMessage(hr)
            )

    # TODO: Missing class docstring (missing-docstring)
    def UnregisterCallback(self):
        if self.callback is not None:
            hr = self.pDevEnum.UnregisterEndpointNotificationCallback(
                self.callback
            )
            if hr:
                print(
                    'UnregisterEndpointNotificationCallback',
                    hr,
                    FormatMessage(hr)
                )
            self.callback = None

    def __call__(self, ID):
        try:
            return AudioEndpoint(
                self.pDevEnum.GetDevice(ID),
                self,
                self.PKEY_Device,
                self.EventContext
            )
        except COMError:
            for endpoint in self:
                if endpoint.getName() == ID:
                    return endpoint

    def __str__(self):
        return str([str(endpoint) for endpoint in self])

    # TODO: Missing class docstring (missing-docstring)
    def ChangeFilter(self, DEVICE_STATE=None, PKEY_Device=None):
        if DEVICE_STATE is not None:
            self.DEVICE_STATE = DEVICE_STATE
        if PKEY_Device is not None:
            self.PKEY_Device = PKEY_Device

    def __iter__(self, dataFlow=Render):
        pEndpoints = self.pDevEnum.EnumAudioEndpoints(
            dataFlow, self.DEVICE_STATE
        )
        for i in range(pEndpoints.GetCount()):
            yield AudioEndpoint(
                pEndpoints.Item(i),
                self,
                self.PKEY_Device,
                self.EventContext
            )

    # FIX: __len__ does not return non-negative integer
    def __len__(self):
        return int(
            self.pDevEnum.EnumAudioEndpoints(
                Render, self.DEVICE_STATE
            ).GetCount()
        )
