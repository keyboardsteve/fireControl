#!/usr/bin/env python


import wx

import gettext
import time

import OperatingMode
import Diagnostics
import Manual
import Sequencer


class FireControlFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        
        self.communicationStatus = "Failure"
        self.numberChannels = 128
        self.manualFireCols = 4
        self.manualFireRows = 4
        self.heartbeatPeriod = 500 # in milliseconds
        self.heartbeatTimer = wx.Timer(self)
        self.heartbeatTimer.Start(self.heartbeatPeriod, False)
        
        self.currentPanel = "Mode"
        
        self.button_Mode = wx.Button(self, wx.ID_ANY, _("Mode"))
        self.button_Diagnostics = wx.Button(self, wx.ID_ANY, _("Diagnostics"))
        self.button_Manual = wx.Button(self, wx.ID_ANY, _("Manual"))
        self.button_Sequencer = wx.Button(self, wx.ID_ANY, _("Sequencer"))
        
        self.panel_OperatingMode = OperatingMode.OperatingMode(self)
        self.operatingMode = self.panel_OperatingMode.operatingMode
        
        self.panel_Diagnostics = Diagnostics.Diagnostics(self)
        self.panel_Diagnostics.Hide()
        
        self.panel_Manual = Manual.Manual(self, numButtons=self.numberChannels, numCols=self.manualFireCols, numRows=self.manualFireRows)
        self.panel_Manual.Hide()
        
        self.panel_Sequencer = Sequencer.Sequencer(self)
        self.panel_Sequencer.Hide()

        self.FireControl_Frame_statusbar = self.CreateStatusBar(2)
        
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnButton_Navigation, self.button_Mode)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Navigation, self.button_Diagnostics)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Navigation, self.button_Manual)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Navigation, self.button_Sequencer)
        
        self.panel_OperatingMode.button_Safety.Bind(wx.EVT_BUTTON, self.OnButton_OperatingMode)
        self.panel_OperatingMode.button_Test.Bind(wx.EVT_BUTTON, self.OnButton_OperatingMode)
        self.panel_OperatingMode.button_Arm.Bind(wx.EVT_BUTTON, self.OnButton_OperatingMode)
        
        self.panel_Diagnostics.button_TestAll.Bind(wx.EVT_BUTTON, self.OnButton_TestAll)
        
        for button in self.panel_Manual.buttonList:
            self.Bind(wx.EVT_BUTTON, self.OnButton_Fire, button)
        
        self.Bind(wx.EVT_TIMER, self.OnTimer_Heartbeat, self.heartbeatTimer)
        

    def __set_properties(self):
        self.SetTitle(_("Fire Control"))
        self.SetSize((800, 480))
        self.FireControl_Frame_statusbar.SetStatusWidths([150, -1])

        # statusbar fields
        FireControl_Frame_statusbar_fields = [_("Communication: %s"%(self.communicationStatus)), _("Status: %s"%(self.operatingMode))]
        for i in range(len(FireControl_Frame_statusbar_fields)):
            self.FireControl_Frame_statusbar.SetStatusText(FireControl_Frame_statusbar_fields[i], i)

    def __do_layout(self):
        Sizer_Main = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Navigation = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Navigation")), wx.VERTICAL)
        Sizer_Navigation.Add(self.button_Mode, 1, wx.EXPAND, 0)
        Sizer_Navigation.Add(self.button_Diagnostics, 1, wx.EXPAND, 0)
        Sizer_Navigation.Add(self.button_Manual, 1, wx.EXPAND, 0)
        Sizer_Navigation.Add(self.button_Sequencer, 1, wx.EXPAND, 0)
        Sizer_Main.Add(Sizer_Navigation, 1, wx.EXPAND, 0)
        
        Sizer_Main.Add(self.panel_OperatingMode, 6, wx.EXPAND, 0)
        Sizer_Main.Add(self.panel_Diagnostics, 6, wx.EXPAND, 0)
        Sizer_Main.Add(self.panel_Manual, 6, wx.EXPAND, 0)
        Sizer_Main.Add(self.panel_Sequencer, 6, wx.EXPAND, 0)
        
        self.SetSizer(Sizer_Main)
        self.Layout()
