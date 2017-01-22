#!/usr/bin/env python
# -*- coding: CP1252 -*-
#
# generated by wxGlade 0.7.2 on Sat Jan 21 18:50:56 2017
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class SequencerProgram(wx.Panel):
    def __init__(self, parent, name):
        # begin wxGlade: SequencerProgram.__init__
        wx.Panel.__init__(self, parent=parent, name = name)
        
        self.panel_SequencerProgram = wx.Panel(self, wx.ID_ANY)
        self.button_Sequencer_Play = wx.Button(self.panel_SequencerProgram, wx.ID_ANY, _("Play"))
        self.button_Sequencer_Stop = wx.Button(self.panel_SequencerProgram, wx.ID_ANY, _("Stop"))
        self.button_Sequencer_Reset = wx.Button(self.panel_SequencerProgram, wx.ID_ANY, _("Reset"))
        self.panel_Sequencer_Simulator = wx.Panel(self.panel_SequencerProgram, wx.ID_ANY, style=wx.BORDER_DOUBLE)
        self.label_9 = wx.StaticText(self.panel_Sequencer_Simulator, wx.ID_ANY, _("%s"%(self.GetName())))
        self.panel_Sequencer_Editor = wx.Panel(self.panel_SequencerProgram, wx.ID_ANY)
        self.button_Load = wx.Button(self.panel_Sequencer_Editor, wx.ID_ANY, _("Load"))
        self.button_Save = wx.Button(self.panel_Sequencer_Editor, wx.ID_ANY, _("Save"))
        self.button_Clear = wx.Button(self.panel_Sequencer_Editor, wx.ID_ANY, _("Clear"))
        self.button_Edit = wx.Button(self.panel_Sequencer_Editor, wx.ID_ANY, _("Edit"))
        self.button_Edit.SetName("Edit_%s"%(name))
        self.list_ctrl_Sequencer = wx.ListCtrl(self.panel_Sequencer_Editor, wx.ID_ANY, style=wx.LC_REPORT|wx.BORDER_SUNKEN)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: SequencerProgram.__set_properties
        self.list_ctrl_Sequencer.InsertColumn(0, "Channel")
        self.list_ctrl_Sequencer.InsertColumn(1, "Time")
        self.list_ctrl_Sequencer.InsertColumn(2, "Executed")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SequencerProgram.__do_layout
        sizer_Outer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Sequencer")), wx.HORIZONTAL)
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
        # end wxGlade

# end of class SequencerProgram