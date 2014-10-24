#!/usr/bin/python

import numpy as np
import argparse
import glob
#from obspy import Stream


'''
Author: Qingkai Kong, qingkai.kong@gmail.com

This is a script quickly view station on maps and the waveforms. 

It plots map of the stations on the top, and the waveform data at bottom. 
When you select the station on the map, the corresponding waveform will 
show up in the bottom. 

To do, add the command line arguments. 
'''

class PointBrowser:
    """
    Click on a point to select and highlight it -- the data that
    generated the point will be shown in the lower axes.  Use the 'n'
    and 'p' keys to browse through the next and previous points
    """
    def __init__(self):
        self.lastind = 0

        self.text = ax.text(0.05, 0.95, 'selected: none',
                            transform=ax.transAxes, va='top')
        self.selected,  = ax.plot([xs[0]], [ys[0]], 'o', ms=12, alpha=0.7,
                                  color='yellow', visible=False)

    def onpress(self, event):
        if self.lastind is None: return
        if event.key not in ('n', 'p'): return
        if event.key=='n': inc = 1
        else:  inc = -1


        self.lastind += inc
        self.lastind = np.clip(self.lastind, 0, len(xs)-1)
        self.update()

    def onpick(self, event):

       if event.artist!=line: return True

       N = len(event.ind)
       if not N: return True

       # the click locations
       x = event.mouseevent.xdata
       y = event.mouseevent.ydata


       distances = np.hypot(x-xs[event.ind], y-ys[event.ind])
       indmin = distances.argmin()
       dataind = event.ind[indmin]

       self.lastind = dataind
       self.update()

    def update(self):
        if self.lastind is None: return

        dataind = self.lastind
        
        rec = X[dataind]
        
        time = np.arange(len(X[dataind])) / sample_rate[dataind]
        
        ax2.cla()
        ax2.plot(time, rec)
        plt.xlabel('Time (sec)', fontsize = 14)

        #ax2.text(0.05, 0.9, 'mu=%1.3f\nsigma=%1.3f'%(xs[dataind], ys[dataind]),transform=ax2.transAxes, va='top')
        self.selected.set_visible(True)
        self.selected.set_data(xs[dataind], ys[dataind])

        self.text.set_text('selected: %s'%stnm[dataind])
        fig.canvas.draw()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from obspy.core import read
    from mpl_toolkits.basemap import Basemap
    
    
    parser = argparse.ArgumentParser(description='Example: data_browser.py -i \'*.BHN.sac\' -evla 38 -evlo -122 -r l')
    
    #option for specify the files
    parser.add_argument('-i', '--input', action='store', dest='input',
                    help='specify input files as strings')
                    
    #option for specify location of the event
    #parser.add_argument ('-e', '--event',nargs=2, action='append',
    #                help='specify the latitude and longitude of the event')  
    
    parser.add_argument('-evla', action='store', type = float,
                    help='specify the latitude of the event as float number')
    parser.add_argument('-evlo', action='store', type = float,
                    help='specify the longitude of the event as float number') 
                    
    parser.add_argument('-r', '--resolution', action='store',
                    help='specify input files as strings')                
        
    results = parser.parse_args()
    
    filename = results.input
    if filename:
        st = read(filename) 
    else:
        st = read('./*.sac')   
    
    if results.evla and results.evlo:
        evla = results.evla
        evlo = results.evlo
    else:
        try:
            tr = st[0]
            evla = tr.stats.sac.evla
            evlo = tr.stats.sac.evlo
        except:
            evla = None
            evlo = None
            
    resolution = results.resolution
    if not resolution:
        resolution = 'l'
            
    data = []   
    stla = []
    stlo = []
    kstnm = []
    sample_rate = []
    
    n = len(st)

    for i in range(0, n):
        stla.append(st[i].stats['sac']['stla'])
        stlo.append(st[i].stats['sac']['stlo'])
        kstnm.append(st[i].stats['station'])
        sample_rate.append(st[i].stats['sampling_rate'])
        data.append(st[i].data)
        
    max_lat = max(stla)
    max_lon = max(stlo)
    min_lat = min(stla)
    min_lon = min(stlo)
    
    ys = np.array(stla)
    xs = np.array(stlo)
    X = np.array(data)    
    #t = np.range()
    stnm = np.array(kstnm)
        
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.set_title('select the seismic station to plot the waveform')
    #line, = ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance
    #ax.set_ylim(33.7527, 33.848)
    #ax.set_xlim(-118.214, -118.125)
    lat0 = min_lat - 0.5
    lat1 = max_lat + 0.5
    lon0 = min_lon - 0.5
    lon1 = max_lon + 0.5
    m = Basemap(lon0, lat0, lon1, lat1, resolution=resolution, ax=ax)
    m.drawcoastlines()
    m.drawcountries(color=(1,1,0))  # country boundaries yellow
    m.drawrivers(color=(0,1,1))  # rivers in cyan
    #m.bluemarble()  # NASA bluemarble image
    #m.etopo()
    parallels = np.linspace(lat0, lat1, 3)
    meridians = np.linspace(lon0, lon1, 3)
    m.drawparallels(parallels, labels=[1,0,0,0], fmt='%.2f')
    m.drawmeridians(meridians, labels=[0,0,0,1], fmt='%.2f')
    
    line, = m.plot(xs, ys, 'o', picker=5)
    
    if evlo is not None and evla is not None:
        x_0, y_0 = m(evlo, evla)
        m.plot(x_0, y_0, 'r*', markersize=20, label = 'Event') 
    
    
    ax2 = fig.add_subplot(212)

    browser = PointBrowser()

    fig.canvas.mpl_connect('pick_event', browser.onpick)
    fig.canvas.mpl_connect('key_press_event', browser.onpress)

    plt.show()
    
    

