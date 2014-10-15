from numpy.distutils.core import Extension, setup

setup(name='hw',
            ext_modules=[Extension(name='hw', sources=['../useFortran77.f'])],) 