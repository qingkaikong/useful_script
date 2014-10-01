'''
This script showing you how to use a sliding window
'''

from itertools import islice
def sliding_window(a, n, step):
    '''
    a - sequence
    n - width of the window
    step - window step
    '''
    z = (islice(a, i, None, step) for i in range(n))
    return zip(*z)
    
##Example
sliding_window(range(10), 2, 1)
    
