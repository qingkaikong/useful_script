'''
This is an example to do the fancy indexing to get the diagonal and set to 0
'''

import scipy.misc
import matplotlib.pyplot as plt
lena = scipy.misc.lena()
xmax = lena.shape[0]
ymax = lena.shape[1]

#here, fancy indexing is done based on an internal numpy iterator object. 
lena[range(xmax), range(ymax)] = 0
lena[range(xmax-1,-1,-1), range(ymax)] = 0
plt.imshow(lena)
plt.show()