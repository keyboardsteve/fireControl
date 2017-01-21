
import wx
import gettext
import math


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
        self.gridSizerList = []
        self.spacing = 5
        
        self.button_Up = wx.Button(self, wx.ID_ANY, _("^"))
        self.text_ctrl_Page = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_Down = wx.Button(self, wx.ID_ANY, _("v"))
        
        
        for i in range(self.numPages): #Add one panel for each page
            self.panelList.append(wx.Panel(self, wx.ID_ANY))
        
        for panel in self.panelList: #Hide all except for the first panel
            panel.Hide()
        self.panelList[0].Show()
        
        currentButton = 0   # Create buttons for each panel and bind them to the panels
        for panel in self.panelList:
            for i in range(self.buttonsPerPage):
                button = wx.Button(panel, wx.ID_ANY, _("%s"%(currentButton+1)))
                self.buttonList.append(button)
                currentButton += 1
                if currentButton + 1 > self.numButtons: #If the next button to be made is too high, break out of the loop
                    break
        #self.button_Fire1 = wx.Button(self.panel_ButtonPanel1, wx.ID_ANY, _("1"))

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.OnButton_Page, self.button_Up)
        self.Bind(wx.EVT_BUTTON, self.OnButton_Page, self.button_Down)

    def __set_properties(self):
        self.text_ctrl_Page.SetLabel("%s"%(self.currentPage))
        for button in self.buttonList:
            button.SetBackgroundColour(wx.NamedColour('YELLOW'))

    def __do_layout(self):
        sizer_Outer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Manual Fire")), wx.HORIZONTAL)
        #grid_sizer_Buttons = wx.GridSizer(4, 4, 5, 5)
        sizer_Page = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Page")), wx.VERTICAL)
        sizer_Page.Add(self.text_ctrl_Page, 0, 0, 0)
        sizer_Page.Add(self.button_Up, 3, wx.EXPAND, 0)
        sizer_Page.Add(self.button_Down, 3, wx.EXPAND, 0)
        sizer_Outer.Add(sizer_Page, 1, wx.EXPAND, 1)
        
        for i in range(self.numPages):
            self.gridSizerList.append(wx.GridSizer(self.numRows, self.numCols, self.spacing, self.spacing))
        
        for i in range(len(self.panelList)): #This looks like it is working
            for button in self.buttonList[i*self.buttonsPerPage : (i+1)*self.buttonsPerPage]:
                #grid_sizer_Buttons.Add(button, 0, wx.EXPAND, 0)
                self.gridSizerList[i].Add(button, 0, wx.EXPAND, 0)
                
        '''
        grid_sizer_Buttons.Add(self.buttonList[0], 0, wx.EXPAND, 0)
        grid_sizer_Buttons.Add(self.button_Fire2, 0, wx.EXPAND, 0)
        '''
        for idx, panel in enumerate(self.panelList):
            panel.SetSizer(self.gridSizerList[idx])
        #self.panelList[0].SetSizer(grid_sizer_Buttons)
        
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
        for panel in self.panelList:
            panel.Hide()
        self.panelList[self.currentPage - 1].Show()
        self.text_ctrl_Page.SetLabel("%s"%(self.currentPage))
        self.Layout()
