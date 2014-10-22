import matplotlib.pyplot as plt
import numpy as np

def plot_stations_fromFile(station_loc, evla = None, evlo = None, llat = 37, ulat = 39, 
    llon = -123.5, ulon = -121.5, figsize = (8, 8), resolution = 'l', 
    mer = (-123.5, -121, 1), par = (37, 39.5, 1), **kwargs):
    
    lats, lons = [], []
    
    dt = dict(names = ('filename', 'stnm', 'stla', 'stlo', 'dist'), formats = ((str,20), (str,8), np.float32, np.float32, np.float32))

    station_loc = np.loadtxt('./station_loc.txt', dtype = dt)
    
    for i, station in enumerate(station_loc):
        lats.append(station_loc['stla'][i])
        lons.append(station_loc['stlo'][i])   
     
    # --- Build Map ---
    from mpl_toolkits.basemap import Basemap
    
    
    fig = plt.figure(figsize=figsize)
    
    #map = Basemap(projection='cyl', resolution = 'l', area_thresh = 1000.0,lat_0=0, lon_0=-130)
    
    #plot only US on the map
        
    map = Basemap(projection='cyl', resolution = resolution, area_thresh = 1000.0,
        llcrnrlon=llon, llcrnrlat=llat,urcrnrlon=ulon,urcrnrlat=ulat)
    
    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color = 'gray')
    map.drawmapboundary()
    #map.drawmeridians(np.arange(-123.5, -121, 1), labels=[0,0,0,1])
    #map.drawparallels(np.arange(37, 39.5, 1), labels=[1,0,0,0])
    map.drawmeridians(np.arange(mer[0], mer[1], mer[2]), labels=[0,0,0,1])
    map.drawparallels(np.arange(par[0], par[1], par[2]), labels=[1,0,0,0])
     
    #plot stations as triangles on the map
    
            
    color = 'b'
    x,y = map(lons, lats)
    map.plot(x, y, '^', c = color,  markersize=9, label = 'stations')
            
    if evla is not None and evlo is not None:
        map.plot(evlo, evla, '*', c = 'r',  markersize=14, label = 'Earthquake')
    
    plt.legend(numpoints=1)
    plt.show()
    
