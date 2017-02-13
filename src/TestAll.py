import wx
import time
import threading

class TestAll(threading.Thread):
    def __init__(self, notifyWindow, buttons, eventObj):
        threading.Thread.__init__(self)
        self.buttons = buttons
        self.done = False
        self.next = False
        self.parent = notifyWindow
        self.testList = []
        self.nextButton = None
        self.eventObj = eventObj
        #print "OK"

    
    def run(self):
        self.next = False
        self.buttonGenerator = self.getNextButton()
        self.nextButton = self.buttonGenerator.next()
        '''
        while True:
            if self.nextButton is not None:
                if self.nextButton == "Done":
                    break
                else:
                    self.sendFire(self.nextButton)

        '''
        
        for button in self.buttons:
            self.sendFire(button)
            self.eventObj.clear()
            self.eventObj.wait()
            
    def getNextButton(self):
        for button in self.buttons:
            yield button

    def sendFire(self, button):
        e = wx.CommandEvent(wx.EVT_BUTTON.evtType[0], button.GetId())
        e.SetEventObject(button)
        wx.PostEvent(self.parent.GetEventHandler(), e)
        #print "Button", button.GetLabel()
        self.nextButton = None

    def setResult(self, msg):
        #print "setREsult", msg
        if msg[-1] == '1':
            self.testList.append(True)
        else:
            self.testList.append(False)
        try:
            self.nextButton = self.buttonGenerator.next()
        except StopIteration:
            self.nextButton = "Done"
        
    def getResults(self):
        return self.testList
    
    def reset(self):
        self.testList = []
        self.nextButton = None
        self.buttonGenerator = self.getNextButton()
        