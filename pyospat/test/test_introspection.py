#!/usr/bin/env python
"""
Test PyoObjects introspection.
"""

from twisted.trial import unittest
from pyospat import introspection as intro
import sys
import pyo

intro.VERBOSE = True

class Test_Introspection(unittest.TestCase):
    _server = None
    def setUp(self):
        if Test_Introspection._server is None:
            Test_Introspection._server = pyo.Server(nchnls=0, audio="offline")
            Test_Introspection._server.boot()
        
    def test_set_instance_properties(self):
        o = pyo.Noise()
        success = intro.set_instance_property(o, "add", 0.5)
        if not success:
            return False
        success = intro.set_instance_property(o, "dummy", 0.5)
        if success:
            print("There should be not property called dummy.")
            return False
        success = intro.set_instance_property(o, "add", "hello")
        if success:
            print("Should not be able to set a float property with a string.")
            return False
        return True

