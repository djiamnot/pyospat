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

    def test_angle(self):
        self.failUnlessEqual(maths.angle([0.0, 1.0, 0.0], [1.0, 0.0, 0.0]), math.pi / 2.0)
        self.failUnlessEqual(maths.angle([0.0, 1.0, 0.0], [0.0, -1.0, 0.0]), math.pi)
        self.failUnlessEqual(maths.angle([0.0, 1.0, 0.0], [0.0, 1.0, 0.0]), 0.0)

    def test_dot_product(self):
        pass
    
    test_dot_product.skip = "to do"

