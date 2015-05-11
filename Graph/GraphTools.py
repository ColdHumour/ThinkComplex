# -*- coding: utf-8 -*-

import string

from matplotlib import pylab

from Graph import *
from SmallWorld import *
from ScaleFreeGraph import *


def prob_connection(n, p, ntest=1):
    """Probability of connectivity of random graph G(n, p)

    @ntest: amount of tests
    """

    if n > 52: 
        raise ValueError("Too many vertices!")

    labels = string.ascii_lowercase + string.ascii_uppercase
    vs = [Vertex(c) for c in labels[:n]]
    
    count = 0
    for _ in range(ntest):
        g = Graph(vs)
        g.add_random_edges(p)
        count += g.is_connected()

    return 1. * count / ntest


def critical_prob(n, error_tolerence=0.001, ntest=100, nconn=0.95):
    """Critical probability p* of random graph G(n, p). 
    When p < p*，G(n, p) is rarely connected.
    When p >= p*, G(n, p) is almost always connected.

    @error_tolerence: precision of p*
    @ntest: amount of tests in each probability getting
    @nconn: prob. of connected which regarded as "always"
    """

    l, r = 0.001, 0.999
    while r - l > error_tolerence:
        m = (l + r) / 2
        p = prob_connection(n, m, ntest)
        if p >= nconn:
            r = m
        else:
            l = m
    return (l + r) / 2


def Watts_Strogatz_Phenomenon(n=1000, k=10):
    """Collective dynamics of 'small-world' networks
    by Watts, Strogatz

    @n: graph scale
    @k: initial degree
    """

    vs = [Vertex('a') for _ in range(n)]
    g = SmallWorld(vs)
    g.add_ring_lattice_edges(k)
    c0 = g.clustering_coefficient()
    l0 = g.characteristic_path_length()
    print 'prob.    clust_coeff   cp/c0   path_len    lp/l0'
    print '{0:<6.4f} {1:11.4f}    {2:6.4f}  {3:8.3f}    {4:6.4f}'.format(0.0, c0, 1.0, l0, 1.0)
    for p in [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 0.9]:
        c = 0.
        l = 0.
        t = 20
        for _ in range(t):
            g = SmallWorld(vs)
            g.add_ring_lattice_edges(10)
            g.rewire(p)
            c += g.clustering_coefficient()
            l += g.characteristic_path_length()
        c /= t
        l /= t    
        print '{0:<6.4f} {1:11.4f}    {2:6.4f}  {3:8.3f}    {4:6.4f}'.format(p, c, c/c0, l, l/l0)


def Barabasi_Albert_Phenomenon(n=1000, m=10, sw=False):
    """Collective dynamics of 'small-world' networks
    by Barabasi, Albert

    @n: graph scale
    @m: initial vertices
    @sw: whether to print out small-world parameters
    """

    vs = [Vertex('a') for _ in range(m)]
    g = ScaleFreeGraph(vs)
    g.add_random_edges(0.5)
    g.add_gp_edges(n)
    z = g.get_probability_distribution()
    x, y = zip(*z)
    pylab.plot(x, y, 'o')
    pylab.title(r'Power Law of Barabasi-Albert Graph at n={0:d}'.format(n))
    pylab.xlabel(r'log(k)')
    pylab.ylabel(r'log(P(k))')
    pylab.xlim([x[0]-0.1, x[-1]+0.1])
    pylab.ylim([y[-1]-0.1, y[0]+0.1])
    pylab.show()

    if sw:
        print 'Barabasi-Albert Graph at n={0:d}'.format(n)
        print 'clustering coefficient:    {0:.2f}'.format(g.clustering_coefficient())
        print 'average vertices distance: {0:.2f}'.format(g.characteristic_path_length())



if __name__ == '__main__':
    # print prob_connection(10, 0.5, 100)
    print critical_prob(10)
    # Watts_Strogatz_Phenomenon()
    # Barabasi_Albert_Phenomenon(5000, 10, 0)