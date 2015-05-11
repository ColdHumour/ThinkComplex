# -*- coding: utf-8 -*-

import string
import random
from collections import deque

from Graph import *


class SmallWorld(Graph):
    def add_ring_lattice_edges(self, d):
        """Make a regular ring lattice graph with given degree based
        on an edgeless Graph.

        A ring lattice graph is a regular graph which is obtained by 
        connecting each vertex to its closest neighbours. The degree 
        must be even. 
        """

        if self._edges:
            raise ValueError("Only edgeless Graph can call this method!")

        if d % 2:
            raise ValueError("Only even degree is allowed!")

        vlist = self.vertices()
        for i,v in enumerate(vlist[:-1]):
            to_connect = range(i-d/2, i) + range(i+1, i+d/2+1)
            for j in to_connect:
                w = vlist[j % len(vlist)]
                if w not in self[v]:
                    self.add_edge(Edge(v, w))
        self._ring_vertices = vlist

    def rewire(self, p):
        """
        With probability p, reconnect edge to a vertex chosen uniformly
        at random over the entire ring, with duplicate edges forbidden. 

        Repeat this process by moving clockwise around the ring lap by 
        lap, from nearest neighbours to second-nearest neighbours, etc.
        
        As there are nk/2 edges in the entire graph, the rewiring
        process stops after k/2 laps.
        """

        vlist = self._ring_vertices
        d = len(self[vlist[0]])

        for k in range(d/2):
            for i,v in enumerate(vlist):
                if random.uniform(0, 1) <= p:
                    w = vlist[i-k]
                    self.remove_edge(Edge(v, w))
                    while 1:
                        w = random.choice(vlist)
                        if w is not v: break
                    self.add_edge(Edge(v, w))

    def clustering_coefficient(self):
        """
        The clustering coefficient C is defined as follows. Suppose that
        a vertex v has k connected neighbours; then at most k(k-1)/2 edges
        can exist between them. Let Cv denote the fraction of these 
        allowable edges that actually exist. Define C as the average of 
        Cv over all v.
        """

        vlist, dens = self.vertices(), {}
        for v in vlist:
            neighbours, k, cv = self[v].keys(), len(self[v]), 0
            for w in self[v]:
                cv += sum(x in neighbours for x in self[w])
            cv = 1. * (cv + k) / k / (k - 1) if k > 1 else 1.
            dens[v] = cv
        return sum(dens.itervalues()) / len(dens)

    def characteristic_path_length(self):
        """
        The characteristic path length L is defined as the number of edges
        in the shortest path between two vertices, averaged over all pairs 
        of vertices.
        """

        n = len(self._vertices)
        dist = {v: dict.fromkeys(self._vertices, n*n) for v in self._vertices}
        for v, w in self._edges:
            dist[v][w] = dist[w][v] = 1

        for v in self._vertices:
            dist[v][v] = 0
            visited, to_search = {v,}.union(self[v]), deque(self[v])
            while to_search:
                w = to_search.popleft()
                for x in self[w]:
                    if x not in visited:
                        visited.add(x)
                        to_search.append(x)
                        dist[v][x] = dist[x][v] = min(dist[v][x], dist[v][w] + 1)
        pl = sum(sum(dm.itervalues()) for _,dm in dist.iteritems())
        return 1. * pl / n / (n-1)


if __name__ == '__main__':
    pass