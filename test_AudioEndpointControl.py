# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import

import unittest


class TestConstants(unittest.TestCase):
    def test_init(self):
        from AudioEndpointControl.MMConstants import Render, Capture, All
        from AudioEndpointControl.MMConstants import Console, Multimedia, Communications
        from AudioEndpointControl.MMConstants import DEVICE_STATE_ACTIVE, DEVICE_STATE_DISABLED, DEVICE_STATE_NOTPRESENT, DEVICE_STATE_UNPLUGGED, DEVICE_STATEMASK_ALL
        #from AudioEndpointControl.MMConstants import PKEY_Device_FriendlyName, PKEY_Device_DeviceDesc, PKEY_DeviceInterface_FriendlyName

        self.assertEqual(str(Render), b'Render')
        self.assertEqual(str(Capture), b'Capture')
        self.assertEqual(str(All), b'All')

        self.assertEqual(str(Console), b'Console')
        self.assertEqual(str(Multimedia), b'Multimedia')
        self.assertEqual(str(Communications), b'Communications')

        self.assertEqual(str(DEVICE_STATE_ACTIVE), b'DEVICE_STATE_ACTIVE')
        self.assertEqual(str(DEVICE_STATE_DISABLED), b'DEVICE_STATE_DISABLED')
        self.assertEqual(str(DEVICE_STATE_NOTPRESENT), b'DEVICE_STATE_NOTPRESENT')
        self.assertEqual(str(DEVICE_STATE_UNPLUGGED), b'DEVICE_STATE_UNPLUGGED')
        self.assertEqual(str(DEVICE_STATEMASK_ALL), b'DEVICE_STATEMASK_ALL')


class TestAudioEndpoints(unittest.TestCase):
    def setUp(self):
        import AudioEndpointControl
        self.AudioEndpointControl = AudioEndpointControl
        self.AudioDevices = AudioEndpointControl.AudioEndpoints()

    def test_init(self):
        self.assertEqual(type(self.AudioDevices), self.AudioEndpointControl.AudioEndpoints)

    def test_GetDefault(self):
        self.assertEqual(type(self.AudioDevices.GetDefault()), self.AudioEndpointControl.AudioEndpoint)

    def test_Methods(self):
        self.assertEqual(type(len(self.AudioDevices)), int)


class TestAudioEndpoint(unittest.TestCase):
    def setUp(self):
        import AudioEndpointControl
        self.AudioEndpointControl = AudioEndpointControl
        self.AudioDevices = AudioEndpointControl.AudioEndpoints()
        self.AudioDevice = self.AudioDevices.GetDefault()

    def test_init(self):
        pass

    def test_isDefault(self):
        from AudioEndpointControl.MMConstants import Console, Render
        self.assertEqual(self.AudioDevice.isDefault(role=Console, dataFlow=Render), True)

    def test_Methods(self):
        self.assertEqual(type(self.AudioDevice.GetMute()), bool)
        SaveOld = self.AudioDevice.GetMute()
        self.AudioDevice.volume = not SaveOld
        self.assertEqual(self.AudioDevice.GetMute(), not SaveOld)
        self.AudioDevice.volume = SaveOld
        self.assertEqual(self.AudioDevice.GetMute(), SaveOld)

        self.assertEqual(type(float(self.AudioDevice.volume)), float)
        SaveOld = float(self.AudioDevice.volume)
        self.AudioDevice.volume = SaveOld / 2
        self.assertAlmostEqual(float(self.AudioDevice.volume), SaveOld / 2, places=6)
        self.AudioDevice.volume = SaveOld
        self.assertAlmostEqual(float(self.AudioDevice.volume), SaveOld, places=6)

#def getName(self):
#def getId(self):
#def getState(self):
#def GetVolumeRange(self):
#def GetMasterVolumeLevel(self, Scalar=True):
#def GetChannelVolumeLevel(self, nChannel, Scalar=True):
#def GetMute(self):
#def GetChannelCount(self):
#def GetVolumeStepInfo(self):
#
#def SetMasterVolumeLevel(self, fLevelDB, Scalar=True):
#def SetChannelVolumeLevel(self, nChannel, fLevelDB, Scalar=True):
#def SetMute(self, bMute):
#def VolumeStepDown(self):
#def VolumeStepUp(self):
#def __eq__(self, other):
#def __ne__(self, other):

