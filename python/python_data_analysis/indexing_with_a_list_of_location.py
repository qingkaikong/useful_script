'''
this is an example to index from a list of locations, we will shuffle the x and y index
of lena, and then using the ix_ to construct an open mesh from multiple sequences.
'''
import scipy.misc
import matplotlib.pyplot as plt
import numpy as np
lena = scipy.misc.lena()
xmax = lena.shape[0]
ymax = lena.shape[1]

def shuffle_indices(size):
    arr = np.arange(size)
    np.random.shuffle(arr)
    return arr
    
xindices = shuffle_indices(xmax)
np.testing.assert_equal(len(xindices), xmax)
yindices = shuffle_indices(ymax)
np.testing.assert_equal(len(yindices), ymax)
plt.imshow(lena[np.ix_(xindices, yindices)])
plt.show()