import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import networkx as nx
import math
import creategraph

fig = plt.figure()

def animationFigure():
    return fig


projectname = "tomcat"
version_array = ["6.0.0", "6.0.43", "7.0.0", "7.0.61", "8.0.0", "8.0.21"]
pos = None
x = None
y = None
size_array = []
numframes = 40
sg = None

def init():
    global projectname
    global version_aray
    global pos
    global x
    global y
    global size_array
    global numframes
    global sg
    for i in range(6):
        data_directory = projectname + "_history/" + projectname + version_array[i] + "/" + projectname
        [g, lines] = creategraph.readfile(data_directory)
        if i == 0:
            sg = creategraph.refine(g, 45)
            [pos, x, y] = creategraph.coordinate(sg)
            size = creategraph.point_sizes(sg, lines)
            zeros = np.array([0] * len(size))
            print 'len(size) = ', len(size)
            print 'zeros = ', zeros
            size_array.append(zeros)
            size_array.append(size)
        else:
            # create the graph induced by nodes from sg
            subg = nx.subgraph(g, nx.nodes(sg))
            print subg, sg
            if nx.number_of_nodes(subg) != nx.number_of_nodes(sg):
                print 'panic at 34' 
            else: #                            v  this seems to be a error, but not
                size = creategraph.point_sizes(sg, lines)
                size_array.append(size)


    x = np.array(x)
    y = np.array(y)
    size_array = np.array(size_array)
    
pause = False
drawnFrames = 1
numsteps = len(size_array)
# event functions
def nextVersion(event):
	global pause
	pause ^= True
        
def show_file_info(event):
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
        print nearest_point#, '\t', lines[nearest_point], ' lines of code'

# main func
def show():
    global numframes
    global numsteps
    global projectname
    global version_aray
    global pos
    global x
    global y
    global size_array
    global numframes
    global sg
    global fig
    xcenter = (x.max() + x.min()) / 2
    ycenter = (y.max() + y.min()) / 2
    xlength = (x.max() - xcenter) * 1.2
    ylength = (y.max() - ycenter) * 1.2
    fig.add_subplot(111,aspect='equal', xlim=(xcenter - xlength, xcenter + xlength),ylim=(ycenter - ylength, ycenter + ylength))

#	nx.draw_networkx_edges(g,pos)
    nx.draw(sg, pos, alpha=.5, node_size=0,
            with_labels = False, width=1, edge_color='#666666')

    color = np.random.random( len(x) )
    scat = plt.scatter(x, y, c=color, s=size_array[0], alpha = 0.5)

    fig.canvas.mpl_connect('key_press_event', nextVersion)
    fig.canvas.mpl_connect('button_press_event', show_file_info)
    ani = animation.FuncAnimation(fig, update_plot, frames=xrange(numframes*numsteps),
            interval = 20, fargs=(size_array, numframes, scat), repeat=True)
    plt.show()


def update_plot(i, area, nframes, scat):
	global pause
	global drawnFrames
	if not pause:
		step = drawnFrames / nframes
		if step >= numsteps:
			drawnFrames = 1
			step = 0
		frameno = drawnFrames % nframes
		c = (size_array[step+1] - size_array[step])/float(nframes**2)
		scat._sizes = -c*((frameno-nframes)**2) + size_array[step+1]
		drawnFrames = drawnFrames + 1
		if (drawnFrames % nframes == 0):
                    print size_array[step+1]
                    print size_array[step]
                    print c
		    pause = True
	return scat,

