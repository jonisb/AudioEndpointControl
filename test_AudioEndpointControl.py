# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import

import unittest


class TestConstants(unittest.TestCase):

    def test_init(self):
        from AudioEndpointControl.MMConstants import eRender, eCapture, eAll
        from AudioEndpointControl import Render, Capture, All
        from AudioEndpointControl.MMConstants import (eConsole, eMultimedia,
                                          eCommunications)
        from AudioEndpointControl import (Console, Multimedia,
                                          Communications)
        from AudioEndpointControl import (DEVICE_STATE_ACTIVE,
                                          DEVICE_STATE_DISABLED,
                                          DEVICE_STATE_NOTPRESENT,
                                          DEVICE_STATE_UNPLUGGED,
                                          DEVICE_STATEMASK_ALL)
        from AudioEndpointControl.MMConstants import (STGM_READ, STGM_WRITE,
                                                      STGM_READWRITE)
        from AudioEndpointControl.MMConstants import PROPERTYKEY
        from AudioEndpointControl import (Device_FriendlyName,
                                          Device_DeviceDesc,
                                          DeviceInterface_FriendlyName)
        from AudioEndpointControl.MMConstants import (
            ENDPOINT_HARDWARE_SUPPORT_VOLUME,
            ENDPOINT_HARDWARE_SUPPORT_MUTE,
            ENDPOINT_HARDWARE_SUPPORT_METER)

        self.assertEqual(int(Render), eRender)
        self.assertEqual(str(Render), b'Render')
        self.assertEqual(int(Capture), eCapture)
        self.assertEqual(str(Capture), b'Capture')
        self.assertEqual(int(All), eAll)
        self.assertEqual(str(All), b'All')

        self.assertEqual(int(Console), eConsole)
        self.assertEqual(str(Console), b'Console')
        self.assertEqual(int(Multimedia), eMultimedia)
        self.assertEqual(str(Multimedia), b'Multimedia')
        self.assertEqual(int(Communications), eCommunications)
        self.assertEqual(str(Communications), b'Communications')

        self.assertEqual(int(DEVICE_STATE_ACTIVE), 0x00000001)
        self.assertEqual(str(DEVICE_STATE_ACTIVE), b'Active')
        self.assertEqual(int(DEVICE_STATE_DISABLED), 0x00000002)
        self.assertEqual(str(DEVICE_STATE_DISABLED), b'Disabled')
        self.assertEqual(int(DEVICE_STATE_NOTPRESENT), 0x00000004)
        self.assertEqual(str(DEVICE_STATE_NOTPRESENT), b'Notpresent')
        self.assertEqual(int(DEVICE_STATE_UNPLUGGED), 0x00000008)
        self.assertEqual(str(DEVICE_STATE_UNPLUGGED), b'Unplugged')
        self.assertEqual(int(DEVICE_STATEMASK_ALL), 0x0000000F)
        self.assertEqual(str(DEVICE_STATEMASK_ALL),
                         b'Unplugged, Active, Disabled, Notpresent')

        self.assertEqual(int(DEVICE_STATE_ACTIVE|DEVICE_STATE_DISABLED|DEVICE_STATE_NOTPRESENT|DEVICE_STATE_UNPLUGGED), int(DEVICE_STATEMASK_ALL))
        self.assertEqual(DEVICE_STATE_ACTIVE|DEVICE_STATE_DISABLED|DEVICE_STATE_NOTPRESENT|DEVICE_STATE_UNPLUGGED, DEVICE_STATEMASK_ALL)

        self.assertEqual(int(STGM_READ), 0x00000000)
        self.assertEqual(str(STGM_READ), b'Read')
        self.assertEqual(int(STGM_WRITE), 0x00000001)
        self.assertEqual(str(STGM_WRITE), b'Write')
        self.assertEqual(int(STGM_READWRITE), 0x00000002)
        self.assertEqual(str(STGM_READWRITE), b'Readwrite')

        self.assertEqual(type(Device_FriendlyName), PROPERTYKEY)
        self.assertEqual(type(Device_DeviceDesc), PROPERTYKEY)
        self.assertEqual(type(DeviceInterface_FriendlyName), PROPERTYKEY)

        self.assertEqual(int(ENDPOINT_HARDWARE_SUPPORT_VOLUME), 0x00000001)
        self.assertEqual(str(ENDPOINT_HARDWARE_SUPPORT_VOLUME), b'Volume')
        self.assertEqual(int(ENDPOINT_HARDWARE_SUPPORT_MUTE), 0x00000002)
        self.assertEqual(str(ENDPOINT_HARDWARE_SUPPORT_MUTE), b'Mute')
        self.assertEqual(int(ENDPOINT_HARDWARE_SUPPORT_METER), 0x00000004)
        self.assertEqual(str(ENDPOINT_HARDWARE_SUPPORT_METER), b'Meter')


