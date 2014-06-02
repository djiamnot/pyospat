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
from pyospat import maths
"""
Speaker positions constants.
"""

STEREO = [
    [math.radians(45), 0.0, 1.0], # each speaker has an aed
    [math.radians(315), 0.0, 1.0]
    ]
"""
QUAD - Left, Right, Rear-Right, Rear-Left
"""
QUAD = [
    [math.radians(45), 0.0, 1.0], 
    [math.radians(315), 0.0, 1.0], 
    [math.radians(225), 0.0, 1.0], 
    [math.radians(135), 0.0, 1.0]
    ]
"""
OCTO - 
Left 315 degrees, center, right 45 degrees, right 90, right-rear 135 
rear center (180), left-rear 225, left 270,
"""
OCTO =   [
    [math.radians(45), 0.0, 1.0],
    [math.radians(0), 0.0, 1.0],
    [math.radians(315), 0.0, 1.0], 
    [math.radians(270), 0.0, 1.0], 
    [math.radians(225), 0.0, 1.0], 
    [math.radians(180), 0.0, 1.0], 
    [math.radians(135), 0.0, 1.0],
    [math.radians(90), 0.0, 1.0],
    ]

"""
DOME -
Speaker layout for the SATosphère as per the domeDev wiki.
As per email from Zack (vbap layout):

VBAP USES:

define_loudspeakers 3 0 90 0 55 45 55 90 55 135 55 180 55 -135 55 -90 55 -45 55 0 20 45 20 90 20 135 20 180 20 -135 20 -90 20 -45 20 0 -15 45 -15 90 -15 135 -15 180 -15 -135 -15 -90 -15 -45 -15


define_loudspeakers <dimension>  azi1 elev1 azi2 azi3 elev3.....



TOP: 0 90
Upper:  0 55 45 55 90 55 135 55 180 55 -135 55 -90 55 -45 55
Middle: 0 20 45 20 90 20 135 20 180 20 -135 20 -90 20 -45 20
Bottom: 0 -15 45 -15 90 -15 135 -15 180 -15 -135 -15 -90 -15 -45 -15

Each pair of numbers represents azimuth and elevation. We will continue to 
assume the distance at 1.0 until further notice. 

And we need to convert the degrees to radians:
"""

# SAT dome specific coordinate offsets
TOP_OFFSET = 0
HIGH_OFFSET = -7.5
MID_OFFSET = 7.5
LOW_OFFSET = 7.5

DOME8x8 = [
    [math.radians(TOP_OFFSET), math.radians(90), 1.0], #top
    # upper ring
    [ math.radians(HIGH_OFFSET + 0), math.radians(55), 1.0],
    [ math.radians(HIGH_OFFSET + 45), math.radians(55), 1.0],
    [ math.radians(HIGH_OFFSET + 90), math.radians(55), 1.0],
    [ math.radians(HIGH_OFFSET + 135), math.radians(55), 1.0],
    [ math.radians(HIGH_OFFSET + 180), math.radians(55), 1.0],
    [ - math.radians(HIGH_OFFSET + 135), math.radians(55), 1.0],
    [ - math.radians(HIGH_OFFSET + 90), math.radians(55), 1.0],
    [ - math.radians(HIGH_OFFSET + 45), math.radians(55), 1.0],
    # middle ring
    [ math.radians(MID_OFFSET + 0), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 45), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 90), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 135), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 180), math.radians(20), 1.0],
    [ - math.radians(MID_OFFSET + 135), math.radians(20), 1.0],
    [ - math.radians(MID_OFFSET + 90), math.radians(20), 1.0],
    [ - math.radians(MID_OFFSET + 45), math.radians(20), 1.0],
    # low ring
    [ math.radians(LOW_OFFSET + 0), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 45), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 90), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 135), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 180), math.radians(-15), 1.0],
    [ - math.radians(LOW_OFFSET + 135), math.radians(-15), 1.0],
    [ - math.radians(LOW_OFFSET + 90), math.radians(-15), 1.0],
    [ - math.radians(LOW_OFFSET + 45), math.radians(-15), 1.0],
    ]


