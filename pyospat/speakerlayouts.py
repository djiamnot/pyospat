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

import math

"""
Speaker positions constants.
"""

STEREO = [
    [- math.pi / 4.0, 0.0, 1.0], # each speaker has an aed
    [math.pi / 4.0, 0.0, 1.0]
    ]
"""
QUAD - Left, Right, Rear-Right, Rear-Left
"""
QUAD = [
    [- math.pi / 4.0, 0.0, 1.0], 
    [math.pi / 4.0, 0.0, 1.0], 
    [3 * math.pi / 4.0, 0.0, 1.0], 
    [- 3 * math.pi / 4.0, 0.0, 1.0]
    ]
"""
OCTO - 
Left 315 degrees, center, right 45 degrees, right 90, right-rear 135 
rear center (180), left-rear 225, left 270,
"""
OCTO =   [
    [- math.pi / 4.0, 0.0, 1.0],
    [0.0, 0.0, 1.0],
    [math.pi / 4.0, 0.0, 1.0], 
    [math.pi / 2.0, 0.0, 1.0], 
    [3 * math.pi / 4.0, 0.0, 1.0], 
    [math.pi, 0.0, 1.0], 
    [- 3 * math.pi / 4.0, 0.0, 1.0],
    [- math.pi / 2.0, 0.0, 1.0],
    ]



