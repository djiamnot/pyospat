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
PyoObjects introspection.
"""

import pyo
from pyospat import logger
#from pyospat import plugins

log = logger.start(name="introspection")

"""
Module-wide global variable.
"""
VERBOSE = False

def has_class(name):
    """
    @rtype: bool
    """
    if pyo.__dict__.has_key(name):
        klass = pyo.__dict__[name]
        return issubclass(klass, pyo.PyoObject)
    else:
        return False

def get_class(name):
    """
    @rtype: pyo object
    """
    try:
        m = getattr(pyo, name)
        return m
    except AttributeError, err:
        print err

# def get_plugin_class(name):
#     """
#     @rtype: pyo object
#     """
#     try:
#         m = getattr(plugins, name)
#         return m
#     except AttributeError, err:
#         print err

def get_instance_properties(instance):
    """
    Returns a dict[name] = type
    Also contains methods and the like.
    @rtype: dict
    """
    ret = {}
    for name in dir(instance):
        ret[name] = type(instance.__getattribute__(name))
    return ret
    
def instance_has_property(instance, property_name):
    """
    @rtype: bool
    """
    props = get_instance_properties(instance)
    return props.has_key(property_name)

def class_has_property(klass, property_name):
    """
    Will check for a property key in a class that has not been instantiated yet.
    @rtype: bool
    """
    return klass.__dict__.has_key(property_name)
    

# def set_instance_property(instance, name, value):
#     """
#     @rtype: bool
#     @return: success
#     value type can be float, str, int, etc.
#     """
#     props = get_instance_properties(instance)
#     if props.has_key(name):
#         prop_type = props[name]
#         if type(value) == prop_type:
#             instance.__setattr__(name, value)
#             return True
#         else:
#             try:
#                 instance.__setattr__(name, prop_type(value))
#                 return True
#             except ValueError, e:
#                 if VERBOSE:
#                     print("pyo.%s.%s is not a %s: %s" % (instance.__class__.__name__, name, type(value).__name__, e))
#                 return False
#     else:
#         if VERBOSE:
#             print("pyo.%s does not have property %s." % (instance.__class__.__name__, name))
#         return False

# FIXME: handle the types properly. The problem here is that pyo
# reports some propties as being <int> but should be floats. This should be fixed
# upstream but a proper bug report needs to be prepared.i
def set_instance_property(instance, name, value):
    """
    @rtype: bool
    @return: success
    value type can be float, str, int, etc.
    """
    props = get_instance_properties(instance)
    try:
        instance.__setattr__(name, value)
        return True
    except ValueError, e:
        if VERBOSE:
            log.info("pyo.%s.%s is not a %s: %s" % (instance.__class__.__name__, name, value.__name__, e))
            return False
    else:
        if VERBOSE:
            log.info("pyo.%s does not have property %s." % (instance.__class__.__name__, name))
        return False

