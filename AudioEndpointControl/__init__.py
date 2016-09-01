from __future__ import print_function, unicode_literals, absolute_import
__version__ =  '0.1a1'
if __name__ == '__main__':
	import os
	from sys import argv
	import logging
	ProgramPath = os.path.dirname(argv[0])
	logging.basicConfig(filename=os.path.join(ProgramPath, 'debug.log'), filemode='w', level=logging.DEBUG)
from ctypes import POINTER as _POINTER
from comtypes import CoCreateInstance, COMObject, CLSCTX_INPROC_SERVER, CLSCTX_ALL
from _ctypes import COMError
try:
	from MMDeviceAPILib import MMDeviceEnumerator as _MMDeviceEnumerator, IMMDeviceEnumerator as _IMMDeviceEnumerator, IMMNotificationClient
except ImportError:
	from comtypes.client import GetModule
	GetModule("mmdeviceapi.tlb")
	from comtypes.gen.MMDeviceAPILib import MMDeviceEnumerator as _MMDeviceEnumerator, IMMDeviceEnumerator as _IMMDeviceEnumerator, IMMNotificationClient
#from comtypes.client import ShowEvents, GetEvents
from .MMConstants import *
from .EndpointvolumeAPI import *
from .PolicyConfigAPI import *

_CLSID_MMDeviceEnumerator = _MMDeviceEnumerator._reg_clsid_

def _GetValue(value):
	"""Need to do this in a function as comtypes seems to have a problem if it's in a class."""
	return value.__MIDL____MIDL_itf_mmdeviceapi_0003_00850001.pwszVal

from functools import partial as _partial

# This is a wrapper for volume related methods.
class AudioVolume(object):
	def __init__(self, endpoint, IAudioEndpointVolume):
		self.endpoint = endpoint
		self.IAudioEndpointVolume = IAudioEndpointVolume

	def GetChannelCount(self):
		"""Gets a count of the channels in the audio stream."""
		#return self.IAudioEndpointVolume.GetChannelCount()
		return self.IAudioEndpointVolume.GetChannelCount()

	def __len__(self):
		return self.GetChannelCount()

	def Get(self, nChannel=0, Scalar=True):
		"""
		When Scaler=True (default): Gets the master volume level, expressed as a normalized, audio-tapered value.
		When Scaler=False: Gets the master volume level of the audio stream, in decibels.
		When Scaler=True (default): Gets the normalized, audio-tapered volume level of the specified channel of the audio stream.
		When Scaler=False: Gets the volume level, in decibels, of the specified channel in the audio stream.
		"""
		if nChannel == 0:
			if Scalar:
				return self.IAudioEndpointVolume.GetMasterVolumeLevelScalar()
			else:
				return self.IAudioEndpointVolume.GetMasterVolumeLevel()
		else:
			if Scalar:
				return self.IAudioEndpointVolume.GetChannelVolumeLevelScalar(nChannel)
			else:
				return self.IAudioEndpointVolume.GetChannelVolumeLevel(nChannel)

	def Set(self, fLevelDB, nChannel=0, Scalar=True, pguidEventContext=None):
		"""
		When Scaler=True (default): Sets the master volume level, expressed as a normalized, audio-tapered value.
		When Scaler=False: Sets the master volume level of the audio stream, in decibels.
		When Scaler=True (default): Sets the normalized, audio-tapered volume level of the specified channel in the audio stream.
		When Scaler=False: Sets the volume level, in decibels, of the specified channel of the audio stream.

		"""
		if type(fLevelDB) == bool:
			return self.Mute(fLevelDB)
		else:
			if nChannel == 0:
				if Scalar: return self.IAudioEndpointVolume.SetMasterVolumeLevelScalar(fLevelDB, pguidEventContext)
				else: return self.IAudioEndpointVolume.SetMasterVolumeLevel(fLevelDB, pguidEventContext)
			else:
				if Scalar: return self.IAudioEndpointVolume.SetChannelVolumeLevelScalar(nChannel-1, fLevelDB, pguidEventContext)
				else: return self.IAudioEndpointVolume.SetChannelVolumeLevel(nChannel-1, fLevelDB, pguidEventContext)

	def GetRange(self):
		"""Gets the volume range of the audio stream, in decibels."""
		return self.IAudioEndpointVolume.GetVolumeRange()

	def StepDown(self, pguidEventContext=None):
		"""Decreases the volume level by one step."""
		return self.IAudioEndpointVolume.VolumeStepDown(pguidEventContext)

	def StepUp(self, pguidEventContext=None):
		"""Increases the volume level by one step."""
		return self.IAudioEndpointVolume.VolumeStepUp(pguidEventContext)

	def GetStepInfo(self):
		"""Gets information about the current step in the volume range."""
		return self.IAudioEndpointVolume.GetVolumeStepInfo()

	def QueryHardwareSupport(self):
		"""Queries the audio endpoint device for its hardware-supported functions."""
		return self.IAudioEndpointVolume.QueryHardwareSupport()

	def RegisterControlChangeNotify(self, Callback):
		"""Registers a client's notification callback interface."""
		self.Callback = Callback
		hr = self.IAudioEndpointVolume.RegisterControlChangeNotify(self.Callback)
		if hr:
			import win32api
			print('RegisterControlChangeNotify', hr)
			print('SetDefaultEndpoint', win32api.FormatMessage(hr))

	def UnregisterControlChangeNotify(self):
		"""Deletes the registration of a client's notification callback interface."""
		try:
			hr = self.IAudioEndpointVolume.UnregisterControlChangeNotify(self.Callback)
			self.Callback = None
			if hr:
				import win32api
				print('UnregisterControlChangeNotify', hr)
				print('SetDefaultEndpoint', win32api.FormatMessage(hr))
		except AttributeError:
			pass

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
	def Mute(self):
		return self.IAudioEndpointVolume.GetMute()

	@Mute.setter
	def Mute(self, bMute):
		return self.IAudioEndpointVolume.SetMute(bMute, None)

	def __eq__(self, other):
		"""Tests if two enpoint devices are the same."""
		return self.getId() == other.getId()

	def __ne__(self, other):
		"""Tests if two enpoint devices are not the same."""
		return self.getId() != other.getId()

	__getitem__ = Get
	__setitem__ = _partial(Set, Scalar=True, pguidEventContext=None)
	__pos__ = __add__
	__neg__ = __add__

	#def __call__(self, test):
	#	return 'Testing {0}'.format(test)