class TestAudioVolume(unittest.TestCase):
    def setUp(self):
        import AudioEndpointControl
        self.AudioEndpointControl = AudioEndpointControl
        self.AudioDevices = AudioEndpointControl.AudioEndpoints()
        self.AudioDevice = self.AudioDevices.GetDefault()

    def test_init(self):
        self.assertEqual(type(self.AudioDevice.volume), self.AudioEndpointControl.AudioVolume)

    def test_Mute(self):
        self.assertEqual(type(self.AudioDevice.volume.Mute), bool)
        SaveOld = self.AudioDevice.volume.Mute
        self.AudioDevice.volume.Mute = not SaveOld
        self.assertEqual(self.AudioDevice.volume.Mute, not SaveOld)
        self.AudioDevice.volume.Mute = SaveOld
        self.assertEqual(self.AudioDevice.volume.Mute, SaveOld)

    def test_Get(self):
        self.assertEqual(type(self.AudioDevice.volume.Get(Channel=0, Scalar=True)), float)
        self.assertEqual(type(self.AudioDevice.volume.Get(Channel=0, Scalar=False)), float)
        for channel in xrange(1, self.AudioDevice.volume.GetChannelCount() + 1):
            self.assertEqual(type(self.AudioDevice.volume.Get(Channel=channel, Scalar=True)), float)
            self.assertEqual(type(self.AudioDevice.volume.Get(Channel=channel, Scalar=False)), float)
            self.assertEqual(type(self.AudioDevice.volume[channel]), float)

    def test_Set(self):
        SaveOld = self.AudioDevice.volume.Mute
        self.AudioDevice.volume.Set(not SaveOld)
        self.assertEqual(self.AudioDevice.volume.Mute, not SaveOld)
        self.AudioDevice.volume.Set(SaveOld)
        self.assertEqual(self.AudioDevice.volume.Mute, SaveOld)

        SaveOld = self.AudioDevice.volume.Get(Channel=0)
        self.AudioDevice.volume.Set(SaveOld / 2)
        self.assertAlmostEqual(self.AudioDevice.volume.Get(Channel=0), SaveOld / 2, places=6)
        self.AudioDevice.volume.Set(SaveOld)
        self.assertAlmostEqual(self.AudioDevice.volume.Get(Channel=0), SaveOld, places=6)

        SaveOld = self.AudioDevice.volume.Get(Channel=0, Scalar=False)
        self.AudioDevice.volume.Set(SaveOld / 2, Scalar=False)
        self.assertAlmostEqual(self.AudioDevice.volume.Get(Channel=0, Scalar=False), SaveOld / 2, places=6)
        self.AudioDevice.volume.Set(SaveOld, Scalar=False)
        self.assertEqual(self.AudioDevice.volume.Get(Channel=0, Scalar=False), SaveOld)

        SaveOld = self.AudioDevice.volume.Get(Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=True)
        self.AudioDevice.volume.Set(SaveOld / 2, Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=True)
        self.assertAlmostEqual(self.AudioDevice.volume.Get(Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=True), SaveOld / 2, places=6)
        self.AudioDevice.volume.Set(SaveOld, Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=True)
        self.assertAlmostEqual(self.AudioDevice.volume.Get(Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=True), SaveOld, places=6)

        SaveOld = self.AudioDevice.volume.Get(Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=False)
        self.AudioDevice.volume.Set(SaveOld / 2, Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=False)
        self.assertEqual(self.AudioDevice.volume.Get(Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=False), SaveOld / 2)
        self.AudioDevice.volume.Set(SaveOld, Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=False)
        self.assertEqual(self.AudioDevice.volume.Get(Channel=self.AudioDevice.volume.GetChannelCount(), Scalar=False), SaveOld)

    def test_Methods(self):
        self.assertEqual(type(self.AudioDevice.volume.GetChannelCount()), long)
        self.assertEqual(len(self.AudioDevice.volume), self.AudioDevice.volume.GetChannelCount())
        self.assertEqual(str(self.AudioDevice.volume).partition(':')[0], b'Volume')
        self.assertEqual(unicode(self.AudioDevice.volume).partition(':')[0], u'Volume')
        self.assertEqual(self.AudioDevice.volume, self.AudioDevice.volume)
        self.assertEqual(type(float(self.AudioDevice.volume)), float)
        self.assertEqual(type(int(self.AudioDevice.volume)), int)

        SaveOld = self.AudioDevice.volume.Get()
        +self.AudioDevice.volume
        self.assertGreaterEqual(self.AudioDevice.volume, SaveOld)
        -self.AudioDevice.volume
        self.assertLessEqual(float(self.AudioDevice.volume), SaveOld)
        self.AudioDevice.volume = SaveOld

        self.assertEqual(type(self.AudioDevice.volume.GetRange()), tuple)
        self.assertEqual(len(self.AudioDevice.volume.GetRange()), 3)
        for value in self.AudioDevice.volume.GetRange():
            self.assertEqual(type(value), float)

        self.assertEqual(type(self.AudioDevice.volume.GetStepInfo()), tuple)
        self.assertEqual(len(self.AudioDevice.volume.GetStepInfo()), 2)
        for value in self.AudioDevice.volume.GetStepInfo():
            self.assertEqual(type(value), long)

        self.assertEqual(type(self.AudioDevice.volume.QueryHardwareSupport()), long)
        self.assertGreaterEqual(self.AudioDevice.volume.QueryHardwareSupport(), 0)
        self.assertLessEqual(self.AudioDevice.volume.QueryHardwareSupport(), 7)

#        def RegisterControlChangeNotify(self, callback):
#        def UnregisterControlChangeNotify(self):
#        def __ne__(self, other):
#        def __le__(self, other):

#class TestStringMethods(unittest.TestCase):
#    def test_split(self):
#        s = 'hello world'
#        self.assertEqual(s.split(), ['hello', 'world'])
#        # check that s.split fails when the separator is not a string
#        with self.assertRaises(TypeError):
#            s.split(2)

if __name__ == '__main__':
    unittest.main()
