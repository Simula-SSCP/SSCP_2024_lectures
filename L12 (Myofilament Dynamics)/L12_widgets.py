"""
Implements widgets that are used in the L11 notebook. Each widget is
implemented as a class that can be imported. To use a widget, create
an object of the class in question and call its display method.

Example:
========
from L11_widgets import ReactionWidget
ReactionWidget().display()
"""

# Size of variable arrays:
sizeAlgebraic = 13
sizeStates = 3
sizeConstants = 19

#import necessary libraries
from math import *
from numpy import *
import pylab
from scipy.integrate import ode
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider, FloatSlider

class ReactionWidget():
    """A widget solving the simplified Razumova Model."""



    def solve_and_plot(self, u, v, w):
        def computeRates(voi, states, constants):
            rates = [0.0] * sizeStates; algebraic = [0.0] * sizeAlgebraic
            #Here we are considering D = states[0],A1 = states[1], and A2 = states[2]
            rates[2] = h*states[1]-(h_prime+g)*states[2]
            lambda_A_2 = states[2]/R_T
            f = f_0*(power(1.00000+lambda_A_2*(exp(v-1.00000)-1.00000), 2.00000))
            f_prime = f_prime_0*(power(1.00000+lambda_A_2*(exp(-(v-1.00000))-1.00000), 2.00000))
            rates[1] = (f*states[0]+h_prime*states[2])-(f_prime+h)*states[1]
            R_off = R_T-(states[0]+states[1]+states[2])
            lambda_on = (states[0]+states[1]+states[2])/R_T
            k_w_on = k_u_on*(power(1.00000+lambda_on*(u-1.00000), 2.00000))
            k_on = k_w_on*(power(1.00000+lambda_A_2*(exp(w-1.00000)-1.00000), 2.00000))
            k_w_off = k_u_off*(power(u-lambda_on*(u-1.00000), 2.00000))
            k_off = k_w_off*(power(1.00000+lambda_A_2*(exp(-(w-1.00000))-1.00000), 2.00000))
            rates[0] = (k_on*R_off+f_prime*states[1]+g*states[2])-(k_off+f)*states[0]
            return(rates)
        self.u = u
        self.v = v
        self.w = w
        print(v)
        init_states = [0.0] * sizeStates;
        R_T = 1
        D_0 = 0.01
        A1_0 = 0.01
        A2_0 = 0.01
        k_0_on = 0
        k_0_off = 100.
        k_Ca_on = 120.
        k_Ca_off = 50
        f_0 = 50
        f_prime_0 = 400
        h = 8
        h_prime = 6
        F = 1
        g = 4
        n_H = 1
        Ca_50 = k_Ca_off/k_Ca_on
        init_states = [D_0,A1_0,A2_0]
        calConc = [0.01,0.02,  0.1,0.2,  1,2, 10,20, 100]
        SS_force = [0.0] * len(calConc)
        log_Cal = [0.0] * len(calConc)
        index = 0
        
        time = linspace(0, 10, 500)
        
        while index<len(calConc):
            Ca = Ca_50*calConc[index]
            k_u_on = round(k_0_on+((k_Ca_on-k_0_on)*Ca)/(Ca_50+Ca),2)
            k_u_off = k_0_off+((k_Ca_off-k_0_off)*Ca)/(Ca_50+Ca)
            constants = [R_T, k_0_on, k_0_off, k_Ca_on, k_Ca_off, f_0, f_prime_0,  h, h_prime, g, n_H, u, w, v, Ca_50, Ca, F, k_u_on, k_u_off]
            
            
            # Construct ODE object to solve
            r = ode(computeRates)
            r.set_integrator('vode', method='bdf', atol=1e-06, rtol=1e-06, max_step=1)
            r.set_initial_value(init_states, time[0])
            r.set_f_params(constants)

            # Solve model
            states = array([[0.0] * len(time)] * sizeStates)
            states[:,0] = init_states
            for (i,t) in enumerate(time[1:]):
                if r.successful():
                    r.integrate(t)
                    states[:,i+1] = r.y
                else:
                    break
        
            D, A_1, A_2 = hsplit(transpose(states), 3)
            SS_force[index] = A_2[len(A_2)-1]
            log_Cal[index] = log(calConc[index])
            index+=1
    
    
    
        plt.plot(log_Cal, SS_force, label=r'Steady State Force-pCa curve')
        plt.xlabel('log(Ca/Ca_50)')
        plt.ylabel('Force')
        plt.legend()
        plt.show()
        #Timecourse of force development at Highest [Ca2+]

        plt.plot(time, A_2, label=r'Relative Force')

        # plot
        plt.xlabel('Time')
        plt.ylabel('Relative Force')
        plt.legend()
        plt.xlim(0,1)

        plt.show()

    def display(self):
        widget = interact(self.solve_and_plot,
                          u = FloatSlider(value=1, min=1, max=3, step=0.1),
                          v = FloatSlider(value=1, min=1, max=3, step=0.1),
                          w = FloatSlider(value=1, min=1, max=3, step=0.1))


if __name__ == '__main__':
    ReactionWidget().display()
