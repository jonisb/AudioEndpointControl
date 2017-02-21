# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import AudioEndpointControl
# DataFlow enumeration: The DataFlow enumeration defines constants that
# indicate the direction in which audio data flows between an audio endpoint
# device and an application.
from AudioEndpointControl import Render, Capture, All
# Role enumeration: The Role enumeration defines constants that indicate the
# role that the system has assigned to an audio endpoint device.
from AudioEndpointControl import Console, Multimedia, Communications
# DEVICE_STATE_XXX Constants: The DEVICE_STATE_XXX constants indicate the
# current state of an audio endpoint device.
from AudioEndpointControl import (
    DEVICE_STATE_ACTIVE,
    DEVICE_STATE_DISABLED,
    DEVICE_STATE_NOTPRESENT,
    DEVICE_STATE_UNPLUGGED,
    DEVICE_STATEMASK_ALL
    )
# Each PKEY_Xxx property identifier in the following list is a constant of type
# PROPERTYKEY that is defined in header file Functiondiscoverykeys_devpkey.h.
# All audio endpoint devices have these three device properties.
from AudioEndpointControl import (
    Device_FriendlyName,
    Device_DeviceDesc,
    DeviceInterface_FriendlyName)

# If you want to know that the volume/mute events are done by this program, you need to send a program specific guid when creating the AudioEndpoints object.
from comtypes import GUID
AppID = GUID('{00000000-0000-0000-0000-000000000001}')

# This is an example class used for getting Audio endpoint notifications(events), you can name the class whatever but the methods need to be defined properly like in the example,
# but what the methods do is up to you. You don't need the methods you don't need events for.
class MMNotificationClient(object):
    def OnDeviceStateChanged(self, AudioDevice, NewState):
        print('OnDeviceStateChanged: {0}, {1}'.format(AudioDevice, NewState))

    def OnDeviceRemoved(self, AudioDevice):
        print('OnDeviceRemoved: {0}'.format(AudioDevice))

    def OnDeviceAdded(self, AudioDevice):
            print('OnDeviceAdded: {0}'.format(AudioDevice))

    def OnDefaultDeviceChanged(self, flow, role, AudioDevice):
        print('OnDefaultDeviceChanged: {0}, {1}, {2}'.format(flow, role, AudioDevice))

    # I'm unsure if the property key has usable data.
    def OnPropertyValueChanged(self, AudioDevice, key):
        print('OnPropertyValueChanged: {0}, {1}'.format(AudioDevice, key))

# This is an example class used for getting Audio endpoint volume notifications(events), you can name the class whatever but the methods need to be defined properly like in the example,
# but what the methods do is up to you. You don't need the methods you don't need events for.
class AudioEndpointVolumeCallback(object):
    def OnNotify(self, Notify, AudioDevice):
        print('OnNotify: AudioDevice: {0}'.format(AudioDevice))
        print('OnNotify: EventContext: {0}'.format(Notify.EventContext))
        if AppID == Notify.EventContext:
            print("I changed the volume, but I did not shoot the deputy.")
        print('OnNotify: Muted: {0}'.format(Notify.Muted))
        print('OnNotify: MasterVolume: {0}'.format(Notify.MasterVolume))
        print('OnNotify: Channels: {0}'.format(Notify.Channels))
        print('OnNotify: ChannelVolumes: {0}'.format(Notify.ChannelVolumes))
        print()

if __name__ == '__main__':
    print("When creating the AudioEndpoints object you can specify what endpoint(s) you want shown (ACTIVE, DISABLED, NOTPRESENT, UNPLUGGED, ALL).\n")
    AudioDevices = AudioEndpointControl.AudioEndpoints(DEVICE_STATE=DEVICE_STATE_ACTIVE, PKEY_Device=Device_FriendlyName, EventContext=AppID)

    print("Using str() or print on a AudioEndpoint or AudioEndpoints object results in the text name of the endpoint.\n")
    print("Number of active audio endpoints: {0}".format(len(AudioDevices)))
    print("Get a list of audio endpoints:", AudioDevices)
    print("Get default endpoint for Console, Render (default):", AudioDevices.GetDefault())
    print("Get default endpoint for Console, Capture:", AudioDevices.GetDefault(Console, Capture))
    print("Get default endpoint for Multimedia:", AudioDevices.GetDefault(Multimedia))
    print("Get default endpoint for Communications:", AudioDevices.GetDefault(Communications))

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
        AudioDevices.RegisterCallback(MMNotificationClient())
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
        endpoints = []
        for AudioDevice in AudioDevices:
            endpoints.append(AudioDevice)
            endpoints[-1].RegisterCallback(AudioEndpointVolumeCallback())
            if endpoints[-1].isDefault():
                endpoint = endpoints[-1]
        VolSave = endpoint.volume.Get()
        time.sleep(5)
        endpoint.volume.Set(VolSave / 2)
        time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        print("Remember to unregister when you don't want notifications anymore.")
        for endpoint in endpoints:
            endpoint.UnregisterCallback()
            if endpoint.isDefault():
                endpoint.volume.Set(VolSave)
        print('and done.')