# This is a wrapper for a single COM endpoint.
class AudioEndpoint(object):
	def __init__(self, endpoint, endpoints, PKEY_Device=PKEY_Device_FriendlyName):
		"""Initializes an endpoint object."""
		self.endpoint = endpoint
		self.endpoints = endpoints
		self.PKEY_Device = PKEY_Device
		self.IAudioEndpointVolume = _POINTER(IAudioEndpointVolume)(endpoint.Activate(IID_IAudioEndpointVolume, CLSCTX_INPROC_SERVER, None))
		self._AudioVolume = AudioVolume(endpoint, self.IAudioEndpointVolume)

	@property
	def volume(self):
		#return self.GetMasterVolumeLevel()
		return self._AudioVolume

	@volume.setter
	def volume(self, fLevelDB):
		if type(fLevelDB) == bool:
			return self._AudioVolume.SetMute(fLevelDB)
		else:
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

	def isDefault(self, role=eConsole, dataFlow=eRender):
		"""Return if endpoint device is default or not."""
		return self == self.endpoints.GetDefault(role, dataFlow)

	def GetVolumeRange(self):
		"""Gets the volume range of the audio stream, in decibels."""
		return self.IAudioEndpointVolume.GetVolumeRange()

	def GetMasterVolumeLevel(self, Scalar=True):
		"""
		When Scaler=True (default): Gets the master volume level, expressed as a normalized, audio-tapered value.
		When Scaler=False: Gets the master volume level of the audio stream, in decibels.
		"""
		if Scalar: return self.IAudioEndpointVolume.GetMasterVolumeLevelScalar()
		else: return self.IAudioEndpointVolume.GetMasterVolumeLevel()

	def SetMasterVolumeLevel(self, fLevelDB, Scalar=True, pguidEventContext=None):
		"""
		When Scaler=True (default): Sets the master volume level, expressed as a normalized, audio-tapered value.
		When Scaler=False: Sets the master volume level of the audio stream, in decibels.

		"""
		if Scalar: return self.IAudioEndpointVolume.SetMasterVolumeLevelScalar(fLevelDB, pguidEventContext)
		else: return self.IAudioEndpointVolume.SetMasterVolumeLevel(fLevelDB, pguidEventContext)

	def GetChannelVolumeLevel(self, nChannel, Scalar=True):
		"""
		When Scaler=True (default): Gets the normalized, audio-tapered volume level of the specified channel of the audio stream.
		When Scaler=False: Gets the volume level, in decibels, of the specified channel in the audio stream.
		"""
		if Scalar: return self.IAudioEndpointVolume.GetChannelVolumeLevelScalar(nChannel)
		else: return self.IAudioEndpointVolume.GetChannelVolumeLevel(nChannel)

	def SetChannelVolumeLevel(self, nChannel, fLevelDB, Scaler=True, pguidEventContext=None):
		"""
		When Scaler=True (default): Sets the normalized, audio-tapered volume level of the specified channel in the audio stream.
		When Scaler=False: Sets the volume level, in decibels, of the specified channel of the audio stream.

		"""
		if Scalar: return self.IAudioEndpointVolume.SetChannelVolumeLevelScalar(nChannel, fLevelDB, pguidEventContext)
		else: return self.IAudioEndpointVolume.SetChannelVolumeLevel(nChannel, fLevelDB, pguidEventContext)

	def GetMute(self):
		"""Gets the muting state of the audio stream."""
		return self.IAudioEndpointVolume.GetMute()

	def SetMute(self, bMute, pguidEventContext=None):
		"""Sets the muting state of the audio stream."""
		return self.IAudioEndpointVolume.SetMute(bMute, pguidEventContext)

	def GetChannelCount(self):
		"""Gets a count of the channels in the audio stream."""
		#return self.IAudioEndpointVolume.GetChannelCount()
		return len(self._AudioVolume)

	def VolumeStepDown(self, pguidEventContext=None):
		"""Decreases the volume level by one step."""
		return self.IAudioEndpointVolume.VolumeStepDown(pguidEventContext)

	def VolumeStepUp(self, pguidEventContext=None):
		"""Increases the volume level by one step."""
		return self.IAudioEndpointVolume.VolumeStepUp(pguidEventContext)

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

