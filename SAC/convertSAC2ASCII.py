from obspy.core import read
import numpy as np
import glob

for item in glob.glob('./*BNZ*'):
    trX = read(item.replace('BNZ', 'BN1'))[0]
    trY = read(item.replace('BNZ', 'BN2'))[0]
    trZ = read(item)[0]
    
    t = trX.times()
    
    accX = trX.data
    accY = trY.data
    accZ = trZ.data
    print t.shape, accX.shape, accY.shape, accZ.shape
    
    a = np.c_[t, accX, accY, accZ]
    
    output = trX.stats.station + '.txt'
    np.savetxt(output, a)