class TestAudioEndpoints(unittest.TestCase):

    def setUp(self):
        import AudioEndpointControl
        from AudioEndpointControl.AudioEndpoints import AudioEndpoint
        self.AudioEndpointControl = AudioEndpointControl
        self.AudioEndpoint = AudioEndpoint
        self.AudioDevices = self.AudioEndpointControl.AudioEndpoints()

    def test_init(self):
        self.assertEqual(type(self.AudioDevices),
                         self.AudioEndpointControl.AudioEndpoints)

        from AudioEndpointControl import (DEVICE_STATE_ACTIVE,
                                          DEVICE_STATE_DISABLED,
                                          DEVICE_STATE_NOTPRESENT,
                                          DEVICE_STATE_UNPLUGGED,
                                          DEVICE_STATEMASK_ALL)

        self.assertEqual(type(self.AudioEndpointControl.AudioEndpoints(
            DEVICE_STATE=DEVICE_STATEMASK_ALL)),
                         self.AudioEndpointControl.AudioEndpoints)
        self.assertEqual(type(self.AudioEndpointControl.AudioEndpoints(
            DEVICE_STATE=DEVICE_STATE_ACTIVE | DEVICE_STATE_DISABLED
            | DEVICE_STATE_NOTPRESENT | DEVICE_STATE_UNPLUGGED
            )), self.AudioEndpointControl.AudioEndpoints)

        from AudioEndpointControl import (Device_FriendlyName,
                                          Device_DeviceDesc,
                                          DeviceInterface_FriendlyName)

        self.assertEqual(type(self.AudioEndpointControl.AudioEndpoints(
            PKEY_Device=Device_FriendlyName)),
                         self.AudioEndpointControl.AudioEndpoints)

        self.assertEqual(type(self.AudioEndpointControl.AudioEndpoints(
            PKEY_Device=Device_DeviceDesc)),
                         self.AudioEndpointControl.AudioEndpoints)

        self.assertEqual(type(self.AudioEndpointControl.AudioEndpoints(
            PKEY_Device=DeviceInterface_FriendlyName)),
                         self.AudioEndpointControl.AudioEndpoints)

    def test_GetDefault(self):
        self.assertEqual(type(self.AudioDevices.GetDefault()),
                         self.AudioEndpoint)

    def test_SetDefault(self):
        self.assertEqual(
            type(self.AudioDevices.SetDefault(
                self.AudioDevices.GetDefault())),
            self.AudioEndpoint)

    def test_Methods(self):
        self.assertEqual(type(str(self.AudioDevices)), str)
        self.assertEqual(type(len(self.AudioDevices)), int)
        self.assertEqual(
            type(self.AudioDevices(self.AudioDevices.GetDefault().getId())),
            self.AudioEndpoint)
        self.assertEqual(
            type(self.AudioDevices(self.AudioDevices.GetDefault().getName())),
            self.AudioEndpoint)

        from _ctypes import COMError
        with self.assertRaises(COMError):
            self.AudioDevices("Wrong number")

        # TODO: test methods after changing these settings
        from AudioEndpointControl import (DEVICE_STATE_ACTIVE,
                                          DEVICE_STATE_DISABLED,
                                          DEVICE_STATE_NOTPRESENT,
                                          DEVICE_STATE_UNPLUGGED,
                                          DEVICE_STATEMASK_ALL)
        for state in (
                DEVICE_STATE_ACTIVE,
                DEVICE_STATE_DISABLED,
                DEVICE_STATE_NOTPRESENT,
                DEVICE_STATE_UNPLUGGED,
                DEVICE_STATEMASK_ALL):
            self.AudioDevices.ChangeFilter(DEVICE_STATE=state)
            self.assertEqual(self.AudioDevices.DEVICE_STATE, state)

        from AudioEndpointControl import (
            Device_FriendlyName,
            Device_DeviceDesc,
            DeviceInterface_FriendlyName)
        for pkey in (
                Device_FriendlyName,
                Device_DeviceDesc,
                DeviceInterface_FriendlyName):
            self.AudioDevices.ChangeFilter(PKEY_Device=pkey)
            self.assertEqual(self.AudioDevices.PKEY_Device, pkey)

    def test_Notificatios(self):
        with self.assertRaises(Exception):
            self.AudioDevices.RegisterCallback(None)
        with self.assertRaises(Exception):
            self.AudioDevices.UnregisterCallback()

        import Queue
        NotificationQueue = Queue.Queue()

        class MMNotificationClient(object):
            def OnDefaultDeviceChanged(self, flow, role, AudioDevice):
                NotificationQueue.put_nowait((self, flow, role, AudioDevice))

        self.assertEqual(self.AudioDevices.RegisterCallback(
            MMNotificationClient()), None)

        import time
        time.sleep(1)
        self.AudioDevices.SetDefault(self.AudioDevices.GetDefault())
        time.sleep(1)

        self.assertEqual(self.AudioDevices.UnregisterCallback(), None)

        class MMNotificationClientTest(object):
            def OnDeviceStateChanged(self, AudioDevice, NewState):
                pass

            def OnDeviceRemoved(self, AudioDevice):
                pass

            def OnDeviceAdded(self, AudioDevice):
                pass

            def OnDefaultDeviceChanged(self, flow, role, AudioDevice):
                pass

            def OnPropertyValueChanged(self, AudioDevice, key):
                pass

        from AudioEndpointControl.Notifications import CMMNotificationClient

        callback = CMMNotificationClient(type(str("MMNotificationClient"), (), {})(), self.AudioDevices)

        self.assertEqual(callback.OnDeviceStateChanged(None, self.AudioDevices.GetDefault().getId(), int(self.AudioEndpointControl.DEVICE_STATE_ACTIVE)), None)
        self.assertEqual(callback.OnDeviceRemoved(None, self.AudioDevices.GetDefault().getId()), None)
        self.assertEqual(callback.OnDeviceAdded(None, self.AudioDevices.GetDefault().getId()), None)
        self.assertEqual(callback.OnDefaultDeviceChanged(None, int(self.AudioEndpointControl.Render), int(self.AudioEndpointControl.Console), self.AudioDevices.GetDefault().getId()), None)
        self.assertEqual(callback.OnPropertyValueChanged(None, self.AudioDevices.GetDefault().getId(), None), None)

        callback = CMMNotificationClient(MMNotificationClientTest(), self.AudioDevices)

        item = NotificationQueue.get(True, 30)
        self.assertEqual(int(item[1]), int(self.AudioEndpointControl.Render))
        self.assertEqual(int(item[2]), int(self.AudioEndpointControl.Console))
        self.assertEqual(item[3].getId(), self.AudioDevices.GetDefault().getId())
        self.assertEqual(callback.OnDefaultDeviceChanged(None, int(item[1]), int(item[2]), item[3].getId()), None)
        NotificationQueue.task_done()

        item = NotificationQueue.get(True, 30)
        self.assertEqual(int(item[1]), int(self.AudioEndpointControl.Render))
        self.assertEqual(int(item[2]), int(self.AudioEndpointControl.Multimedia))
        self.assertEqual(item[3].getId(), self.AudioDevices.GetDefault().getId())
        self.assertEqual(callback.OnDefaultDeviceChanged(None, int(item[1]), int(item[2]), item[3].getId()), None)
        NotificationQueue.task_done()

        NotificationQueue.join()


