#! /bin/csh

foreach filename (`ls -d *.BHZ.sac`)
#echo $filename |cut -d'.' -f2 | read station
#echo $filename |cut -d'.' -f3 | read component
set station = `echo $filename | awk '{split($0,a,"."); print a[1]}'`

echo $station
sac << sacend
read $station.BHE.sac
rmean
transfer from polezero s ../../zp/${station}.BHE.zp
mul 100
write tmpe
read $station.BHN.sac
rmean
transfer from polezero s ../../zp/${station}.BHN.zp
mul 100
write tmpn
read $station.BHZ.sac
rmean
transfer from polezero s ../../zp/${station}.BHZ.zp
mul 100
write tmpz
read tmpe tmpn
rot to gcp
read more tmpz
int
bp co 0.02 0.05 p 2
interpolate delta 1.0
write tmp2 tmp1 tmp3
quit
sacend

sac2helm out={$station}.data


end


