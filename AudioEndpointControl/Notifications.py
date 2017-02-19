# -*- coding: utf-8 -*-
"""Notifications wrapper classes"""

from __future__ import print_function, unicode_literals, absolute_import

import sys
import traceback
from ctypes import POINTER as _POINTER, c_float as _c_float, cast as _cast

from comtypes import COMObject as _COMObject

from .MMConstants import DataFlowType, RoleType, Device_StateType
from .AudioEndpoints import IMMNotificationClient
from .EndpointvolumeAPI import IAudioEndpointVolumeCallback


class cNotify(object):  # TODO: Missing class docstring (missing-docstring)
    # FIX: Too few public methods (0/2) (too-few-public-methods)
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


# TODO: Missing class docstring (missing-docstring)
class CAudioEndpointVolumeCallback(_COMObject):
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def __init__(self, Callback, endpoint):
        if Callback is None:
            raise Exception("Callback object required, got:", repr(Callback))
        self._Callback = Callback
        self._endpoint = endpoint
        _COMObject.__init__(self)

    def OnNotify(self, this, pNotify):  # TODO: Missing method docstring
        try:
            self._Callback.OnNotify(cNotify(pNotify), self._endpoint)
        except AttributeError:  # TODO: Log warning "OnNotify" method missing
            pass


class CMMNotificationClient(_COMObject):  # TODO: Missing class docstring
    _com_interfaces_ = [IMMNotificationClient]

    def __init__(self, Callback, endpoints):
        if Callback is None:
            raise Exception("Callback object required, got:", repr(Callback))
        self._AudioDevices = endpoints
        self._Callback = Callback
        _COMObject.__init__(self)

    def OnDeviceStateChanged(self, this, pwstrDeviceId, dwNewState):
        # TODO: Missing method docstring (missing-docstring)
        try:
            self._Callback.OnDeviceStateChanged(
                self._AudioDevices(pwstrDeviceId),
                Device_StateType(dwNewState)
            )
        except AttributeError:
            pass
        except:  # FIX: No exception type(s) specified (bare-except)
            traceback.print_exc(file=sys.stdout)

    def OnDeviceRemoved(self, this, pwstrDeviceId):
        # TODO: Missing method docstring (missing-docstring)
        try:
            self._Callback.OnDeviceRemoved(self._AudioDevices(pwstrDeviceId))
        except AttributeError:
            pass
        except:  # FIX: No exception type(s) specified (bare-except)
            traceback.print_exc(file=sys.stdout)

    def OnDeviceAdded(self, this, pwstrDeviceId):
        # TODO: Missing method docstring (missing-docstring)
        try:
            self._Callback.OnDeviceAdded(self._AudioDevices(pwstrDeviceId))
        except AttributeError:
            pass
        except:  # FIX: No exception type(s) specified (bare-except)
            traceback.print_exc(file=sys.stdout)

    def OnDefaultDeviceChanged(self, this, flow, role, pwstrDeviceId):
        # TODO: Missing method docstring (missing-docstring)
        try:
            self._Callback.OnDefaultDeviceChanged(
                DataFlowType(flow),
                RoleType(role),
                self._AudioDevices(pwstrDeviceId)
            )
        except AttributeError:
            pass
        except:  # FIX: No exception type(s) specified (bare-except)
            traceback.print_exc(file=sys.stdout)

    def OnPropertyValueChanged(self, this, pwstrDeviceId, key):
        # TODO: Missing method docstring (missing-docstring)
        try:
            self._Callback.OnPropertyValueChanged(
                self._AudioDevices(pwstrDeviceId),
                key
            )
        except AttributeError:
            pass
        except:  # FIX: No exception type(s) specified (bare-except)
            traceback.print_exc(file=sys.stdout)
