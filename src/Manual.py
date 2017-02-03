
import wx
import gettext
import math

import ManualButtonPanel

class Manual(wx.Panel):
    def __init__(self, parent, numButtons, numCols, numRows):
        wx.Panel.__init__(self, parent=parent)
        
        self.numButtons = numButtons
        self.numCols = numCols
        self.numRows = numRows
        self.buttonsPerPage = self.numCols*self.numRows
        self.currentPage = 1
        self.numPages = int(math.ceil(float(self.numButtons)/(float(self.numCols)*float(self.numRows))))
        self.panelList = []
        self.buttonList = []
        
        self.button_Up = wx.Button(self, wx.ID_ANY, _("^"))
        self.staticTxt_Page = wx.StaticText(self, wx.ID_ANY, style = wx.ALIGN_CENTER_HORIZONTAL)
        self.button_Down = wx.Button(self, wx.ID_ANY, _("v"))
        
        for i in range(self.numPages): #Add one panel for each page
            tmpButtonList = self.buttonList[i:i+(self.numCols+numRows)]
            self.panelList.append(ManualButtonPanel.ManualButtonPanel(self, self.numCols, self.numRows))
        
        currentButton = 1
        for panel in self.panelList:
            for i in range(self.buttonsPerPage):
                button = panel.addButton(currentButton)
                self.buttonList.append(button)
                currentButton += 1
                if currentButton > self.numButtons: #If the next button to be made is too high, break out of the loop
                    break
                
        self.hidePanels()  # Hide all panels and only show the first one
        self.panelList[0].Show()

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.OnButton_Page, self.button_Up)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Page, self.button_Down)

    def __set_properties(self):
        self.staticTxt_Page.SetLabel("Bank: %s"%(self.currentPage))
        for button in self.buttonList:
            button.SetBackgroundColour(wx.NamedColour('YELLOW'))

    def __do_layout(self):
        sizer_Outer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Manual Fire")), wx.HORIZONTAL)
        sizer_Page = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Bank Select")), wx.VERTICAL)
        sizer_Page.Add(self.staticTxt_Page, 0, wx.EXPAND, 0)
        sizer_Page.Add(self.button_Up, 3, wx.EXPAND, 0)
        sizer_Page.Add(self.button_Down, 3, wx.EXPAND, 0)
        sizer_Outer.Add(sizer_Page, 1, wx.EXPAND, 1)
        
        for panel in self.panelList:
            sizer_Outer.Add(panel, 5, wx.EXPAND, 0)

        self.SetSizer(sizer_Outer)
        sizer_Outer.Fit(self)
        self.Layout()

    def OnButton_Page(self, event):
        button = event.GetEventObject().LabelText.strip()
        if button == "^":
            if (self.currentPage - 1 >= 1):
                self.currentPage = self.currentPage - 1
        elif button == "v":
            if (self.currentPage + 1 <= len(self.panelList)):
                self.currentPage = self.currentPage + 1

        print "OnButton_Page: Page change %s to %s"%(button, self.currentPage)
        
        self.hidePanels()
        self.panelList[self.currentPage - 1].Show()
        self.staticTxt_Page.SetLabel("Bank: %s"%(self.currentPage))
        self.Layout()
        
    def hidePanels(self):
        for panel in self.panelList:
            panel.Hide()
