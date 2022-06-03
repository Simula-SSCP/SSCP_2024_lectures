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


class CICRWidget:
    Cao = 1000
    gamma = 0.24

    k_entry = 2e-5 # 1/s
    k_extrusion = 0.132 # 1/s
    k_uptake = 0.9 # 1/s

    kappa0 = 0.054 # 1/s
    kappa1 = 2.4 # 1/s
    Kd = 0.23 # µM
    n = 3.8


    def rhs(self, t, y, Cao, k_entry, k_extrusion, k_uptake, kappa0, kappa1, Kd, n, gamma):
        # Split up the state vector
        Cai, CaSR = y    
        
        # Define the linear fluxes
        Jentry = k_entry * (Cao - Cai)
        Jextrusion = k_extrusion * Cai
        Juptake = k_uptake * Cai
        
        # Compute the release rate (CICR)
        k_rel = kappa0 + kappa1 * Cai**n/(Cai**n + Kd**n)
        Jrel = k_rel * (CaSR - Cai)
        
        # Define the derivatives
        dCai_dt = Jentry + Jrel - Jextrusion - Juptake
        dCaSR_dt = (Juptake - Jrel)/gamma
        
        # Return RHS vector
        return dCai_dt, dCaSR_dt
    
    def krel_widget(self):
        def solve_and_plot(kappa0, kappa1, Kd, n):
            Cai = np.linspace(0, 1, 1001)
            k_rel = kappa0 + kappa1 * Cai**n/(Cai**n + Kd**n)

            plt.plot(Cai, k_rel)
            plt.xlabel('Cyt. calcium (µM)')
            plt.ylabel('Release rate (1/s)')
            plt.axis((0, 1, 0, 1))
            plt.show()

        widget = interact(solve_and_plot,
                          kappa0 = FloatSlider(value=0.1, min=0, max=1.0, step=0.1),
                          kappa1 = FloatSlider(value=0.6, min=0.0, max=1.0, step=0.1),
                          Kd = FloatSlider(value=0.5, min=0.2, max=0.8, step=0.1),
                          n = FloatSlider(value=1, min=2.8, max=3.8, step=0.1))


    def Kd_widget(self, Kd, n):
        y0 = (0.0795, 4.1725)
        T = (0, 400)

        solution = solve_ivp(self.rhs, T, y0, args=self.parameters, max_step=0.1)

        Cai, CaSR = solution.y
        t = solution.t

        plt.subplot(2, 1, 1)
        plt.plot(t, Cai)
        plt.ylabel('Cyt. calcium (µM)')
        plt.xlim(*T)
        plt.ylim(0, 1)

        plt.subplot(2, 1, 2)
        plt.plot(t, CaSR)
        plt.xlabel('Time (ms)')
        plt.ylabel('SR Calcium (µM)')
        plt.xlim(*T)
        plt.ylim(0, 10)
        plt.show()

    @property
    def parameters(self):
        params = (self.Cao, self.k_entry, self.k_extrusion, self.k_uptake, 
                  self.kappa0, self.kappa1, self.Kd, self.n, self.gamma)
    




class CICR_Widget ():




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
