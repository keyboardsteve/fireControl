import wx
from wx.lib.pubsub import pub

import threading

import serial


class SerialComs():
    def __init__(self, handler):
        self.handler = handler
        #self.xbee = serial.Serial(timeout = 0.1)
        self.xbee = serial.Serial(timeout = 1)
        self.xbee.baudrate = 9600
        self.xbee.port = "COM3"  #THIS NEED TO AUTOMATICALLY FIND THE SERIAL DEVICE SOMEHOW...
        self.xbee.open()
        self.t = threading.Thread(target=self.recv)
        self.t.daemon = True
        self.t.start()
        
    def send(self, msg):
        tmp = msg+'\n'
        self.xbee.write(tmp.encode())
        
    def recv(self):
        msg = []
        while True:
            data = self.xbee.readline()
            pub.sendMessage("Receive_Coms", data = data)
    
    def shutdown(self):
        self.t.stop()
        self.xbee.close()
        