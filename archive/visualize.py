import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import networkx as nx
import math
import creategraph

fig = plt.figure()

projectname = "tomcat_history/tomcat6.0.0/tomcat"
[g, nodes] = creategraph.readfile(projectname)
#print g
sg = creategraph.refine(g, 40)


[pos,x,y] = creategraph.coordinate(sg)
size = creategraph.point_sizes(sg, nodes)

color = np.random.random(len(size))

nx.draw(sg, pos, alpha=.5, node_size=0, node_color=color,
        with_labels = False, width=1, edge_color='#aaaaaa')

plt.scatter(x, y, s=size, alpha = 0.5, c=color)

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
        print nearest_point, '\t', nodes[nearest_point], ' lines of code'

fig.canvas.mpl_connect('button_press_event', show_file_info)
# this should be the last command
plt.show()

"""
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
	fig.canvas.mpl_connect('button_press_event', showInfo)
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
"""
