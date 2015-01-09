import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button


class Buttons:
    def __init__(self, filename):
        self.filename = filename
        
    def OK(self, event):
        plt.savefig(filename)
        plt.close()
        
class DraggableRectangle:
    def __init__(self, rect, vline):
        self.rect = rect
        self.xx = self.rect.xy[0]
        self.press = None
        self.line = vline
        self.line.set_offset_position('data')
        self.vline_loc = 0

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        #self.line.remove()
        contains, attrd = self.rect.contains(event)
        if not contains: return
        #print 'event contains', self.rect.xy
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print 'x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f'%(x0, xpress, event.xdata, dx, x0+dx)
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0)
        self.line.set_offsets([x0 + dx - self.xx, 0])
        
        self.rect.figure.canvas.draw()
        self.line.figure.canvas.draw()

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.rect.figure.canvas.draw()
        x0, y0 = self.rect.xy
        #set the center line points
        self.vline_loc = x0 + self.rect.get_width()/2
        

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)
        
fig = plt.figure()
ax = fig.add_subplot(111)
Fs = 150.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = np.arange(0,1,Ts) # time vector

ff = 5;   # frequency of the signal
y = np.sin(2*np.pi*ff*t)

n = len(t)
ax.plot(t, y)
filename = 'myfigure.png'
plt.title(filename)
maxV = np.max(np.abs(y))

#plot the background bar for selecting purpose
rect1 = ax.bar(t[int(n/3)], 2*maxV, 0.03, bottom = -maxV, color = '#FFFF00', alpha = 0.3, linewidth=0, zorder = 10)[0]
rect2 = ax.bar(t[int(n/2)], 2*maxV, 0.03, bottom = -maxV, color = '#FE2E2E', alpha = 0.3, linewidth=0, zorder = 10)[0]

#plot the center refernce line
vline1 = plt.vlines(rect1.xy[0] + rect1.get_width()/2, -maxV, maxV, zorder = 10, color = 'r')
vline2 = plt.vlines(rect2.xy[0] + rect2.get_width()/2, -maxV, maxV, zorder = 10, color = 'r')

#This is the class to do the main job
dr1= DraggableRectangle(rect1, vline1)
dr2 = DraggableRectangle(rect2, vline2)
dr1.connect()
dr2.connect()

start = dr1.vline_loc
end = dr2.vline_loc
print 'The start and end points you selected are (' + str(start) + ', ' + str(end) + ')'
callback = Buttons(filename)
axprev = plt.axes([0.7, 0.01, 0.1, 0.04])
bok = Button(axprev, 'OK')
bok.on_clicked(callback.OK)



plt.show()
