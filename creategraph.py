import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import math

built_in_pkgs = [
        'java',         'xml',
        'util',
        'net',
        'lang',
        'javax',
        'awt',
        'concurrent'
]

class GraphShell:
    def __init__(self):
        self.graph = nx.Graph()
        self.pos = {}
        self.x = []
        self.y = []
        self.sizeDict = {}          # a dict from node name to integer
        self.sizes = []
    
    def setGraph(self, g):
        self.graph = g
        self.pos = nx.spring_layout(g)
        for n in nx.nodes_iter(g):
            self.x.append(self.pos[n][0])
            self.y.append(self.pos[n][1])
    
    def setSizeDict(self, sd):
        self.sizeDict = sd
        for key in sd:
            self.sizes.append(sd[key])

    def setEdges(self, edges):
        self.graph.add_edges_from(edges)

    def updateSizes(self):
        for n in nx.nodes_iter(self.graph):
            if self.sizeDict.has_key(n):
                pass
            else:
                self.sizeDict[n] = 0;
        if ( len(self.sizeDict) != len(self.graph.nodes()) ):
            print 'panic'
        self.sizes = []
        for key in self.sizeDict:
            self.sizes.append(self.sizeDict[key] * 40)

    def updateLayout(self):
        self.pos = nx.spring_layout(self.graph)
        self.x = []
        self.y = []
        for n in nx.nodes_iter(self.graph):
            self.x.append(self.pos[n][0])
            self.y.append(self.pos[n][1])

    def refine(self, threshold):

        big_nodes = []
        for n in nx.nodes_iter(self.graph):
            if nx.degree(self.graph, n) >= threshold:
                big_nodes.append(n)

        sg = self.graph.subgraph(big_nodes)
        self.setGraph(sg);




def readfile(project_name):
    # read in files
    filename = project_name + ".txt"
    print filename
    f = open(filename, "r")
    if not f:
        return None

    g = nx.Graph()
    nodes = {}
    
    while True:
        line = f.readline()
        if not line: break
        u = line.strip().split()
        if not nodes.has_key(u[0].strip()) and len(u) >= 2:
            if (u[1] != 'None'):
                nodes[u[0].strip()] = int(u[1])
    
    f.close()
    
    filename = project_name + "_depends.txt"
    f = open(filename, "r")
    
    while True:
        line = f.readline()
        if not line: break
        u = line.strip().split()
        if not nodes.has_key(u[0]):
            continue
        if not nodes.has_key(u[1]):
            continue
        g.add_edge(u[0], u[1])


    f.close()

    return g,nodes

# filter

def readpkg(project_name):
    pkgname = project_name + "_pack.txt"
    
    f = open(pkgname, "r")
    if not f:
        return None
    g = nx.Graph()
    nodes = {}

    while True:
        line = f.readline()
        if not line: break
        u = line.strip()
        root_pkg = u.split('.')
        if root_pkg[0] in built_in_pkgs: 
            continue
        if not nodes.has_key(u) and u != 'None':
            nodes[u] = 200
    f.close()

    pkgname = project_name + "_pack_depends.txt"
    f = open(pkgname, "r")

    while True:
        line = f.readline()
        if not line: break
        u = line.strip().split()
        if not nodes.has_key(u[0]): continue
        if not nodes.has_key(u[1]): continue
        if u[0] == u[1]:
            pass
        else:
            g.add_edge(u[0], u[1])
    f.close()
    return g,nodes

def refine(g, threshold):

    big_nodes = []
    
    for n in nx.nodes_iter(g):
        if nx.degree(g, n) >= threshold:
            big_nodes.append(n)

    sg = g.subgraph(big_nodes)

    return sg

def coordinate(g):
    pos = nx.spring_layout(g)
    
    x = []
    y = []
    for n in nx.nodes_iter(g):
        x.append(pos[n][0])
        y.append(pos[n][1])
    return pos, x, y

def point_sizes(g, node_sizes):
    sizes = []
    for n in nx.nodes_iter(g):
        if (node_sizes.has_key(n)):
            sizes.append(node_sizes[n])
        else:
            sizes.append(0)
    return sizes

def pkg_filter(g):
    # removes built-in packages
    non_built_in = g.nodes()
    for n in nx.nodes_iter(g):
        prime_pkg = n.split('.')
        if prime_pkg[0] in built_in_pkgs:
            non_built_in.remove(n)
    return g.subgraph(non_built_in)


