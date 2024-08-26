from setuptools import setup

setup(name='wrf_tools',
      version='0.8.1',
      description='The WRF tools are used to be a unified tool for running the \
                   simulations with handy utils. The namelist can be created by \
                   a single script with unified information to WPS and WRF instead \
                   or changing namelist here and there. Testing for BB',
      url='https://github.com/hydrogencl/WRF_TOOLS',
      author='Yen-Sen Lu',
      author_email='hydrogencl@gmail.com',
      license='MIT',
      packages=['wrf_tools'],
      zip_safe=False)