#--------------BUTTON CALLBACKS----------------
    def OnButton_Navigation(self, event):
        self.currentPanel = event.GetEventObject().LabelText.strip()
        print "OnButton_Navigation: Panel changed to", self.currentPanel
        if self.currentPanel == "Mode":
            self.panel_Diagnostics.Hide()
            self.panel_Manual.Hide()
            self.panel_Sequencer.Hide()
            self.panel_OperatingMode.Show()
        elif self.currentPanel == "Diagnostics":
            self.panel_OperatingMode.Hide()
            self.panel_Manual.Hide()
            self.panel_Sequencer.Hide()
            self.panel_Diagnostics.Show()
        elif self.currentPanel == "Manual":
            self.panel_OperatingMode.Hide()
            self.panel_Diagnostics.Hide()
            self.panel_Sequencer.Hide()
            self.panel_Manual.Show()
        elif self.currentPanel == "Sequencer":
            self.panel_OperatingMode.Hide()
            self.panel_Diagnostics.Hide()
            self.panel_Manual.Hide()
            self.panel_Sequencer.Show()
        self.Layout()
        
    def OnButton_OperatingMode(self, event):
        print "OnButton_OperatingMode: Mode changed to", event.GetEventObject().LabelText.strip()
        self.operatingMode = event.GetEventObject().LabelText.strip()
        if self.operatingMode == "Arm":
            self.operatingMode = "Armed"
            wx.MessageBox('System is now armed.\nExcercise caution as all channels are active', 'Safety first...', wx.OK | wx.ICON_STOP)
        self.FireControl_Frame_statusbar.SetStatusText("Status: %s"%(self.operatingMode), 1)

    def OnButton_TestAll(self, event):
        self.panel_Diagnostics.gauge_TestAll.SetValue(0)
        self.panel_Diagnostics.text_ctrl_TestAll.Clear()
        testList = [True]*128
        testList[15] = False
        if self.operatingMode == "Safety":
            wx.MessageBox('System is in Safety.  Please change mode to "Test" to test all channels.', 'Safety first...', wx.OK)
        elif self.operatingMode == "Armed":
            wx.MessageBox('System is Armed.  Please change mode to "Test" to test all channels.', 'Safety first...', wx.OK | wx.ICON_ERROR)
        elif self.operatingMode == "Test":
            ###ADDCODE
            # This need to send the proper message and receive a result before moving onto the next test
            for channel in range(1, self.numberChannels + 1):
                print "OnButton_TestAll: Testing channel number", channel
                self.panel_Diagnostics.text_ctrl_TestAll.AppendText("Testing channel number %s "%(channel))
                if testList[channel-1]:
                    self.panel_Diagnostics.text_ctrl_TestAll.AppendText("PASS")
                    self.changeFireButtonColor(channel, "RED")
                else:
                    self.panel_Diagnostics.text_ctrl_TestAll.AppendText("FAIL")
                    self.changeFireButtonColor(channel, "GREEN")
                self.panel_Diagnostics.text_ctrl_TestAll.AppendText("\n")
                self.panel_Diagnostics.gauge_TestAll.SetValue(int(channel/self.numberChannels)*100)
            if all(testList):
                wx.MessageBox('Test Completed.  All channels passed!', 'Test Complete', wx.OK)
            else:
                wx.MessageBox('Test Completed.  Some channels failed!\nPlease check the logs for more information', 'Test Complete', wx.OK | wx.ICON_ERROR)

    def OnButton_Fire(self, event):
        if self.operatingMode == "Armed" or self.operatingMode == "Test":
            e = event.GetEventObject().LabelText.strip()
            print "OnButton_Fire: Fire Event for button", e
            self.writeToTxLog("Fire for channel %s"%(e))
            
#--------------CHECKBOX CALLBACKS----------------  
    def OnCheckbox_TxFilter(self, event):
        print "Toggling logging of TxHeartbeat messages"
        event.Skip()

    def OnCheckbox_RxFilter(self, event):
        print "Toggling logging of TxHeartbeat messages"
        event.Skip()
        
        
#--------------TIMER CALLBACKS----------------
    def OnTimer_Heartbeat(self, event):
        if not self.panel_Diagnostics.checkbox_TxLogFilter.IsChecked():
            self.writeToTxLog("Heartbeat message sent (Not really)")
            
#--------------HELPER FUNCTIONS----------------
    def writeToTxLog(self, msg):
        # Just adds the newline & helps me remember what I'm writing to...
        self.panel_Diagnostics.text_ctrl_TxLog.AppendText("%s-%s\n"%(time.strftime("%H:%M:%S", time.localtime()), msg))
        #self.text_ctrl_TxLog.AppendText(msg+'\n')
        
    def writeToRxLog(self, msg):
        # Just adds the newline & helps me remember what I'm writing to...
        self.panel_Diagnostics.text_ctrl_RxLog.AppendText("%s-%s\n"%(time.strftime("%H:%M:%S", time.localtime()), msg))
        #self.text_ctrl_RxLog.AppendText(msg+'\n')
    
    def changeFireButtonColor(self, number, color):
        self.panel_Manual.buttonList[number-1].SetBackgroundColour(wx.NamedColour('%s'%(color)))
    
class FireControl(wx.App):
    def OnInit(self):
        FireControl_Frame = FireControlFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(FireControl_Frame)
        FireControl_Frame.Show()
        return True

# end of class FireControl

if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = FireControl(0)
    app.MainLoop()