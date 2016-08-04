#!/bin/bash

####################################### Example 1
# The -R specify xmin, xmax, ymin, ymax
# The -J specify the projection, with X4i/3i as scale
# -Ba specify the annotation and major tick spacing 
# -B+glightred+t is to fill in with color (+g), and title (+t)
# -P portrait 
gmt psbasemap -R10/70/-3/8 -JX4i/3i -Ba -B+glightred+t"My first plot" -P > GMT_tut_1.ps

