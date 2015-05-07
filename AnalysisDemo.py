import wx
#import animate
#import matplotlib

class AnalysisDemo(wx.Frame):
    def __init__(self, *args, **kw):
        super(AnalysisDemo, self).__init__(*args, **kw)
        self.initMain()

    def initMain(self):
        pn = wx.Panel(self)

        self.showPackage = wx.RadioButton(pn, label='Organize in package')
        self.showClass = wx.RadioButton(pn, label='Organize in class')
#       self.canvas = animate.animationFigure()
        self.canvas = wx.TextCtrl(pn, style=wx.TE_MULTILINE | wx.HSCROLL)
        self.codeField = wx.TextCtrl(pn, style=wx.TE_MULTILINE | wx.HSCROLL)
        self.create = wx.Button(pn, label='Create Figure')
        self.prevVersion = wx.Button(pn, label='Previous Version')
        self.nextVersion = wx.Button(pn, label='Next Version')
        self.clickXText = wx.TextCtrl(pn, size=(50,-1))
        self.clickYText = wx.TextCtrl(pn, size=(50,-1))

        self.create.Bind(wx.EVT_BUTTON, self.createFigure)
        self.prevVersion.Bind(wx.EVT_BUTTON, self.movePrevVersion)
        self.nextVersion.Bind(wx.EVT_BUTTON, self.moveNextVersion)
        self.clickXText.SetEditable(False)
        self.clickYText.SetEditable(False)

        bodyBoxSizer = wx.BoxSizer()
        bodyBoxSizer.Add(self.canvas, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        bodyBoxSizer.Add(self.codeField, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        optionBoxSizer = wx.BoxSizer()
        optionBoxSizer.Add(self.showPackage, proportion=0, flag=wx.ALL, border=5)
        optionBoxSizer.Add(self.showClass, proportion=0, flag=wx.ALL, border=5)
        optionBoxSizer.Add(self.create, proportion=0, flag=wx.ALL, border=5)

        versionBoxSizer = wx.BoxSizer()
        versionBoxSizer.Add(self.nextVersion, proportion=0, flag=wx.ALL, border=5)
        versionBoxSizer.Add(self.prevVersion, proportion=0, flag=wx.ALL, border=5)
        versionBoxSizer.Add(self.clickXText, proportion=0, border=5)
        versionBoxSizer.Add(self.clickYText, proportion=0, border=5)

        bottomBoxSizer = wx.BoxSizer()
        bottomBoxSizer.Add(optionBoxSizer, proportion=0, flag=wx.ALL, border=5)
        bottomBoxSizer.Add(versionBoxSizer, proportion=0, flag=wx.ALL, border=5)

        mainBoxSizer = wx.BoxSizer(wx.VERTICAL)
        mainBoxSizer.Add(bodyBoxSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        mainBoxSizer.Add(bottomBoxSizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        pn.SetSizer(mainBoxSizer)
        self.SetTitle('Analysis Demo')
        self.SetSize((800,600))
        self.Centre()
        self.Show(True)

    def createFigure(self, event):
        pass

    def movePrevVersion(self, event):
        pass

    def moveNextVersion(self, event):
        pass

def main():
    app = wx.App()
    AnalysisDemo(None)
    app.MainLoop()

if __name__ == '__main__':
    main()
