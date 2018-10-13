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

from gnuradio import gr, blocks, digital, filter, analog, fft
from gnuradio.filter import firdes
from constellations import *
import classify
import numpy as np


'''
All constellation based transmitters
'''
class constellation_source(gr.hier_block2):
    def __init__(self, mod_name="", samp_per_sym=2, excess_bw=.35):
        gr.hier_block2.__init__(
            self, mod_name,
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_gr_complex)
        )
        self.random_source = \
            blocks.vector_source_b(
                map(int, np.random.randint(0, 255, int(1e6))), True
            )
        num_filters = 32
        num_taps = num_filters * 11 * int(samp_per_sym)  # make nfilts filters of ntaps each
        rrc_taps = filter.firdes.root_raised_cosine(
            num_filters,  # gain
            num_filters,  # sampling rate based on 32 filters in resampler
            1.0,  # symbol rate
            excess_bw,  # excess bandwidth (roll-off factor)
            num_taps)

        self.rrc_filter = filter.pfb_arb_resampler_ccf(samp_per_sym, rrc_taps)
        self.rrc_filter.declare_sample_delay(0)


class tx_ook(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="ook", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_ook()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_bpsk(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="bpsk", samp_per_sym=2, excess_bw=.35)
        self.const = digital.constellation_bpsk().base()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_4pam(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="4pam", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_4_pam()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_4ask(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="4ask", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_4_ask()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_8pam(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="8pam", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_8_pam()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_8psk(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="8psk", samp_per_sym=2, excess_bw=.35)
        self.const = digital.constellation_8psk().base()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_8qam_circular(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="8qam_circular", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_8qam_cross()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_8qam_cross(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="8qam_cross", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_8qam_cross()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_16qam(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="16pam", samp_per_sym=2, excess_bw=.35)
        self.const = digital.constellation_16qam().base()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_16psk(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="16psk", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_16_psk()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_32qam_cross(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="32qam_cross", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_32qam_cross()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_32qam_rect(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="32qam_rect", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_32qam_rect()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


class tx_64qam(constellation_source):
    def __init__(self):
        constellation_source.__init__(self, mod_name="64qam", samp_per_sym=2, excess_bw=.35)
        self.const = constellation_64qam()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.connect(self.random_source, self.pack, self.map, self.rrc_filter, self)


'''
All FSK Transmitters
'''
class fsk_source(gr.hier_block2):
    def __init__(self, mod_name="", samp_per_sym=8):
        gr.hier_block2.__init__(
            self, mod_name,
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_gr_complex)
        )
        self.samp_per_sym = samp_per_sym
        self.random_source = \
            blocks.vector_source_b(
                map(int, np.random.randint(0, 255, int(1e6))), True
            )


class tx_2gfsk(fsk_source):
    def __init__(self):
        fsk_source.__init__(self, mod_name="2gfsk", samp_per_sym=8)
        self.pack = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bf(np.linspace(-2, 2, 2), 1)
        # This design mirrors the internals of the GMSK mod block
        self.taps = np.convolve(firdes.gaussian(1, self.samp_per_sym, .35, 4*self.samp_per_sym), (1,)*self.samp_per_sym)
        self.filt = \
            filter.interp_fir_filter_fff(
                self.samp_per_sym,
                self.taps,
            )
        self.filt.declare_sample_delay(0)
        self.mod = analog.frequency_modulator_fc(1)
        self.connect(self.random_source, self.pack, self.map, self.filt, self.mod, self)


class tx_4gfsk(fsk_source):
    def __init__(self):
        fsk_source.__init__(self, mod_name="4gfsk", samp_per_sym=8)
        self.pack = blocks.packed_to_unpacked_bb(2, gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bf(np.linspace(-2, 2, 4), 1)
        # This design mirrors the internals of the GMSK mod block
        self.taps = np.convolve(firdes.gaussian(1, self.samp_per_sym, .35, 4*self.samp_per_sym), (1,)*self.samp_per_sym)
        self.filt = \
            filter.interp_fir_filter_fff(
                self.samp_per_sym,
                self.taps,
            )
        self.filt.declare_sample_delay(0)
        self.mod = analog.frequency_modulator_fc(1)
        self.connect(self.random_source, self.pack, self.map, self.filt, self.mod, self)

class tx_8gfsk(fsk_source):
    def __init__(self):
        fsk_source.__init__(self, mod_name="8gfsk", samp_per_sym=8)
        self.pack = blocks.packed_to_unpacked_bb(3, gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bf(np.linspace(-2, 2, 8), 1)
        # This design mirrors the internals of the GMSK mod block
        self.taps = np.convolve(firdes.gaussian(1, self.samp_per_sym, .35, 4*self.samp_per_sym), (1,)*self.samp_per_sym)
        self.filt = \
            filter.interp_fir_filter_fff(
                self.samp_per_sym,
                self.taps,
            )
        self.filt.declare_sample_delay(0)
        self.mod = analog.frequency_modulator_fc(1)
        self.connect(self.random_source, self.pack, self.map, self.filt, self.mod, self)


class tx_2cpfsk(fsk_source):
    def __init__(self):
        fsk_source.__init__(self, mod_name="2cpfsk", samp_per_sym=8)
        self.pack = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.mod = classify.cpfsk_bc(.5, 1.0, self.samp_per_sym, 1)
        self.connect(self.random_source, self.pack, self.mod, self)


class tx_4cpfsk(fsk_source):
    def __init__(self):
        fsk_source.__init__(self, mod_name="4cpfsk", samp_per_sym=8)
        self.pack = blocks.packed_to_unpacked_bb(2, gr.GR_MSB_FIRST)
        self.mod = classify.cpfsk_bc(.5, 1.0, self.samp_per_sym, 2)
        self.connect(self.random_source, self.pack, self.mod, self)


class tx_8cpfsk(fsk_source):
    def __init__(self):
        fsk_source.__init__(self, mod_name="8cpfsk", samp_per_sym=8)
        self.pack = blocks.packed_to_unpacked_bb(3, gr.GR_MSB_FIRST)
        self.mod = classify.cpfsk_bc(.5, 1.0, self.samp_per_sym, 3)
        self.connect(self.random_source, self.pack, self.mod, self)


'''
All OFDM Transmitters
'''
class ofdm_source(gr.hier_block2):
    def __init__(self, mod_name="", fft_len=32):
        gr.hier_block2.__init__(
            self, mod_name,
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_gr_complex)
        )
        self.random_source = \
            blocks.vector_source_b(
                map(int, np.random.randint(0, 255, int(1e6))), True
            )
        self.null = blocks.null_source(gr.sizeof_gr_complex*1)
        self.rolloff = 2
        self.fft_len = fft_len

        self.mult = blocks.multiply_const_vcc((1.0/np.sqrt(self.fft_len/2), ))
        self.s2v = blocks.stream_to_vector(gr.sizeof_gr_complex*1, self.fft_len)
        self.mux = blocks.stream_mux(gr.sizeof_gr_complex*1, (self.fft_len/4, self.fft_len/2, self.fft_len/4))
        self.fft = fft.fft_vcc(self.fft_len, False, (()), True, 1)
        self.cp = digital.ofdm_cyclic_prefixer(self.fft_len, self.fft_len+self.fft_len/4, self.rolloff, '')


class tx_ofdm_16_bpsk(ofdm_source):
    def __init__(self):
        ofdm_source.__init__(self, mod_name="ofdm_16_bpsk", fft_len=32)
        self.const = digital.constellation_bpsk().base()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)

        self.connect(self.random_source, self.pack, self.map)
        self.connect(self.null, (self.mux, 0))
        self.connect(self.map, (self.mux, 1))
        self.connect(self.null, (self.mux, 2))
        self.connect(self.mux, self.s2v, self.fft, self.cp, self.mult, self)


class tx_ofdm_32_bpsk(ofdm_source):
    def __init__(self):
        ofdm_source.__init__(self, mod_name="ofdm_32_bpsk", fft_len=64)
        self.const = digital.constellation_bpsk().base()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)

        self.connect(self.random_source, self.pack, self.map)
        self.connect(self.null, (self.mux, 0))
        self.connect(self.map, (self.mux, 1))
        self.connect(self.null, (self.mux, 2))
        self.connect(self.mux, self.s2v, self.fft, self.cp, self.mult, self)


class tx_ofdm_64_bpsk(ofdm_source):
    def __init__(self):
        ofdm_source.__init__(self, mod_name="ofdm_64_bpsk", fft_len=128)
        self.const = digital.constellation_bpsk().base()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)

        self.connect(self.random_source, self.pack, self.map)
        self.connect(self.null, (self.mux, 0))
        self.connect(self.map, (self.mux, 1))
        self.connect(self.null, (self.mux, 2))
        self.connect(self.mux, self.s2v, self.fft, self.cp, self.mult, self)


class tx_ofdm_16_qpsk(ofdm_source):
    def __init__(self):
        ofdm_source.__init__(self, mod_name="ofdm_16_qpsk", fft_len=32)
        self.const = digital.constellation_qpsk().base()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)

        self.connect(self.random_source, self.pack, self.map)
        self.connect(self.null, (self.mux, 0))
        self.connect(self.map, (self.mux, 1))
        self.connect(self.null, (self.mux, 2))
        self.connect(self.mux, self.s2v, self.fft, self.cp, self.mult, self)


class tx_ofdm_32_qpsk(ofdm_source):
    def __init__(self):
        ofdm_source.__init__(self, mod_name="ofdm_32_qpsk", fft_len=64)
        self.const = digital.constellation_qpsk().base()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)

        self.connect(self.random_source, self.pack, self.map)
        self.connect(self.null, (self.mux, 0))
        self.connect(self.map, (self.mux, 1))
        self.connect(self.null, (self.mux, 2))
        self.connect(self.mux, self.s2v, self.fft, self.cp, self.mult, self)


class tx_ofdm_64_qpsk(ofdm_source):
    def __init__(self):
        ofdm_source.__init__(self, mod_name="ofdm_64_qpsk", fft_len=128)
        self.const = digital.constellation_qpsk().base()
        self.pack = blocks.packed_to_unpacked_bb(self.const.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.map = digital.chunks_to_symbols_bc((self.const.points()), 1)

        self.connect(self.random_source, self.pack, self.map)
        self.connect(self.null, (self.mux, 0))
        self.connect(self.map, (self.mux, 1))
        self.connect(self.null, (self.mux, 2))
        self.connect(self.mux, self.s2v, self.fft, self.cp, self.mult, self)


'''
All analog data-bearing transmitters
'''
class analog_source(gr.hier_block2):
    def __init__(self, mod_name="", audio_rate=44.1e3):
        gr.hier_block2.__init__(
            self, mod_name,
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_gr_complex)
        )
        self.random_source = \
            analog.noise_source_f(analog.GR_GAUSSIAN, 1, 0)
        self.audio_rate = audio_rate


class tx_wbfm(analog_source):
    def __init__(self):
        analog_source.__init__(self, mod_name="wbfm", audio_rate=44.1e3)
        self.mod = analog.wfm_tx(audio_rate=self.audio_rate, quad_rate=220.5e3)
        self.connect(self.random_source, self.mod, self)


class tx_am_dsb(analog_source):
    def __init__(self):
        analog_source.__init__(self, mod_name="am-dsb", audio_rate=44.1e3)
        self.interp = filter.fractional_resampler_ff(0.0, self.audio_rate/200e3)
        self.cnv = blocks.float_to_complex()
        self.add = blocks.add_const_cc(1.0)
        self.mod = blocks.multiply_cc()
        self.connect(self.random_source, self.interp, self.cnv, self.add, self)


class tx_am_ssb(analog_source):
    def __init__(self):
        analog_source.__init__(self, mod_name="am-ssb", audio_rate=44.1e3)
        self.interp = filter.fractional_resampler_ff(0.0, self.audio_rate/200e3)
        self.add = blocks.add_const_ff(1.0)
        self.mod = blocks.multiply_ff()
        self.filt = filter.hilbert_fc(401)
        self.connect(self.random_source, self.interp, self.add, self.filt, self)


'''
All radar transmitters
'''
class radar_source(gr.hier_block2):
    def __init__(self, mod_name="", chirp_len=1024):
        gr.hier_block2.__init__(
            self, mod_name,
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_gr_complex)
        )
        self.chirp_len = chirp_len
        self.fm = analog.frequency_modulator_fc(np.pi)


class tx_lfm_triangle(radar_source):
    def __init__(self):
        radar_source.__init__(self, mod_name="fmcw-triangle", chirp_len=1024)
        self.source = blocks.vector_source_f(
            np.linspace(-.5, .5, self.chirp_len),
            True
        )
        self.connect(self.source, self.fm, self)


class tx_lfm_sawtooth(radar_source):
    def __init__(self):
        radar_source.__init__(self, mod_name="fmcw-sawtooth", chirp_len=1024)
        self.source = blocks.vector_source_f(
            np.concatenate(
                np.linspace(-.5, .5, self.chirp_len/2),
                np.linspace(.5, -.5, self.chirp_len/2)
            ),
            True
        )
        self.connect(self.source, self.fm, self)
