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
Classes representing spatosc nodes and the scene
"""
class Node(object):
    """
    Abstract Node.
    """
    def __init__(self, node_id):
        self._id = node_id
        self._position = [0.0, 0.0, 0.0]
        self._properties = {
            int: {},
            float: {},
            str: {}
        }
        self._is_active = True

    def set_is_active(self, is_active):
        self._is_active = is_active

    def get_is_active(self):
        return self._is_active

    def get_id(self):
        return self._id

    def set_position(self, x, y, z):
        self._position = [x, y, z]

    def get_position(self):
        return self._position

    def set_property(self, property_type, key, value):
        if self._properties.has_key(property_type):
            self._properties[property_type][key] = value

    def get_property(self, property_type, key, value):
        if self._properties.has_key(property_type):
            if self._properties[property_type].has_key(key):
                return self._properties[property_type][key]
            else:
                print("No %s property %s" % (property_type, key))
                return None
        else:
            print("No %s properties" % (property_type))
            return None

class SoundSource(Node):
    """
    SoundSource node.
    """
    def __init__(self):
        self._uri = None
        self._connect_to = []

    def set_uri(self, uri):
        self._uri = uri

    def get_uri(self):
        return self._uri

    def add_connection_to(self, node):
        if node not in self._connect_to:
            self._connect_to.append(node)

    def remove_connection_to(self, node):
        if node in self._connect_to:
            self._connect_to.remove(node)

class Listener(Node):
    """
    Listener node.
    """
    def __init__(self):
        self._connect_from = []

    def add_connection_from(self, node):
        if node not in self._connect_from:
            self._connect_from.append(node)

    def remove_connection_from(self, node):
        if node in self._connect_from:
            self._connect_from.remove(node)

class Connection(object):
    """
    Connection between two nodes.
    """
    def __init__(self, source, sink):
        self._source = source
        self._sink = sink

    def get_source(self):
        return self._source
    
    def get_sink(self):
        return self._sink

class Scene(object):
    """
    SpatOSC scene
    """
    def __init__(self):
        self._sources = {}
        self._connections = []
        self._listeners = {}
    
    def delete_all_nodes(self):
        self._sources = {}
        self._connections = []
        self._listeners = {}

    def get_listener(self, identifier):
        if self._listeners.has_key(identifier):
            return self._listeners[identifier]
        else:
            return None

    def get_sound_source(self, identifier):
        if self._sources.has_key(identifier):
            return self._sources[identifier]
        else:
            return None

    def get_connection(self, source_id, sink_id):
        for conn in self._connections:
            src = conn.get_source()
            sink = conn.get_sink()
            if src.get_id() == source_id and sink.get_id() == sink_id:
                return conn
        return None

    def create_listener(self, identifier):
        if self.get_listener(identifier) is None:
            node = Listener(identifier)
            self._listeners[identifier] =node
            return True
        else:
            return False

    def create_sound_source(self, identifier):
        if self.get_sound_source(identifier) is None:
            node = SoundSource(identifier)
            self._sources[identifier] =node
            return True
        else:
            return False

    def connect(self, source_id, sink_id):
        src = self.get_sound_source(source_id)
        sink = self.get_listener(sink_id)
        if src is None:
            print("No such SoundSource: %s" % (source_id))
            return False
        if sink is None:
            print("No such Listener: %s" % (sink_id))
            return False
        conn = self.get_connection(source_id, sink_id)
        if conn is not None:
            print("Already connection: %s and %s" % (source_id, sink_id))
            return False
        self._connections.append(Connection(source_id, sink_id))

    def delete_node(self, node_id):
        node = self.get_listener(node_id)
        if node is not None:
            del self._sources[node_id]
            for conn in self._connections:
                if conn.get_sink().get_id() == node_id:
                    self._connection.remove(conn)

        node = self.get_sound_source(node_id)
        if node is not None:
            del self._sources[node_id]
            for conn in self._connections:
                if conn.get_source().get_id() == node_id:
                    self._connection.remove(conn)

