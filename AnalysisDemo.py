import wx
#import matplotlib

class AnalysisDemo(wx.Frame):
    def __init__(self, *args, **kw):
        super(AnalysisDemo, self).__init__(*args, **kw)
        self.initMain()

    def initMain(self):
        pn = wx.Panel(self)

        self.showPackage = wx.RadioButton(pn, label='Organize in package')
        self.showClass = wx.RadioButton(pn, label='Organize in class')
#       self.canvas = matplotlib.figure.Figure()
        self.canvas = wx.TextCtrl(pn, style=wx.TE_MULTILINE | wx.HSCROLL)
        self.create = wx.Button(pn, label='Create Figure')

        self.create.Bind(wx.EVT_BUTTON, self.createFigure)

        optionBoxSizer = wx.BoxSizer(wx.VERTICAL)
        optionBoxSizer.Add(self.showPackage, proportion=0, flag=wx.TOP, border=5)
        optionBoxSizer.Add(self.showClass, proportion=0, flag=wx.TOP, border=5)
        optionBoxSizer.Add(self.create, proportion=0, flag=wx.TOP, border=5)

        mainBoxSizer = wx.BoxSizer()
        mainBoxSizer.Add(self.canvas, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        mainBoxSizer.Add(optionBoxSizer, proportion=0, flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, border=5)

        pn.SetSizer(mainBoxSizer)
        self.SetTitle('Analysis Demo')
        self.SetSize((600,400))
        self.Centre()
        self.Show(True)

    def createFigure(self, event):
        pass

def main():
    app = wx.App()
    AnalysisDemo(None)
    app.MainLoop()

if __name__ == '__main__':
    main()
