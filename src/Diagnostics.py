#!/usr/bin/env python


import wx
import gettext

import TestAll


class Diagnostics(wx.Panel):
    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent)
        self.checkbox_TxLogFilter = wx.CheckBox(self, wx.ID_ANY, _("Filter out Heartbeat entries"))
        self.text_ctrl_TxLog = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.checkbox_RxLogFilter = wx.CheckBox(self, wx.ID_ANY, _("Filter out Heartbeat entries"))
        self.text_ctrl_RxLog = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.button_TestAll = wx.Button(self, wx.ID_ANY, _("Test All"))
        self.gauge_TestAll = wx.Gauge(self, wx.ID_ANY, 100)
        self.text_ctrl_TestAll = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        

        self.__set_properties()
        self.__do_layout()
        


    def __set_properties(self):
        self.checkbox_TxLogFilter.SetValue(1)
        self.checkbox_RxLogFilter.SetValue(1)

    def __do_layout(self):
        sizer_Outer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Diagnostics")), wx.VERTICAL)
        sizer_Test = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Test")), wx.VERTICAL)
        sizer_TestButton = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Logs = wx.BoxSizer(wx.HORIZONTAL)
        sizer_RxLog = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Rx Log")), wx.VERTICAL)
        sizer_TxLog = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Tx Log")), wx.VERTICAL)
        sizer_TxLog.Add(self.checkbox_TxLogFilter, 0, wx.EXPAND, 0)
        sizer_TxLog.Add(self.text_ctrl_TxLog, 1, wx.EXPAND, 0)
        sizer_Logs.Add(sizer_TxLog, 1, wx.EXPAND, 0)
        sizer_RxLog.Add(self.checkbox_RxLogFilter, 0, wx.EXPAND, 0)
        sizer_RxLog.Add(self.text_ctrl_RxLog, 1, wx.EXPAND, 0)
        sizer_Logs.Add(sizer_RxLog, 1, wx.EXPAND, 0)
        sizer_Outer.Add(sizer_Logs, 1, wx.EXPAND, 0)
        sizer_TestButton.Add(self.button_TestAll, 0, wx.EXPAND, 0)
        sizer_TestButton.Add(self.gauge_TestAll, 0, wx.ALIGN_CENTER, 0)
        sizer_Test.Add(sizer_TestButton, 1, wx.EXPAND, 0)
        sizer_Test.Add(self.text_ctrl_TestAll, 2, wx.EXPAND, 0)
        sizer_Outer.Add(sizer_Test, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_Outer)
        sizer_Outer.Fit(self)
        self.Layout()
