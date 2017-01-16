# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import

from . import (
    COMObject as _COMObject,
    IMMNotificationClient,
    IAudioEndpointVolumeCallback
)
from . import DataFlowType, RoleType, Device_StateType
import sys
import traceback

from ctypes import POINTER as _POINTER, c_float as _c_float, cast as _cast


class cNotify(object):
    def __init__(self, pNotify):
        self.EventContext = pNotify.contents.guidEventContext
        self.Muted = bool(pNotify.contents.bMuted)
        self.MasterVolume = pNotify.contents.fMasterVolume
        self.Channels = pNotify.contents.nChannels
        self.ChannelVolumes = []
        pfChannelVolumes = _cast(
            pNotify.contents.afChannelVolumes, _POINTER(_c_float)
        )
        for channel in range(pNotify.contents.nChannels):
            self.ChannelVolumes.append(pfChannelVolumes[channel])


class CAudioEndpointVolumeCallback(_COMObject):
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def __init__(self, Callback, endpoint):
        self._Callback = Callback
        self._endpoint = endpoint
        _COMObject.__init__(self)

    def OnNotify(self, this, pNotify):
        try:
            self._Callback.OnNotify(cNotify(pNotify), self._endpoint)
        except:
            traceback.print_exc(file=sys.stdout)


class CMMNotificationClient(_COMObject):
    _com_interfaces_ = [IMMNotificationClient]

    def __init__(self, Callback, endpoints):
        self._AudioDevices = endpoints
        self._Callback = Callback
        _COMObject.__init__(self)

    def OnDeviceStateChanged(self, this, pwstrDeviceId, dwNewState):
        try:
            self._Callback.OnDeviceStateChanged(
                self._AudioDevices(pwstrDeviceId),
                Device_StateType(dwNewState)
            )
        except AttributeError:
            pass
        except:
            traceback.print_exc(file=sys.stdout)

    def OnDeviceRemoved(self, this, pwstrDeviceId):
        try:
            self._Callback.OnDeviceRemoved(self._AudioDevices(pwstrDeviceId))
        except AttributeError:
            pass
        except:
            traceback.print_exc(file=sys.stdout)

    def OnDeviceAdded(self, this, pwstrDeviceId):
        try:
            self._Callback.OnDeviceAdded(self._AudioDevices(pwstrDeviceId))
        except AttributeError:
            pass
        except:
            traceback.print_exc(file=sys.stdout)

    def OnDefaultDeviceChanged(self, this, flow, role, pwstrDeviceId):
        try:
            self._Callback.OnDefaultDeviceChanged(
                DataFlowType(flow),
                RoleType(role),
                self._AudioDevices(pwstrDeviceId)
            )
        except AttributeError:
            pass
        except:
            traceback.print_exc(file=sys.stdout)

    def OnPropertyValueChanged(self, this, pwstrDeviceId, key):
        try:
            self._Callback.OnPropertyValueChanged(
                self._AudioDevices(pwstrDeviceId),
                key
            )
        except AttributeError:
            pass
        except:
            traceback.print_exc(file=sys.stdout)
