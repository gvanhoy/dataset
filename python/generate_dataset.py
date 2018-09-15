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
from classify.data_source import *
from classify.channel import *
from gnuradio import gr, blocks
from numpy import random
import pandas as pd
import time


def generate_dataset(channel_type="awgn",
                     snr_vals=range(-20, 20, 2),
                     num_cplx_samples=128,
                     num_exemplars_per_key=1000,
                     dataset="all_tx"):
    all_data = pd.DataFrame()
    all_tx = get_dataset(dataset)

    for idx_snr, snr_db in enumerate(snr_vals):
        for idx_tx, tx_key in enumerate(all_tx.keys()):
            # Make the top block with tx and channel
            tb = gr.top_block()
            snk = blocks.vector_sink_c()
            max_data_len = 5*num_cplx_samples*num_exemplars_per_key + 500
            limit = blocks.head(gr.sizeof_gr_complex, max_data_len)
            chan = get_channel(channel_type, snr_db)
            tb.connect(all_tx[tx_key], chan, limit, snk)
            tb.start()
            while len(snk.data()) != max_data_len:
                time.sleep(.01)
            tb.stop()

            # Gather the data
            raw_output_vector = np.array(snk.data(), dtype=np.complex64)

            # start the sampler some random time after channel model transients (arbitrary values here)
            random_idx = np.cumsum(random.randint(2*num_cplx_samples, 4*num_cplx_samples, size=(num_exemplars_per_key,))) + 500
            data = np.zeros((num_exemplars_per_key,
                             num_cplx_samples,
                             2), dtype=np.float32)
            for idx_exemplar, offset in enumerate(random_idx):
                sampled_vector = raw_output_vector[offset:offset + num_cplx_samples]
                energy = np.sum(np.abs(sampled_vector)**2)
                sampled_vector = sampled_vector / energy
                data[idx_exemplar, :, 0] = np.real(sampled_vector)
                data[idx_exemplar, :, 1] = np.imag(sampled_vector)
            mod_data = pd.DataFrame(data=data.reshape(num_exemplars_per_key, num_cplx_samples*2))
            mod_data["mod_name"] = tx_key
            mod_data["snr_db"] = snr_db
            all_data = all_data.append(mod_data)
    return all_data


def get_channel(channel_string, snr_db):
    if channel_string is "":
        return chan_none()
    elif channel_string == "awgn":
        return chan_awgn(snr_db)
    elif channel_string == "flat_fading":
        return chan_flat_fading(snr_db)
    elif channel_string == "selective_fading":
        return chan_selective_fading(snr_db)
    elif channel_string == "radio_awgn":
        return chan_radio_awgn(snr_db)
    elif channel_string == "radio_flat_fading":
        return chan_radio_flat_fading(snr_db)
    elif channel_string == "radio_selective_fading":
        return chan_radio_selective_fading(snr_db)


