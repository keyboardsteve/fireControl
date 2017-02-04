#!/usr/bin/env python


import wx
from wx.lib.pubsub import pub

import gettext
import time
import os

import SerialComs # For xbee connection

import OperatingMode
import Diagnostics
import Manual
import Sequencer
import EditSequencer
import FireTimer


class FireControlFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        
        self.communicationStatus = "Failure"
        self.numberFireChannels = 128
        self.manualFireCols = 4
        self.manualFireRows = 4
        self.heartbeatPeriod = 500 # in milliseconds
        self.heartbeatTimer = wx.Timer(self)
        self.heartbeatTimer.Start(self.heartbeatPeriod, False)
        self.numSequencers = 4
        
        self.serial = SerialComs.SerialComs(handler = "Receive_Coms")
        
        self.remoteOperatingMode = "Unknown"
                
        self.testList = [None]*self.numberFireChannels
        self.currentPanel = "Mode"
        
        self.button_Mode = wx.Button(self, wx.ID_ANY, _("Mode"))
        self.button_Diagnostics = wx.Button(self, wx.ID_ANY, _("Diagnostics"))
        self.button_Manual = wx.Button(self, wx.ID_ANY, _("Manual"))
        self.button_Sequencer = wx.Button(self, wx.ID_ANY, _("Sequencer"))
        self.defaultColor = self.button_Sequencer.GetBackgroundColour()
        
        self.modeButtonList = [self.button_Mode,
                               self.button_Diagnostics,
                               self.button_Manual,
                               self.button_Sequencer]
        
        self.panel_OperatingMode = OperatingMode.OperatingMode(self)
        self.panel_Diagnostics = Diagnostics.Diagnostics(self)
        self.panel_Manual = Manual.Manual(self, numButtons=self.numberFireChannels, numCols=self.manualFireCols, numRows=self.manualFireRows)
        self.panel_Sequencer = Sequencer.Sequencer(self, self.numSequencers)
        self.modePanelList = [self.panel_OperatingMode,
                              self.panel_Diagnostics,
                              self.panel_Manual,
                              self.panel_Sequencer]
        
        self.operatingMode = self.panel_OperatingMode.operatingMode
        self.FireControl_Frame_statusbar = self.CreateStatusBar(3)
        
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

        for sequencer in self.panel_Sequencer.panelList:
            self.Bind(wx.EVT_BUTTON, self.OnButton_Play, sequencer.button_Sequencer_Play)
            self.Bind(wx.EVT_BUTTON, self.OnButton_Add, sequencer.editWindow.button_Add)
            self.Bind(wx.EVT_BUTTON, self.OnButton_Remove, sequencer.editWindow.button_Remove)
            sequencer.button_Sequencer_Stop.Disable()
            sequencer.button_Sequencer_Reset.Disable()
        
        self.Bind(wx.EVT_BUTTON, self.propegateButtonLabelChanges, self.panel_Manual.renamePanel.button_OK)
        
        self.Bind(wx.EVT_TIMER, self.OnTimer_Heartbeat, self.heartbeatTimer)
        
        
        self.subcsriber_Coms = pub.subscribe(self.OnPubSub_Coms, "Receive_Coms")

    def __set_properties(self):
        self.SetTitle(_("Fire Control"))
        self.SetSize((800, 480))
        self.FireControl_Frame_statusbar.SetStatusWidths([200, 200, -1])
        
        for panel in self.modePanelList:
            panel.Hide()
        self.modePanelList[0].Show()
        
        for button in self.modeButtonList:
            button.SetBackgroundColour(self.defaultColor)
        self.modeButtonList[0].SetBackgroundColour(wx.NamedColour('YELLOW'))

        # statusbar fields
        FireControl_Frame_statusbar_fields = [_("Communication: %s"%(self.communicationStatus)), 
                                              _("Local Mode: %s"%(self.operatingMode)),
                                              _("Remote Mode: %s"%(self.remoteOperatingMode))]
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
        for panel in self.modePanelList:
            panel.Hide()
        for button in self.modeButtonList:
            button.SetBackgroundColour(self.defaultColor)
        if self.currentPanel == "Mode":
            self.panel_OperatingMode.Show()
            self.button_Mode.SetBackgroundColour(wx.NamedColour('YELLOW'))
        elif self.currentPanel == "Diagnostics":
            self.panel_Diagnostics.Show()
            self.button_Diagnostics.SetBackgroundColour(wx.NamedColour('YELLOW'))
        elif self.currentPanel == "Manual":
            self.panel_Manual.Show()
            self.button_Manual.SetBackgroundColour(wx.NamedColour('YELLOW'))
        elif self.currentPanel == "Sequencer":
            self.panel_Sequencer.Show()
            self.button_Sequencer.SetBackgroundColour(wx.NamedColour('YELLOW'))
        self.Layout()
        
    def OnButton_OperatingMode(self, event):
        print "OnButton_OperatingMode: Mode changed to", event.GetEventObject().LabelText.strip()
        self.operatingMode = event.GetEventObject().LabelText.strip()
        if self.operatingMode == "Safety":
            self.serial.send("M0")
        elif self.operatingMode == "Test":
            self.serial.send("M1")
        elif self.operatingMode == "Arm":
            self.operatingMode = "Armed"
            wx.MessageBox('System is now armed.\nExcercise caution as all channels are active', 'Safety first...', wx.OK | wx.ICON_STOP)
            self.serial.send("M2")
        self.FireControl_Frame_statusbar.SetStatusText("Local Mode: %s"%(self.operatingMode), 1)

    def OnButton_TestAll(self, event):
        self.panel_Diagnostics.gauge_TestAll.SetValue(0)
        self.panel_Diagnostics.text_ctrl_TestAll.Clear()
        
        self.testList = [None]*self.numberFireChannels
        
        if self.operatingMode == "Safety":
            wx.MessageBox('System is in Safety.  Please change mode to "Test" to test all channels.', 'Safety first...', wx.OK)
        elif self.operatingMode == "Armed":
            wx.MessageBox('System is Armed.  Please change mode to "Test" to test all channels.', 'Safety first...', wx.OK | wx.ICON_ERROR)
        elif self.operatingMode == "Test":
            ###ADDCODE
            # This need to send the proper message and receive a result before moving onto the next test
            if self.remoteOperatingMode == "Test":
                for channel in range(1, self.numberFireChannels + 1):
                    print "OnButton_TestAll: Testing channel number", channel
                    self.panel_Diagnostics.text_ctrl_TestAll.AppendText("Testing channel number %s "%(channel))

                    self.serial.send("F%s"%(channel))
                    done = False
                    
                    '''
                    if self.testList[channel-1]:
                        self.panel_Diagnostics.text_ctrl_TestAll.AppendText("PASS")
                        self.changeFireButtonColor(channel, "GREEN")
                    else:
                        self.panel_Diagnostics.text_ctrl_TestAll.AppendText("FAIL")
                        self.changeFireButtonColor(channel, "RED")
                    '''
                        
                    self.panel_Diagnostics.text_ctrl_TestAll.AppendText("\n")
                    self.panel_Diagnostics.gauge_TestAll.SetValue(int(float(channel)/float(self.numberFireChannels)*100.0))
                if all(testList):
                    wx.MessageBox('Test Completed.  All channels passed!', 'Test Complete', wx.OK)
                else:
                    failedChannels = [self.testList.index(x)+1 for x in self.testList if x == False]
                    wx.MessageBox('Test Completed.  Some channels failed!\nPlease check the logs for more information.\n\
                                   Failed channels: %s', 'Test Complete'%(','.join(failedChannels)), wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox('Test aborted.  The local and remote system mode are out of sync', 'Modes out of sync', wx.OK | wx.ICON_ERROR)

    def OnButton_Fire(self, event):
        if self.operatingMode == "Armed" or self.operatingMode == "Test":
            e = event.GetEventObject().GetId()
            if self.operatingMode == self.remoteOperatingMode:
                print "OnButton_Fire: Fire Event for button", e
                self.writeToTxLog("Fire for channel %s"%(e))
                self.serial.send("F%s"%(e))
            else:
                wx.MessageBox('Fire aborted.  The local and remote system mode are out of sync', 'Modes out of sync', wx.OK | wx.ICON_ERROR)

    def OnButton_Play(self, event):
        if self.operatingMode == "Armed" or self.operatingMode == "Test":
            id = event.GetEventObject().GetId()
            #Find which panel threw it
            for i, seq in enumerate(self.panel_Sequencer.panelList):
                if seq.button_Sequencer_Play.GetId() == id:
                    idx = i
                    break;
            sequencer = self.panel_Sequencer.panelList[idx]
            # Disable the play button, so you cannot hit it twice...
            sequencer.button_Sequencer_Play.Disable()
            sequencer.button_Sequencer_Stop.Enable()
            sequencer.button_Sequencer_Reset.Disable()
            sequencer.button_Load.Disable()
            sequencer.button_Save.Disable()
            sequencer.startTime = time.time()
            if sequencer.stopTime is None:
                sequencer.stopTime = time.time()
            for i, timer in enumerate(sequencer.timerList):
                targetTime = float(sequencer.list_ctrl_Sequencer.GetItem(i, 2).GetText())
                delay = sequencer.stopTime - sequencer.startTime
                scheduledTime = targetTime + delay
                #print "Delay:", delay, "Scheduled Time:", scheduledTime
                if scheduledTime >= 0.0: # If the scheduled time happens in the future
                    self.Bind(wx.EVT_TIMER, self.OnTimer_SequencerFire, timer)
                    delayinms = int(float(scheduledTime)*1000)
                    timer.Start(delayinms, oneShot=True)
        else:
            wx.MessageBox('System is in Safety.  Please change mode to "Test" to test all channels.', 'Safety first...', wx.OK)
    
    def OnButton_Add(self, event):
        id = event.GetEventObject().GetId()
        #Find which panel threw it
        for i, seq in enumerate(self.panel_Sequencer.panelList):
            if seq.editWindow.button_Add.GetId() == id:
                idx = i
                break;
        sequencer = self.panel_Sequencer.panelList[idx]
        if not (sequencer.editWindow.text_ctrl_Channel.GetValue() == '' or sequencer.editWindow.text_ctrl_Time.GetValue() == ''):
            c = int(sequencer.editWindow.text_ctrl_Channel.GetValue())
            t = float(sequencer.editWindow.text_ctrl_Time.GetValue())
            l = self.panel_Manual.buttonList[c-1].GetLabel()
        else:
            wx.MessageBox('Please enter both a channel and time when adding an item.', 'Error', wx.OK | wx.ICON_ERROR)
            
        try:
            if self.panel_Manual.buttonList[c-1].IsEnabled():
                self.panel_Manual.buttonList[c-1].Disable()
                self.panel_Manual.buttonList[c-1].SetBackgroundColour(wx.NamedColour("GREY"))
                sequencer.list_ctrl_Sequencer.Append([str(c), l, str(t), ""])
                sequencer.editWindow.text_ctrl_Channel.Clear()
                sequencer.editWindow.text_ctrl_Time.Clear()
                timer = FireTimer.FireTimer(self, c, t)
                sequencer.timerList.append(timer)
            else:
                wx.MessageBox('The channel %s is already in use elsewhere.'%(c), 'Used Channel', wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)
        except IndexError:
                wx.MessageBox('The channel %s does not exist.'%(c), 'Used Channel', wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)

    def OnButton_Remove(self, event):
        print "OnButton_Remove"
        id = event.GetEventObject().GetId()
        #Find which panel threw it
        for i, seq in enumerate(self.panel_Sequencer.panelList):
            if seq.editWindow.button_Remove.GetId() == id:
                idx = i
                break;
        sequencer = self.panel_Sequencer.panelList[idx]
        #print sequencer.editWindow.text_ctrl_Channel.GetValue()
        if not (sequencer.editWindow.text_ctrl_Channel.GetValue() == ''):
            c = int(sequencer.editWindow.text_ctrl_Channel.GetValue())
            sequencer.editWindow.text_ctrl_Channel.Clear()
            sequencer.editWindow.text_ctrl_Time.Clear()
            for j, timer in enumerate(sequencer.timerList):
                if timer.GetChannel() == c:
                    sequencer.timerList.pop(j)
                    break
        else:
            wx.MessageBox('Please enter a channel when removing an item', 'Error', wx.OK | wx.ICON_ERROR)
        
        row = sequencer.list_ctrl_Sequencer.FindItem(-1, str(c))
        sequencer.list_ctrl_Sequencer.DeleteItem(row)
        self.panel_Manual.buttonList[c-1].Enable()
        self.panel_Manual.buttonList[c-1].SetBackgroundColour(wx.NamedColour("YELLOW"))

    def propegateButtonLabelChanges(self, event):
        for sequencer in self.panel_Sequencer.panelList:
            for i in range(sequencer.list_ctrl_Sequencer.GetItemCount()):
                seqChannel = sequencer.list_ctrl_Sequencer.GetItem(i, 0).GetText()
                newLabel = self.panel_Manual.buttonList[int(seqChannel)-1].GetLabel()
                sequencer.list_ctrl_Sequencer.SetStringItem(i, 2, newLabel)
            

#-------------PUB/SUB CALLBACKS------------------

    def OnPubSub_Coms(self, data):
        msg = data.strip()
        print "Incoming message:|%s|"%(msg)
        if msg == "":  # we timed out...  no response.  Not good.
            if self.communicationStatus == "Connected":
                self.communicationStatus = "Failure"
                self.remoteOperatingMode = "Unknown"
                self.FireControl_Frame_statusbar.SetStatusText("Communication: %s"%(self.communicationStatus), 0)
                self.FireControl_Frame_statusbar.SetStatusText("remote Mode: %s"%(self.remoteOperatingMode), 2)
                self.writeToRxLog("Communications with remote lost!")
        elif msg[0] == "R":
            if not self.panel_Diagnostics.checkbox_RxLogFilter.IsChecked():
                self.writeToRxLog("Heartbeat echo received")
            if self.communicationStatus == "Failure":
                self.communicationStatus = "Connected"
                self.FireControl_Frame_statusbar.SetStatusText("Communication: %s"%(self.communicationStatus), 0)
                self.writeToRxLog("Communications with remote restored!")
            if data[1] == "0":
                    self.remoteOperatingMode = "Safety"
            elif data[1] == "1":
                    self.remoteOperatingMode = "Test"
            elif data[1] == "2":
                    self.remoteOperatingMode = "Armed"
            self.FireControl_Frame_statusbar.SetStatusText("Remote Mode: %s"%(self.remoteOperatingMode), 2)
        elif msg[0] == "T":
            statusIdx = msg.index("S")
            channel = msg[1:statusIdx]
            status = msg[-1]
            self.writeToRxLog("Channel fired: %s"%(channel))
            if self.operatingMode == "Test":
                if status == "1":
                    self.panel_Manual.buttonList[int(channel)-1].SetBackgroundColour(wx.NamedColour("Green"))
                    self.testList[int(channel)-1] = True
                elif status == "0":
                    self.panel_Manual.buttonList[int(channel)-1].SetBackgroundColour(wx.NamedColour("RED"))
                    self.testList[int(channel)-1] = False
            elif self.operatingMode == "Armed":
                self.panel_Manual.buttonList[int(channel)-1].SetBackgroundColour(wx.NamedColour("RED"))
        elif msg[0] == "O":
            if msg[1] == "0":
                self.writeToRxLog("Remote set to Safety")
            elif msg[1] == "1":
                self.writeToRxLog("Remote set to Test")
            elif msg[1] == "2":
                self.writeToRxLog("Remote set to Armed")
            else:
                self.writeToRxLog("Error! Remote set to %s"%(msg[1]))
        elif msg[0] == "D":
            print "Serial Debug Message:", msg
        else:
            self.writeToRxLog("Unknown msg: %s"%(data))
        
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
            self.writeToTxLog("Heartbeat message sent (H)")
        self.serial.send("H")
        
    def OnTimer_Heartbeat_Expire(self, event):
        self.communicationStatus = "Failure"
        self.FireControl_Frame_statusbar.SetStatusText("Communication: %s"%(self.communicationStatus), 0)
        
    def OnTimer_SequencerFire(self, event):
        id = event.GetId()
        for i, sequencer in enumerate(self.panel_Sequencer.panelList):
            for timer in sequencer.timerList:
                if id == timer.GetId():
                    channel = timer.GetChannel()
                    idx = i
                    break
        panel = self.panel_Sequencer.panelList[idx]
        row = panel.list_ctrl_Sequencer.FindItem(-1, str(channel))
        panel.list_ctrl_Sequencer.SetStringItem(row, 3, "FIRED")
        e = wx.CommandEvent(wx.EVT_BUTTON.evtType[0], self.panel_Manual.buttonList[channel-1].GetId())
        e.SetEventObject(self.panel_Manual.buttonList[channel-1])
        wx.PostEvent(self.GetEventHandler(), e)
                    
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