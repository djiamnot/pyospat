#!/usr/bin/env python
"""
Dummy tests
"""
from twisted.trial import unittest
from pyospat import application
from txosc import osc

class Test_Parsers(unittest.TestCase):
    def test_connection_id(self):
        m = osc.Message("/foo/bar/egg/spam")
        self.failUnlessEqual(application._get_connection_id(m), "egg")

    def test_node_id(self):
        m = osc.Message("/foo/bar/egg/spam")
        self.failUnlessEqual(application._get_connection_id(m), "egg")

    def test_type_tags_match(self):
        m = osc.Message("/foo", "hello", 123)
        self.failUnless(application._type_tags_match(m, "si"))

