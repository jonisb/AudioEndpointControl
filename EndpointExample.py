from __future__ import print_function, unicode_literals
import AudioEndpointControl
# COMObject, IMMNotificationClient are used for notifications
from AudioEndpointControl import COMObject, IMMNotificationClient, IAudioEndpointVolumeCallback
# EDataFlow enumeration: The EDataFlow enumeration defines constants that indicate the direction in which audio data flows between an audio endpoint device and an application.
from AudioEndpointControl import EDataFlow, eRender, eCapture, eAll, EDataFlow_enum_count
# ERole enumeration: The ERole enumeration defines constants that indicate the role that the system has assigned to an audio endpoint device.
from AudioEndpointControl import ERole, eConsole, eMultimedia, eCommunications, ERole_enum_count
# DEVICE_STATE_XXX Constants: The DEVICE_STATE_XXX constants indicate the current state of an audio endpoint device.
from AudioEndpointControl import DEVICE_STATE, DEVICE_STATE_ACTIVE, DEVICE_STATE_DISABLED, DEVICE_STATE_NOTPRESENT, DEVICE_STATE_UNPLUGGED, DEVICE_STATEMASK_ALL
#Each PKEY_Xxx property identifier in the following list is a constant of type PROPERTYKEY that is defined in header file Functiondiscoverykeys_devpkey.h. All audio endpoint devices have these three device properties.
from AudioEndpointControl import PKEY_Device_FriendlyName, PKEY_Device_DeviceDesc, PKEY_DeviceInterface_FriendlyName

# This is an example class used for getting Audio endpoint notifications(events), you can name the class whatever but the methods need to be defined properly like in the example,
# but what the methods do is up to you. You don't need the methods you don't need events for.
class CMMNotificationClient(COMObject):
	_com_interfaces_=[IMMNotificationClient]

	def OnDeviceStateChanged(self, this, pwstrDeviceId, dwNewState):
			print('OnDeviceStateChanged: {0}, {1}'.format(AudioDevices(pwstrDeviceId), DEVICE_STATE[dwNewState]))

	def OnDeviceRemoved(self, this, pwstrDeviceId):
			print('OnDeviceRemoved: {0}'.format(AudioDevices(pwstrDeviceId)))

	def OnDeviceAdded(self, this, pwstrDeviceId):
			print('OnDeviceAdded: {0}'.format(AudioDevices(pwstrDeviceId)))

	def OnDefaultDeviceChanged(self, this, flow, role, pwstrDeviceId):
			print('OnDefaultDeviceChanged: {0}, {1}, {2}'.format(EDataFlow[flow], ERole[role], AudioDevices(pwstrDeviceId)))

	def OnPropertyValueChanged(self, this, pwstrDeviceId, key):
			print('OnPropertyValueChanged: {0}, {1}'.format(AudioDevices(pwstrDeviceId), key))

class CAudioEndpointVolumeCallback(COMObject):
	_com_interfaces_=[IAudioEndpointVolumeCallback]

	def OnNotify(self, this, pNotify):
		try:
			print('OnNotify: guidEventContext {0}'.format(pNotify.contents.guidEventContext))
		except: pass
		try:
			print('OnNotify: bMuted {0}'.format(pNotify.contents.bMuted))
		except: pass
		try:
			print('OnNotify: fMasterVolume {0}'.format(pNotify.contents.fMasterVolume))
		except: pass
		try:
			print('OnNotify: nChannels {0}'.format(pNotify.contents.nChannels))
		except: pass
		from ctypes import POINTER, c_float, cast
		try:
			for channel in range(pNotify.contents.nChannels):
				print('OnNotify: afChannelVolumes {0}'.format(cast(pNotify.contents.afChannelVolumes, POINTER(c_float))[channel]))
		except: pass

if __name__ == '__main__':
	print("When creating the AudioEndpoints object you can specify what endpoint(s) you want shown (ACTIVE, DISABLED, NOTPRESENT, UNPLUGGED, ALL).\n")
	AudioDevices = AudioEndpointControl.AudioEndpoints(DEVICE_STATE=DEVICE_STATE_ACTIVE, PKEY_Device=PKEY_Device_FriendlyName)

	print("Using str() or print on a AudioEndpoint or AudioEndpoints object results in the text name of the endpoint.\n")
	print("Number of active audio endpoints: {0}".format(len(AudioDevices)))
	print("Get a list of audio endpoints:", AudioDevices)
	print("Get default endpoint for eConsole, eRender (default):", AudioDevices.GetDefault())
	print("Get default endpoint for eConsole, eCapture:", AudioDevices.GetDefault(eConsole, eCapture))
	print("Get default endpoint for eMultimedia:", AudioDevices.GetDefault(eMultimedia))
	print("Get default endpoint for eCommunications:", AudioDevices.GetDefault(eCommunications))

	print("\nAudioEndpoints supports iteration so can be used in for and while loops:")
	for endpoint in AudioDevices:
		print()
		if endpoint == AudioDevices.GetDefault():
			print('AudioEndpoint objects can be compared to see if they are the same device: The same:', endpoint, AudioDevices.GetDefault())
		if endpoint.isDefault():
			print("AudioEndpoint objects can be tested if they are the default: ", endpoint)
		else:
			print("Not default AudioEndpoint:", endpoint)
		print("You can use a AudioEndpoint Id:", AudioDevices(endpoint.getId()))
		print("or the AudioEndpoint name to get a AudioEndpoint object:", AudioDevices(endpoint.getName()))

	import time
	try:
		print("\nLets activate some AudioEndpoint device notifications, you need to create a class with methods that respond to the events.")
		print("You can change the default audio device or enable/disable some devices to see more events.\nTo exit press CTRL+C.\n")
		AudioDevices.RegisterCallback(CMMNotificationClient())
		#OldDefault = AudioDevices.SetDefault(AudioDevices('{0.0.0.00000000}.{1797e540-0196-47fd-9a36-9e34916bfc5f}'))
		time.sleep(60)
	except KeyboardInterrupt:
		pass
	finally:
		#AudioDevices.SetDefault(OldDefault)
		time.sleep(1)
		print("Remember to unregister when you don't want notifications anymore.")
		AudioDevices.UnregisterCallback()
		print()

	try:
		print("\nLets activate some AudioEndpoint volume notifications, you need to create a class with methods that respond to the events.")
		print("You can change the volume or mute/unmute of any channel on the default audio device.\nTo exit press CTRL+C.\n")
		endpoint = AudioDevices.GetDefault()
		endpoint.volume.RegisterControlChangeNotify(CAudioEndpointVolumeCallback())
		time.sleep(60)
	except KeyboardInterrupt:
		pass
	finally:
		print("Remember to unregister when you don't want notifications anymore.")
		endpoint.volume.UnregisterControlChangeNotify()
		print('and done.')
