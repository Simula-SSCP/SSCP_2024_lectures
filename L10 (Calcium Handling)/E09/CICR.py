import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.integrate

from array import array
from pylab import *
from scipy.integrate.odepack import odeint

from scipy.integrate import odeint
from math import exp, log, sqrt, pi
from ipywidgets import interact, IntSlider, FloatSlider


class CICR_Widget ():

  def solve_and_plot(self, gamma, k_1, k_2, k_31, k_4):
    #initial conditions
    y0 = [0.0795,4.1725];
    time = np.linspace(0.0,1000.0, num = 1000)
    self.gamma = gamma
    self.k_1 = k_1
    self.k_2 = k_2
    self.k_31 = k_31
    self.k_4 = k_4

    #ode function call
    y = scipy.integrate.odeint(self.CICR, y0, time);

    plt.subplot(2,1,1); plt.plot(time,y[:,0]); plt.title('c'); plt.axis([0, 1000, 0, 1])
    plt.subplot(2,1,2); plt.plot(time,y[:,1]); plt.title('cSR'); plt.axis([0, 1000, 0, 10])
    plt.show()


  def display(self):
    widget = interact(self.solve_and_plot,
            gamma = FloatSlider(value = 4.17, min = 0, max = 10, step= 0.5),
            k_1 = FloatSlider(value = 2*10**(-5), min = 0, max = 2*10**(-5) * 2, step= 10**(-5)),
            k_2 = FloatSlider(value = 0.13, min = 0.05, max = 0.13*2, step= 0.02),
            k_4 = FloatSlider(value = 0.9, min = 0, max = 0.9*2, step= 0.2),
            k_31 = FloatSlider(value = 1, min = 0, max = 2, step= 0.2))


  def CICR(self, y, t):
    #constants
    # k_1 = 2*10**(-5);
    # k_2 = 0.13;
    # k_4 = 0.9;
    kappa_1 = 0.013;
    kappa_2 = 0.58;
    K_d = 0.5;
    n = 3;
    #gamma = 4.17;
    c0 = 1000;

    #input
    c = y[0];
    cSR = y[1];

    #calculation of k_3
    k_3 = self.k_31 *(kappa_1 + (kappa_2*c**n)/(K_d**n+c**n))

    #calcium entry
    J_L1 = self.k_1 * (c0 - c)

    #calcium extrusion
    J_P1 = self.k_2 * c;

    #calcium release
    J_L2  = k_3 *(cSR - c);

    #calcium uptake
    J_P2 = self.k_4 *c;

    #caculate time dependent functions
    ydot = [(J_L1-J_P1+J_L2-J_P2) , self.gamma*(-J_L2+J_P2)]; #dc #dcSR

    return ydot
