import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

numframes = 30
numpoints = 10
numsteps = 10
color_data = np.random.random((numframes, numpoints))
area = np.random.random((numsteps+1, numpoints))*4000
area[0] = 0

pause = False
drawnFrames = 1

def onClick(event):
	global pause
	pause ^= True

def main():
	x, y, c = np.random.random((3, numpoints))*2.0
	fig = plt.figure()

	xcenter = (x.max() + x.min()) / 2
	ycenter = (y.max() + y.min()) / 2
	xlength = (x.max() - xcenter) * 1.5
	ylength = (y.max() - ycenter) * 1.5
	fig.add_subplot(111,aspect='equal',
				 xlim=(xcenter - xlength, xcenter + xlength),
				 ylim=(ycenter - ylength, ycenter + ylength))
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
		if step > numsteps:
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
