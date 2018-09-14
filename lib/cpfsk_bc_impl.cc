/* -*- c++ -*- */
/* 
 * Copyright 2018 University of Arizona.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <gnuradio/expj.h>
#include <math.h>
#include "cpfsk_bc_impl.h"
#include <iostream>

namespace gr {
  namespace classify {

    #define M_TWOPI (2*M_PI)

    cpfsk_bc::sptr
    cpfsk_bc::make(float k, float ampl, int samples_per_sym, int bits_per_symbol)
    {
      return gnuradio::get_initial_sptr
        (new cpfsk_bc_impl(k, ampl, samples_per_sym, bits_per_symbol));
    }

    /*
     * The private constructor
     */
    cpfsk_bc_impl::cpfsk_bc_impl(float k, float ampl, int samples_per_sym, int bits_per_symbol)
      : gr::sync_interpolator("cpfsk_bc",
              gr::io_signature::make(1, 1, sizeof(char)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)), samples_per_sym),
      d_samples_per_sym(samples_per_sym),
      d_freq(k*M_PI/(samples_per_sym*bits_per_symbol)),
      d_ampl(ampl),
      d_phase(0.0),
      d_mid(pow(2, (bits_per_symbol - 1)))
    {

    }

    /*
     * Our virtual destructor.
     */
    cpfsk_bc_impl::~cpfsk_bc_impl()
    {
    }

    int
    cpfsk_bc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const char *in = (const char *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];

      // Do <+signal processing+>
      
      for(int i = 0; i < noutput_items/d_samples_per_sym; i++){
        for(int j = 0; j < d_samples_per_sym; j++){
          if(in[i] >= d_mid){
            d_phase += (in[i] - d_mid + 1)*d_freq;
          }
          else{
            d_phase -= (d_mid - in[i])*d_freq;
          }

          while(d_phase > M_TWOPI) d_phase -= M_TWOPI;
          while(d_phase < M_TWOPI) d_phase += M_TWOPI;

          *out++ = gr_expj(d_phase)*d_ampl;
        }
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace classify */
} /* namespace gr */

