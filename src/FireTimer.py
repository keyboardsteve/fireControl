import wx
from twisted.conch.ssh import channel

class FireTimer(wx.Timer):
    
    #def __init__(self, parent, seqName, channel, delay):
    def __init__(self, parent, channel, delay):
        wx.Timer.__init__(self, owner=parent)
        
        self.channel = channel
        self.delay = delay
        #self.seqName = seqName
    
    def GetChannel(self):
        return self.channel
    
    def GetDelay(self):
        return self.delay
    '''
    def GetSequencerName(self):
        return self.seqName
    '''