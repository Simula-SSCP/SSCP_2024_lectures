"""
Implements widgets that are used in the L3 notebook. Each widget is 
implemented as a class that can be imported. To use a widget, create
an object of the class in question and call its display method.

Example:
========
from L3_widgets import VoltageClampWidget
VoltageClampWidget().display()
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from ipywidgets import interact, IntSlider, FloatSlider


class VoltageClampWidget:
    """A widget solving the simple voltage clamp circuit with a step change.
    Used for Exercise 1 of E3.
    """
    Cm = 0.05 # nF
    Rs = 10 # MOhm

    def V_target(self, t):
        return (t > 2)*(t < 6)*40 - 80

    def I_app(self, t, V):
        return (V - self.V_target(t))/self.Rs

    def I_cap(self, t, V):
        return -self.I_app(t, V)

    def dV_dt(self, t, V):
        return -self.I_app(t, V)/self.Cm

    def solve_and_plot(self, Cm, Rs):
        self.Cm = Cm
        self.Rs = Rs
        T = (0, 10)
        t = np.linspace(0, 10, 101)
        V0 = (-80,)
        solution = solve_ivp(self.dV_dt, T, V0, t_eval=t, max_step=0.01)
        
        t = solution.t
        V, = solution.y

        f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        # Potential Plot
        ax1.plot(t, V, label='Actual')
        ax1.step(t, self.V_target(t), label='Target')
        ax1.set_ylabel('Mem. Potential [mV]')
        ax1.axis((0, 10, -85, -35))
        ax1.legend()

        # I_cap plot
        ax2.plot(t, self.I_cap(t, V))
        ax2.set_ylabel('Cap. current')
        ax2.set_xlabel('Time [ms]')
        ax2.axis((0, 10, -5, 5))
        plt.show()
        
    def display(self):
        widget = interact(self.solve_and_plot,
                          Cm = FloatSlider(value=0.05, min=0.005, max=0.1, step=0.005),  
                          Rs = IntSlider(value=10, min=5, max=20, step=1))


class MembraneWidget():
    """A widget that finds the equilibrium potential at different conductances.

    Used for exercise 3 of E3.
    """
    Cm = 0.05
    g_Na = 0.005
    g_Ca = 0.002
    g_K = 0.02
    E_Na = 70
    E_K = -86
    E_Ca = 114

    def dV_dt(self, t, V):
        g_Na, g_Ca, g_K = self.g_Na, self.g_Ca, self.g_K
        E_Na, E_Ca, E_K = self.E_Na, self.E_Ca, self.E_K
        return -(g_Na*(V-E_Na) + g_K*(V - E_K) + g_Ca*(V - E_Ca))/self.Cm

    def solve_and_plot(self, g_Na, g_Ca, g_K):
        self.g_Na = g_Na*1e-3
        self.g_Ca = g_Ca*1e-3
        self.g_K = g_K*1e-3

        T = (0, 20)
        V0 = (0,)
        solution = solve_ivp(self.dV_dt, T, V0, max_step=0.5)
        
        t = solution.t
        V, = solution.y

        plt.plot(t, V, linewidth=2.0)
        plt.title(f"Potential after 20 ms: {V[-1]:.1f} mV")
        plt.axhline(114, alpha=0.5, color='black', linestyle='--')
        plt.axhline(70, alpha=0.5, color='black', linestyle='--')
        plt.axhline(-86, alpha=0.5, color='black', linestyle='--')
        plt.xlabel('Time [ms]')
        plt.ylabel('Mem. Potential [mV]')
        plt.axis((0., 20, -90, 120))
        plt.xticks(range(0, 25, 5))
        plt.show()

    def display(self):
        widget = interact(self.solve_and_plot,
                          g_Na = IntSlider(value=5, min=0, max=30, step=1),
                          g_Ca = IntSlider(value=5, min=0, max=30, step=1),
                          g_K  = IntSlider(value=5, min=0, max=30, step=1))


if __name__ == '__main__':
   VoltageClampWidget().display()
   MembraneWidget().display()