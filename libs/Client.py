# -*- encoding:UTF-8 -*-
import wx

"""
Author：You Wu

"""


class Client(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="Assistant Tool For Jenkins (HSS CI)", size=(600, 600))
        self.Center()
        self.panel = wx.Panel(self, -1)





if __name__ == '__main__':
    app = wx.App()
    client = Client()
    client.Show()
    app.MainLoop()
