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

def angle(v1, v2):
    """
    Returns the angle between two vectors.
    @param v1: list of three floats.
    @param v2: list of three floats.
    @return: float
    """
    return math.acos(dot_product(v1, v2) / (length(v1) * length(v2)))
