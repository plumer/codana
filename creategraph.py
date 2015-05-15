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
        if not nodes.has_key(u[0].strip()) and len(u) == 2:
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

    #print g.number_of_nodes()
    #print g.number_of_edges()

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
#        print "hi"
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
 #       print n, node_sizes[n]
    return sizes

def pkg_filter(g):
    # removes built-in packages
    non_built_in = g.nodes()
    print "here"
    print nx.number_of_nodes(g)
    for n in nx.nodes_iter(g):
        print "n = ", n
        prime_pkg = split(n, ',')
        print prime_pkg
        if prime_pkg in built_in_pkgs:
            non_built_in.remove(prime_pkg)
    print "there"
    return g.subgraph(non_built_in)

"""
# get edge info from graph

nx.draw(sg, pos, alpha = .5, node_size = 0, node_color = color,
       with_labels = False, width=1, edge_color = '#aaaaaa', font_family = 'erewhon')
# show file points
plt.scatter(x,y,c=color, s=size, alpha=.5)

# register mouse event

def show_file_info(event):
#    print event.xdata, event.ydata
    nearest_dist = 1
    nearest_point = None
    for p in pos:
        dx = pos[p][0] - event.xdata
        dy = pos[p][1] - event.ydata
        distance = math.sqrt(dx**2 + dy**2)
        if (distance < 0.1 and distance < nearest_dist):
            nearest_dist = distance
            nearest_point = p

    if nearest_point != None:
        print nearest_point
"""
