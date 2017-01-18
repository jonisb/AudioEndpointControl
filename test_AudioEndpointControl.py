# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import

import unittest

#import AudioEndpointControl
#from AudioEndpointControl.MMConstants import Render, Capture, All
#from AudioEndpointControl.MMConstants import Console, Multimedia, Communications
#from AudioEndpointControl.MMConstants import DEVICE_STATE_ACTIVE, DEVICE_STATE_DISABLED, DEVICE_STATE_NOTPRESENT, DEVICE_STATE_UNPLUGGED, DEVICE_STATEMASK_ALL
#from AudioEndpointControl.MMConstants import PKEY_Device_FriendlyName, PKEY_Device_DeviceDesc, PKEY_DeviceInterface_FriendlyName


class TestConstants(unittest.TestCase):
    def test_init(self):
        from AudioEndpointControl.MMConstants import Render

        self.assertEqual(str(Render), b'Render')


class TestAudioEndpoints(unittest.TestCase):
    def setUp(self):
        import AudioEndpointControl
        self.AudioEndpointControl = AudioEndpointControl
        self.AudioDevices = AudioEndpointControl.AudioEndpoints()

    def test_init(self):
        self.assertEqual(type(self.AudioDevices), self.AudioEndpointControl.AudioEndpoints)

    def test_Methods(self):
        self.assertEqual(type(len(self.AudioDevices)), int)


class TestAudioEndpoint(unittest.TestCase):
    def setUp(self):
        import AudioEndpointControl
        self.AudioEndpointControl = AudioEndpointControl
        self.AudioDevices = AudioEndpointControl.AudioEndpoints()

    def test_init(self):
        self.assertEqual(type(self.AudioDevices.GetDefault()), self.AudioEndpointControl.AudioEndpoint)

    def test_Methods(self):
        self.assertEqual(type(self.AudioDevices.GetDefault().GetMute()), bool)
        SaveOld = self.AudioDevices.GetDefault().GetMute()
        self.AudioDevices.GetDefault().volume = not SaveOld
        self.assertEqual(self.AudioDevices.GetDefault().GetMute(), not SaveOld)
        self.AudioDevices.GetDefault().volume = SaveOld
        self.assertEqual(self.AudioDevices.GetDefault().GetMute(), SaveOld)

        self.assertEqual(type(float(self.AudioDevices.GetDefault().volume)), float)
        SaveOld = float(self.AudioDevices.GetDefault().volume)
        self.AudioDevices.GetDefault().volume = SaveOld / 2
        self.assertAlmostEqual(float(self.AudioDevices.GetDefault().volume), SaveOld / 2, places=6)
        self.AudioDevices.GetDefault().volume = SaveOld
        self.assertAlmostEqual(float(self.AudioDevices.GetDefault().volume), SaveOld, places=6)


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
#        self.assertAlmostEqual(self.AudioDevice.volume.Get(Channel=0), SaveOld )
#
#
#        self.AudioDevice.volume.Set(SaveOld / 2)
#        self.assertAlmostEqual(self.AudioDevice.volume.Get(Channel=0), SaveOld / 2)
#        self.AudioDevice.volume.Set(SaveOld)
#        self.assertEqual(self.AudioDevice.volume.Get(Channel=0), SaveOld)

        #print(AudioDevice.volume.QueryHardwareSupport())
        #print(AudioDevice.volume.GetStepInfo())
        #print(AudioDevice.volume.GetRange())
#        __pos__ = __add__
#        __neg__ = __add__
#        def StepDown(self):
#        def StepUp(self):
#        def QueryHardwareSupport(self):
#        def RegisterControlChangeNotify(self, callback):
#        def UnregisterControlChangeNotify(self):
#        def __add__(self, other=1):
#        def __sub__(self, other=1):
#        @Mute.setter
#        def Mute(self, bMute):
#        def __ne__(self, other):
#        __setitem__ = _partial(Set, Scalar=True)

#class TestStringMethods(unittest.TestCase):
#
#    def test_isupper(self):
#        self.assertTrue('FOO'.isupper())
#        self.assertFalse('Foo'.isupper())
#
#    def test_split(self):
#        s = 'hello world'
#        self.assertEqual(s.split(), ['hello', 'world'])
#        # check that s.split fails when the separator is not a string
#        with self.assertRaises(TypeError):
#            s.split(2)

if __name__ == '__main__':
    unittest.main()
