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
Maths stuff for audio spatialization.
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
    Returns the length of a 3D vector.
    @param v: list of three floats.
    @return: float
    """
    return math.sqrt(dot_product(v, v))

def aed_to_xyz(aed):
    """
    Converts AED to XYZ.
    @param aed: list of three floats.
    @return: list of three floats.
    """
    azimuth = aed[0]-math.pi/2
    elevation = aed[1]-math.pi/2
    _distance = aed[2]
    x = _distance * math.sin(azimuth) * math.cos(elevation)
    y = _distance * math.sin(azimuth) * math.sin(elevation)
    z = _distance * math.cos(azimuth)
    return [x, y, z]

def xyz_to_aed(xyz):
    """
    Converts XYZ to AED.
    @param aed: list of three floats.
    @return: list of three floats.
    """
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    distance = math.sqrt((x*x) + (y*y) + (z*z))
    azimuth = math.atan2(y,x)
    # put in range of [-pi, pi]
    if azimuth > math.pi:
        azimuth -= 2 * math.pi
    else:
        azimuth += 2 * math.pi
    if distance > 0.00001:
        elevation = math.acos(z/distance)
    else:
        elevation = 0.0
    return [azimuth, elevation, distance]


def normalize(vec):
    """
    Normalizes a 3D vector.
    @param vec: list of three floats.
    @return: list of three floats.
    """
    _length = length(vec) # get the length of the 3D vector
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

def distance_to_attenuation(distance):
    """
    A very crude distance to attenuation conversion.
    (we use the abs of the number you give us.)
    @param distance: Absolute distance in meters.
    @type distance: float
    @rtype: float
    """
    d = abs(distance)
    if d <= 1.0:
        return 1.0
    attenuation = 1.0 / d
    return attenuation

def map_from_zero_to_one(value):
    """
    Maps a value in the range [-1.0, 1.0] to the range [0.0, 1.0]
    @param value: float in the range [-1.0, 1.0]
    @rtype: float
    """
    return value * 0.5 + 0.5

def attenuate_according_to_angle(angle):
    """
    Computes attenuation per speaker (0..1)
    @param angle: radian
    @rtype: float
    """
    return map_from_zero_to_one(math.cos(angle))

def spread(value, factor=2):
    """
    Apply spread factor (according to constant total power)
    @param value: input
    @param factor: exponent, default=2
    @rtype: float
    """
    #TODO: give this a better name
    return math.pow(value, factor)

def subtract(aed0, aed1):
    """
    Subtract one vector from another.
    """
    return [
        aed0[0] - aed1[0], 
        aed0[1] - aed1[1], 
        aed0[2] - aed1[2], 
        ]

def angles_to_attenuation(speaker_aed, source_aed, exponent=2.0):
    """
    The most important function in this application!
    Returns the volume to mix a sound source for its position relative to the position of a speaker.
    @param speaker_aed: AED position of the loudspeaker.
    @param source_aed: AED position of the sound source.
    @param exponent: spread between speakers. 2.0 is for stereo or quad. 4.0 for octo. 4 is more discrete than 2.
    @rtype: float
    @return: Audio level factor.
    """
    aed = subtract(speaker_aed, source_aed)
    factor = 1.0
    factor *= spread(attenuate_according_to_angle(aed[0]), exponent)
    factor *= spread(attenuate_according_to_angle(aed[1]), exponent)
    dist = aed[2]
    factor *= distance_to_attenuation(dist)
    return factor

