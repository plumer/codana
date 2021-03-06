import wx
import wx.grid
from matplotlib.figure import Figure
from matplotlib import pyplot
import matplotlib.animation as animation
import networkx as nx
import numpy as np
import math
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import creategraph
from projectdata import DataManager
import os

class AnalysisDemo(wx.Frame):
    """
    Attributes:
        versionArray (list) : a list of all versions
        dataManager(DataManager) : DataManager objects providing all versions of VersionDataManager
        curManager (VersionDataManager) : VersionDataManager object with corresponding version
        tpgShell (list) : a GraphShell object containing graph to be drawn
        sizes (array of arrays) : an array (corresponding to versions) of sizes
            of all nodes in the graph
    """
    APP_EXIT = 0
    APP_PREVVERSION = 1
    APP_NEXTVERSION = 2
    APP_PACKAGE = 3
    APP_CLASS = 4

    def __init__(self, *args, **kw):
        super(AnalysisDemo, self).__init__(*args, **kw)
        self.dataManage = DataManager()
        self.versionArray = self.dataManage.getVersionArray()
        self.curManage = self.dataManage.getManager(self.versionArray[0])
        self.curPackage = ''
        self.initMain()
        self.loadPackGraph()

    def loadPackGraph(self):
        self.tpgShell = []
        unionGraph = nx.Graph()
        for version in self.versionArray:
            dm = self.dataManage.getManager(version)
            gs = creategraph.GraphShell()
            g = nx.Graph()
            g.add_nodes_from(dm.getPackages())
            g.add_edges_from(dm.getPackageDependence())
            g = creategraph.pkg_filter(g)
            g = creategraph.refine(g, 20)
            
            # get size info

            sd = {}
            for n in nx.nodes_iter(g):
                node_attr = dm.getPackageAttr(n)
                if node_attr == None:
                    sd[n] = 0
                else:
                    file_num = node_attr['filenum']
                    if file_num == None:
                        sd[n] = 0
                    else:
                        sd[n] = int(file_num)

            # unionGraph has all the nodes

            unionGraph.add_nodes_from(g)
            unionGraph.add_edges_from(g.edges())

            bugList = []
            for p in g.nodes():
                if dm.getBugNumberOfPackage(p) != 0:
                    bugList.append(p)

            self.tpgShell.append( creategraph.GraphShell() )
            self.tpgShell[-1].setGraph(g)
            self.tpgShell[-1].setSizeDict(sd)
            self.tpgShell[-1].setBugList(bugList)

        # set all bottom graphs as u
        for gs in self.tpgShell:
            gs.graph.add_nodes_from(unionGraph)
            gs.updateSizes()

        
    def loadFileGraph(self, package):
        self.fgShell = []
        unionGraph = nx.Graph()
        for version in self.versionArray:
            dm = self.dataManage.getManager(version)
            # gs = creategraph.GraphShell()
            g = nx.Graph()
            g.add_nodes_from(dm.getFilesOfPackage(package))
            g.add_edges_from(dm.getFileDependenceOfPackage(package))
            g = creategraph.pkg_filter(g)
            #g = creategraph.refine(g, 2)

            sd = {}
            for n in nx.nodes_iter(g):
                node_attr = dm.getFileAttr(n)
                if node_attr == None:
                    sd[n] = 0
                else:
                    code_line = node_attr['codelines']
                    if code_line == None:
                        sd[n] = 0
                    else:
                        sd[n] = int(code_line)

            unionGraph.add_nodes_from(g)
            unionGraph.add_edges_from(g.edges())

            bugList = []
            for f in g.nodes():
                if dm.getBugNumberOfFile(f) != 0:
                    bugList.append(f)

            self.fgShell.append( creategraph.GraphShell() )
            self.fgShell[-1].setGraph(g)
            self.fgShell[-1].setSizeDict(sd)
            self.fgShell[-1].setBugList(bugList)

        for gs in self.fgShell:
            gs.graph.add_nodes_from(unionGraph)
            gs.updateSizes(8)


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
        self.showFile = wx.RadioButton(pn, label='Organize in file')

        self.prevVersion = wx.Button(pn, label='Previous Version')
        self.nextVersion = wx.Button(pn, label='Next Version')
        self.versionSlider = wx.Slider(pn, minValue=0, maxValue=len(self.versionArray)-1, size=(150,-1), style=wx.SL_AUTOTICKS)
        self.version = wx.TextCtrl(pn, value=self.versionArray[0], size=(50,-1))
        self.version.SetEditable(False)

        self.figure = pyplot.figure(facecolor='#f3f3f3')
        self.canvas = FigureCanvas(pn, -1, self.figure)
        self.axe = self.figure.add_subplot(111,aspect='equal')

        self.nameList = wx.ListBox(pn, choices=['All packages...', 'All files...'] + self.curManage.getPackages())
        self.codeField = wx.TextCtrl(pn, style=wx.TE_MULTILINE | wx.HSCROLL)
        self.codeField.SetEditable(False)
        self.codeField.SetFont( wx.Font(11,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL, faceName="Ubuntu Mono") )

        self.attrField = wx.grid.Grid(pn)
        self.attrField.CreateGrid(1, len(self.curManage.listPackageAttr()))
        self.attrField.SetRowLabelValue(0, 'Package name')
        self.attrField.SetRowLabelSize(200)
        readonlyAttr = wx.grid.GridCellAttr()
        readonlyAttr.SetReadOnly(True)
        self.attrField.SetRowAttr(0, readonlyAttr)
        for i in xrange(len(self.curManage.listPackageAttr())):
            self.attrField.SetColSize(i, 100)
            self.attrField.SetColLabelValue(i, self.curManage.listPackageAttr()[i])

        self.prevVersion.Bind(wx.EVT_BUTTON, self.movePrevVersion)
        self.nextVersion.Bind(wx.EVT_BUTTON, self.moveNextVersion)
        self.nameList.Bind(wx.EVT_LISTBOX_DCLICK, self.onDNameList)
        self.nameList.Bind(wx.EVT_LISTBOX, self.onNameList)
        self.showPackage.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton)
        self.showFile.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton)
        self.versionSlider.Bind(wx.EVT_SCROLL_CHANGED, self.onVersionScroll)

        contextBoxSizer = wx.BoxSizer(wx.VERTICAL)
        contextBoxSizer.Add(self.canvas, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        contextBoxSizer.Add(self.attrField, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, border=0)

        bodyBoxSizer = wx.BoxSizer()
        bodyBoxSizer.Add(self.nameList, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        bodyBoxSizer.Add(contextBoxSizer, proportion=3, flag=wx.EXPAND | wx.ALL, border=5)
        bodyBoxSizer.Add(self.codeField, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        optionBoxSizer = wx.BoxSizer()
        optionBoxSizer.Add(self.showPackage, proportion=0, flag=wx.ALL, border=0)
        optionBoxSizer.Add(self.showFile, proportion=0, flag=wx.ALL, border=0)

        versionCtrlBoxSizer = wx.BoxSizer()
        versionCtrlBoxSizer.Add(self.prevVersion, proportion=0, flag=wx.ALL, border=0)
        versionCtrlBoxSizer.Add(self.versionSlider, proportion=1, flag=wx.ALL, border=0)
        versionCtrlBoxSizer.Add(self.version, proportion=0, flag=wx.ALL, border=0)
        versionCtrlBoxSizer.Add(self.nextVersion, proportion=0, flag=wx.ALL, border=0)

        topSizer = wx.GridSizer()
        topSizer.Add(optionBoxSizer, proportion=0, flag=wx.LEFT | wx.RIGHT, border=5)
        topSizer.Add(versionCtrlBoxSizer, proportion=0, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT, border=5)

        mainBoxSizer = wx.BoxSizer(wx.VERTICAL)
        mainBoxSizer.Add(topSizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        mainBoxSizer.Add(bodyBoxSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        pn.SetSizer(mainBoxSizer)
        self.SetTitle('Analysis Demo')
        self.SetSize((1280,700))
        self.Centre()
        self.Show(True)

    def organizeInPackage(self, event):
        self.showPackage.SetValue(True)
        self.createFigure(event)

    def organizeInClass(self, event):
        self.showFile.SetValue(True)
        self.onRadioButton(event)

    def onRadioButton(self, event):
        if self.showPackage.GetValue() == True:
            self.curPackage = ''
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['All files...', 'All packages...'] + self.curManage.getPackages())
            if len(self.curManage.listPackageAttr()) == self.attrField.GetNumberCols():
                return
            elif len(self.curManage.listPackageAttr()) > len(self.curManage.listFileAttr()):
                self.attrField.AppendCols(len(self.curManage.listPackageAttr()) - len(self.curManage.listFileAttr()))
            elif len(self.curManage.listPackageAttr()) < len(self.curManage.listFileAttr()):
                self.attrField.DeleteCols(len(self.curManage.listFileAttr())-1, len(self.curManage.listFileAttr()) - len(self.curManage.listPackageAttr()))
            self.setAttrs('Package name')
            self.showDetails('Package name')
        else:
            self.curPackage = ''
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['Packages...', 'Files...'] + self.curManage.getFilenames())
            if len(self.curManage.listFileAttr()) == self.attrField.GetNumberCols():
                return
            elif len(self.curManage.listFileAttr()) > len(self.curManage.listPackageAttr()):
                self.attrField.AppendCols(len(self.curManage.listFileAttr()) - len(self.curManage.listPackageAttr()))
            elif len(self.curManage.listFileAttr()) < len(self.curManage.listPackageAttr()):
                self.attrField.DeleteCols(len(self.curManage.listPackageAttr())-1, len(self.curManage.listPackageAttr()) - len(self.curManage.listFileAttr()))
            self.setAttrs('File name')
            self.showDetails('File name')

    def onNameList(self, event):
        # TODO Center the current selection
        curChoice = self.nameList.GetString(self.nameList.GetSelection()).encode('ascii', 'ignore')
        if curChoice == '':
            return
        if self.showPackage.GetValue() == True:
            if curChoice == 'All files...' or curChoice == 'All packages...':
                self.setAttrs('Package name')
                self.showDetails('Package name')
            else:
                self.setAttrs(curChoice)
                self.showDetails(curChoice)
        else:
            if curChoice == 'Files...' or curChoice == 'Packages...':
                self.setAttrs('File name')
                self.showDetails('File name')
            else:
                self.setAttrs(curChoice)
                self.showDetails(curChoice)

    def onDNameList(self, event):
        namestr = self.nameList.GetString(self.nameList.GetSelection()).encode('ascii', 'ignore')
        if namestr == '':
            return
        if self.showPackage.GetValue() == True:
            # Select package here, update figure
            if namestr == 'All files...':
                # TODO Back to all file figure
                self.showFile.SetValue(True)
                self.nameList.Clear()
                self.nameList.InsertItems(pos=0, items=['Packages...', 'Files...'] + self.curManage.getFilenames())
                if len(self.curManage.listFileAttr()) > len(self.curManage.listPackageAttr()):
                    self.attrField.AppendCols(len(self.curManage.listFileAttr()) - len(self.curManage.listPackageAttr()))
                elif len(self.curManage.listFileAttr()) < len(self.curManage.listPackageAttr()):
                    self.attrField.DeleteCols(len(self.curManage.listPackageAttr())-1, len(self.curManage.listPackageAttr()) - len(self.curManage.listFileAttr()))
                self.setAttrs('File name')
                self.showDetails('File name')
            elif namestr == 'All packages...':
                # Done Back to all package figure
                self.preparePackGraph()
                self.scat.remove()
                self.remove_lines()
                self.draw()
            else:
                self.curPackage = namestr
                self.showFile.SetValue(True)
                self.nameList.Clear()
                self.nameList.InsertItems(pos=0, items=['Packages...', 'Files...'] + self.curManage.getFilesOfPackage(namestr))
                if len(self.curManage.listFileAttr()) > len(self.curManage.listPackageAttr()):
                    self.attrField.AppendCols(len(self.curManage.listFileAttr()) - len(self.curManage.listPackageAttr()))
                elif len(self.curManage.listFileAttr()) < len(self.curManage.listPackageAttr()):
                    self.attrField.DeleteCols(len(self.curManage.listPackageAttr())-1, len(self.curManage.listPackageAttr()) - len(self.curManage.listFileAttr()))
                self.setAttrs('File name')
                self.showDetails('File name')

                # Done Update figure here
                self.prepareFileGraph(self.curPackage)
                self.scat.remove()
                self.remove_lines()
                self.draw()
        else:
            # Select file here, update figure
            if namestr == 'Packages...':
                self.curPackage = ''
                self.showPackage.SetValue(True)
                self.nameList.Clear()
                self.nameList.InsertItems(pos=0, items=['All files...', 'All packages...'] + self.curManage.getPackages())
                if len(self.curManage.listPackageAttr()) > len(self.curManage.listFileAttr()):
                    self.attrField.AppendCols(len(self.curManage.listPackageAttr()) - len(self.curManage.listFileAttr()))
                elif len(self.curManage.listPackageAttr()) < len(self.curManage.listFileAttr()):
                    self.attrField.DeleteCols(len(self.curManage.listFileAttr())-1, len(self.curManage.listFileAttr()) - len(self.curManage.listPackageAttr()))
                self.setAttrs('Package name')
                self.showDetails('Package name')
                # Done Back to package figure
                self.preparePackGraph()
                self.scat.remove()
                self.remove_lines()
                self.draw()
            elif namestr == 'Files...':
                # TODO Back to file figure, circular
                pass
            else:
                # TODO Update figure here, circular
                pass

    def onVersionScroll(self, event):
        self.version.SetValue(self.versionArray[self.versionSlider.GetValue()])
        self.curManage = self.dataManage.getManager(self.versionArray[self.versionSlider.GetValue()])
        if self.showPackage.GetValue() == True:
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['All files...', 'All packages...'] + self.curManage.getPackages())
        elif self.curPackage == '':
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['Packages...', 'Files...'] + self.curManage.getFilenames())
        else:
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['Packages...', 'Files...'] + self.curManage.getFilesOfPackage(self.curPackage))
       
    def movePrevVersion(self, event):
        versionValue = self.versionSlider.GetValue()
        if self.versionSlider.GetMin() < versionValue:
            versionValue = versionValue - 1
        self.versionSlider.SetValue(versionValue)
        self.version.SetValue(self.versionArray[versionValue])
        self.curManage = self.dataManage.getManager(self.versionArray[versionValue])
        if self.showPackage.GetValue() == True:
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['All files...', 'All packages...'] + self.curManage.getPackages())
        elif self.curPackage == '':
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['Packages...', 'Files...'] + self.curManage.getFilenames())
        else:
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['Packages...', 'Files...'] + self.curManage.getFilesOfPackage(self.curPackage))
        self.codeField.SetValue('Move to previous version')
        if self.pause == True:
            if (self.step > 0):
                #print 'prev version, step = ', self.step
                self.currentSizes = np.array(self.gShell[self.step].sizes)
                self.nextSizes = np.array(self.gShell[self.step - 1].sizes)
                self.c = np.array(self.nextSizes - self.currentSizes) / float(self.numframes**2)
                self.stepdelta = -1
                self.pause = False

    def moveNextVersion(self, event):
        versionValue = self.versionSlider.GetValue()
        if versionValue < self.versionSlider.GetMax():
            versionValue = versionValue + 1
        self.versionSlider.SetValue(versionValue)
        self.version.SetValue(self.versionArray[versionValue])
        self.curManage = self.dataManage.getManager(self.versionArray[versionValue])
        if self.showPackage.GetValue() == True:
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['All files...', 'All packages...'] + self.curManage.getPackages())
        elif self.curPackage == '':
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['Packages...', 'Files...'] + self.curManage.getFilenames())
        else:
            self.nameList.Clear()
            self.nameList.InsertItems(pos=0, items=['Packages...', 'Files...'] + self.curManage.getFilesOfPackage(self.curPackage))
        self.codeField.SetValue('Move to next version...')
        if self.pause == True:
            #print 'next version, step = ', self.step
            if (self.step < len(self.versionArray)):
                self.currentSizes = np.array(self.gShell[self.step].sizes, dtype=float)
                self.nextSizes = np.array(self.gShell[self.step + 1].sizes, dtype=float)
                self.c = np.array(self.nextSizes - self.currentSizes) / float(self.numframes**2)
                self.stepdelta = 1
                self.pause = False

    def setAttrs(self, name):
        self.attrField.SetRowLabelValue(0, name)
        if name == 'Package name':
            for i in xrange(len(self.curManage.listPackageAttr())):
                self.attrField.SetColSize(i, 100)
                self.attrField.SetColLabelValue(i, self.curManage.listPackageAttr()[i])
                self.attrField.SetCellValue(0, i, '')
        elif name == 'File name':
            for i in xrange(len(self.curManage.listFileAttr())):
                self.attrField.SetColSize(i, 100)
                self.attrField.SetColLabelValue(i, self.curManage.listFileAttr()[i])
                self.attrField.SetCellValue(0, i, '')
        else:
            if self.showPackage.GetValue() == True:
                for i in xrange(len(self.curManage.listPackageAttr())):
                    self.attrField.SetCellValue(0, i, self.curManage.getPackageAttr(name)[self.attrField.GetColLabelValue(i)])
            else:
                for i in xrange(len(self.curManage.listFileAttr())):
                    self.attrField.SetCellValue(0, i, self.curManage.getFileAttr(name)[self.attrField.GetColLabelValue(i)])

    def showDetails(self, name):
        if name == 'Package name':
            showstr = 'Packages in this project:\n'
            for packs in self.curManage.getPackages():
                showstr = showstr + packs + '\n'
            self.codeField.SetValue(showstr)
        elif name == 'File name':
            showstr = ''
            if self.curPackage == '':
                showstr = showstr + 'Files in this project:\n'
                for files in self.curManage.getFilenames():
                    showstr = showstr + files + '\n'
            else:
                showstr = showstr + 'Files in ' + self.curPackage + ' package:\n'
                for files in self.curManage.getFilesOfPackage(self.curPackage):
                    showstr = showstr + files + '\n'
            self.codeField.SetValue(showstr)
        else:
            showstr = ''
            if self.showPackage.GetValue() == True:
                showstr = showstr + 'Files in ' + name + ' package:\n'
                for files in self.curManage.getFilesOfPackage(name):
                    showstr = showstr + files + '\n'
                self.codeField.SetValue(showstr)
            else:
                if os.name == 'posix' and self.version.GetValue() != self.versionArray[0]\
                    and name in self.dataManage.getManager(self.versionArray[self.versionSlider.GetValue()-1]).getFilenames():
                    self.codeField.SetValue(os.popen(r"diff --new-line-format='+%L' --old-line-format='-%L' --unchanged-line-format='%L' tomcat_files/"
                                                     + self.version.GetValue() + "/" + name + " tomcat_files/" + self.versionArray[self.versionSlider.GetValue() - 1]
                                                     + "/" + name).read())
                else:
                    self.codeField.LoadFile(r'tomcat_files/' + self.version.GetValue() + '/' + name)

    def onQuit(self, event):
        self.Close()

    def preparePackGraph(self):
        self.gShell = self.tpgShell
        self.updatePosition()

    def prepareFileGraph(self, package):
        self.loadFileGraph(package)
        self.gShell = self.fgShell
        self.updatePosition()
        #print self.pos

    def updatePosition(self):
        unionGraph = nx.Graph()
        for g in self.gShell:
            unionGraph.add_nodes_from(g.graph)
            unionGraph.add_edges_from(g.graph.edges())
        self.pos = nx.spring_layout(unionGraph)
        self.x = []
        self.y = []
        for n in nx.nodes_iter(unionGraph):
            self.x.append(self.pos[n][0])
            self.y.append(self.pos[n][1])

    def updateColor(self, version):
        self.color = []
        bugList = self.gShell[version].bugList
        for k in self.pos.keys():
            if k in bugList:
                self.color.append( self.randomBadColor() )
            else:
                self.color.append( self.randomNormalColor() )

    def randomNormalColor(self):
        rcolor = int(np.random.random() * 60)
        gcolor = int(np.random.random() * 60 + 80)
        bcolor = int(np.random.random() * 60 + 160)
        c = '#%06x' % (rcolor * 65536 + gcolor * 256 + bcolor)
        return c

    def randomBadColor(self):
        rcolor = int(np.random.random() * 60 + 160)
        gcolor = int(np.random.random() * 60 + 80)
        bcolor = int(np.random.random() * 60)

        c = '#%06x' % (rcolor * 65536 + gcolor * 256 + bcolor)
        return c

        

    def draw(self):
        self.pause = True
        self.drawnFrames = 1
        self.numframes = 40
        self.numsteps = len(self.versionArray) + 1
        self.c = []
        self.currentSizes = []
        self.nextSizes = []
        self.step = 0

        x = np.array(self.x)
        y = np.array(self.y)
        xcenter = (x.max() + x.min()) / 2
        ycenter = (y.max() + y.min()) / 2
        xlength = (x.max() - xcenter) * 1.1
        ylength = (y.max() - ycenter) * 1.1
        self.axe.set_xlim(xcenter-xlength, xcenter+xlength)
        self.axe.set_ylim(ycenter-ylength, ycenter+ylength)

        self.draw_edges()

        self.color = []
        self.updateColor(self.step)
        self.scat = self.axe.scatter(x, y, c=self.color,
                s=self.gShell[self.step].sizes, alpha = .6)

        self.axe.set_frame_on(False)
        self.axe.axes.get_yaxis().set_visible(False)
        self.axe.axes.get_xaxis().set_visible(False)
        self.ani = animation.FuncAnimation(self.figure, self.update_plot, frames=xrange(self.numframes*self.numsteps),
            interval = 20, fargs=(self.numframes, self.scat), repeat=True, repeat_delay = 80) 
        #self.figure.show()


    def draw_edges(self, a = .4):
        self.plot_lines = []
        for e in nx.edges_iter(self.gShell[self.step].graph):
            p1 = self.pos[e[0]]
            p2 = self.pos[e[1]]
            l, = self.axe.plot([p1[0],p2[0]], [p1[1], p2[1]], alpha=a, aa=True, color='#999999')
            self.plot_lines.append(l)

    def update_plot(self, i, nframes, scat):
        if not self.pause:
            # self.step = self.drawnFrames / nframes

            if self.step >= self.numsteps:
                self.drawnFrames = 1
                self.step = 0
            frameno = self.drawnFrames % nframes
            scat._sizes = -self.c*((frameno-nframes)**2) + self.nextSizes
            self.drawnFrames = self.drawnFrames + 1
            if (self.drawnFrames % nframes == 0):
                self.pause = True
                self.remove_lines()
                self.step = self.step + self.stepdelta
                self.draw_edges()
                self.updateColor(self.step)
                scat.set_color(self.color)
        return scat,

    def show_info(self, event):
        if event.xdata == None or event.ydata == None:
            print 'None'
            return
        nearest_dist = 1
        nearest_point = None
        sd = self.gShell[self.step].sizeDict
        for p in self.pos:
            dx = self.pos[p][0] - event.xdata
            dy = self.pos[p][1] - event.ydata
            distance = math.sqrt(dx**2 + dy**2)
            if (distance < 0.1 and distance < nearest_dist and sd[p] != 0):
                nearest_dist = distance
                nearest_point = p
#        print 'nearest_point = ', nearest_point

        if nearest_point != None:
            #message = nearest_point + '\t' + str(sd[nearest_point])
            #self.codeField.SetValue(message)
            self.setAttrs(nearest_point)
            self.showDetails(nearest_point)
    
    def remove_lines(self):
        while self.plot_lines:
            l = self.plot_lines.pop(0)
            l.remove()
            del l

def main():
    app = wx.App()
    analysis = AnalysisDemo(None) 
    analysis.preparePackGraph()
    analysis.draw()
#    ani = animation.FuncAnimation(analysis.figure, analysis.update_plot, frames=xrange(analysis.numframes*analysis.numsteps),
#        interval = 20, fargs=(analysis.size_array, analysis.numframes, analysis.scat), repeat=True)

    # analysis.figure.canvas.mpl_connect('key_press_event', analysis.next_version)
    analysis.figure.canvas.mpl_connect('button_press_event', analysis.show_info)
    app.MainLoop()

if __name__ == '__main__':
    main()
