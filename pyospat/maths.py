#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pyospat
# Copyright (C) 2011 Alexandre Quessy
# Copyright (C) 2011 Michal Seta
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Pyospat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyospat.  If not, see <http://www.gnu.org/licenses/>.

"""
maths stuff.
"""
import math

def dot_product(v1, v2):
    """
    Returns the dot products of two vectors.
    @param v1: list of three floats.
    @param v2: list of three floats.
    @return: float
    """
    return sum((a * b) for a, b in zip(v1, v2))

def length(v):
    """
    Returns the length of a vector.
    @param v: list of three floats.
    @return: float
    """
    return math.sqrt(dot_product(v, v))

def aed_to_xyz(aed):
    """
    Converts AED to XYZ.
    @param vec: list of three floats.
    @return: list of three floats.
    """
    azimuth = aed[0]
    elevation = aed[1]
    distance = aed[2]
    x = distance * math.sin(azimuth) * math.cos(elevation)
    y = distance * math.sin(azimuth) * math.sin(elevation)
    z = distance * math.cos(azimuth)
    return [x, y, z]

def normalize(vec):
    """
    Normalizes a 3D vector.
    @param vec: list of three floats.
    @return: list of three floats.
    """
    _length = length(vec)
    return [vec[0] / _length, vec[1] / _length, vec[2] / _length]

def angle_between_vectors(v1, v2):
    """
    Returns an absolute angle difference between v1 and v2 (with no notion of
    which is ahead or behind the other). Returned angle is from 0 to PI
    @param v1: list of three floats.
    @param v2: list of three floats.
    @rtype: float
    """
    # used to be:
    # return math.acos(dot_product(v1, v2) / (length(v1) * length(v2)))

    # normalize vectors (note: this must be done alone, not within any vector arithmetic. why?!)
    v1 = normalize(v1)
    v2 = normalize(v2)

    # Get the dot product of the vectors
    dotProduct = dot_product(v1, v2)

    # for acos, the value has to be between -1.0 and 1.0, but due to numerical imprecisions it sometimes comes outside this range
    if dotProduct > 1.0:
        dotProduct = 1.0;
    if dotProduct < -1.0:
        dotProduct = -1.0;

    # Get the angle in radians between the 2 vectors (should this be -acos ? ie, negative?)
    angle = math.acos(dotProduct)

    # Here we make sure that the angle is not a -1.#IND0000000 number, which means indefinite
    # if (isnan(angle))  //__isnand(x)
    #     return 0.0
    # Return the angle in radians
    return angle

def add(aed0, aed1):
    """
    Adds one vector to another.
    """
    return [
        aed0[0] + aed1[0], 
        aed0[1] + aed1[1], 
        aed0[2] + aed1[2], 
        ]
