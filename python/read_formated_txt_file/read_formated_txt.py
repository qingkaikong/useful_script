#Read in formated data from numpy

import numpy as np

convertfunc = lambda x: float(x.strip("%"))/100

dt = dict(names = ('Week', 'ice_cream', 'ice_cream_std', 'full_moon', 'full_moon_std'), formats = (np.float64, np.float64, np.float32, np.float64, np.float32))

data = np.loadtxt('astro.csv', delimiter=',', dtype=dt, converters={0: md.datestr2num, 2: convertfunc, 4: convertfunc}, skiprows=1)

date = data['Week']
full_moon = data['full_moon']


