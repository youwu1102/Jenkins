# -*- encoding:UTF-8 -*-
import wx
from Panel.TestSuite import TestSuite
"""
Author：You Wu

"""



class Client(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="Assistant Tool For Jenkins (HSS CI)", size=(800, 540))
        self.Center()
        panel = wx.Panel(self, -1)
        note_book = wx.Notebook(panel)
        note_book.AddPage(TestSuite(note_book), "Test Suite")



        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(note_book, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)



if __name__ == '__main__':
    app = wx.App()
    client = Client()
    client.Show()
    app.MainLoop()
