import wx
import gettext
import math
import os


class ManualButtonPanel(wx.Panel):
    def __init__(self, parent, numCols, numRows):
        wx.Panel.__init__(self, parent=parent)
        
        self.numCols = numCols
        self.numRows = numRows
        self.spacing = 5
        
        #self.disabledBitmap = wx.Bitmap(os.path.join(os.getcwd(),'assets',"disabledMask.PNG"), wx.BITMAP_TYPE_PNG)
        self.__set_Properties()
        self.__do_layout()
        
    def __set_Properties(self):
        pass
    
    def __do_layout(self):
        self.sizer_Grid = wx.GridSizer(self.numRows, self.numCols, self.spacing, self.spacing)
            
        self.SetSizer(self.sizer_Grid)
        self.sizer_Grid.Fit(self)
        
    def addButton(self, channel):
        b = wx.Button(self, int(channel), _("%s"%(channel)))
        self.sizer_Grid.Add(b, 1, wx.EXPAND)
        return b
        