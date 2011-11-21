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
    if has_class(name):
        return pyo.__dict__[name]
    else:
        raise RuntimeError("Could not find class pyo.%s" % (name))

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

def set_instance_property(instance, name, value):
    """
    @rtype: bool
    @return: success
    value type can be float, str, int, etc.
    """
    props = get_instance_properties(instance)
    if props.has_key(name):
        prop_type = props[name]
        if type(value) == prop_type:
            instance.__setattr__(name, value)
            return True
        else:
            try:
                instance.__setattr__(name, prop_type(value))
                return True
            except ValueError, e:
                if VERBOSE:
                    print("pyo.%s.%s is not a %s: %s" % (instance.__class__.__name__, name, type(value).__name__, e))
                return False
    else:
        if VERBOSE:
            print("pyo.%s does not have property %s." % (instance.__class__.__name__, name))
        return False
