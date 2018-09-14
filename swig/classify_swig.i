/* -*- c++ -*- */

#define CLASSIFY_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "classify_swig_doc.i"

%{
#include "classify/cpfsk_bc.h"
%}


%include "classify/cpfsk_bc.h"
GR_SWIG_BLOCK_MAGIC2(classify, cpfsk_bc);
