
import wx
import gettext
import string
import SequencerProgram

class Sequencer(wx.Panel):
    def __init__(self, parent, numSequencers):
        wx.Panel.__init__(self, parent=parent)
        self.numSequencers = numSequencers
        
        self.masterTimerDecoder = []
        self.buttonList = []
        self.sequencerList = []
        self.panelList = []
        
        for i in range(self.numSequencers):
            name = string.ascii_uppercase[i]
            self.buttonList.append(wx.Button(self, wx.ID_ANY, _("%s"%(name))))
            self.panelList.append(SequencerProgram.SequencerProgram(self, name = name))

        self.defaultColor = self.buttonList[0].GetBackgroundColour()
        
        for panel in self.panelList:
            panel.Hide()
        self.panelList[0].Show()

        self.__set_properties()
        self.__do_layout()
        
        for i in range(self.numSequencers):
            self.Bind(wx.EVT_BUTTON, self.OnButton_Bank, self.buttonList[i])

    def __set_properties(self):
        # begin wxGlade: Sequencer.__set_properties
        for button in self.buttonList:
            button.SetBackgroundColour(self.defaultColor)
        #self.button_Sequencer_BankA.SetBackgroundColour(wx.NamedColour('YELLOW'))
        self.buttonList[0].SetBackgroundColour(wx.NamedColour('YELLOW'))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Sequencer.__do_layout
        sizer_Outer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Sequencer")), wx.HORIZONTAL)
        sizer_BankSelect = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Bank Select")), wx.VERTICAL)
        for i in range(self.numSequencers):
            sizer_BankSelect.Add(self.buttonList[i], 1, wx.EXPAND, 0)

        sizer_Outer.Add(sizer_BankSelect, 1, wx.EXPAND, 0)

        for panel in self.panelList:
            sizer_Outer.Add(panel, 6, wx.EXPAND, 0)
        
        self.SetSizer(sizer_Outer)
        sizer_Outer.Fit(self)
        self.Layout()
    
    def OnButton_Bank(self, event):
        id = event.GetEventObject().GetId()
        for panel in self.panelList:
            panel.Hide()
        for button in self.buttonList:
            button.SetBackgroundColour(self.defaultColor)
            
        for idx, button in enumerate(self.buttonList):
            if button.GetId() == id:
                button.SetBackgroundColour(wx.NamedColour('YELLOW'))
                self.panelList[idx].Show()
                print "OnButton_Bank: Showing Panel %s"%(string.ascii_uppercase[idx])
                break
        self.Layout()
