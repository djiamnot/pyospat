#!/usr/bin/env python
"""
Test maths stuff.
"""
from twisted.trial import unittest
from pyospat import maths
import math

class Test_Vector_Stuff(unittest.TestCase):
    def test_vector_length(self):
        self.failUnlessEqual(maths.length([0.0, 1.0, 0.0]), 1.0)
        self.failUnlessEqual(maths.length([1.0, 1.0, 1.0]), 1.7320508075688772)

    def test_angle_between_vectors(self):
        self.failUnlessEqual(maths.angle_between_vectors([0.0, 1.0, 0.0], [1.0, 0.0, 0.0]), math.pi / 2.0)
        self.failUnlessEqual(maths.angle_between_vectors([0.0, 1.0, 0.0], [0.0, -1.0, 0.0]), math.pi)
        self.failUnlessEqual(maths.angle_between_vectors([0.0, 1.0, 0.0], [0.0, 1.0, 0.0]), 0.0)

    def test_normalize(self):
        for v in [
            [0.0, 1.0, 0.0],
            [1.0, 4.0, 2.0],
            [2.0, 3.0, 1.0],
            [3.0, 1.0, 2.0],
            [4.0, 5.0, 4.0],
            [7.0, 1.0, 5.0],
        ]:
            self.failUnlessEqual(round(maths.length(maths.normalize(v)), 1), 1.0)

    def test_dot_product(self):
        def _test(v1, v2, expected):
            self.failUnlessEqual(maths.dot_product(v1, v2), expected)
        for v1, v2, expected in [
            [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
            [[2.0, 2.0, 2.0], [1.0, 2.0, 3.0], [2.0, 4.0, 6.0]],
        ]:
            _test(v1, v2, expected)
    
    test_dot_product.skip = "to do"

class Test_Audio_Spatialization(unittest.TestCase):
    def test_angles_to_attenuation(self):
        def _test(speaker_aed, source_aed, expected_volume, exponent=2.0):
            self.failUnlessEqual(maths.angles_to_attenuation(speaker_aed, source_aed, exponent), expected_volume)

        _test([0.0, 0.0, 1.0], [0.0, 0.0, 1.0], 1.0) # same position
        _test([math.pi, 0.0, 1.0], [0.0, 0.0, 1.0], 0.0) # opposite

        expect = math.cos(math.pi/2.0) * 0.5 + 0.5
        _test([math.pi / 2.0, 0.0, 1.0], [0.0, 0.0, 1.0], expect, 1.0) # one quarter

