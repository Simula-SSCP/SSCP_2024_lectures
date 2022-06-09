import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from ipywidgets import interact, IntSlider, FloatSlider


class CICRWidget:
    Cao = 1000 # µM

    k_entry = 2e-5 # 1/s
    k_extrusion = 0.132 # 1/s
    k_uptake = 0.9 # 1/s
    
    kappa0 = 0.013 # 1/s
    kappa1 = 0.58 # 1/s
    Kd = 0.5 # µM
    n = 3.
    gamma = 0.24
    
    @property
    def parameters(self):
        return (self.Cao, self.k_entry, self.k_extrusion, self.k_uptake, 
                self.kappa0, self.kappa1, self.Kd, self.n, self.gamma)

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
        
        return dCai_dt, dCaSR_dt
    
    def initial_conditions_widget(self):
        def solve_and_plot(Cai_0, CaSR_0):
            y0 = Cai_0, CaSR_0
            T = (0, 800)

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

        widget = interact(solve_and_plot,
                          Cai_0 = FloatSlider(value=0.1, min=0, max=1.0, step=0.1, continuous_update=False),
                          CaSR_0 = FloatSlider(value=4.0, min=0.0, max=8.0, step=0.25, continuous_update=False))



    def krel_widget(self):
        def solve_and_plot(kappa0, kappa1, Kd, n):
            Cai = np.linspace(0, 1, 1001)
            k_rel = kappa0 + kappa1 * Cai**n/(Cai**n + Kd**n)

            plt.plot(Cai, k_rel)
            plt.xlabel('Cyt. calcium (µM)')
            plt.ylabel('Release rate (1/s)')
            plt.axis((0, 1, 0, 2))
            plt.show()

        widget = interact(solve_and_plot,
                          kappa0 = FloatSlider(value=0.1, min=0, max=1.0, step=0.1),
                          kappa1 = FloatSlider(value=0.6, min=0.0, max=1.0, step=0.1),
                          Kd = FloatSlider(value=0.5, min=0.2, max=0.8, step=0.1),
                          n = FloatSlider(value=1, min=2.8, max=3.8, step=0.1))


    def cicr_widget(self):
        def solve_and_plot(Kd, n):
            self.Kd = Kd
            self.n = n
            y0 = (0.080, 4.0)
            T = (0, 800)

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

        widget = interact(solve_and_plot,
                  n = FloatSlider(value=3.0, min=2.0, max=4.0, step=0.1),
                  Kd = FloatSlider(value=0.5, min=0.0, max=1.0, step=0.1))


