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

import numpy as np
from gnuradio import digital


def constellation_ook():
    '''
        0 1
    '''
    constellation_points = [
        0, 1
    ]
    gray_code = [
        0, 1
    ]
    return digital.constellation_calcdist(
        constellation_points,
        gray_code,
        1,  # rotational symmetry
        1   # dimensionality
    ).base()


def constellation_4_pam():
    '''
        0 1 3 2
    '''
    constellation_points = [
        0, 1, 2, 3
    ]
    gray_code = [
        0, 1, 3, 2
    ]
    return digital.constellation_calcdist(
        constellation_points,
        gray_code,
        1,  # rotational symmetry
        1   # dimensionality
    ).base()


def constellation_4_ask():
    '''
        0   1   3   2
    '''
    constellation_points = [
        -3, -1, 1, 3
    ]
    gray_code = [
        0, 1, 3, 2
    ]
    return digital.constellation_rect(
        constellation_points,
        gray_code,
        2,  # rotational symmetry
        4,  # real sectors
        1,  # imaginary sectors
        2,  # real sector width
        2   # imaginary sector width
    ).base()


def constellation_8_pam():
    '''
        6   2   3   1   0   4   5   7
    '''
    constellation_points = [
        0, 1, 2, 3, 4, 5, 6, 7
    ]
    gray_code = [
        6, 2, 3, 1, 0, 4, 5, 7
    ]
    return digital.constellation_calcdist(
        constellation_points,
        gray_code,
        1,  # rotational symmetry
        1   # dimensionality
    ).base()


def constellation_8_ask():
    '''
        6   2   3   1   0   4   5   7
    '''
    constellation_points = [
        -7, -5, -3, -1, 1, 3, 5, 7
    ]
    gray_code = [
        6, 2, 3, 1, 0, 4, 5, 7
    ]
    return digital.constellation_rect(
        constellation_points,
        gray_code,
        2,  # rotational symmetry
        8,  # real sectors
        1,  # imaginary sectors
        2,  # real sector width
        2   # imaginary sector width
    ).base()


def constellation_8qam_circular():
    '''
            1
          5   4
        2       0
          6   7
            3
    '''
    constellation_points = [
        complex(0, 1 + np.sqrt(3)),
        -1 + 1j, 1 + 1j,
        -1 - np.sqrt(3), 1 + np.sqrt(3),
        -1 - 1j, 1 - 1j,
        complex(0, -1 - np.sqrt(3))
        ]
    gray_code = [
        1,
        5, 4,
        2, 0,
        6, 7,
        3
    ]
    return digital.constellation_calcdist(
        constellation_points,
        gray_code,
        4,  # rotational symmetry
        1   # dimensionality
    ).base()


def constellation_8qam_rectangular():
    '''
        2   3   1   0
        6   7   5   4
    '''
    constellation_points = [
        -3 + 1j, -1 + 1j, 1 + 1j, 3 + 1j,
        -3 - 1j, -1 - 1j, 1 - 1j, 3 - 1j
    ]
    gray_code = [
        2, 3, 1, 0,
        6, 7, 5, 4
    ]
    return digital.constellation_calcdist(
        constellation_points,
        gray_code,
        2,  # rotational symmetry
        1   # dimensionality
    ).base()


def constellation_8qam_cross():
    '''
            0
        4   6   2
        5   7   3
            1
    '''
    constellation_points = [
        0 + 3j,
        -2 + 1j, 0 + 1j, 2 + 1j,
        -2 - 1j, 0 - 1j, 2 - 1j,
        0 - 3j
    ]
    gray_code = [
        0,
        4, 6, 2,
        5, 7, 3,
        1
    ]
    return digital.constellation_rect(
        constellation_points,
        gray_code,
        2,  # rotational symmetry
        3,  # real sectors
        4,  # imaginary sectors
        2,  # real sector width
        2   # imaginary sector width
    ).base()


