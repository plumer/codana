import wx
from matplotlib.figure import Figure
import matplotlib.animation as animation
import networkx as nx
import numpy as np
import math
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import creategraph
from projectdata import DataManager

class AnalysisDemo(wx.Frame):
    APP_EXIT = 0
    APP_PREVVERSION = 1
    APP_NEXTVERSION = 2
    APP_PACKAGE = 3
    APP_CLASS = 4
    def __init__(self, *args, **kw):
        super(AnalysisDemo, self).__init__(*args, **kw)
        self.dataManage = DataManager()
        self.initMain()

    def initMenuBar(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        quitProg = wx.MenuItem(fileMenu, self.APP_EXIT, '&Quit\tCtrl+Q')
        fileMenu.AppendItem(quitProg)

        ctrlMenu = wx.Menu()
        prevVer = wx.MenuItem(ctrlMenu, self.APP_PREVVERSION, '&Prev Version\tCtrl+P')
        nextVer = wx.MenuItem(ctrlMenu, self.APP_NEXTVERSION, '&Next Version\tCtrl+N')
        orgInPackage = wx.MenuItem(ctrlMenu, self.APP_PACKAGE, 'Organize in &Package\tF5')
        orgInClass = wx.MenuItem(ctrlMenu, self.APP_CLASS, 'Organize in &Class\tF6')
        ctrlMenu.AppendItem(prevVer)
        ctrlMenu.AppendItem(nextVer)
        ctrlMenu.AppendSeparator()
        ctrlMenu.AppendItem(orgInPackage)
        ctrlMenu.AppendItem(orgInClass)

        self.Bind(wx.EVT_MENU, self.movePrevVersion, id=self.APP_PREVVERSION)
        self.Bind(wx.EVT_MENU, self.moveNextVersion, id=self.APP_NEXTVERSION)
        self.Bind(wx.EVT_MENU, self.onQuit, id=self.APP_EXIT)
        self.Bind(wx.EVT_MENU, self.organizeInPackage, id=self.APP_PACKAGE)
        self.Bind(wx.EVT_MENU, self.organizeInClass, id=self.APP_CLASS)

        menubar.Append(fileMenu, '&File')
        menubar.Append(ctrlMenu, '&Ctrl')
        self.SetMenuBar(menubar)

    def initMain(self):
        pn = wx.Panel(self)

        self.initMenuBar()

        self.showPackage = wx.RadioButton(pn, label='Organize in package')
        self.showClass = wx.RadioButton(pn, label='Organize in class')

        #self.figure = animate.animationFigure()
        #animate.init()
        #animate.show()
        self.figure = Figure(facecolor='#f3f3f3')
        self.canvas = FigureCanvas(pn, -1, self.figure)

        self.nameList = wx.ListBox(pn, choices=['Packages...', 'Files...'] + self.dataManage.getPackages())
        self.codeField = wx.TextCtrl(pn, style=wx.TE_MULTILINE | wx.HSCROLL)
        self.create = wx.Button(pn, label='Create Figure')
        self.prevVersion = wx.Button(pn, label='Previous Version')
        self.nextVersion = wx.Button(pn, label='Next Version')

        self.create.Bind(wx.EVT_BUTTON, self.createFigure)
        self.prevVersion.Bind(wx.EVT_BUTTON, self.movePrevVersion)
        self.nextVersion.Bind(wx.EVT_BUTTON, self.moveNextVersion)
        self.nameList.Bind(wx.EVT_LISTBOX_DCLICK, self.onNameList)

        bodyBoxSizer = wx.BoxSizer()
        bodyBoxSizer.Add(self.nameList, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        bodyBoxSizer.Add(self.canvas, proportion=3, flag=wx.EXPAND | wx.ALL, border=5)
        bodyBoxSizer.Add(self.codeField, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        optionBoxSizer = wx.BoxSizer()
        optionBoxSizer.Add(self.showPackage, proportion=0, flag=wx.ALL, border=0)
        optionBoxSizer.Add(self.showClass, proportion=0, flag=wx.ALL, border=0)
        optionBoxSizer.Add(self.create, proportion=0, flag=wx.ALL, border=0)

        versionBoxSizer = wx.BoxSizer()
        versionBoxSizer.Add(self.nextVersion, proportion=0, flag=wx.ALL, border=0)
        versionBoxSizer.Add(self.prevVersion, proportion=0, flag=wx.ALL, border=0)

        topBoxSizer = wx.BoxSizer()
        topBoxSizer.Add(versionBoxSizer, proportion=0, flag=wx.RIGHT, border=20)
        topBoxSizer.Add(optionBoxSizer, proportion=0, flag=wx.ALL, border=0)

        mainBoxSizer = wx.BoxSizer(wx.VERTICAL)
        mainBoxSizer.Add(topBoxSizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        mainBoxSizer.Add(bodyBoxSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        pn.SetSizer(mainBoxSizer)
        self.SetTitle('Analysis Demo')
        self.SetSize((1080,600))
        self.Centre()
        self.Show(True)

    def organizeInPackage(self, event):
        self.showPackage.SetValue(True)
        self.createFigure(event)

    def organizeInClass(self, event):
        self.showClass.SetValue(True)
        self.createFigure(event)

    def onNameList(self, event):
        namestr = self.nameList.GetString(self.nameList.GetSelection())
        if self.showClass.GetValue() == True:
            # TODO Select package here, update figure
            if namestr == 'All files...':
                # TODO Back to all file figure
                pass
            else:
                pass
        else:
            # TODO Select file here, update figure
            if namestr == 'Packages...':
                # TODO Back to package figure
                pass
            elif namestr == 'Files...':
                # TODO Back to file figure
                pass
            else:
                pass

    def createFigure(self, event):
        if self.showPackage.GetValue() == True:
            self.prepare(True)
        elif self.showClass.GetValue() == True:
            self.prepare(False)
        self.draw()
       
    def movePrevVersion(self, event):
        pass

    def moveNextVersion(self, event):
        self.next_version(event)

    def onQuit(self, event):
        self.Close()
    
    def prepare(self, is_package):
        projectname = "tomcat"
        version_array = ["6.0.0", "6.0.43", "7.0.0", "7.0.61", "8.0.0", "8.0.21"]
        self.pos = None
        self.x = None
        self.y = None
        self.size_array = []
        self.numframes = 40
        self.sg = None
        self.lines = []
        for i in range(6):
            data_directory = projectname + "_history/" + projectname + version_array[i] + "/" + projectname
            if is_package == False:
                [g, self.lines] = creategraph.readfile(data_directory)
                filter_threshold = 45
            else :
                [g, self.lines] = creategraph.readpkg(data_directory)
                filter_threshold = 20
                #print "|g.V| = ", nx.number_of_nodes(g)

            if i == 0:
                self.sg = creategraph.refine(g, filter_threshold)
                print nx.number_of_nodes(self.sg)
                [self.pos, self.x, self.y] = creategraph.coordinate(self.sg)
                size = creategraph.point_sizes(self.sg, self.lines)
                zeros = np.array([0] * len(size))
                self.size_array.append(zeros)
                self.size_array.append(size)
            else:
                # create the graph induced by nodes from sg
                subg = nx.subgraph(g, nx.nodes(self.sg))
                if nx.number_of_nodes(subg) != nx.number_of_nodes(self.sg):
                    print 'panic at 34', nx.number_of_nodes(subg), nx.number_of_nodes(self.sg)
                #else: #                            v  this seems to be a error, but not
                size = creategraph.point_sizes(self.sg, self.lines)
                self.size_array.append(size)
        self.x = np.array(self.x)
        self.y = np.array(self.y)
        self.size_array = np.array(self.size_array)

        self.pause = False
        self.drawnFrames = 1
        self.numsteps = len(self.size_array)

    def draw(self):
        print "what am I doing"
        xcenter = (self.x.max() + self.x.min()) / 2
        ycenter = (self.y.max() + self.y.min()) / 2
        xlength = (self.x.max() - xcenter) * 1.2
        ylength = (self.y.max() - ycenter) * 1.2
        self.figure.clf()
        self.axe = self.figure.add_subplot(111,aspect='equal', xlim=(xcenter - xlength, xcenter + xlength),
                  ylim=(ycenter - ylength, ycenter + ylength))

        # nx.draw_networkx_edges(g,pos)
        nx.draw(self.sg, self.pos, alpha=.3, node_size=0,
                  with_labels = False, width=1, edge_color='#666666')
        for e in nx.edges_iter(self.sg):
            p1 = self.pos[e[0]]
            p2 = self.pos[e[1]]
            self.axe.plot([p1[0],p2[0]], [p1[1], p2[1]], alpha=.5, aa=True, color='#666666')
        # self.axe.draw()

        color = np.random.random( len(self.x) )
        self.scat = self.axe.scatter(self.x, self.y, c=color, s=self.size_array[0], alpha = 0.5)

        self.axe.set_frame_on(False)
        self.axe.axes.get_yaxis().set_visible(False)
        self.axe.axes.get_xaxis().set_visible(False)

    def update_plot(self, i, area, nframes, scat):
        if not self.pause:
            self.step = self.drawnFrames / nframes
            if self.step >= self.numsteps:
                self.drawnFrames = 1
                self.step = 0
            frameno = self.drawnFrames % nframes
            c = (self.size_array[self.step+1] - self.size_array[self.step])/float(nframes**2)
            scat._sizes = -c*((frameno-nframes)**2) + self.size_array[self.step+1]
            self.drawnFrames = self.drawnFrames + 1
            if (self.drawnFrames % nframes == 0):
                self.pause = True
        return scat,

    def next_version(self,event):
        self.pause ^= True
        
    def show_file_info(self, event):
        nearest_dist = 1
        nearest_point = None
        for p in self.pos:
            dx = self.pos[p][0] - event.xdata
            dy = self.pos[p][1] - event.ydata
            distance = math.sqrt(dx**2 + dy**2)
            if (distance < 0.1 and distance < nearest_dist):
                nearest_dist = distance
                nearest_point = p

        if nearest_point != None:
            # print nearest_point#, '\t', lines[nearest_point], ' lines of code'
            self.codeField.SetValue(nearest_point)

def main():
    app = wx.App()
    analysis = AnalysisDemo(None) 
    analysis.prepare(False)
    analysis.draw()
    ani = animation.FuncAnimation(analysis.figure, analysis.update_plot, frames=xrange(analysis.numframes*analysis.numsteps),
        interval = 20, fargs=(analysis.size_array, analysis.numframes, analysis.scat), repeat=True)

    # analysis.figure.canvas.mpl_connect('key_press_event', analysis.next_version)
    analysis.figure.canvas.mpl_connect('button_press_event', analysis.show_file_info)
    app.MainLoop()

if __name__ == '__main__':
    main()
