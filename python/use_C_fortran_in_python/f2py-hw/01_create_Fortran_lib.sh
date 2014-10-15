#! /bin/sh

#create a lib from fortran
#-m specifies the name of the extension module
#-c indicates that F2PY should compile and link the module
f2py -m hw -c ../useFortran77.f
#or we can specify a suitable Fortran compiler
#f2py -m hw -c --fcompiler=Gnu ../useFortran77.f

#Sometimes when you have complicated fortran code, you can only 
#use two functions from it. 
#f2py -m hw -c ../useFortran77.f only: hw1 hw2

#f2py -c --help-fcompiler
#the above showing you all the compilers on your system

#test if it is working
#-c allows us to write a short script as a text argument
python -c 'import hw'



###############################################################################
#after you create the setup.py script, (this is the way you need to create the lib)
#then you can use 'python setup.py build' or 'python setup.py install' to create 
#a build folder with the lib, but for testing, you can use the following line
#to create a lib in the current folder
python setup.py build build_ext --inplace
