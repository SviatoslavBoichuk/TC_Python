from distutils.core import setup, Extension
c_module = Extension('_c_module', sources=['c_module_wrap.c', 'c_module.c'])
setup(name='c_module', ext_modules=[c_module], py_modules=['c_module'])