class TestAudioEndpoint(unittest.TestCase):

    def setUp(self):
        import AudioEndpointControl
        self.AudioEndpointControl = AudioEndpointControl
        self.AudioDevices = AudioEndpointControl.AudioEndpoints()
        self.AudioDevice = self.AudioDevices.GetDefault()

    def test_init(self):
        pass

    def test_isDefault(self):
        from AudioEndpointControl import Console, Render
        self.assertEqual(self.AudioDevice.isDefault(
            role=Console, dataFlow=Render), True)

    def test_Methods(self):
        self.assertEqual(type(self.AudioDevice.GetMute()), bool)
        SaveOld = self.AudioDevice.GetMute()
        self.AudioDevice.SetMute(not SaveOld)
        self.assertEqual(self.AudioDevice.GetMute(), not SaveOld)
        self.AudioDevice.volume = SaveOld
        self.assertEqual(self.AudioDevice.GetMute(), SaveOld)

        self.assertEqual(type(float(self.AudioDevice.volume)), float)
        SaveOld = float(self.AudioDevice.volume)
        self.AudioDevice.volume = SaveOld / 2
        self.assertAlmostEqual(
            float(self.AudioDevice.volume), SaveOld / 2, places=6)
        self.AudioDevice.volume = SaveOld
        self.assertAlmostEqual(
            float(self.AudioDevice.volume), SaveOld, places=6)

        self.assertEqual(type(self.AudioDevice.getName()), unicode)
        self.assertEqual(type(unicode(self.AudioDevice)), unicode)
        self.assertEqual(type(str(self.AudioDevice)), str)
        self.assertEqual(type(self.AudioDevice.getId()), unicode)
        self.assertEqual(type(self.AudioDevice.getState()), long)
        self.assertEqual(type(self.AudioDevice.GetMute()), bool)

    def test_Notificatios(self):
        with self.assertRaises(Exception):
            self.AudioDevice.RegisterCallback(None)
        with self.assertRaises(Exception):
            self.AudioDevice.UnregisterCallback()

        import Queue
        NotificationQueue = Queue.Queue()

        import ctypes
        import copy
        class pNotifyClass(object):
            def __init__(self, cNotify):
                class contentsClass(object):
                    pass
                self.contents = contentsClass()
                self.contents.guidEventContext = copy.copy(cNotify.EventContext)
                self.contents.bMuted = cNotify.Muted
                self.contents.fMasterVolume = cNotify.MasterVolume
                self.contents.nChannels = cNotify.Channels
                self.contents.afChannelVolumes = (ctypes.c_float * len(cNotify.ChannelVolumes))(*cNotify.ChannelVolumes)

        class AudioEndpointVolumeCallback(object):
            def OnNotify(self, Notify, AudioDevice):
                NotificationQueue.put_nowait((pNotifyClass(Notify), AudioDevice))

        self.assertEqual(self.AudioDevice.RegisterCallback(
            AudioEndpointVolumeCallback()), None)

        SaveOld = float(self.AudioDevice.volume)

        import time
        time.sleep(1)
        self.AudioDevice.volume = SaveOld / 2
        time.sleep(1)

        self.assertEqual(self.AudioDevice.UnregisterCallback(), None)
        self.AudioDevice.volume = SaveOld

        item = NotificationQueue.get(True, 30)
        self.assertEqual(item[0].contents.guidEventContext, self.AudioDevices.EventContext)
        self.assertEqual(item[1].getId(), self.AudioDevices.GetDefault().getId())

        class AudioEndpointVolumeCallbackTest(object):
            def OnNotify(self, Notify, AudioDevice):
                pass

        from AudioEndpointControl.Notifications import CAudioEndpointVolumeCallback

        callback = CAudioEndpointVolumeCallback(AudioEndpointVolumeCallbackTest(), self.AudioDevices.GetDefault())
        self.assertEqual(callback.OnNotify(None, item[0]), None)

        NotificationQueue.task_done()


