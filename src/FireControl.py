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
        self.panel_Sequencer = Sequencer.Sequencer(self)
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
            self.Bind(wx.EVT_BUTTON, self.OnButton_Edit, sequencer.button_Edit)
            self.Bind(wx.EVT_BUTTON, self.OnButton_Clear, sequencer.button_Clear)
            self.Bind(wx.EVT_BUTTON, self.OnButton_Load, sequencer.button_Load)
            self.Bind(wx.EVT_BUTTON, self.OnButton_Save, sequencer.button_Save)
            self.Bind(wx.EVT_BUTTON, self.OnButton_Play, sequencer.button_Sequencer_Play)
            self.Bind(wx.EVT_BUTTON, self.OnButton_Stop, sequencer.button_Sequencer_Stop)
            self.Bind(wx.EVT_BUTTON, self.OnButton_Reset, sequencer.button_Sequencer_Reset)
            sequencer.button_Sequencer_Stop.Disable()
            sequencer.button_Sequencer_Reset.Disable()
        #self.panel_Sequencer.button_Edit.Bind(wx.EVT_BUTTON, self.OnButton_Edit)
        
        self.Bind(wx.EVT_TIMER, self.OnTimer_Heartbeat, self.heartbeatTimer)
        
        self.subcsriber_Add = pub.subscribe(self.OnPubSub_Add, "Sequencer_Add")
        self.subcsriber_Remove = pub.subscribe(self.OnPubSub_Remove, "Sequencer_Remove")
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

    def OnButton_Edit(self, event):
        name =  event.GetEventObject().GetName()
        print "OnButton_Edit: Editing Sequencer Bank %s"%(name)
        editWindow = EditSequencer.EditSequencer(self, name)
        editWindow.Show()

    def OnButton_Clear(self, event):
        sequencer =  event.GetEventObject().GetName()
        print "OnButton_Edit: Clearing Sequencer Bank %s"%(sequencer)
        option = ['A','B','C','D']
        letter = sequencer[-1]
        idx = option.index(letter)
        self.OnButton_Reset(event)
        self.panel_Sequencer.panelList[idx].button_Save.Enable()
        self.panel_Sequencer.panelList[idx].button_Load.Enable()
        listcontrol = self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer
        for i in range(listcontrol.GetItemCount()):
            item = listcontrol.GetItem(0)
            channel = item.GetText()
            self.panel_Manual.buttonList[int(channel)-1].Enable()
            row = self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.FindItem(-1, channel)
            self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.DeleteItem(row)
            self.panel_Sequencer.panelList[idx].timerList.pop(row)
            for timerDecode in self.panel_Sequencer.masterTimerDecoder:
                if timerDecode["Sequencer"] == letter and timerDecode["Channel"] == int(channel):
                    self.panel_Sequencer.masterTimerDecoder.remove(timerDecode)
        
    def OnButton_Load(self, event):
        sequencer =  event.GetEventObject().GetName()
        print "OnButton_Load: Loading Sequencer Bank %s"%(sequencer)
        letter = sequencer[-1] # Gets the last letter of the sequencer "Load_A", "Load_B", etc...
        self.OnButton_Clear(event)
        path = os.path.join(os.getcwd(),"assets","Sequencer_%s.txt"%(letter))
        with open(path, 'r') as file:
            for line in file.readlines():
                channel, time = line.split(',')
                self.OnPubSub_Add("Edit_%s"%(letter), int(channel), float(time))
                
    def OnButton_Save(self, event):
        sequencer =  event.GetEventObject().GetName()
        print "OnButton_Save: Saving Sequencer Bank %s"%(sequencer)
        option = ['A','B','C','D']
        letter = sequencer[-1]
        idx = option.index(letter)
        path = os.path.join(os.getcwd(),"assets","Sequencer_%s.txt"%(letter))
        with open(path, 'w') as file:
            for i in range(self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.GetItemCount()):
                channel = self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.GetItem(i, 0).GetText()
                time = self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.GetItem(i, 1).GetText()
                file.write("%s,%s\n"%(channel, time))
        wx.MessageBox('This sequence was saved', 'Finished', wx.OK | wx.STAY_ON_TOP)
        
    def OnButton_Play(self, event):
        if self.operatingMode == "Armed" or self.operatingMode == "Test":
            sequencer =  event.GetEventObject().GetName()
            print "OnButton_Play: Playing Sequencer Bank %s"%(sequencer)
            option = ['A','B','C','D']
            letter = sequencer[-1]
            idx = option.index(letter)
            
            # Disable the play button, so you cannot hit it twice...
            self.panel_Sequencer.panelList[idx].button_Sequencer_Play.Disable()
            self.panel_Sequencer.panelList[idx].button_Sequencer_Stop.Enable()
            self.panel_Sequencer.panelList[idx].button_Sequencer_Reset.Disable()
            self.panel_Sequencer.panelList[idx].button_Load.Disable()
            self.panel_Sequencer.panelList[idx].button_Save.Disable()
            self.panel_Sequencer.panelList[idx].startTime = time.time()
            if self.panel_Sequencer.panelList[idx].stopTime is None:
                self.panel_Sequencer.panelList[idx].stopTime = time.time()
            for i, timer in enumerate(self.panel_Sequencer.panelList[idx].timerList):
                targetTime = float(self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.GetItem(i, 1).GetText())
                delay = self.panel_Sequencer.panelList[idx].stopTime - self.panel_Sequencer.panelList[idx].startTime
                scheduledTime = targetTime + delay
                print "Delay:", delay, "Scheduled Time:", scheduledTime
                if scheduledTime >= 0.0: # If the scheduled time happens in the future
                    self.Bind(wx.EVT_TIMER, self.OnTimer_SequencerFire, timer)
                    delayinms = int(float(scheduledTime)*1000)
                    timer.Start(delayinms, oneShot=True)
        else:
            wx.MessageBox('System is in Safety.  Please change mode to "Test" to test all channels.', 'Safety first...', wx.OK)
        
    def OnButton_Stop(self, event):
        sequencer =  event.GetEventObject().GetName()
        print "OnButton_Stopping: Stopping Sequencer Bank %s"%(sequencer)
        option = ['A','B','C','D']
        letter = sequencer[-1]
        idx = option.index(letter)
        self.panel_Sequencer.panelList[idx].button_Sequencer_Play.Enable()
        self.panel_Sequencer.panelList[idx].button_Sequencer_Stop.Disable()
        self.panel_Sequencer.panelList[idx].button_Sequencer_Reset.Enable()
        for timer in self.panel_Sequencer.panelList[idx].timerList:
            if timer.IsRunning():
                timer.Stop()
        self.panel_Sequencer.panelList[idx].stopTime = time.time()
         
    def OnButton_Reset(self, event):
        sequencer =  event.GetEventObject().GetName()
        print "OnButton_Reset: Resetting Sequencer Bank %s"%(sequencer)
        option = ['A','B','C','D']
        letter = sequencer[-1]
        idx = option.index(letter)
        
        self.panel_Sequencer.panelList[idx].button_Sequencer_Play.Enable()
        self.panel_Sequencer.panelList[idx].button_Sequencer_Stop.Disable()
        self.panel_Sequencer.panelList[idx].button_Sequencer_Reset.Disable()
        self.panel_Sequencer.panelList[idx].startTime = time.time()
        self.panel_Sequencer.panelList[idx].stopTime = None
        # Need to flush out all of the masterTimerList entries for that sequencer
        # Need to Stop all of the timers in the masterTimerList
        for timer in self.panel_Sequencer.panelList[idx].timerList:
            if timer.IsRunning():
                timer.Stop()
            for i, timerDecode in enumerate(self.panel_Sequencer.masterTimerDecoder):
                if timerDecode["Id"] == timer.GetId():
                    self.panel_Sequencer.masterTimerDecoder.pop(i)
        self.panel_Sequencer.panelList[idx].timerList = []
        self.panel_Sequencer.panelList[idx].startTime = 0.0
        # Need to clear out all of the "FIRED" entries
        listcontrol = self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer
        for i in range(listcontrol.GetItemCount()):
            #print i
            listcontrol.SetStringItem(i, 2, "")
        # Need to Requeue all of the sequencer's timers again from the ListControl
        # Need to Requeue all of the timers into the masterTimerList
            channel = int(self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.GetItem(i, 0).GetText())
            delay = self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.GetItem(i, 1).GetText()
            timer = wx.Timer(self)
            self.panel_Sequencer.masterTimerDecoder.append({"Id":timer.GetId(),
                                                                "Sequencer": letter,
                                                                "Channel": channel,
                                                                "Time": time})
            self.panel_Sequencer.panelList[idx].timerList.append(timer)

        #print "TimerList", len(self.panel_Sequencer.panelList[idx].timerList)
        #print "MasterTimerDecode", self.panel_Sequencer.masterTimerDecoder
        
