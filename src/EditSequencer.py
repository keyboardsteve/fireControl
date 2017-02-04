#!/usr/bin/env python

import wx
from wx.lib.pubsub import pub

import gettext



class EditSequencer(wx.PopupWindow):
    def __init__(self, parent, name, *args, **kwargs):
        wx.PopupWindow.__init__(self, parent=parent, *args, **kwargs)
        
        self.name = name
        self.focus = None #Will store which text field has the cursor
        
        self.panel_Background = wx.Panel(self, wx.ID_ANY)
        self.label_HelpText = wx.StaticText(self.panel_Background, wx.ID_ANY, _("To add entries, enter the channel number and the time delay and click \"Add\".\nTo remove entries, enter the channel number and click remove.\nWhen you are finished, click Close and review your changes in the Sequencer screen."))
        self.label_ChannelText = wx.StaticText(self.panel_Background, wx.ID_ANY, _("Channel Number"))
        self.text_ctrl_Channel = wx.TextCtrl(self.panel_Background, wx.ID_ANY, "")
        self.label_TimeDelay = wx.StaticText(self.panel_Background, wx.ID_ANY, _("Time Delay (s)"))
        self.text_ctrl_Time = wx.TextCtrl(self.panel_Background, wx.ID_ANY, "")
        self.button_1 = wx.Button(self.panel_Background, wx.ID_ANY, _("1"))
        self.button_2 = wx.Button(self.panel_Background, wx.ID_ANY, _("2"))
        self.button_3 = wx.Button(self.panel_Background, wx.ID_ANY, _("3"))
        self.button_4 = wx.Button(self.panel_Background, wx.ID_ANY, _("4"))
        self.button_5 = wx.Button(self.panel_Background, wx.ID_ANY, _("5"))
        self.button_bksp = wx.Button(self.panel_Background, wx.ID_ANY, _("<"))
        self.button_6 = wx.Button(self.panel_Background, wx.ID_ANY, _("6"))
        self.button_7 = wx.Button(self.panel_Background, wx.ID_ANY, _("7"))
        self.button_8 = wx.Button(self.panel_Background, wx.ID_ANY, _("8"))
        self.button_9 = wx.Button(self.panel_Background, wx.ID_ANY, _("9"))
        self.button_0 = wx.Button(self.panel_Background, wx.ID_ANY, _("0"))
        self.button_dot = wx.Button(self.panel_Background, wx.ID_ANY, _("."))
        self.button_Add = wx.Button(self.panel_Background, wx.ID_ANY, _("Add"))
        self.button_Remove = wx.Button(self.panel_Background, wx.ID_ANY, _("Remove"))
        self.button_Close = wx.Button(self.panel_Background, wx.ID_ANY, _("Close"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_5)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_bksp)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_7)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_8)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_9)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Key, self.button_dot)
        #self.Bind(wx.EVT_BUTTON, self.OnButton_Add, self.button_Add)
        #self.Bind(wx.EVT_BUTTON, self.OnButton_Remove, self.button_Remove)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Close, self.button_Close)
        
        #was ex.EVT_SET_FOCUS
        self.text_ctrl_Channel.Bind(wx.EVT_SET_CURSOR, self.OnCursor_Channel)
        self.text_ctrl_Time.Bind(wx.EVT_SET_CURSOR, self.OnCursor_Time)
    

    def __set_properties(self):
        self.SetBackgroundColour(wx.Colour(171, 171, 171))


    def __do_layout(self):
        # begin wxGlade: EditSequencer.__do_layout
        sizer_Background = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Outer = wx.BoxSizer(wx.VERTICAL)
        sizer_Buttons = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_Keys = wx.GridSizer(2, 6, 0, 0)
        sizer_Input = wx.BoxSizer(wx.HORIZONTAL)
        sizer_InputRow = wx.StaticBoxSizer(wx.StaticBox(self.panel_Background, wx.ID_ANY, _("Values")), wx.HORIZONTAL)
        sizer_Time = wx.BoxSizer(wx.VERTICAL)
        sizer_Channel = wx.BoxSizer(wx.VERTICAL)
        sizer_Outer.Add(self.label_HelpText, 0, wx.ALIGN_CENTER, 0)
        sizer_Channel.Add(self.label_ChannelText, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_Channel.Add(self.text_ctrl_Channel, 0, wx.ALIGN_CENTER, 0)
        sizer_InputRow.Add(sizer_Channel, 1, 0, 0)
        sizer_Time.Add(self.label_TimeDelay, 0, wx.ALIGN_CENTER, 0)
        sizer_Time.Add(self.text_ctrl_Time, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_InputRow.Add(sizer_Time, 1, 0, 0)
        sizer_Input.Add(sizer_InputRow, 1, 0, 0)
        sizer_Outer.Add(sizer_Input, 1, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_1, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_2, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_3, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_4, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_5, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_bksp, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_6, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_7, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_8, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_9, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_0, 0, wx.EXPAND, 0)
        grid_sizer_Keys.Add(self.button_dot, 0, wx.EXPAND, 0)
        sizer_Outer.Add(grid_sizer_Keys, 1, 0, 0)
        sizer_Buttons.Add(self.button_Add, 1, wx.EXPAND, 0)
        sizer_Buttons.Add(self.button_Remove, 1, wx.EXPAND, 0)
        sizer_Buttons.Add(self.button_Close, 1, wx.EXPAND, 0)
        sizer_Outer.Add(sizer_Buttons, 1, wx.EXPAND, 0)
        self.panel_Background.SetSizer(sizer_Outer)
        sizer_Background.Add(self.panel_Background, 1, 0, 0)
        self.SetSizer(sizer_Background)
        sizer_Background.Fit(self)
        self.Layout()
        # end wxGlade

    def OnButton_Key(self, event):
        label = event.GetEventObject().GetLabel()
        if label == "<":
            self.focus.SetValue(self.focus.GetValue()[:-1])
        else:
            if not (self.focus is self.text_ctrl_Channel and label == '.'): #Cannot put periods in the channel box
                if not (self.focus is self.text_ctrl_Time and "." in self.text_ctrl_Time.GetValue() and label == "."): # Cannot have two periods in the time box
                    try:
                        self.focus.AppendText(label)
                    except:
                        print "No text field selected!"

    def OnButton_Close(self, event):
        #self.Destroy()
        self.Hide()
        
    def OnCursor_Channel(self, event):
        self.focus = self.text_ctrl_Channel
        
    def OnCursor_Time(self, event):
        #print "Time has the cursor"
        self.focus = self.text_ctrl_Time

# end of class EditSequencer
