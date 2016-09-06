from __future__ import print_function, unicode_literals, absolute_import
from . import COMObject as _COMObject, IAudioEndpointVolumeCallback
from ctypes import POINTER as _POINTER, c_float as _c_float, cast as _cast
import sys, traceback

class cNotify(object):
	def __init__(self, pNotify):
		self.EventContext = pNotify.contents.guidEventContext
		self.Muted = bool(pNotify.contents.bMuted)
		self.MasterVolume = pNotify.contents.fMasterVolume
		self.Channels = pNotify.contents.nChannels
		self.ChannelVolumes = []
		pfChannelVolumes = _cast(pNotify.contents.afChannelVolumes, _POINTER(_c_float))
		for channel in range(pNotify.contents.nChannels):
			self.ChannelVolumes.append(pfChannelVolumes[channel])

class CAudioEndpointVolumeCallback(_COMObject):
	_com_interfaces_=[IAudioEndpointVolumeCallback]

	def __init__(self, Callback, endpoint):
		self._Callback = Callback
		self._endpoint = endpoint
		_COMObject.__init__(self)

	def OnNotify(self, this, pNotify):
		try:
			self._Callback.OnNotify(cNotify(pNotify), self._endpoint)
		except:
			traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
	pass
	sys.exit()
