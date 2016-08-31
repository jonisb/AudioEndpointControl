from __future__ import print_function, unicode_literals, absolute_import
#from ctypes import POINTER
#from ctypes.wintypes import DWORD, BOOL
#from comtypes import *
#from comtypes.gen.MMDeviceAPILib import *
from ctypes import POINTER as _POINTER, HRESULT as _HRESULT, c_float as _c_float
from ctypes.wintypes import (
    BOOL as _BOOL,
    DWORD as _DWORD,
    #c_ulong as _c_ulong,
    UINT as _UINT,
    #c_int as _c_int,
    #c_uint32 as _c_uint32,
#    c_float as _c_float,
    #LPWSTR as _LPWSTR,
    #LPCWSTR as _LPCWSTR,
    #c_wchar_p as _PCWSTR,
    #LPCWSTR as _PCWSTR,
    #PCWSTR as _PCWSTR,
)
from comtypes import (
	GUID as _GUID,
	IUnknown as _IUnknown,
	COMMETHOD as _COMMETHOD,
	STDMETHOD as _STDMETHOD,
)
from .MMConstants import *

IID_IAudioEndpointVolume = _GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')

class IAudioEndpointVolume(_IUnknown):
		_iid_ = _GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
		_methods_ = [
				_STDMETHOD(_HRESULT, 'RegisterControlChangeNotify', []),
				_STDMETHOD(_HRESULT, 'UnregisterControlChangeNotify', []),
				_COMMETHOD([], _HRESULT, 'GetChannelCount',
						(['out','retval'], _POINTER(_UINT), 'pnChannelCount'),
				),
				_COMMETHOD([], _HRESULT, 'SetMasterVolumeLevel',
						(['in'], _c_float, 'fLevelDB'),
						(['in'], _POINTER(_GUID), 'pguidEventContext')
				),
				_COMMETHOD([], _HRESULT, 'SetMasterVolumeLevelScalar',
						(['in'], _c_float, 'fLevelDB'),
						(['in'], _POINTER(_GUID), 'pguidEventContext')
				),
				_COMMETHOD([], _HRESULT, 'GetMasterVolumeLevel',
						(['out','retval'], _POINTER(_c_float), 'pfLevelDB')
				),
				_COMMETHOD([], _HRESULT, 'GetMasterVolumeLevelScalar',
						(['out','retval'], _POINTER(_c_float), 'pfLevelDB')
				),
				_COMMETHOD([], _HRESULT, 'SetChannelVolumeLevel',
						(['in'], _UINT, 'nChannel'),
						(['in'], _c_float, 'fLevelDB'),
						(['in'], _POINTER(_GUID), 'pguidEventContext')
				),
				_COMMETHOD([], _HRESULT, 'SetChannelVolumeLevelScalar',
						(['in'], _UINT, 'nChannel'),
						(['in'], _c_float, 'fLevelDB'),
						(['in'], _POINTER(_GUID), 'pguidEventContext')
				),
				_COMMETHOD([], _HRESULT, 'GetChannelVolumeLevel',
						(['in'], _UINT, 'nChannel'),
						(['out','retval'], _POINTER(_c_float), 'pfLevelDB')
				),
				_COMMETHOD([], _HRESULT, 'GetChannelVolumeLevelScalar',
						(['in'], _UINT, 'nChannel'),
						(['out','retval'], _POINTER(_c_float), 'pfLevelDB')
				),
				_COMMETHOD([], _HRESULT, 'SetMute',
						(['in'], _BOOL, 'bMute'),
						(['in'], _POINTER(_GUID), 'pguidEventContext')
				),
				_COMMETHOD([], _HRESULT, 'GetMute',
						(['out','retval'], _POINTER(_BOOL), 'pbMute')
				),
				_COMMETHOD([], _HRESULT, 'GetVolumeStepInfo',
						(['out','retval'], _POINTER(_UINT), 'pnStep'),
						(['out','retval'], _POINTER(_UINT), 'pnStepCount'),
				),
				_COMMETHOD([], _HRESULT, 'VolumeStepUp',
						(['in'], _POINTER(_GUID), 'pguidEventContext')
				),
				_COMMETHOD([], _HRESULT, 'VolumeStepDown',
						(['in'], _POINTER(_GUID), 'pguidEventContext')
				),
				_COMMETHOD([], _HRESULT, 'QueryHardwareSupport',
						(['out','retval'], _POINTER(_DWORD), 'pdwHardwareSupportMask')
				),
				_COMMETHOD([], _HRESULT, 'GetVolumeRange',
						(['out','retval'], _POINTER(_c_float), 'pfLevelMinDB'),
						(['out','retval'], _POINTER(_c_float), 'pfLevelMaxDB'),
						(['out','retval'], _POINTER(_c_float), 'pfVolumeIncrementDB')
				),

		]

if __name__ == '__main__':
	import sys
	sys.exit()
	import win32com
	import comtypes.client

	MMDeviceApiLib = \
			GUID('{2FDAAFA3-7523-4F66-9957-9D5E7FE698F6}')
	IID_IMMDevice = \
			GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
	IID_IMMDeviceEnumerator = \
			GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
	CLSID_MMDeviceEnumerator = \
			GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
	IID_IMMDeviceCollection = \
			GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
	IID_IAudioEndpointVolume = \
			GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')

	class IMMDeviceCollection(_IUnknown):
			_iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
			pass

	class IMMDevice(_IUnknown):
			_iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
			_methods_ = [
					_COMMETHOD([], _HRESULT, 'Activate',
							(['in'], _POINTER(GUID), 'iid'),
							(['in'], _DWORD, 'dwClsCtx'),
							(['in'], _POINTER(_DWORD), 'pActivationParans'),
							(['out','retval'], _POINTER(_POINTER(IAudioEndpointVolume)), 'ppInterface')
					),
					_STDMETHOD(_HRESULT, 'OpenPropertyStore', []),
					_STDMETHOD(_HRESULT, 'GetId', []),
					_STDMETHOD(_HRESULT, 'GetState', [])
			]
			pass

	class IMMDeviceEnumerator(_IUnknown):
			_iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')

			_methods_ = [
					_COMMETHOD([], _HRESULT, 'EnumAudioEndpoints',
							(['in'], _DWORD, 'dataFlow'),
							(['in'], _DWORD, 'dwStateMask'),
							(['out','retval'], _POINTER(_POINTER(IMMDeviceCollection)), 'ppDevices')
					),
					_COMMETHOD([], _HRESULT, 'GetDefaultAudioEndpoint',
							(['in'], _DWORD, 'dataFlow'),
							(['in'], _DWORD, 'role'),
							(['out','retval'], _POINTER(_POINTER(IMMDevice)), 'ppDevices')
					)
			]




	enumerator = comtypes.CoCreateInstance(
			CLSID_MMDeviceEnumerator,
			IMMDeviceEnumerator,
			comtypes.CLSCTX_INPROC_SERVER
	)

	print(enumerator)
	endpoint = enumerator.GetDefaultAudioEndpoint( 0, 1 )
	print(endpoint)
	volume = endpoint.Activate( IID_IAudioEndpointVolume, comtypes.CLSCTX_INPROC_SERVER, None )
	print(volume)
	print(volume.GetMasterVolumeLevel())
	print(volume.GetVolumeRange())
	#volume.SetMasterVolumeLevel(-20.0, None)
