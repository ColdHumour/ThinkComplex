# -*- coding: utf-8 -*-

import numpy as np
import scipy.ndimage as sni
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as pyplot


class Life(object):
    def __init__(self, n, mode='wrap', random=False):
        """Attributes:
        n:      number of rows and columns
        mode:   how border conditions are handled
        array:  the numpy array that contains the data.
        weights: the kernel used for convolution
        """
        self.n = n
        self.mode = mode
        if random:
            self.array = np.random.random_integers(0, 1, (n, n))
        else:
            self.array = np.zeros((n, n), np.int8)
        self.weights = np.array([[1,1,1],
                                 [1,10,1],
                                 [1,1,1]])

    def step(self):
        con = sni.filters.convolve(self.array, self.weights,
                                   mode=self.mode)
        boolean = (con==3) | (con==12) | (con==13)
        self.array = np.int8(boolean)

    def add_glider(self, x=0, y=0):
        coords = [(0,1), (1,2), (2,0), (2,1), (2,2)]
        for i, j in coords:
            self.array[x+i, y+j] = 1

    def loop(self, steps=1):
        """Executes the given number of time steps."""
        [self.step() for _ in xrange(steps)]



class LifeViewer(object):
    def __init__(self, life, cmap=mpl.cm.gray_r):
        self.life = life
        self.cmap = cmap
        self.fig = pyplot.figure()
        pyplot.axis([0, life.n, 0, life.n])
        pyplot.xticks([])
        pyplot.yticks([])
        self.pcolor = None
        self.update()

    def update(self):
        if self.pcolor:
            self.pcolor.remove()
        
        a = self.life.array
        self.pcolor = pyplot.pcolor(a, cmap=self.cmap)
        self.fig.canvas.draw()

    def animate(self, steps=10):
        self.steps = steps
        self.fig.canvas.manager.window.after(1000, self.animate_callback)
        pyplot.show()
    
    def animate_callback(self):
        for _ in range(self.steps):
            self.life.step()
            self.update()



if __name__ == '__main__':
    n = 30

    life = Life(n, random=True)
    # life.add_glider()
    viewer = LifeViewer(life)
    viewer.animate(steps=500)