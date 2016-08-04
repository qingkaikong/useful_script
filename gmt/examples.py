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

####################################### Example 3
# Mercator projection, this will distort the high latitude 
# -JMwidth
# -G	Set color of dry areas (default does not paint)
# -S	Set color for wet areas (default does not paint)
# -D	Select data resolution (bull, high, intermediate, low, or crude)
# -N	Draw political borders (including US state borders)
# if add -W0.25p instead of -G, -S, then it will draw the coastal line with 0.25 linewidth
gmt pscoast -R-90/-70/0/20 -JM6i -P -Ba -Gchocolate -Slightblue -Dh -N > GMT_tut_3.ps

####################################### Example 4
# Albers projection, is an equal-area conical projection
# -JBlon_0/lat_0/lat_1/lat_2/width
# where (lon_0, lat_0) is the map (projection) center and lat_1, lat_2 are the two standard parallels where the cone intersects the Earth’s surface.
# -Amin_area[/min_level/max_level][+ag|i|s|S][+r|l][+ppercent], Features with an area smaller than min_area in km^2 or of hierarchical level that is lower than min_level or higher than max_level will not be plotted
gmt pscoast -R-130/-70/24/52 -JB-100/35/33/45/6i -Ba -B+t"Conic Projection" -N1/thickest -N2/thinnest -A500 -Ggray -Wthinnest -P > GMT_tut_4.ps

####################################### Example 5
# Orthographic projection
# -JGlon_0/lat_0/width, where (lon_0, lat_0) is the center of the map (projection)
gmt pscoast -Rg -JG280/30/6i -Bag -Dc -A5000 -Gwhite -SDarkTurquoise -P > GMT_tut_5.ps

####################################### Example 7
# psxy
# -W specify the outline on the symbol 
# -G fill in color
# -S specify the shape of the symbol 
gmt psxy data -R0/6/0/6 -Jx1i -P -Baf -W1.5p -Sa0.5 -Gred> GMT_tut_7.ps

####################################### Example 8
# add lines between the symbols 
# -K Do not finalize the PostScript plot.
# -O Append to existing PostScript plot.
gmt psxy data -R0/6/0/6 -Jx1i -Baf -P -K -Wthinner > GMT_tut_8.ps
gmt psxy data -R -J -O -W -Si0.2i >> GMT_tut_8.ps

####################################### Example 9
# where the c appended to the -Sc option ensures that symbols sizes are interpreted to be in cm
# 
gmt pscoast -R130/150/35/50 -JM6i -B5 -P -Ggray -K > GMT_tut_9.ps
gmt psxy -R -J -O quakes.ngdc -Wfaint -i4,3,5,6s0.1 -h3 -Scc -Cquakes.cpt >> GMT_tut_9.ps

####################################### Example 10
# write text strings
gmt pstext -R0/7/0/5 -Jx1i -P -Ba -F+f30p,Times-Roman,DarkOrange+jBL << EOF > GMT_tut_10.ps
1  1  It's P@al, not Pal!
1  2  Try @%33%ZapfChancery@%% today
1  3  @~D@~g@-b@- = 2@~pr@~G@~D@~h.
1  4  University of Hawaii at M@!a\225noa
EOF

####################################### Example 11
# contour
# -A1000 using 1 km as annotation interval
# -C250 250 m as contour interval
gmt grdcontour bermuda.nc -JM7i -C250 -A1000 -P -Ba > GMT_tut_11.ps


