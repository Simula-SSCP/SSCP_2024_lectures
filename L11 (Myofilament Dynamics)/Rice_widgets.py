"""
Implements widgets that are used in the L11 notebook. Each widget is
implemented as a class that can be imported. To use a widget, create
an object of the class in question and call its display method.

Example:
========
from L11_widgets import ReactionWidget
ReactionWidget().display()
"""
import rice_model_2008 as rice
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from ipywidgets import interact, IntSlider, FloatSlider
import math

class Fig3AWidget():
    """A widget solving the Rice model to steady state, allowing an 
    version of Figure 3A from Rice et al (2008)."""
    def __init__(self):
        

        interact(self.solve_and_plot,
                          SL = FloatSlider(value=1.85, min=1.4, max=2.4, step=0.05),
                          Fmax = FloatSlider(value=0.17, min=0.17, max=0.92, step=0.05),
                          Ca50 = FloatSlider(value=3.0, min=0.87, max=3.0, step=0.05),
                          n = FloatSlider(value=7.6, min=3, max=10, step=0.5)


                     )

    
    def solve_and_plot(self, SL, Fmax, Ca50, n):
        """
        Solve the model to steady state for Ca values in [0,10], for a
        given value of SL, and plot the resulting F-Ca curve.
        """
        t = np.linspace(0,100,101)
        Cai = np.linspace(0,10,101)
        force_index = rice.monitor_indices("active")
        
        init = rice.init_state_values(SL=SL)
        Fss = np.empty_like(Cai)
        for i in range(len(Cai)):
            p = (rice.init_parameter_values(start_time=1000,Ca_diastolic=Cai[i],SLmin=2.5),)
            s = odeint(rice.rhs,init,t,p)
            m = rice.monitor(s[-1],t[-1],p[0])
            Fss[i] = m[force_index]

        plt.semilogx(Cai,Fss)
        plt.ylabel('Normalized force at steady state')
        plt.xlabel('Ca concentration')


        #plot one dynamic Hill curve
        Fh = Fmax*np.power(Cai,n)/(math.pow(Ca50,n)+np.power(Cai,n))
        plt.plot(Cai,Fh,':')
        
        #plot two Hill curves for the extreme SL values
        Fmax = 0.17
        Ca50 = 3.0
        n = 7.6
        Fh = Fmax*np.power(Cai,n)/(math.pow(Ca50,n)+np.power(Cai,n))
        plt.plot(Cai,Fh,'--')

        Fmax =0.92
        Ca50= 0.87
        Fh = Fmax*np.power(Cai,n)/(math.pow(Ca50,n)+np.power(Cai,n))
        plt.plot(Cai,Fh,'--')
        
        plt.show()


    def display(self):
        widget = interact(self.solve_and_plot,
                          SL = FloatSlider(value=1.85, min=1.4, max=2.4, step=0.05))



class Fig5Awidget():
    def __init__(self):
        interact(self.solve_and_plot,
                     SL = FloatSlider(value=1.85, min=1.4, max=2.4, step=0.05),
                     Ca_amplitude = FloatSlider(value=1.45, min=1.0, max=1.9, step=0.05),
                     tau1 = FloatSlider(value=20, min=10, max=30, step=1),
                     tau2 = FloatSlider(value=110, min=80, max=140, step=5),
                     kn_p = FloatSlider(value=0.5, min=0.25, max=1.0, step=0.05),
                     kp_n = FloatSlider(value=0.05, min=0.025, max=0.1, step=0.02),
                     f_app = FloatSlider(value=0.5, min=0.2, max=1.0, step=0.05),
                     g_app = FloatSlider(value=0.07, min=0.03, max=0.14, step=0.01),
                     h_f = FloatSlider(value=2.0, min=1.0, max=3.0, step=0.1),
                     h_b = FloatSlider(value=0.4, min=0.2, max=0.8, step=0.05),
                     gxb = FloatSlider(value=0.07, min=0.02, max=0.1, step=0.01))
                     
        
    def solve_and_plot(self,SL,Ca_amplitude,tau1,tau2,kn_p,kp_n,f_app,g_app,h_f,h_b,gxb):
        t = np.linspace(0,1000,101)
        
        p = rice.init_parameter_values(SLmin=2.5, Ca_amplitude=Ca_amplitude, tau1=tau1, tau2=tau2,
                                           kn_p=kn_p, kp_n=kp_n, fapp=f_app, gapp=g_app,
                                           hf=h_f,hb=h_b,gxb=gxb)
        force_ind = rice.monitor_indices("active")     
        ca_ind = rice.monitor_indices("Cai")     

        init = rice.init_state_values(SL=SL)
        s = odeint(rice.rhs,init,t,(p,))
        force = []
        cai = []
        for tn,sn in zip(t,s):
            m = rice.monitor(sn,tn,p)
            force.append(m[force_ind])
            cai.append(m[ca_ind])

        plt.figure(1)
        plt.plot(t,cai)

        plt.figure(2)
        plt.plot(t,force)
        plt.show()

        
#if __name__ == '__main__':
#    ReactionWidget().display()
