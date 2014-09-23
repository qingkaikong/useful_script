import numpy as np
import matplotlib.pyplot as plt
import glob
import math
import shutil
from matplotlib.widgets import Button
import os
from obspy.sac import SacIO 
from obspy import UTCDateTime
from obspy.core.util.geodetics import gps2DistAzimuth

'''
This script is to read in the V1 files from the strong motion center, and then 
convert it into sac files. Note that: right now I converted the data into unit
m/s/s, and also resample the data to 50 Hz. 

Author: Qingkai Kong, kongqk@berkeley.edu
'''


class Index:
    def Next(self, event):       
        pass          
        plt.close()

    def Ok(self, event):    
        #shutil.move(filename, move_path)
        save2peerFormat(acc_new_data, header1, header2, header3, move_path)
        #save_data(acc_new_data, header1, header2, header3, dist, move_path)
        #fig.savefig(move_path + str(stnm) +'.png')
        plt.close()
        
def save_data(acc_new_data, header1, header2, header3, dist, move_path):
    file_loc1 = move_path + str(stnm) + '_' + 'chan1.txt'
    f=open(file_loc1,'w')
    for i,j in zip(acc_new_data['CHANNEL1'][0],acc_new_data['CHANNEL1'][1]):
        format_data = '%0.3f , %0.5f \n' %(i, j/10.0)
        f.write(format_data)
    f.close()
    log1 = file_loc1 + ', ' + header1['comp'] + ', %0.2f km, ' % dist + \
    str(header1['stla']) + ', ' + str(header1['stlo']) + '\n' 
    print log1
        
    file_loc2 = move_path + str(stnm) + '_' + 'chan2.txt'
    f=open(file_loc2,'w')
    for i,j in zip(acc_new_data['CHANNEL2'][0],acc_new_data['CHANNEL2'][1]):
        format_data = '%0.3f , %0.5f \n' %(i, j/10.0)
        f.write(format_data)
    f.close()
    
    log2 = file_loc2 + ', ' + header2['comp'] + ', %0.2f km, ' % dist + \
    str(header2['stla']) + ', ' + str(header2['stlo']) + '\n' 
    
    file_loc3 = move_path + str(stnm) + '_' + 'chan3.txt'
    f=open(file_loc3,'w')
    for i,j in zip(acc_new_data['CHANNEL3'][0],acc_new_data['CHANNEL3'][1]):
        format_data = '%0.3f , %0.5f \n' %(i, j/10.0)
        f.write(format_data)
    f.close()
    
    log3 = file_loc3 + ', ' + header3['comp'] + ', %0.2f km, ' % dist + \
    str(header3['stla']) + ', ' + str(header3['stlo']) + '\n'
    
    f = open(move_path + 'log.txt', "a")
    f.write(log1)
    f.write(log2)
    f.write(log3)
    f.close()
    
        
def get_data_from_file(lookup, filename):
    data = {}
    start = 0
    f=open(filename)
    myFile=f.readlines()
    f.close()
    
    for num, line in enumerate(myFile, 1):
        if lookup in line:
            #print 'found at line:', num
            split = line.split()
            channel = split[-3].lower() + split[-2]
            ix =  slice(start, num-1)
            data[channel] = myFile[ix]
            start = num
    return data

def resample(t,old_data, new_delta):
    
    t_new = np.arange(0, t[-1], new_delta)
    
    #interpolate the data using the new sampling frequency

    new_data = np.interp(t_new, t, old_data)
    return t_new, new_data

def get_resampled_data(delat_new, data):
    acc_data = {}
    acc_new_data = {}
    
    for i, key in enumerate(data):
        temp = np.array(data[key][28:])
        h = data[key][0:28]
        
        arrays = [map(float, line.split()) for line in temp]
        
        array_data = sum(arrays, [])
        
        header = get_header(h)
        df = header['sampling_rate']
        npts = header['npts']
        
        t = np.linspace(0, npts/df, npts)
        d = array_data 
        acc_data[key] = [t, d, h]
        t_new,d_new = resample(t,d,delta_new)
        acc_new_data[key] = [t_new, d_new * 9.81]
    return acc_data, acc_new_data

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

