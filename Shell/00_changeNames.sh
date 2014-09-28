#! /bin/csh
###############################Change the data name###########################################
ls *BN?.sac | awk -F '[_]' '{printf "mv %s %s.%s.%s\n",$0,$2,$1,$3}' >! rename.temp

cat ./rename.temp
chmod 777 ./rename.temp
./rename.temp

rm ./rename.temp


