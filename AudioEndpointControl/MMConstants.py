# -*- coding: utf-8 -*-
# TODO: Missing module docstring (missing-docstring)

from __future__ import print_function, unicode_literals

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
    """ """  # Todo
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
PKEY_Device_FriendlyName = PROPERTYKEY(
    _GUID('{A45C254E-DF1C-4EFD-8020-67D146A850E0}'), 14)
PKEY_Device_DeviceDesc = PROPERTYKEY(
    _GUID('{A45C254E-DF1C-4EFD-8020-67D146A850E0}'), 2)
PKEY_DeviceInterface_FriendlyName = PROPERTYKEY(
    _GUID('{026E516E-B814-414B-83CD-856D6FEF4822}'), 2)
