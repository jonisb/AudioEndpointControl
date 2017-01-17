import unittest

#import AudioEndpointControl
#from AudioEndpointControl.MMConstants import Render, Capture, All
#from AudioEndpointControl.MMConstants import Console, Multimedia, Communications
#from AudioEndpointControl.MMConstants import DEVICE_STATE_ACTIVE, DEVICE_STATE_DISABLED, DEVICE_STATE_NOTPRESENT, DEVICE_STATE_UNPLUGGED, DEVICE_STATEMASK_ALL
#from AudioEndpointControl.MMConstants import PKEY_Device_FriendlyName, PKEY_Device_DeviceDesc, PKEY_DeviceInterface_FriendlyName
class TestAudioEndpoints(unittest.TestCase):
    def test_init(self):
        import AudioEndpointControl
        AudioDevices = AudioEndpointControl.AudioEndpoints()

        self.assertEqual(type(AudioDevices), AudioEndpointControl.AudioEndpoints)


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
        self.assertEqual(float(self.AudioDevices.GetDefault().volume), SaveOld / 2)
        self.AudioDevices.GetDefault().volume = SaveOld
        self.assertEqual(float(self.AudioDevices.GetDefault().volume), SaveOld)


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

    def test_Get(self):
        self.assertEqual(type(self.AudioDevice.volume.Get(Channel=0)), float)
        for channel in xrange(1, self.AudioDevice.volume.GetChannelCount() + 1):
            self.assertEqual(type(self.AudioDevice.volume.Get(Channel=channel)), float)

    def test_Set(self):
        SaveOld = self.AudioDevice.volume.Mute
        self.AudioDevice.volume.Set(not SaveOld)
        self.assertEqual(self.AudioDevice.volume.Mute, not SaveOld)
        self.AudioDevice.volume.Set(SaveOld)
        self.assertEqual(self.AudioDevice.volume.Mute, SaveOld)

        SaveOld = self.AudioDevice.volume.Get(Channel=0)
        self.AudioDevice.volume.Set(SaveOld / 2)
        self.assertEqual(self.AudioDevice.volume.Get(Channel=0), SaveOld / 2)
        self.AudioDevice.volume.Set(SaveOld)
        self.assertEqual(self.AudioDevice.volume.Get(Channel=0), SaveOld)

        SaveOld = self.AudioDevice.volume.Get(Channel=self.AudioDevice.volume.GetChannelCount())
        self.AudioDevice.volume.Set(SaveOld / 2, Channel=self.AudioDevice.volume.GetChannelCount())
        self.assertEqual(self.AudioDevice.volume.Get(Channel=self.AudioDevice.volume.GetChannelCount()), SaveOld / 2)
        self.AudioDevice.volume.Set(SaveOld, Channel=self.AudioDevice.volume.GetChannelCount())
        self.assertEqual(self.AudioDevice.volume.Get(Channel=self.AudioDevice.volume.GetChannelCount()), SaveOld)

#        self.assertEqual(type(self.AudioDevices.GetDefault().GetMute()), bool)
#        SaveOld = self.AudioDevices.GetDefault().GetMute()
#        self.AudioDevices.GetDefault().volume = not SaveOld
#        self.AudioDevices.GetDefault().volume = SaveOld
#        self.assertEqual(self.AudioDevices.GetDefault().GetMute(), SaveOld)
    def test_Methods(self):
        self.assertEqual(type(self.AudioDevice.volume.GetChannelCount()), long)
        self.assertEqual(len(self.AudioDevice.volume), self.AudioDevice.volume.GetChannelCount())
        for channel in xrange(1, self.AudioDevice.volume.GetChannelCount()+1):
            self.assertEqual(type(self.AudioDevice.volume.Get(Channel=channel, Scalar=True)), float)
            self.assertEqual(type(self.AudioDevice.volume.Get(Channel=channel, Scalar=False)), float)
            self.assertEqual(type(self.AudioDevice.volume[channel]), float)
        self.assertEqual(str(self.AudioDevice.volume).partition(':')[0], b'Volume')
        self.assertEqual(unicode(self.AudioDevice.volume).partition(':')[0], u'Volume')
        self.assertEqual(self.AudioDevice.volume, self.AudioDevice.volume)

        self.assertEqual(type(float(self.AudioDevice.volume)), float)
        self.assertEqual(type(int(self.AudioDevice.volume)), int)

        #print(AudioDevice.volume.QueryHardwareSupport())
        #print(AudioDevice.volume.GetStepInfo())
        #print(AudioDevice.volume.GetRange())
#        def Set(self, fLevelDB, nChannel=0, Scalar=True):
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
#        __pos__ = __add__
#        __neg__ = __add__

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