#!/usr/bin/env python

import wx
from wx.lib.pubsub import pub

import gettext
import os
import time

import EditSequencer
import FireTimer

class SequencerProgram(wx.Panel):
    def __init__(self, parent, name):
        # begin wxGlade: SequencerProgram.__init__
        wx.Panel.__init__(self, parent=parent, name = name)
        
        self.name = name
        self.timerList = []
        self.startTime = time.time()
        self.stopTime = None
        self.loadDelay = 250
        
        self.panel_SequencerProgram = wx.Panel(self, wx.ID_ANY)
        self.button_Sequencer_Play = wx.Button(self.panel_SequencerProgram, wx.ID_ANY, _("Play"))
        self.button_Sequencer_Play.SetName("Play_%s"%(name))
        self.button_Sequencer_Stop = wx.Button(self.panel_SequencerProgram, wx.ID_ANY, _("Stop"))
        self.button_Sequencer_Stop.SetName("Stop_%s"%(name))
        self.button_Sequencer_Reset = wx.Button(self.panel_SequencerProgram, wx.ID_ANY, _("Reset"))
        self.button_Sequencer_Reset.SetName("Reset_%s"%(name))
        self.panel_Sequencer_Simulator = wx.Panel(self.panel_SequencerProgram, wx.ID_ANY, style=wx.BORDER_DOUBLE)
        self.label_9 = wx.StaticText(self.panel_Sequencer_Simulator, wx.ID_ANY, _("%s"%(self.GetName())))
        self.panel_Sequencer_Editor = wx.Panel(self.panel_SequencerProgram, wx.ID_ANY)
        self.button_Load = wx.Button(self.panel_Sequencer_Editor, wx.ID_ANY, _("Load"))
        self.button_Load.SetName("Load_%s"%(name))
        self.button_Save = wx.Button(self.panel_Sequencer_Editor, wx.ID_ANY, _("Save"))
        self.button_Save.SetName("Save_%s"%(name))
        self.button_Clear = wx.Button(self.panel_Sequencer_Editor, wx.ID_ANY, _("Clear"))
        self.button_Clear.SetName("Clear_%s"%(name))
        self.button_Edit = wx.Button(self.panel_Sequencer_Editor, wx.ID_ANY, _("Edit"))
        self.button_Edit.SetName("Edit_%s"%(name))
        self.list_ctrl_Sequencer = wx.ListCtrl(self.panel_Sequencer_Editor, wx.ID_ANY, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        
        self.editWindow = EditSequencer.EditSequencer(self, self.name)

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.OnButton_Clear, self.button_Clear)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Stop, self.button_Sequencer_Stop)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Reset, self.button_Sequencer_Reset)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Save, self.button_Save)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Load, self.button_Load)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Edit, self.button_Edit)

    def __set_properties(self):
        # begin wxGlade: SequencerProgram.__set_properties
        self.list_ctrl_Sequencer.InsertColumn(0, "Channel")
        self.list_ctrl_Sequencer.InsertColumn(1, "Label")
        self.list_ctrl_Sequencer.InsertColumn(2, "Time")
        self.list_ctrl_Sequencer.InsertColumn(3, "Executed")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SequencerProgram.__do_layout
        sizer_Outer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Sequencer %s"%(self.name))), wx.HORIZONTAL)
        sizer_Sequencer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Sequencer_Editor = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_Sequencer_Buttons = wx.GridSizer(2, 2, 0, 0)
        sizer_Sequencer_Buttons = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self.panel_Sequencer_Simulator, wx.ID_ANY, _("Simulator")), wx.VERTICAL)
        sizer_Sequencer_Buttons.Add(self.button_Sequencer_Play, 0, 0, 0)
        sizer_Sequencer_Buttons.Add(self.button_Sequencer_Stop, 0, 0, 0)
        sizer_Sequencer_Buttons.Add(self.button_Sequencer_Reset, 0, 0, 0)
        sizer_6.Add(self.label_9, 3, wx.EXPAND, 0)
        self.panel_Sequencer_Simulator.SetSizer(sizer_6)
        sizer_Sequencer_Buttons.Add(self.panel_Sequencer_Simulator, 3, wx.ALL | wx.EXPAND, 1)
        sizer_Sequencer.Add(sizer_Sequencer_Buttons, 1, 0, 0)
        grid_sizer_Sequencer_Buttons.Add(self.button_Load, 0, 0, 0)
        grid_sizer_Sequencer_Buttons.Add(self.button_Save, 0, 0, 0)
        grid_sizer_Sequencer_Buttons.Add(self.button_Clear, 0, 0, 0)
        grid_sizer_Sequencer_Buttons.Add(self.button_Edit, 0, 0, 0)
        sizer_Sequencer_Editor.Add(grid_sizer_Sequencer_Buttons, 1, 0, 0)
        sizer_Sequencer_Editor.Add(self.list_ctrl_Sequencer, 4, wx.EXPAND, 0)
        self.panel_Sequencer_Editor.SetSizer(sizer_Sequencer_Editor)
        sizer_Sequencer.Add(self.panel_Sequencer_Editor, 1, wx.EXPAND, 0)
        self.panel_SequencerProgram.SetSizer(sizer_Sequencer)
        sizer_Outer.Add(self.panel_SequencerProgram, 6, wx.EXPAND, 0)
        self.SetSizer(sizer_Outer)
        sizer_Outer.Fit(self)


    def OnButton_Edit(self, event):
        print "OnButton_Edit: Editing Sequencer Bank %s"%(self.name)
        #editWindow = EditSequencer.EditSequencer(self, self.name)
        self.editWindow.Show()

    def OnButton_Load(self, event):
        print "OnButton_Load: Loading Sequencer Bank %s"%(self.name)
        self.OnButton_Clear(event)
        path = os.path.join(os.getcwd(),"assets","Sequencer_%s.txt"%(self.name))
        #notifyList = []
        with open(path, 'r') as file:
            for i, line in enumerate(file.readlines()):
                channel, time = line.split(',')
                wx.CallLater(self.loadDelay * i, self.loadHelper, channel, time)

    def OnButton_Clear(self, event):
        print "OnButton_Edit: Clearing Sequencer Bank %s"%(self.name)

        self.button_Save.Enable()
        self.button_Load.Enable()
        for i in range(self.list_ctrl_Sequencer.GetItemCount()):
            item = self.list_ctrl_Sequencer.GetItem(i)
            channel = item.GetText()
            wx.CallLater(self.loadDelay * i, self.clearHelper, channel)
            
    def loadHelper(self, c, t):
        self.editWindow.text_ctrl_Channel.SetValue(str(c))
        self.editWindow.text_ctrl_Time.SetValue(str(t))
        e = wx.CommandEvent(wx.EVT_BUTTON.evtType[0], self.editWindow.button_Add.GetId())
        e.SetEventObject(self.editWindow.button_Add)
        wx.PostEvent(self.GetEventHandler(), e)
        
    def clearHelper(self, c):
        self.editWindow.text_ctrl_Channel.SetValue(str(c))
        e = wx.CommandEvent(wx.EVT_BUTTON.evtType[0], self.editWindow.button_Remove.GetId())
        e.SetEventObject(self.editWindow.button_Remove)
        wx.PostEvent(self.GetEventHandler(), e)

    def OnButton_Save(self, event):
        print "OnButton_Save: Saving Sequencer Bank %s"%(self.name)
        path = os.path.join(os.getcwd(),"assets","Sequencer_%s.txt"%(self.name))
        with open(path, 'w') as file:
            for i in range(self.list_ctrl_Sequencer.GetItemCount()):
                channel = self.list_ctrl_Sequencer.GetItem(i, 0).GetText()
                time = self.list_ctrl_Sequencer.GetItem(i, 2).GetText()
                file.write("%s,%s\n"%(channel, time))
        wx.MessageBox('This sequence was saved', 'Finished', wx.OK | wx.STAY_ON_TOP)
        
    def OnButton_Stop(self, event):
        print "OnButton_Stopping: Stopping Sequencer Bank %s"%(self.name)
        self.button_Sequencer_Play.Enable()
        self.button_Sequencer_Stop.Disable()
        self.button_Sequencer_Reset.Enable()
        for timer in self.timerList:
            if timer.IsRunning():
                timer.Stop()
        self.stopTime = time.time()
         
    def OnButton_Reset(self, event):
        print "OnButton_Reset: Resetting Sequencer Bank %s"%(self.name)
        
        self.button_Sequencer_Play.Enable()
        self.button_Sequencer_Stop.Disable()
        self.button_Sequencer_Reset.Disable()
        self.startTime = time.time()
        self.stopTime = None

        for timer in self.timerList:
            if timer.IsRunning():
                timer.Stop()

        self.startTime = 0.0
        # Need to clear out all of the "FIRED" entries
        for i in range(self.list_ctrl_Sequencer.GetItemCount()):
            self.list_ctrl_Sequencer.SetStringItem(i, 3, "")
