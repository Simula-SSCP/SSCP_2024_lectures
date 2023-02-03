"""
Implements widgets that are used in the L11 notebook. Each widget is
implemented as a class that can be imported. To use a widget, create
an object of the class in question and call its display method.

Example:
========
from L11_widgets import ReactionWidget
ReactionWidget().display()
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from ipywidgets import interact, IntSlider, FloatSlider


class ReactionWidget():
    """A widget solving the simplified Razumova Model."""
    
    def rhs(self, y, t, R_T, k_on, k_off, f, f_prime,  h, h_prime, g):
        D, A_1, A_2 = y
        dD_dt = k_on*(R_T - D - A_1 - A_2)+f_prime*A_1+g*A_2-(k_off+f)*D
        dA1_dt = f*D+h_prime*A_2-(f_prime+h)*A_1
        dA2_dt = h*A_1-(h_prime+g)*A_2
        return [dD_dt, dA1_dt, dA2_dt]

    def solve_and_plot(self, k_on, f, h, g):
        self.k_on = k_on
        self.f = f
        self.h = h
        self.g = g
        R_T = 1;
        k_off = 50;
        f_prime = 400;
        h_prime = 6;
        time = np.linspace(0, 10, 5000)
        params = (R_T, k_on, k_off, f, f_prime,  h, h_prime, g)
        initial_condition = (0, 0, 0)
        solutions = odeint(self.rhs, initial_condition, time, params)
        D, A_1, A_2 = np.hsplit(solutions, 3)
        
        
        plt.plot(time, D, label=r'D')
        plt.plot(time, A_1, label=r'A$_1$')
        plt.plot(time, A_2, label=r'A$_2$')
        plt.axis((0, 5, 0, 1))
        plt.xlabel('Time')
        plt.ylabel('Probability of State Occupation')
        plt.legend()
        plt.show()
    
        #Timecourse of force development at constant [Ca2+]

        plt.plot(time, A_2, label=r'Relative Force')

        # plot
        plt.xlabel('Time')
        plt.ylabel('Relative Force')
        plt.legend()
        plt.xlim(0,1)

        plt.show()

        #calculate k_dev
        f_max = A_2[len(A_2)-1]
        f_half = (1-(1/np.exp(1)))*f_max
        index = 0
        while A_2[index] < f_half:
            index+=1
        t_half = time[index]
        ktr = 1 / t_half
        print("k_dev = ",ktr, " 1/sec")

    def display(self):
        widget = interact(self.solve_and_plot,
                          k_on = FloatSlider(value=400, min=100, max=500, step=2),
                          f = FloatSlider(value=50, min=0, max=500, step=5),
                          h = FloatSlider(value=8, min=0, max=15, step=0.1),
                          g = FloatSlider(value=4, min=0, max=10, step=0.1))


if __name__ == '__main__':
    ReactionWidget().display()
