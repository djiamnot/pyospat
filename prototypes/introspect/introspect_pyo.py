#!/usr/bin/env python
"""
Prototype of PyoObjects introspection.
"""

import pyo
import sys

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

def check_set_instance_properties():
    o = pyo.Noise()
    success = set_instance_property(o, "add", 0.5)
    if not success:
        return False
    success = set_instance_property(o, "dummy", 0.5)
    if success:
        print("There should be not property called dummy.")
        return False
    success = set_instance_property(o, "add", "hello")
    if success:
        print("Should not be able to set a float property with a string.")
        return False
    return True

if __name__ == "__main__":
    VERBOSE = True
    server = pyo.Server(nchnls=0, audio="offline")
    server.boot()
    if not check_set_instance_properties():
        sys.exit(1)
    print("SUCCESS")
    sys.exit(0)

