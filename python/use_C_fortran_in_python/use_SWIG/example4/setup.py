import commands, os
from distutils.core import setup, Extension

name = 'example'    #name of the module
version = '1.0'

swig_cmd = 'swig -python -I./lib %s.i' %name
print 'running SWIG:', swig_cmd

failure, output = commands.getstatusoutput(swig_cmd)

sources = ['./lib/example.c', 'example_wrap.c']

setup(name = name, version = version, ext_modules = [Extension('_' + name, sources,
    include_dirs=[os.pardir])])