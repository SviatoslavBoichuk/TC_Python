%module c_module
%{
#define SWIG_FILE_WITH_INIT
#include "c_module.h“
%}

const char * ReadDataFromFile(const char * fileName);
