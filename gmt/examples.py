#!/bin/bash

####################################### Example 1
# The -R specify xmin, xmax, ymin, ymax
# The -J specify the projection, with X4i/3i as scale
# -Ba specify the annotation and major tick spacing 
# -B+glightred+t is to fill in with color (+g), and title (+t)
# -P portrait 
gmt psbasemap -R10/70/-3/8 -JX4i/3i -Ba -B+glightred+t"My first plot" -P > GMT_tut_1.ps

####################################### Example 2
# Logarithmic projection
# Note the l added to the options
# the little p in the -Bya1p is not showing the plus sign on the power, i.e. 1e25 instead of 1e+25
# if we add -Bxg3a2+l -Byg3a1f3+l, it will add the grid line
gmt psbasemap -R1/10000/1e20/1e25 -JX9il/6il -Bxa2+l"Wavelength (m)" -Bya1pf3+l"Power (W)" -BWS > GMT_tut_2.ps