#-------------PUB/SUB CALLBACKS------------------

    def OnPubSub_Add(self, sequencer, channel, time):
        item = [channel, time]
        option = ['A','B','C','D']
        letter = sequencer[-1]
        idx = option.index(letter)
            
        #Disable the button in the manual panel
        try:
            if self.panel_Manual.buttonList[channel-1].IsEnabled():
                self.panel_Manual.buttonList[channel-1].Disable()
                self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.Append(item)
                timer = wx.Timer(self)
                self.panel_Sequencer.masterTimerDecoder.append({"Id":timer.GetId(),
                                                                "Sequencer": letter,
                                                                "Channel": channel,
                                                                "Time": time})
                self.panel_Sequencer.panelList[idx].timerList.append(timer)
            else:
                wx.MessageBox('The channel %s is already in use elsewhere.'%(channel), 'Used Channel', wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)
        except IndexError:
                wx.MessageBox('The channel %s does not exist.'%(channel), 'Used Channel', wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)

    def OnPubSub_Remove(self, sequencer, channel):
        item = str(channel)
        option = ['A','B','C','D']
        letter = sequencer[-1]
        idx = option.index(letter)

        row = self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.FindItem(-1, item)
        self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer.DeleteItem(row)
        self.panel_Sequencer.panelList[idx].timerList.pop(row)
        self.panel_Manual.buttonList[channel-1].Enable()

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
        #print self.panel_Sequencer.masterTimerDecoder
        for item in self.panel_Sequencer.masterTimerDecoder:
            if item["Id"] == id:
                sequencer = item["Sequencer"]
                channel = item["Channel"]
                option = ['A','B','C','D']
                letter = sequencer[-1]
                idx = option.index(letter)
                listcontrol = self.panel_Sequencer.panelList[idx].list_ctrl_Sequencer
                #print listcontrol.GetItemCount()
                #print "channel", channel
                row = listcontrol.FindItem(-1, str(channel))
                #print "row", row
                listcontrol.SetStringItem(row, 2, "FIRED")
                print "OnTimer_SequencerFire: Fire command for sequencer %s, channel %s"%(sequencer, channel)
                
                ''' Holy cow, this works.  To fire the channel, I wanted to "virtually" press a button on the Manual page.  Obviously
                this couldn't be done with a mouse click, so I manually created the event that would have been generated by the click,
                and then assigned the button on the Manual page as the event object, then posted it!
                '''
                e = wx.CommandEvent(wx.EVT_BUTTON.evtType[0], self.panel_Manual.buttonList[channel-1].GetId())
                e.SetEventObject(self.panel_Manual.buttonList[channel-1])
                wx.PostEvent(self.GetEventHandler(), e)
                break
        self.panel_Sequencer.masterTimerDecoder.remove(item)
            
        
                    
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