class TestAudioVolume(unittest.TestCase):

    def setUp(self):
        import AudioEndpointControl
        from AudioEndpointControl.AudioEndpoints import AudioVolume
        self.AudioEndpointControl = AudioEndpointControl
        self.AudioVolume = AudioVolume
        self.AudioDevices = AudioEndpointControl.AudioEndpoints()
        self.AudioDevice = self.AudioDevices.GetDefault()

    def test_init(self):
        self.assertEqual(type(self.AudioDevice.volume),
                         self.AudioVolume)

    def test_Mute(self):
        self.assertEqual(type(self.AudioDevice.volume.Mute), bool)
        SaveOld = self.AudioDevice.volume.Mute
        self.AudioDevice.volume.Mute = not SaveOld
        self.assertEqual(self.AudioDevice.volume.Mute, not SaveOld)
        self.AudioDevice.volume.Mute = SaveOld
        self.assertEqual(self.AudioDevice.volume.Mute, SaveOld)

    def test_Get(self):
        self.assertEqual(
            type(self.AudioDevice.volume.Get(Channel=0, Scalar=True)), float)
        self.assertEqual(
            type(self.AudioDevice.volume.Get(Channel=0, Scalar=False)), float)
        for channel in xrange(
                1, self.AudioDevice.volume.GetChannelCount() + 1):
            self.assertEqual(type(self.AudioDevice.volume.Get(
                Channel=channel, Scalar=True)), float)
            self.assertEqual(type(self.AudioDevice.volume.Get(
                Channel=channel, Scalar=False)), float)
            self.assertEqual(type(self.AudioDevice.volume[channel]), float)

    def test_Set(self):
        SaveOld = self.AudioDevice.volume.Mute
        self.AudioDevice.volume.Set(not SaveOld)
        self.assertEqual(self.AudioDevice.volume.Mute, not SaveOld)
        self.AudioDevice.volume.Set(SaveOld)
        self.assertEqual(self.AudioDevice.volume.Mute, SaveOld)

        SaveOld = self.AudioDevice.volume.Get(Channel=0)
        self.AudioDevice.volume.Set(SaveOld / 2)
        self.assertAlmostEqual(self.AudioDevice.volume.Get(
            Channel=0), SaveOld / 2, places=6)
        self.AudioDevice.volume.Set(SaveOld)
        self.assertAlmostEqual(self.AudioDevice.volume.Get(
            Channel=0), SaveOld, places=6)

        SaveOld = self.AudioDevice.volume.Get(Channel=0, Scalar=False)
        self.AudioDevice.volume.Set(SaveOld / 2, Scalar=False)
        self.assertAlmostEqual(self.AudioDevice.volume.Get(
            Channel=0, Scalar=False), SaveOld / 2, places=6)
        self.AudioDevice.volume.Set(SaveOld, Scalar=False)
        self.assertEqual(self.AudioDevice.volume.Get(
            Channel=0, Scalar=False), SaveOld)

        SaveOld = self.AudioDevice.volume.Get(
            Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=True)
        self.AudioDevice.volume.Set(
            SaveOld / 2,
            Channel=self.AudioDevice.volume.GetChannelCount(),
            Scalar=True)
        self.assertAlmostEqual(
            self.AudioDevice.volume.Get(
                Channel=self.AudioDevice.volume.GetChannelCount(),
                Scalar=True),
            SaveOld / 2,
            places=6)
        self.AudioDevice.volume.Set(
            SaveOld,
            Channel=self.AudioDevice.volume.GetChannelCount(),
            Scalar=True)
        self.assertAlmostEqual(
            self.AudioDevice.volume.Get(
                Channel=self.AudioDevice.volume.GetChannelCount(),
                Scalar=True),
            SaveOld,
            places=6)

        SaveOld = self.AudioDevice.volume.Get(
            Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=False)
        self.AudioDevice.volume.Set(
            SaveOld / 2,
            Channel=self.AudioDevice.volume.GetChannelCount(),
            Scalar=False)
        self.assertAlmostEqual(
            self.AudioDevice.volume.Get(
                Channel=self.AudioDevice.volume.GetChannelCount(),
                Scalar=False),
            SaveOld / 2,
            places=6)
        self.AudioDevice.volume.Set(
            SaveOld,
            Channel=self.AudioDevice.volume.GetChannelCount(),
            Scalar=False)
        self.assertEqual(
            self.AudioDevice.volume.Get(
                Channel=self.AudioDevice.volume.GetChannelCount(),
                Scalar=False),
            SaveOld)

    def test_Methods(self):
        self.assertEqual(type(self.AudioDevice.volume.GetChannelCount()), long)
        self.assertEqual(len(self.AudioDevice.volume),
                         self.AudioDevice.volume.GetChannelCount())
        self.assertEqual(
            str(self.AudioDevice.volume).partition(':')[0], b'Volume')
        self.assertEqual(
            unicode(self.AudioDevice.volume).partition(':')[0], u'Volume')
        self.assertEqual(self.AudioDevice.volume, self.AudioDevice.volume)
        self.assertEqual(type(float(self.AudioDevice.volume)), float)
        self.assertEqual(type(int(self.AudioDevice.volume)), int)

        SaveOld = self.AudioDevice.volume.Get()
        +self.AudioDevice.volume
        +self.AudioDevice.volume
        self.assertGreaterEqual(self.AudioDevice.volume, SaveOld)
        -self.AudioDevice.volume
        -self.AudioDevice.volume
        self.assertLessEqual(self.AudioDevice.volume, SaveOld)
        self.AudioDevice.volume = SaveOld

        self.assertEqual(type(self.AudioDevice.volume.GetRange()), tuple)
        self.assertEqual(len(self.AudioDevice.volume.GetRange()), 3)
        for value in self.AudioDevice.volume.GetRange():
            self.assertEqual(type(value), float)

        self.assertEqual(type(self.AudioDevice.volume.GetStepInfo()), tuple)
        self.assertEqual(len(self.AudioDevice.volume.GetStepInfo()), 2)
        for value in self.AudioDevice.volume.GetStepInfo():
            self.assertEqual(type(value), long)

        self.assertEqual(
            type(self.AudioDevice.volume.QueryHardwareSupport()), long)
        self.assertGreaterEqual(
            self.AudioDevice.volume.QueryHardwareSupport(), 0)
        self.assertLessEqual(self.AudioDevice.volume.QueryHardwareSupport(), 7)

#        def __ne__(self, other):
#        def __le__(self, other):


if __name__ == '__main__':
    unittest.main()
