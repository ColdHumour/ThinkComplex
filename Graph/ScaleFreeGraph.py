# -*- coding: utf-8 -*-

import string
import random
import math
from collections import deque, Counter

from Graph import *


class ScaleFreeGraph(Graph):
    def get_random_candidate(self):
        """Get a random candidate vertex to connect. Based on following
        formula: P(v_i) = k_i / sum(k_i), where k_i is the number of 
        connections of vertex i.
        """

        vdicts, cdf, s = {}, [0], 0
        for i,v in enumerate(self._vertices):
            vdicts[i] = v
            x = len(self[v])
            cdf += [cdf[-1] + x]
            s += x
        p = random.uniform(0, 1) * s
        for i,n in enumerate(cdf[:-1]):
            if n <= p < cdf[i+1]:
                return vdicts[i]

    def get_probability_distribution(self, loglog=True):
        pdf, s = Counter(), 0
        for v in iter(self._vertices):
            x = len(self[v])
            s += x
            pdf[x] += 1
        out = []
        for k,n in pdf.iteritems():
            if n < 3: 
                continue

            if loglog:
                out.append((math.log(k), math.log(1.* n / s)))
            else:
                out.append(k, 1.* n / s)
        return sorted(out)

    def add_gp_edges(self, n):
        """Make a scale free graph with given amount of vertices based
        on an edgeless Graph. Following two rules:

        Growth: start with a small graph and add vertices gradually.
        Preferential attachment: When a new edge is created, it is more
        likely to connect to a vertex that already has a large number 
        of edges.
        """

        n0 = len(self._vertices)

        if n <= n0:
            raise ValueError("Target scale must larger than current!")

        for _ in xrange(n-n0):
            v = self.get_random_candidate()
            new_v = Vertex('a')
            self.add_vertex(new_v)
            self.add_edge(Edge(v, new_v))

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