def constellation_16_psk():
    '''
                    6
                7       2
            5               3
        4                       1
    12                              0
        13                      8
            15              9
                14      11
                    10
    '''
    constellation_points = np.exp(2j*np.linspace(0, np.pi*15/16.0, 16))
    gray_code = [
        6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8, 0, 1, 3, 2
    ]
    return digital.constellation_calcdist(
        constellation_points,
        gray_code,
        16,  # rotational symmetry
        1   # dimensionality
    ).base()


def constellation_32qam_cross():
    '''
            0   1   29  28
        4   8   12  16  20  24
        5   9   13  17  21  25
        6   10  14  18  22  26
        7   11  15  19  23  27
            3   2   30  31
    '''
    constellation_points = [
        -3 + 5j, -1 + 5j, 1 + 5j, 3 + 5j,
        -5 + 3j, -3 + 3j, -1 + 3j, 1 + 3j, 3 + 3j, 5 + 3j,
        -5 + 1j, -3 + 1j, -1 + 1j, 1 + 1j, 3 + 1j, 5 + 1j,
        -5 - 1j, -3 - 1j, -1 - 1j, 1 - 1j, 3 - 1j, 5 - 1j,
        -5 - 3j, -3 - 3j, -1 - 3j, 1 - 3j, 3 - 3j, 5 - 3j,
        -3 - 5j, -1 - 5j, 1 - 5j, 3 - 5j
    ]
    gray_code = [
        0, 1, 29, 28,
        4, 8, 12, 16, 20, 24,
        5, 9, 13, 17, 21, 25,
        6, 10, 14, 18, 22, 26,
        7, 11, 15, 19, 23, 27,
        3, 2, 30, 31
    ]
    return digital.constellation_rect(
        constellation_points,
        gray_code,
        4,  # rotational symmetry
        6,  # real sectors
        6,  # imaginary sectors
        2,  # real sector width
        2   # imaginary sector width
    ).base()


def constellation_32qam_rect():
    '''
    2   6   14  19  26  29  22  18
    3   7   15  11  27  30  23  19
    1   5   13  9   25  28  21  17
    0   4   12  8   24  27  20  16
    '''
    real, imaginary = np.meshgrid(np.linspace(-7, 7, 8), np.linspace(-3, 3, 4))
    constellation_points = real + np.multiply(imaginary, 1j)
    gray_code = [
        2, 6, 14, 10, 26, 29, 22, 18,
        3, 7, 15, 11, 27, 30, 23, 19,
        1, 5, 13, 9, 25, 28, 21, 17,
        0, 4, 12, 8, 24, 27, 20, 16
    ]
    return digital.constellation_rect(
        constellation_points.flatten(),
        gray_code,
        2,  # rotational symmetry
        4,  # real sectors
        8,  # imaginary sectors
        2,  # real sector width
        2   # imaginary sector width
    ).base()


def constellation_64qam():
    # points are separated as such
    real, imaginary = np.meshgrid(np.linspace(-7, 7, 8), np.linspace(-7, 7, 8))
    constellation_points = real + np.multiply(imaginary, 1j)
    gray_code = [
        4, 12, 28, 20, 52, 60, 44, 36,
        5, 13, 29, 21, 53, 61, 45, 37,
        7, 15, 31, 23, 55, 63, 47, 39,
        6, 14, 30, 22, 54, 62, 46, 39,
        2, 10, 26, 18, 50, 58, 42, 34,
        3, 11, 27, 19, 51, 59, 43, 35,
        1, 9, 25, 17, 49, 57, 41, 33,
        0, 8, 24, 16, 48, 56, 40, 32
    ]
    return digital.constellation_rect(
        constellation_points.flatten(),
        gray_code,
        4,  # rotational symmetry
        8,  # real sectors
        8,  # imaginary sectors
        2,  # real sector width
        2   # imaginary sector width
    ).base()
 