def get_dataset(dataset_string):
    if dataset_string == "all_tx":
        return {
            'ook': tx_ook(),
            'bpsk': tx_bpsk(),
            '4ask': tx_4ask(),
            '4pam': tx_4pam(),
            '8pam': tx_8pam(),
            '8qam_circular': tx_8qam_circular(),
            '8qam_cross': tx_8qam_cross(),
            '16qam': tx_16qam(),
            '16psk': tx_16psk(),
            '32qam_cross': tx_32qam_cross(),
            '32qam_rect': tx_32qam_rect(),
            '64qam': tx_64qam(),
            '2gfsk': tx_2gfsk(),
            '4gfsk': tx_4gfsk(),
            '8gfsk': tx_8gfsk(),
            '2cpfsk': tx_2cpfsk(),
            '4cpfsk': tx_4cpfsk(),
            '8cpfsk': tx_8cpfsk(),
            'ofdm-16-bpsk': tx_ofdm_16_bpsk(),
            'ofdm-32-bpsk': tx_ofdm_32_bpsk(),
            'ofdm-64-bpsk': tx_ofdm_64_bpsk(),
            'ofdm-16-qpsk': tx_ofdm_16_qpsk(),
            'ofdm-32-qpsk': tx_ofdm_32_qpsk(),
            'ofdm-64-qpsk': tx_ofdm_64_qpsk(),
            'am-dsb': tx_am_dsb(),
            'am-ssb': tx_am_ssb(),
            'wbfm': tx_wbfm(),
            'lfm_sawtooth': tx_lfm_sawtooth(),
            'lfm_squarewave': tx_lfm_squarewave()
        }
    elif dataset_string == "small":
        return {
            'ook': tx_ook(),
            'bpsk': tx_bpsk(),
            '4pam': tx_4pam(),
            '8qam_circular': tx_8qam_circular(),
            '16qam': tx_16qam(),
            'ofdm-32-bpsk': tx_ofdm_16_bpsk(),
            '2gfsk': tx_2gfsk(),
            '2cpfsk': tx_2cpfsk(),
            'am-dsb': tx_am_dsb(),
            'wbfm': tx_wbfm()
        }
    elif dataset_string == "ofdm":
        return {
            'ofdm-16-bpsk': tx_ofdm_16_bpsk(),
            'ofdm-32-bpsk': tx_ofdm_32_bpsk(),
            'ofdm-64-bpsk': tx_ofdm_64_bpsk(),
            'ofdm-16-qpsk': tx_ofdm_16_qpsk(),
            'ofdm-32-qpsk': tx_ofdm_32_qpsk(),
            'ofdm-64-qpsk': tx_ofdm_64_qpsk()
        }
    elif dataset_string == "constellation":
        return {
            'ook': tx_ook(),
            'bpsk': tx_bpsk(),
            '4ask': tx_4ask(),
            '4pam': tx_4pam(),
            '8pam': tx_8pam(),
            '8qam_circular': tx_8qam_circular(),
            '8qam_cross': tx_8qam_cross(),
            '16qam': tx_16qam(),
            '16psk': tx_16psk(),
            '32qam_cross': tx_32qam_cross(),
            '32qam_rect': tx_32qam_rect(),
            '64qam': tx_64qam()
        }
    elif dataset_string == "fsk":
        return {
            '2gfsk': tx_2gfsk(),
            '4gfsk': tx_4gfsk(),
            '8gfsk': tx_8gfsk(),
            '2cpfsk': tx_2cpfsk(),
            '4cpfsk': tx_4cpfsk(),
            '8cpfsk': tx_8cpfsk()
        }
    elif dataset_string == "analog":
        return {
            'am-dsb': tx_am_dsb(),
            'am-ssb': tx_am_ssb(),
            'wbfm': tx_wbfm(),
            'lfm_sawtooth': tx_lfm_sawtooth(),
            'lfm_squarewave': tx_lfm_squarewave()
        }


def get_hierarchy():
    return {
        'analog': {
            'radar': {
                'lfm_sawtooth': tx_lfm_sawtooth(),
                'lfm_squarewave': tx_lfm_squarewave()
            },
            'data-bearing': {
                'wbfm': tx_wbfm(),
                'am-ssb': tx_am_ssb(),
                'am-dsb': tx_am_dsb()
            }
        },
        'digital': {
            'constellation': {
                'ook': tx_ook(),
                'bpsk': tx_bpsk(),
                '4ask': tx_4ask(),
                '4pam': tx_4pam(),
                '8pam': tx_8pam(),
                '8qam_circular': tx_8qam_circular(),
                '8qam_cross': tx_8qam_cross(),
                '16qam': tx_16qam(),
                '16psk': tx_16psk(),
                '32qam_cross': tx_32qam_cross(),
                '32qam_rect': tx_32qam_rect(),
                '64qam': tx_64qam()
            },
            'fsk': {
                '2gfsk': tx_2gfsk(),
                '4gfsk': tx_4gfsk(),
                '8gfsk': tx_8gfsk(),
                '2cpfsk': tx_2cpfsk(),
                '4cpfsk': tx_4cpfsk(),
                '8cpfsk': tx_8cpfsk()
            },
            'ofdm': {
                'ofdm-16-bpsk': tx_ofdm_16_bpsk(),
                'ofdm-32-bpsk': tx_ofdm_32_bpsk(),
                'ofdm-64-bpsk': tx_ofdm_64_bpsk(),
                'ofdm-16-qpsk': tx_ofdm_16_qpsk(),
                'ofdm-32-qpsk': tx_ofdm_32_qpsk(),
                'ofdm-64-qpsk': tx_ofdm_64_qpsk()
            }
        }
    }
