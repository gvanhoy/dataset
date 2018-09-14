#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 University of Arizona.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from gnuradio import gr, blocks, channels, analog
import numpy as np


class channel(gr.hier_block2):
    def __init__(self, snr_db=0):
        gr.hier_block2.__init__(
            self, "channel",
            gr.io_signature(1, 1, gr.sizeof_gr_complex),
            gr.io_signature(1, 1, gr.sizeof_gr_complex)
        )
        self.add = blocks.add_vcc(1)
        self.snr_db = snr_db
        # Need /sqrt(2.0) when doing complex noise. GNU Radio does this internally
        self.noise = \
            analog.noise_source_c(
                analog.GR_GAUSSIAN,
                np.sqrt(10.0 ** (-self.snr_db / 10.0)),  # Noise amp
                0
            )
        self.connect(self.add, self)
        self.connect(self.noise, (self.add, 1))


class chan_none(channel):
    def __init__(self):
        channel.__init__(self, snr_db=0)
        self.disconnect(self.add, self)
        self.disconnect(self.noise, (self.add, 1))
        self.add = blocks.add_const_cc(0.0)  # pass through
        self.connect(self, self.add, self)


class chan_awgn(channel):
    def __init__(self, snr_db=0):
        channel.__init__(self, snr_db=snr_db)
        self.connect(self, self.add)


class chan_flat_fading(channel):
    def __init__(self, snr_db=0):
        channel.__init__(self, snr_db=snr_db)
        self.chan = \
            channels.fading_model(
                8,                          # n_max_sinusoids
                1.0/200e3,                  # max Doppler
                False,                      # LOS(True)/NLOS(False)
                4.0,                        # K-value in Rician
                0                           # seed
            )
        self.connect(self, self.chan, self.add)


class chan_selective_fading(channel):
    def __init__(self, snr_db=0):
        channel.__init__(self, snr_db=snr_db)
        self.chan = \
            channels.selective_fading_model(
                8,                          # n sinusoids
                1.0/200e3,                  # max Doppler
                False,                      # LOS(True)/NLOS(False)
                4.0,                        # K-value in Rician fading
                0,                          # seed
                (0.0, 0.9, 1.7),            # PDP delays
                (1, 0.8, 0.3),              # PDP Magnitudes
                8                           # ntaps in channel impulse response
            )
        self.connect(self, self.chan, (self.add, 0))


class chan_radio_awgn(channel):
    '''
    Haven't tested
    '''
    def __init__(self, snr_db=0):
        channel.__init__(self, snr_db=snr_db)
        self.chan = \
            channels.dynamic_channel_model(
                200e3,      # sample_rate
                0.01,       # sro_stdev
                50,         # sro_maxdev
                0.01,       # cfo_stdev
                .5e3,       # cfo_maxdev
                8,          # n sinusoids in jakes model
                0.0,        # max fDoppler
                False,      # LOS(True)/NLOS(False)
                4.0,        # K-value in Rician fading
                (1,),       # PDP delays
                (1,),       # PDP Magnitudes
                1,                  # ntaps in channel impulse response
                0,                  # Noise amp (is added later)
                0                   # seed
            )
        self.connect(self, self.chan, self.add)


class chan_radio_flat_fading(channel):
    def __init__(self, snr_db=0):
        channel.__init__(self, snr_db=snr_db)
        self.chan = \
            channels.dynamic_channel_model(
                200e3,      # sample_rate
                0.01,       # sro_stdev
                50,         # sro_maxdev
                0.01,       # cfo_stdev
                .5e3,       # cfo_maxdev
                8,          # n sinusoids in jakes model
                1.0,        # max fDoppler
                False,      # LOS(True)/NLOS(False)
                4.0,        # K-value in Rician fading
                (1,),       # PDP delays
                (1,),       # PDP Magnitudes
                1,                  # ntaps in channel impulse response
                0,                  # Noise amp (is added later)
                0                   # seed
            )
        self.connect(self, self.chan, self.add)


class chan_radio_selective_fading(channel):
    def __init__(self, snr_db=0):
        channel.__init__(self, snr_db=snr_db)
        self.chan = \
            channels.dynamic_channel_model(
                200e3,      # sample_rate
                0.01,       # sro_stdev
                50,         # sro_maxdev
                0.01,       # cfo_stdev
                .5e3,       # cfo_maxdev
                8,          # n sinusoids in jakes model
                1.0,        # max fDoppler
                False,      # LOS(True)/NLOS(False)
                4.0,        # K-value in Rician fading
                (0.0, 0.9, 1.7),    # PDP delays
                (1, 0.8, 0.3),      # PDP Magnitudes
                8,                  # ntaps in channel impulse response
                0,                  # Noise amp (is added later)
                0                   # seed
            )
        self.connect(self, self.chan, self.add)
