'''
Author: Qingkai Kong
Date: 2015-01-28
Email: qingkai.kong@gmail.com
'''

import numpy as np
import matplotlib.pyplot as plt
import datetime
import re
from obspy.sac import SacIO 
from obspy import UTCDateTime

def read_in_data(filename):
    '''
    Function to read in data from K-net or Kik-net
    Inputs: 
    filename - Path to the file
    Returns:
    data - Acceleration data in unit g
    headers_dict - dictionary of header information
    '''
    headers_dict = {}
    with open(filename, "r") as ins:
        headers = [next(ins) for x in xrange(17)]
    
    #Origin time
    orig = headers[0]
    #evla, evlo, evdp, mag
    headers_dict['evla'] = float(headers[1].split()[-1])
    headers_dict['evlo'] = float(headers[2].split()[-1])
    headers_dict['evdp'] = float(headers[3].split()[-1])
    headers_dict['mag'] = float(headers[4].split()[-1])
    #station name, stla, stlo, stel, 
    headers_dict['stnm'] = headers[5].split()[-1]
    headers_dict['stla'] = float(headers[6].split()[-1])
    headers_dict['stlo'] = float(headers[7].split()[-1])
    headers_dict['stel'] = float(headers[8].split()[-1])
    #record time, sampling rate, duration, direction
    B = headers[9]
    headers_dict['df'] = float(headers[10].split()[-1].replace('Hz', ''))
    headers_dict['duration'] = float(headers[11].split()[-1])
    comp_num = headers[12].split()[-1]
    
    #determine the component from the header, you can also easily get this from the ext.
    if comp_num == '1':
        comp = 'NS1'
    elif comp_num == '2':
        comp = 'EW1'
    elif comp_num == '3':
        comp = 'UD1'
    elif comp_num == '4':
        comp = 'NS2'
    elif comp_num == '5':
        comp = 'EW2'
    elif comp_num == '6':
        comp = 'UD2'
    elif comp_num == 'N-S':
        comp = 'NS'
    elif comp_num == 'E-W':
        comp = 'EW'
    elif comp_num == 'U-D':
        comp = 'UD'
        
    headers_dict['comp'] = comp
    
    #scale factor, max Acc, 
    scaleF = headers[13].split()[-1]
    maxAcc = float(headers[14].split()[-1])
    
    scaleF = re.split(r'[\(/]+',scaleF)
    headers_dict['factor'] = float(scaleF[0]) / float(scaleF[-1]) /100 / 9.81
    
    data = np.loadtxt(filename, skiprows=17)
    data = np.hstack(data)
    
    #convert data to unit g
    data = data * headers_dict['factor']
    
    #convert the record start time to obspy UTCDateTime
    date = map(int, B.split()[2].split('/'))
    time = map(int, B.split()[3].split(':'))
    t0 = UTCDateTime(date[0], date[1], date[2], time[0], time[1], time[2])
    headers_dict['record_time'] = t0
    
    #convert the event origin time to obspy UTCDateTime
    date = map(int, orig.split()[2].split('/'))
    time = map(int, orig.split()[3].split(':'))
    t1 = UTCDateTime(date[0], date[1], date[2], time[0], time[1], time[2])

    #event time relative to the record start time
    headers_dict['o'] = t1 - t0
    
    return data, headers_dict

def write2sac(d, header, output):
    '''
    Function to write the data and header to sac files
    Inputs:
    d - data array
    header - dictionary of the header info
    output - filename of the output sac file
    '''
    sacio = SacIO()
    sacio.fromarray(d)
    # set the date
    t = header['record_time']
    sacio.SetHvalue('nzyear',t.year)
    sacio.SetHvalue('nzjday',t.julday)
    sacio.SetHvalue('delta', 1./header['df'])
    sacio.SetHvalue('nzhour',t.hour)
    sacio.SetHvalue('nzmin',t.minute)
    sacio.SetHvalue('nzsec',t.second)
    sacio.SetHvalue('kstnm',header['stnm'])
    sacio.SetHvalue('stla',header['stla'])
    sacio.SetHvalue('stlo',header['stlo'])
    sacio.SetHvalue('stel',header['stel'])
    sacio.SetHvalue('kcmpnm',header['comp'])
    sacio.SetHvalue('evla',header['evla'])
    sacio.SetHvalue('evlo',header['evlo'])
    sacio.SetHvalue('o',header['o'])
    sacio.SetHvalue('mag',header['mag'])
    sacio.SetHvalue('o',header['o'])
    #TRUE if DIST AZ BAZ and GCARC are to be calculated from st event coordinates.
    sacio.SetHvalue('LCALDA', 1)
        
    #set the type of the dependent variable as acceleration nm/sec/sec
    #sacio.SetHvalue('idep',8)
                    
    sacio.WriteSacBinary(output)
    
#An example is here
data, headers = read_in_data('./IBRH121104111716.EW1')
write2sac(data, headers, 'test.sac')