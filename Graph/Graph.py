# -*- coding: utf-8 -*-

import random
from collections import deque


class Vertex(object):
    """A Vertex is a node in a graph."""

    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        """Returns a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__
    """The str and repr forms of this object are the same."""


class Edge(tuple):
    """An Edge is a list of two vertices."""

    def __new__(cls, *vs):
        """The Edge constructor takes two vertices."""
        if len(vs) != 2:
            raise ValueError, 'Edges must connect exactly two vertices.'
        return tuple.__new__(cls, vs)

    def __repr__(self):
        """Return a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__
    """The str and repr forms of this object are the same."""


class Graph(dict):
    """A Graph is a dictionary of dictionaries.  The outer
    dictionary maps from a vertex to an inner dictionary.
    The inner dictionary maps from other vertices to edges.
    
    For vertices a and b, graph[a][b] maps
    to the edge that connects a->b, if it exists."""

    def __init__(self, vs=[], es=[]):
        """Creates a new graph.  
        vs: list of vertices;
        es: list of edges.
        """
        self._vertices = set([])
        for v in vs:
            self.add_vertex(v)
        
        self._edges = set([])    
        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        """Add a vertex to the graph."""
        self._vertices.add(v)
        self[v] = {}

    def add_edge(self, e):
        """Adds and edge to the graph by adding an entry in both directions.

        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """
        v, w = e
        self._edges.add(e)
        self[v][w] = e
        self[w][v] = e

    def get_edge(self, v, w):
        try:
            return self[v][w]
        except:
            return None

    def remove_edge(self, e):
        v, w = e
        if e in self._edges:
            self._edges.remove(e)
            del self[v][w]
            del self[w][v]
        elif Edge(w, v) in self._edges:
            self._edges.remove(Edge(w, v))
            del self[v][w]
            del self[w][v]
        else:
            pass

    def vertices(self):
        return list(self._vertices)

    def edges(self):
        return list(self._edges)

    def out_vertices(self, v):
        return self[v].keys()

    def out_edges(self, v):
        return self[v].values()

    def add_all_edges(self):
        """Make a complete graph based on an edgeless Graph."""

        if self._edges:
            raise ValueError("Only edgeless Graph can call this method!")

        vlist = self.vertices()
        for i,v in enumerate(vlist[:-1]):
            for w in vlist[i+1:]:
                self.add_edge(Edge(v, w))

    def add_regular_edges(self, d):
        """Make a regular graph with given degree based on an edgeless Graph."""

        if self._edges:
            raise ValueError("Only edgeless Graph can call this method!")

        if (len(self._vertices) * d) % 2:
            raise ValueError("Impossible degree of regular graph!")

        vlist = self.vertices()
        for i,v in enumerate(vlist[:-1]):
            for w in sorted(vlist[i+1:], key=lambda x: len(self[x])):
                if len(self[v]) < d and len(self[w]) < d:
                    self.add_edge(Edge(v, w))
                elif len(self[v]) >= d:
                    break

    def add_random_edges(self, p):
        """Make a random graph with given probability based on an edgeless Graph,
        which follows G(n, p) in http://en.wikipedia.org/wiki/Erdos-Renyi_model.
        """
        
        if self._edges:
            raise ValueError("Only edgeless Graph can call this method!")

        vlist = self.vertices()
        for i,v in enumerate(vlist[:-1]):
            for w in vlist[i+1:]:
                if random.uniform(0, 1) <= p:
                    self.add_edge(Edge(v, w))

    def is_regular(self):
        """Test whether self is a regular graph"""

        d = len(self[self.keys()[0]])
        for v in self._vertices:
            if len(self.out_vertices(v)) != d:
                return False
        return True

    def is_connected(self):
        """Test whether self is a connected graph"""
        
        v = self.vertices()[0]
        visited, to_search = {v,}, deque([v])
        while to_search:
            v = to_search.popleft()
            for w in self[v]:
                if w not in visited:
                    visited.add(w)
                    to_search.append(w)
        return len(visited) == len(self._vertices)
                

if __name__ == '__main__':
    v = Vertex('v')
    print v
    w = Vertex('w')
    print w
    e = Edge(v, w)
    print e
    g = Graph([v,w], [e])
    print g
    print g.vertices()