def get_header(h):
    '''
    Input:
    h is the list which stores header information
    '''
    header = {}
    '''
    #the following method has problem, because some of the records contains
    #50010001 data
    
    #get the orientation of the channel (azimuth clockwise from North,
    #0-360 for horizontal sensor, for vertical sensor, 500=up, 600=down
    header['orientation'] = h[14].split()[10]
    
    if header['orientation'] == '500':
        header['comp'] = 'vertical up'
    elif header['orientation'] == '600':
        header['comp'] = 'vertical down'
    else:
        header['comp'] = header['orientation'] + '$^\circ$ from north'
    
    inst = h[20].split()
    #get natural period of transducer (seconds)
    header['wn'] = inst[0]
    #Damping of transducer (fraction of oritical)
    header['damping'] = inst[1]
    #Length of digitized record (in seconds)
    header['t_len'] = inst[2]
    #RMS value of digitized record (in g)
    header['rms'] = inst[3]
    #Unitis of digitized acceleration in file (fractions of g), typically 0.10
    header['unit'] = inst[4]
    #Sensitivity of transducer (cm/g)
    header['sensitivity'] = inst[5]
    #Peak acceleration for this component (in g)
    header['pga'] = inst[6]
    #Time of peak acceration value 
    header['t_pga'] = inst[7]
    '''
    
    header['comp'] = h[6].split(':')[1].strip()
    
    #get latitude and longitude
    station_info = h[4]

    lat = station_info[20:27]
    lon = station_info[29:37]
    
    header['stnm'] = station_info[12:17].strip()

    if lat[-2] == 'S':
        header['stla'] = -1 * float(lat[:-2])
    else:
        header['stla'] = float(lat[:-2])
    
    if lon[-1] == 'W':
        header['stlo'] = -1 * float(lon[:-2])
    else:
        header['stlo'] = float(lon[:-2])
        
    integer1 = h[13].split()
    header['sampling_rate'] = float(integer1[5])
    
    integer3 = h[15].split()
    header['npts'] = float(integer3[0])
    
    date_time = h[14].split()
    header['nzhour'] = date_time[0]
    header['nzmin'] = date_time[1]
    header['nzsec'] = date_time[2]
    header['nzmsec'] = date_time[3]
    header['nzjday'] = date_time[4]
    header['nzmm'] = date_time[5]
    header['nzdd'] = date_time[6]
    header['nzyear'] = date_time[7]
    
    return header

def save2peer(a, stnm, comp, filename):
    n = len(a)/5
    initial=np.zeros([n,5], dtype=np.float64)
    
    count = 0
    for i in range(n):
          for j in range(0,5):
             initial[i,j]=a[count] / 10.
             count += 1
    with open(filename, 'wb') as f:
        f.write(b'USGS STRONG MOTION DATABASE RECORD\n')  
        f.write(b'LOMA PRIETA 10/18/89 00:05, Station %s,   %s\n' %(stnm, comp))  
        f.write(b'ACCELERATION TIME HISTORY IN UNITS OF G\n')  
        f.write(b'NPTS= %d DT= 0.0050000\n' % len(a)) 
        np.savetxt(f, initial, fmt='%15.6e',delimiter='')
        
def save2peerFormat(acc_new_data, header1, header2, header3, move_path):
    stnm = header1['stnm']
    #save Channel 1
    file_loc1 = move_path + str(stnm) + '_' + 'chan1_peer_format.txt'
    a = acc_new_data['CHANNEL1'][1]
    save2peer(a, stnm, header1['comp'], file_loc1)
    
    #save Channel 2
    file_loc2 = move_path + str(stnm) + '_' + 'chan2_peer_format.txt'
    a = acc_new_data['CHANNEL2'][1]
    save2peer(a, stnm, header2['comp'], file_loc2)
    
    #save Channel 3
    file_loc3 = move_path + str(stnm) + '_' + 'chan3_peer_format.txt'
    a = acc_new_data['CHANNEL3'][1]
    save2peer(a, stnm, header3['comp'], file_loc3)
    
