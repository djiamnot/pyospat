#!/usr/bin/env python
"""
The Configuration class.
"""

class Configuration(object):
    """
    Configuration for the application.
    """
    def __init__(self):
        self.verbose = False
        self.osc_receive_port = 10001

