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


#ifndef INCLUDED_CLASSIFY_CPFSK_BC_H
#define INCLUDED_CLASSIFY_CPFSK_BC_H

#include <classify/api.h>
#include <gnuradio/sync_interpolator.h>

namespace gr {
  namespace classify {

    /*!
     * \brief <+description of block+>
     * \ingroup classify
     *
     */
    class CLASSIFY_API cpfsk_bc : virtual public gr::sync_interpolator
    {
     public:
      typedef boost::shared_ptr<cpfsk_bc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of classify::cpfsk_bc.
       *
       * To avoid accidental use of raw pointers, classify::cpfsk_bc's
       * constructor is in a private implementation
       * class. classify::cpfsk_bc::make is the public interface for
       * creating new instances.
       */
      static sptr make(float k, float ampl, int samples_per_sym, int bits_per_symbol);
      virtual void set_amplitude(float amplitude) = 0;
      virtual float freq() = 0;
      virtual float amplitude() = 0;
      virtual float phase() = 0;
    };

  } // namespace classify
} // namespace gr

#endif /* INCLUDED_CLASSIFY_CPFSK_BC_H */