def write2sac(d, header, evla, evlo, evdp, mag, output):
    sacio = SacIO()
    sacio.fromarray(d)
    # set the date to today
    sacio.SetHvalue('nzyear',header['nzyear'])
    sacio.SetHvalue('nzjday',header['nzjday'])
    sacio.SetHvalue('delta',0.02)
    sacio.SetHvalue('nzhour',header['nzhour'])
    sacio.SetHvalue('nzmin',header['nzmin'])
    sacio.SetHvalue('nzsec',header['nzsec'])
    sacio.SetHvalue('nzmsec',header['nzmsec'])
    sacio.SetHvalue('kstnm',header['stnm'])
    sacio.SetHvalue('stla',header['stla'])
    sacio.SetHvalue('stlo',header['stlo'])
    sacio.SetHvalue('kcmpnm',header['comp'])
    sacio.SetHvalue('evla',evla)
    sacio.SetHvalue('evlo',evlo)
    sacio.SetHvalue('evdp',evdp)
    sacio.SetHvalue('mag',mag)
    
    #dist = sacio.GetHvalue('dist')
    #print dist
    dist = gps2DistAzimuth(stla, stlo, evla, evlo)[0] /1000.
    sacio.SetHvalue('dist',dist)
    
    #sacio.SetHvalue('knetwk','phones')
    #sacio.SetHvalue('kstnm',phone)
    #sacio.SetHvalue('kcmpnm',comp)
    #sacio.SetHvalue('kevnm',loc)
    #sacio.SetHvalue('kuser0',test + ' test')
    #sacio.SetHvalue('kuser0',version)
    #sacio.SetHvalue('kuser1',brand)
    #set the type of the dependent variable as acceleration nm/sec/sec
    #sacio.SetHvalue('idep',8)
                    
    sacio.WriteSacBinary(output)
    
lookup = '/&  ----------  End of Data for'

path = './'
move_path = path + 'done/'

if not os.path.exists(move_path):
    os.makedirs(move_path)

for filename in glob.glob(path + '*.v1'):
    network = filename.split("/")[-1][0:2]
    data = get_data_from_file(lookup, filename)
    delta_new = 0.02
    acc_data, acc_new_data = get_resampled_data(delta_new, data)
    
    h1 = acc_data['channel1'][2]
    h2 = acc_data['channel2'][2]
    h3 = acc_data['channel3'][2]
    
    header1 = get_header(h1)
    header2 = get_header(h2)
    header3 = get_header(h3)
    
    stnm = header1['stnm']
    stla = header1['stla']
    stlo = header1['stlo']
    
    comp1 = header1['comp'].split()[0]
    comp2 = header2['comp'].split()[0]
    comp3 = header3['comp'].split()[0]
    
    comp_poz = []
    count = 1
    for comp in [comp1, comp2, comp3]:
        if comp != 'Up':
            comp_poz.append('BN' + str(count))
            count += 1
        else:
            comp_poz.append('BNZ')
            
    
    output1 = path + stnm + '_' + network + '_' + comp_poz[0] + '.sac'
    output2 = path + stnm + '_' + network + '_' + comp_poz[1] + '.sac'
    output3 = path + stnm + '_' + network + '_' + comp_poz[2] + '.sac'
    
    evla = 38.220
    evlo = -122.313
    evdp = 11.3 # in km
    mag = 6.0
    dist = float(6371. * distance_on_unit_sphere(stla, stlo, evla, evlo))
    
    #title = 'Station ' + stnm + ', distance: %0.2f km' % dist
    '''
    fig = plt.figure(figsize = (14,8))
    
    ax1 = fig.add_subplot(311)
    ax1.plot(acc_new_data['channel1'][0],acc_new_data['channel1'][1], label = header1['comp'])
    plt.ylabel('Acceleration ($m/{s}^2$)')
    plt.title(title)
    plt.legend()
    
    ax2 = fig.add_subplot(312, sharex = ax1)
    ax2.plot(acc_new_data['channel2'][0],acc_new_data['channel2'][1], label = header2['comp'])
    plt.ylabel('Acceleration ($m/{s}^2$)')
    plt.legend()
    
    ax3 = fig.add_subplot(313, sharex = ax1)
    ax3.plot(acc_new_data['channel3'][0],acc_new_data['channel3'][1], label = header3['comp'])
    plt.ylabel('Acceleration ($m/{s}^2$)')
    plt.xlabel('Time (sec)')
    plt.legend()
    
    
    
    callback = Index()
    
    axprev = plt.axes([0.7, 0.02, 0.1, 0.04])
    axnext = plt.axes([0.81, 0.02, 0.1, 0.04])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.Next)
    bprev = Button(axprev, 'Ok')
    bprev.on_clicked(callback.Ok)
    
    plt.show()
    '''
    
    write2sac(acc_new_data['channel1'][1], header1, evla, evlo, evdp, mag, output1)
    write2sac(acc_new_data['channel2'][1], header2, evla, evlo, evdp, mag, output2)
    write2sac(acc_new_data['channel3'][1], header3, evla, evlo, evdp, mag, output3)
    shutil.move(filename, move_path)
    
    
