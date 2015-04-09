import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import networkx as nx
import math

filename = "tomcat_depends.txt"
f = open(filename, "r")
edges = []
nodes = []
g = nx.Graph()

lcount = 0

while True:
	line = f.readline()
	if not line: break
	u = line.split('\t')
	g.add_edge(u[0],u[1])
	lcount = lcount + 1

f.close()
#print g.number_of_nodes()
#print g.number_of_edges()

small_nodes = []

for n in nx.nodes_iter(g):
	if nx.degree(g, n) <= 50:
		small_nodes.append(n)

for n in small_nodes:
	g.remove_node(n)

print "after:", g.number_of_nodes()


numframes = 30
numpoints = g.number_of_nodes()
numsteps = 1
color_data = np.random.random((numframes))
area = np.random.random((numsteps+1, numpoints))*1000
area[0] = 0

pos = nx.random_layout(g)

x = []
y = []

posv = pos.values()

for i in range(numpoints):
	x.append(posv[i][0])
	y.append(posv[i][1])

x = np.array(x)
y = np.array(y)

pause = False
drawnFrames = 1

def onClick(event):
	global pause
	pause ^= True

def main():

	c = np.random.random((1,numpoints))
	fig = plt.figure()

	xcenter = (x.max() + x.min()) / 2
	ycenter = (y.max() + y.min()) / 2
	xlength = (x.max() - xcenter) * 1.2
	ylength = (y.max() - ycenter) * 1.2
	fig.add_subplot(111,aspect='equal', xlim=(xcenter - xlength, xcenter + xlength),ylim=(ycenter - ylength, ycenter + ylength))

	nx.draw_networkx_edges(g,pos)

	scat = plt.scatter(x, y, c=c, s=x*y*1000, alpha = 0.5)
#	plt.plot(x,y)
	fig.canvas.mpl_connect('button_press_event', onClick)
	ani = animation.FuncAnimation(fig, update_plot, frames=xrange(numframes*numsteps),
		interval = 20, fargs=(area, numframes, scat), repeat=True)
	plt.show()
	

def update_plot(i, area, nframes, scat):
	global pause
	global drawnFrames
	if not pause:
		step = drawnFrames / numframes
		if step >= numsteps:
			drawnFrames = 1
			step = 0
		frameno = drawnFrames % nframes
		c = (area[step+1] - area[step])/(nframes**2)
		scat._sizes = -c*((frameno-nframes)**2) + area[step+1]
		drawnFrames = drawnFrames + 1
		if (drawnFrames % nframes == 0):
			pause = True
#			print drawnFrames
	return scat,

main()