"""
QueryHardwareSupport

Queries the audio endpoint device for its hardware-supported functions.

UnregisterControlChangeNotify

Deletes the registration of a client's notification callback interface.
RegisterControlChangeNotify

Registers a client's notification callback interface.
"""
class AudioEndpoints(object):
	def __init__(self, DEVICE_STATE=DEVICE_STATE_ACTIVE, PKEY_Device=PKEY_Device_FriendlyName):
		self.DEVICE_STATE = DEVICE_STATE
		self.PKEY_Device = PKEY_Device
		self.pDevEnum = CoCreateInstance(_CLSID_MMDeviceEnumerator, _IMMDeviceEnumerator, CLSCTX_INPROC_SERVER)
		self.pPolicyConfig = None

	def GetDefault(self, role=eConsole, dataFlow=eRender):
		return AudioEndpoint(self.pDevEnum.GetDefaultAudioEndpoint(dataFlow, role), self, self.PKEY_Device)

	def SetDefault(self, endpoint, role=eConsole):
		OldDefault = self.GetDefault(role)

		if not self.pPolicyConfig:
			self.pPolicyConfig = CoCreateInstance(CLSID_CPolicyConfigVistaClient, IPolicyConfigVista, CLSCTX_ALL)

		hr = self.pPolicyConfig.SetDefaultEndpoint(endpoint.getId(), role)
		if hr:
			import win32api
			print('SetDefaultEndpoint', win32api.FormatMessage(hr))
		return OldDefault

	def RegisterCallback(self, Callback):
		self.Callback = Callback
		hr = self.pDevEnum.RegisterEndpointNotificationCallback(self.Callback)
		if hr:
			import win32api
			print('RegisterEndpointNotificationCallback', hr)
			print('SetDefaultEndpoint', win32api.FormatMessage(hr))

	def UnregisterCallback(self):
		try:
			hr = self.pDevEnum.UnregisterEndpointNotificationCallback(self.Callback)
			self.Callback = None
			if hr:
				import win32api
				print('UnregisterEndpointNotificationCallback', hr)
				print('SetDefaultEndpoint', win32api.FormatMessage(hr))
		except AttributeError:
			pass

	def __call__(self, ID):
		try:
			return AudioEndpoint(self.pDevEnum.GetDevice(ID), self, self.PKEY_Device)
		except COMError:
			for endpoint in self:
				if endpoint.getName() == ID:
					return endpoint

	def __str__(self):
		return str([str(endpoint) for endpoint in self])

	def ChangeFilter(self, DEVICE_STATE=None, PKEY_Device=None):
		if DEVICE_STATE != None: self.DEVICE_STATE = DEVICE_STATE
		if PKEY_Device != None: self.PKEY_Device = PKEY_Device

	def __iter__(self, dataFlow=eRender):
		pEndpoints = self.pDevEnum.EnumAudioEndpoints(dataFlow, self.DEVICE_STATE)
		for i in range(pEndpoints.GetCount()):
			yield AudioEndpoint(pEndpoints.Item(i), self, self.PKEY_Device)

	def __len__(self):
		return int(self.pDevEnum.EnumAudioEndpoints(eRender, self.DEVICE_STATE).GetCount())

