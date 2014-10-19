import numpy as np
import matplotlib.pyplot as plt
from obspy import UTCDateTime
import re
import urllib
import urllib2
from mpl_toolkits.basemap import Basemap
from obspy.imaging.beachball import Beach
from collections import OrderedDict
from matplotlib.lines import Line2D


def get_hist_mt(t1, t2, llat = '-90', ulat = '90', llon = '-180', ulon = '180', 
    lmw = 0, umw = 10,
    evla = None, evlo = None, step = 2.0, list = '6'):
    yr = t1.year
    mo = t1.month
    day = t1.day
    oyr = t2.year
    omo = t2.month
    oday = t2.day
    mat = {}
    locs = locals()  
    
    base_url = 'http://www.globalcmt.org/cgi-bin/globalcmt-cgi-bin/CMT4/form'
    
    #note here, we must use the ordered Dictionary, so that the order in the 
    #url is exactly the same order
    param = OrderedDict()
    param['itype'] = 'ymd'
    param['yr'] = yr
    param['mo'] = mo
    param['day'] = day
    param['otype'] = 'ymd'
    param['oyr'] = oyr
    param['omo'] = omo
    param['oday'] = oday
    param['jyr'] = '1976'
    param['jday'] = '1'
    param['ojyr'] = '1976'
    param['ojday'] = '1'
    
    param['nday'] = '1'
    param['lmw'] = str(lmw)
    param['umw'] = str(umw)
    param['lms'] = '0'
    param['ums'] = '10'
    param['lmb'] = '0'
    param['umb'] = '10'
    
    ind = 1
    if evla and evlo is not None:
        llat = evla - step
        ulat = evla + step
        llon = evlo - step
        ulon = evlo + step
        ind = 0

    
    param['llat'] = llat
    param['ulat'] = ulat
    param['llon'] = llon
    param['ulon'] = ulon
    
    param['lhd'] = '0'
    param['uhd'] = '1000'
    param['lts'] = '-9999'
    param['uts'] = '9999'
    param['lpe1'] = '0'
    param['upe1'] = '90'
    param['lpe2'] = '0'
    param['upe2'] = '90'
    param['list'] = list
    
    url = "?".join((base_url, urllib.urlencode(param)))
    print url
    
    page = urllib2.urlopen(url)
    from BeautifulSoup import BeautifulSoup

#
    parsed_html = BeautifulSoup(page)

    mecs_str = parsed_html.findAll('pre')[1].text.split('\n')

    def convertString(mecs_str):
        return map(float, mecs_str.split()[:9])
        
    psmeca = np.array(map(convertString, mecs_str))
    
    mat['psmeca'] = psmeca
    mat['ind'] = ind
    mat['url'] = url
    mat['range'] = (llat, ulat, llon, ulon)
    mat['evloc'] = (evla, evlo)
    return mat
    
def plot_hist_mt(psmeca_dict, figsize = (16,24), mt_size = 10, pretty = False, resolution='l'):
    if len(psmeca_dict['psmeca']) < 1:
        print 'No historical MT found!'
    else:
        
        psmeca = psmeca_dict['psmeca']
        #get the latitudes, longitudes, and the 6 independent component
        lats = psmeca[:,1]
        lons = psmeca[:,0]
        focmecs = psmeca[:,3:9]
        depths =  psmeca[:,2]    
        (llat, ulat, llon, ulon) = psmeca_dict['range'] 
        evla = psmeca_dict['evloc'][0]
        evlo = psmeca_dict['evloc'][1]

        plt.figure(figsize=figsize)
        m = Basemap(projection='cyl', lon_0=142.36929, lat_0=38.3215, 
                    llcrnrlon=llon,llcrnrlat=llat,urcrnrlon=ulon,urcrnrlat=ulat,resolution=resolution)
    
        m.drawcoastlines()
        m.drawmapboundary()
    
        if pretty:    
            m.etopo()
        else:
            m.fillcontinents()
    
        llat = float(llat)
        ulat = float(ulat)
        llon = float(llon)
        ulon = float(ulon)
    
        m.drawparallels(np.arange(llat, ulat, (ulat - llat) / 4.0), labels=[1,0,0,0])
        m.drawmeridians(np.arange(llon, ulon, (ulon - llon) / 4.0), labels=[0,0,0,1])   
    
        ax = plt.gca()
    
        x, y = m(lons, lats)
    
        for i in range(len(focmecs)):
            '''
            if x[i] < 0:
                x[i] = 360 + x[i]
            '''
        
            if depths[i] <= 50:
                color = '#FFA500'
                #label_
            elif depths[i] > 50 and depths [i] <= 100:
                color = 'g'
            elif depths[i] > 100 and depths [i] <= 200:
                color = 'b'
            else:
                color = 'r'
        
            index = np.where(focmecs[i] == 0)[0]
        
            #note here, if the mrr is zero, then you will have an error
            #so, change this to a very small number 
            if focmecs[i][0] == 0:
                focmecs[i][0] = 0.001
        
            try:
                b = Beach(focmecs[i], xy=(x[i], y[i]),width=mt_size, linewidth=1, facecolor=color)
            except:
                pass
            
            b.set_zorder(10)
            ax.add_collection(b)
        
        x_0, y_0 = m(evlo, evla)
        m.plot(x_0, y_0, 'r*', markersize=25) 
    
        circ1 = Line2D([0], [0], linestyle="none", marker="o", alpha=0.6, markersize=10, markerfacecolor="#FFA500")
        circ2 = Line2D([0], [0], linestyle="none", marker="o", alpha=0.6, markersize=10, markerfacecolor="g")
        circ3 = Line2D([0], [0], linestyle="none", marker="o", alpha=0.6, markersize=10, markerfacecolor="b")
        circ4 = Line2D([0], [0], linestyle="none", marker="o", alpha=0.6, markersize=10, markerfacecolor="r")
        plt.legend((circ1, circ2, circ3, circ4), ("depth $\leq$ 50 km", "50 km $<$ depth $\leq$ 100 km", 
                        "100 km $<$ depth $\leq$ 200 km", "200 km $<$ depth"), numpoints=1, loc=3)
        plt.show()
    
        
if __name__ == "__main__":
          
    t1 = UTCDateTime("1979-01-01T00:00:00.000")
    t2 = UTCDateTime("2013-01-01T00:00:00.000")

    psmeca = get_hist_mt(t1, t2, llat = '-90', ulat = '90', llon = '-180', ulon = '180',\
     lmw = 7, umw = 10,evla = 12.576 , evlo = -88.046, step = 5.0, list = '6')

    plot_hist_mt(psmeca, figsize = (16,24), mt_size = 0.4, pretty = False, resolution='l')