"""
However, the above information
does not conform to https://code.sat.qc.ca/redmine/projects/dome-dev/wiki

We need to convert these cartesian coordinates to radians and follow the
wiki layout:
"""

SATDOME = [
    [math.radians(TOP_OFFSET), math.radians(90), 1.0], #top
    # upper ring (6 positions)
    [ math.radians(HIGH_OFFSET + 0), math.radians(55), 1.0],
    [ math.radians(HIGH_OFFSET + 60), math.radians(55), 1.0],
    [ math.radians(HIGH_OFFSET + 120), math.radians(55), 1.0],
    [ math.radians(HIGH_OFFSET + 180), math.radians(55), 1.0],
    [ - math.radians(HIGH_OFFSET + 120), math.radians(55), 1.0],
    [ - math.radians(HIGH_OFFSET + 60), math.radians(55), 1.0],
    # middle ring (12 positions)
    [ math.radians(MID_OFFSET + 0), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 30), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 60), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 90), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 120), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 150), math.radians(20), 1.0],
    [ math.radians(MID_OFFSET + 180), math.radians(20), 1.0],
    [ - math.radians(MID_OFFSET + 150), math.radians(20), 1.0],
    [ - math.radians(MID_OFFSET + 120), math.radians(20), 1.0],
    [ - math.radians(MID_OFFSET + 90), math.radians(20), 1.0],
    [ - math.radians(MID_OFFSET + 60), math.radians(20), 1.0],
    [ - math.radians(MID_OFFSET + 30), math.radians(20), 1.0],
    # low ring (12 positions)
    [ math.radians(LOW_OFFSET + 0), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 30), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 60), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 90), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 120), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 150), math.radians(-15), 1.0],
    [ math.radians(LOW_OFFSET + 180), math.radians(-15), 1.0],
    [ - math.radians(LOW_OFFSET + 150), math.radians(-15), 1.0],
    [ - math.radians(LOW_OFFSET + 120), math.radians(-15), 1.0],
    [ - math.radians(LOW_OFFSET + 90), math.radians(-15), 1.0],
    [ - math.radians(LOW_OFFSET + 60), math.radians(-15), 1.0],
    [ - math.radians(LOW_OFFSET + 30), math.radians(-15), 1.0],
    ]

FIVE = [
    [math.radians(288), 0.0, 1.0],
    [math.radians(0), 0.0, 1.0],
    [math.radians(72), 0.0, 1.0],
    [math.radians(144), 0.0, 1.0],
    [math.radians(216), 0.0, 1.0]
    ]

# this is a setup specific to OKTA setup by Field Sound
OKTA = [
    [math.radians(12), 0.0, 9.], # A1
    [math.radians(348), 0.0, 9.0], # A2
    [math.radians(328), 0.0, 10.2], # A3
    [math.radians(52), 0.0, 8.55], # B1 
    [math.radians(35), 0.0, 6.], # B2
    [math.radians(0), 0.0, 5.25], # B3
    [math.radians(330), 0.0, 6.44], # B4
    [math.radians(81), 0.0, 9.0], # C1
    [math.radians(71), 0.0, 5.25], # C2
    [math.radians(45), 0.0, 2.25], # C3
    [math.radians(320), 0.0, 2.25], # C4
    [math.radians(287), 0.0, 5.25], # C5
    [math.radians(280), 0.0, 9.0], # C6
    [math.radians(118), 0.0, 9.0], # D1
    [math.radians(109), 0.0, 5.25], # D2
    [math.radians(143), 0.0, 2.25], # D3
    [math.radians(225), 0.0, 2.25], # D4
    [math.radians(250), 0.0, 5.25], # D5
    [math.radians(120), 0.0, 10.5], # E1
    [math.radians(147), 0.0, 6.0], # E2
    [math.radians(163), 0.0, 5.69], # E3
    [math.radians(223), 0.0, 5.69], # E4
    [math.radians(151), 0.0, 9.75], # F1
    [math.radians(172), 0.0, 9.0] # F2
    ]