if __name__ == '__main__':
	AudioDevices = AudioEndpoints()

	endpoint = AudioDevices.GetDefault()

	Vol = endpoint.volume.Get()
	endpoint.volume.Set(0)
	assert endpoint.volume.Get() == 0.0, 'endpoint.volume.Get() wrong'
	endpoint.volume.Set(Vol)
	assert endpoint.volume.Get() == Vol, 'endpoint.volume.Get() wrong'

	#try:
	#	from EndpointExample import CMMNotificationClient
	#except:
	#	pass
	#else:

	#
	#pVolume = _POINTER(IAudioEndpointVolume)(volume)

	#print(endpoint.volume)
	#endpoint.volume = .8
	#print(endpoint.volume.test)
	#print(endpoint.volume('Oh my'))
	#for endpoint in AudioDevices:
		#pVolume = _POINTER(IAudioEndpointVolume)(endpoint.endpoint.Activate(IID_IAudioEndpointVolume, CLSCTX_INPROC_SERVER, None))
		#print(pVolume)
		#print(endpoint)
		#print(endpoint.GetMasterVolumeLevel())
		#print(endpoint.GetVolumeStepInfo())
		#print(endpoint.GetMute())
		#print(endpoint.GetChannelCount())
		#print(endpoint.volume)
		#endpoint.volume = 1
		#print(endpoint.volume)
		#print(endpoint.SetMute(not endpoint.GetMute()))
		#print(endpoint.GetVolumeRange())
		#endpoint.SetMasterVolumeLevel(1)

		#print(len(AudioDevices))
		#print(AudioDevices)
		#print("eConsole", str(AudioDevices.GetDefault()))
		#print("eMultimedia", str(AudioDevices.GetDefault(eMultimedia)))
		#print("eCommunications", str(AudioDevices.GetDefault(eCommunications)))
		#	eRender, eCapture, eAll, EDataFlow_enum_count = range(4)
		#for endpoint in AudioDevices:
			#if endpoint == AudioDevices.GetDefault():
			#	print('The Same', str(endpoint), str(AudioDevices.GetDefault()))
			#if endpoint.isDefault():
			#print(repr(endpoint))
			#	print("Default", str(endpoint))
			#else:
			#	print(endpoint)
			#print(endpoint.getId())
			#print(AudioDevices(endpoint.getId()))
			#print(AudioDevices(endpoint.getName()))
		#result = lib.test(666)
		#print(AudioDevices.pDevEnum)
		#print(super(_compointer_base, AudioDevices.pDevEnum).value)

		#p = _POINTER(IUnknown)()
		#print(dir(byref(p)))
		#byref(p) =
		#print(repr(super(_compointer_base, p).value))
		#print(dir(p))
		#oledll.oleaut32.GetActiveObject(byref(CLSID_MMDeviceEnumerator), None, byref(p))
		#print(p)

		#import re
		#print(int(re.match("<POINTER\(.*\) ptr=0x(\S+)", str(AudioDevices.pDevEnum)).group(1), 16))
		#DevEnum = int(re.match("<POINTER\(.*\) ptr=0x(\S+)", str(AudioDevices.pDevEnum)).group(1), 16)
		#<POINTER(IMMDeviceEnumerator) ptr=0x519a28 at 2edcbc0>
		#print(dir(POINTER(IMMDevice)))
		#import time
		#try:
		#	AudioDevices.RegisterCallback(CMMNotificationClient())
		#	time.sleep(5)
		#	AudioDevices.SetDefault(AudioDevices('{0.0.0.00000000}.{1797e540-0196-47fd-9a36-9e34916bfc5f}'))
		#	time.sleep(100)
		#except KeyboardInterrupt:
		#	pass
		#finally:
		#	AudioDevices.UnregisterCallback()
		#	print('and done.')
		#print("eConsole", str(AudioDevices.GetDefault(eConsole)))
		#print("eMultimedia", str(AudioDevices.GetDefault(eMultimedia)))
		#print("eCommunications", str(AudioDevices.GetDefault(eCommunications)))
