#!/user/bin/env python

"""Pure python version of the module"""

import math, sys

def hw1(r1, r2):
    """
    Return the sine of two numbers
    """
    s = math.sin(r1+r2)
    return s
    
def hw2(r1, r2):
    """
    Same as above, but write the result together with Hello world
    """
    s = math.sin(r1+r2)
    print "Hello, world! sine(%g+%g)=%g" % (r1, r2, s)