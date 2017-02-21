# -*- coding: utf-8 -*-
"""Defines constants and types needed"""

from __future__ import print_function, unicode_literals

__all__ = (b"Render", b"Capture", b"All", b"Console",
           b"Multimedia", b"Communications", b"DEVICE_STATE_ACTIVE",
           b"DEVICE_STATE_DISABLED", b"DEVICE_STATE_NOTPRESENT",
           b"DEVICE_STATE_UNPLUGGED", b"DEVICE_STATEMASK_ALL",
           b"Device_FriendlyName", b"Device_DeviceDesc",
           b"DeviceInterface_FriendlyName")

from comtypes import GUID as _GUID

try:
    from MMDeviceAPILib import (
        _tagpropertykey,
        eRender,
        eCapture,
        eAll,
        EDataFlow_enum_count,
        eConsole,
        eMultimedia,
        eCommunications,
        ERole_enum_count
    )
except ImportError:
    from comtypes.client import GetModule
    GetModule("mmdeviceapi.tlb")
    from comtypes.gen.MMDeviceAPILib import (
        _tagpropertykey,
        eRender,
        eCapture,
        eAll,
        EDataFlow_enum_count,
        eConsole,
        eMultimedia,
        eCommunications,
        ERole_enum_count
    )

PROPERTYKEY = _tagpropertykey


class _ValueTypeClass(object):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._valueMap[self._value]

    def __int__(self):
        return self._value


def _CreateValueType(Name, ValueMap):
    """ """  # TODO
    ValueType = type(str(Name), (_ValueTypeClass,), {'_valueMap': ValueMap})

    for _value, _name in ValueMap.iteritems():
        globals()[_name] = ValueType(_value)

    return ValueType


# DataFlow enumeration: The DataFlowType class defines constants that indicate
# the direction in which audio data flows between an audio endpoint device and
# an application.
DataFlowType = _CreateValueType(
    'DataFlowType',
    {
        eRender: 'Render',
        eCapture: 'Capture',
        eAll: 'All',
        EDataFlow_enum_count: 'DataFlow_enum_count'
    }
)

# Role enumeration: The RoleType class defines constants that indicate the role
# that the system has assigned to an audio endpoint device.
RoleType = _CreateValueType(
    'RoleType',
    {
        eConsole: 'Console',
        eMultimedia: 'Multimedia',
        eCommunications: 'Communications',
        ERole_enum_count: 'Role_enum_count'
    }
)

# DEVICE_STATE_XXX Constants: The DEVICE_STATE_XXX constants indicate the
# current state of an audio endpoint device.
Device_StateType = _CreateValueType(
    'Device_StateType',
    {
        0x00000001: 'DEVICE_STATE_ACTIVE',
        0x00000002: 'DEVICE_STATE_DISABLED',
        0x00000004: 'DEVICE_STATE_NOTPRESENT',
        0x00000008: 'DEVICE_STATE_UNPLUGGED',
        0x0000000F: 'DEVICE_STATEMASK_ALL'
    }
)

# The STGM constants are flags that indicate conditions for creating and
# deleting the object and access modes for the object. The STGM constants
# are included in the IStorage, IStream, and IPropertySetStorage interfaces
# and in the StgCreateDocfile, StgCreateStorageEx,
# StgCreateDocfileOnILockBytes, StgOpenStorage, and StgOpenStorageEx functions.
# The storage-access mode. This parameter specifies whether to open the
# property store in read mode, write mode, or read/write mode. Set this
# parameter to one of the following STGM constants:
STGM_READ = 0x00000000
STGM_WRITE = 0x00000001
STGM_READWRITE = 0x00000002

# Each PKEY_Xxx property identifier in the following list is a constant of
# type PROPERTYKEY that is defined in header file
# Functiondiscoverykeys_devpkey.h. All audio endpoint devices have these
# three device properties.
Device_FriendlyName = PROPERTYKEY(
    _GUID('{A45C254E-DF1C-4EFD-8020-67D146A850E0}'), 14)
Device_DeviceDesc = PROPERTYKEY(
    _GUID('{A45C254E-DF1C-4EFD-8020-67D146A850E0}'), 2)
DeviceInterface_FriendlyName = PROPERTYKEY(
    _GUID('{026E516E-B814-414B-83CD-856D6FEF4822}'), 2)


# ENDPOINT_HARDWARE_SUPPORT_XXX Constants
#
# The ENDPOINT_HARDWARE_SUPPORT_XXX constants are hardware support flags for an
# audio endpoint device.
#
# Remarks
#
# The IAudioEndpointVolume::QueryHardwareSupport and
# IAudioMeterInformation::QueryHardwareSupport methods use the
# ENDPOINT_HARDWARE_SUPPORT_XXX constants.
#
# A hardware support mask indicates which functions an audio endpoint device
# implements in hardware. The mask can be either 0 or the bitwise-OR
# combination of one or more ENDPOINT_HARDWARE_SUPPORT_XXX constants. If a bit
# that corresponds to a particular ENDPOINT_HARDWARE_SUPPORT_XXX constant is
# set in the mask, then the meaning is that the function represented by that
# constant is implemented in hardware by the device.

# The audio endpoint device supports a hardware volume control.
ENDPOINT_HARDWARE_SUPPORT_VOLUME = 0x00000001
# The audio endpoint device supports a hardware mute control.
ENDPOINT_HARDWARE_SUPPORT_MUTE = 0x00000002
# The audio endpoint device supports a hardware peak meter.
ENDPOINT_HARDWARE_SUPPORT_METER = 0x00000004
