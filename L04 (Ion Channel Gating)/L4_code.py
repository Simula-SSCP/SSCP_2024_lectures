import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider, FloatSlider
from scipy.integrate import odeint

########################################################
####################   Exercise 1   #################### 
########################################################

class GatingWidget():
    """A widget solving the gating equation dm/dt = a*(1-m) -m*b."""

    def __init__(self):
        interact(self.solve_and_plot,
                 m0 = FloatSlider(value=0, min=0.0, max=1, step=0.1, continuous_update=False),  
                 a = FloatSlider(value=1, min=0.0, max=10, step=0.1, continuous_update=False),  
                 b = FloatSlider(value=1, min=0.0, max=10, step=0.1, continuous_update=False))
     
    def dm_dt(self, m, t):
        return self.a*(1-m) - self.b*m

    def solve_and_plot(self, m0, a, b):

        self.a = a
        self.b = b
        self.m0 = m0
        time = np.arange(0, 1, 0.01)
        m = odeint(self.dm_dt, self.m0, time)
        m = m[:, 0]

        plt.plot(time, m, time, 0*time + a/(a+b))
        plt.xlabel('Time [ms]')
        plt.legend((r'$m(t)$',r'$m_{\infty}$'));
        plt.ylim(0, 1)
        plt.show()

########################################################
####################   Exercise 2   #################### 
########################################################



def plot_voltage_dependence(Va0, da, Vb0, db):
    
    V = np.linspace(-100, 100, num=1000)
    a = np.exp((V-Va0)/da)
    b = np.exp((V-Vb0)/db)

    plt.rcParams["figure.figsize"] = (12,5)
    plt.rcParams["font.size"] = 16
    plt.subplot(1,3,1)
    plt.plot(V, a, V, b)
    plt.legend((r'$\alpha_m$',r'$\beta_m$'));
    plt.ylim(0, 5)
    plt.subplot(1,3,2)
    plt.plot(V, a/(a+b),'k')
    plt.title(r'$m_{\infty}$')
    plt.subplot(1,3,3)
    plt.plot(V, 1/(a+b),'k')
    plt.title(r'$\tau_m$')
    plt.show()


def voltage_dependence():    
    interact(plot_voltage_dependence,  Va0=(-100, 100), da=(1,100), Vb0=(-100, 100), db=(-100,-1))

########################################################
####################   Exercise 3   #################### 
########################################################


class ConstantConductancesWidget():
    """A widget solving the scalar ODE for voltage with constant conductances."""
    Cm = 0.05 # nF
    E_Na = 50;
    E_K = -80;
    #gNa = 0.8; # uS, 20pS/channel*40,000 channels pr cell.
    #gK = 0.2
    #I_amp = 1;

    def I_app(self, t):
        return -self.I_amp if t<1 else 0.0

    def I_Na(self, V):
        return self.gNa*(V - self.E_Na)

    def I_K(self, V):
        return self.gK*(V - self.E_K)

    def dV_dt(self, V, t):
        return (-self.I_app(t)-self.I_Na(V)-self.I_K(V))/self.Cm

    def solve_and_plot(self, V0, I_amp, gNa, gK):
        self.V0 = V0;
        self.I_amp = I_amp
        self.gNa = gNa
        self.gK = gK
        time = np.arange(0, 2, 0.01)

        V = odeint(self.dV_dt, V0, time)
        V = V[:, 0]
        # Potential Plot
        plt.plot(time, V, time, time*0 + self.E_Na, time, time*0 + self.E_K)
        plt.legend(['$V$','$E_{Na}$','$E_{K}$'], loc = "center right")
        plt.ylabel('Mem. Potential [mV]')
        plt.grid()
        plt.show()
        

    def __init__(self):
        interact(self.solve_and_plot,  I_amp = FloatSlider(value=1.0, min=0.0, max=10, step=0.1, continuous_update=False), V0 = FloatSlider(value=-60, min=-100.0, max=100, step=1, continuous_update=False),  gNa = FloatSlider(value=0, min=0, max=1, step=0.01, continuous_update=False),  gK = FloatSlider(value=0.2, min=0, max=1, step=0.01, continuous_update=False))

########################################################
####################   Exercise 4   #################### 
########################################################



        
class VoltageDependentConductancesWidget():
    """A widget solving the scalar ODE for voltage with constant conductances."""
    Cm = 0.05 # nF
    E_Na = 50;
    E_K = -80;
    gNa = 0.8; # uS, 20pS/channel*40,000 channels pr cell.
    gK = 0.1
    #I_amp = 1;

    def I_app(self, t):
        return -self.I_amp if t<1 else 0.0

    def m_rates(self, V):
        alpha = np.exp((V-self.Vs)/self.d)
        beta  = np.exp(-(V-self.Vs)/self.d)
        return alpha, beta
    
    def m_inf(self, V):
        alpha_m, beta_m = self.m_rates(V)
        return alpha_m/(alpha_m+beta_m)
    
    def I_Na(self, V):
        return self.gNa*self.m_inf(V)*(V - self.E_Na)

    def I_K(self, V):
        return self.gK*(V - self.E_K)

    def dV_dt(self, V, t):
        return (-self.I_app(t)-self.I_Na(V)-self.I_K(V))/self.Cm

    def solve_and_plot(self, V0, I_amp, Vs, d):
        self.V0 = V0;
        self.I_amp = I_amp
        self.Vs = Vs
        self.d = d
        time = np.arange(0, 10, 0.01)

        V = odeint(self.dV_dt, V0, time)
        V = V[:, 0]
        # Potential Plot
        plt.subplot(1,3,1)
        plt.plot(time, V, time, time*0 + self.E_Na, time, time*0 + self.E_K)
        plt.legend(['$V$','$E_{Na}$','$E_{K}$'], loc = "center right")
        plt.title(r'$V(t)$')
        V = np.linspace(-100, 100, num=1000)
        m_ss =  self.m_inf(V)
        plt.subplot(1,3,2)
        plt.plot(V, m_ss)
        plt.title(r'$m_{\infty}$')

        plt.subplot(1,3,3)
        I = -self.I_Na(V)-self.I_K(V)
        plt.plot(V, I)
        plt.title(r'$I(V) =  - I_{\rm Na}(V) - I_{\rm K}(V)$')
        plt.ylim(-10, 10)

        
        plt.grid()
        plt.show()
        

    def __init__(self):
        interact(self.solve_and_plot,
                     I_amp = FloatSlider(value=0.0, min=0.0, max=10, step=0.1, continuous_update=False),
                     V0 = FloatSlider(value=-80, min=-100.0, max=100, step=1, continuous_update=False),
                     Vs = FloatSlider(value=-20, min=-100, max=100, step=1, continuous_update=False),
                     d = FloatSlider(value=10, min=1, max=100, step=1, continuous_update=False))


    

########################################################
####################   Exercise 5   #################### 
########################################################

C_m = 0.05 # nF
E_Na = 50;
E_K = -80;
g_Na = 0.8; # uS, 20pS/channel*40,000 channels pr cell.
g_K = 0.1
I_amp = 0;
h0 = 0.5;
V0 = -50;

dm = 15
dh = -5
dam = dm
dah = dh;
dbm = -dm
dbh = -dh;


def I_app(t):
    return -I_amp if t<1 else 0.0

def m_rates(V):
    alpha = np.exp((V-Vam)/dam)
    beta  = np.exp((V-Vbm)/dbm)
    return alpha, beta

def h_rates(V):
    alpha = np.exp((V-Vah)/dah)
    beta  = np.exp((V-Vbh)/dbh)
    return alpha, beta

def m_inf(V):
    alpha_m, beta_m = m_rates(V)
    return alpha_m/(alpha_m+beta_m)

def h_inf(V):
    alpha_h, beta_h = h_rates(V)
    return alpha_h/(alpha_h+beta_h)

def m_tau(V):
    alpha_m, beta_m = m_rates(V)
    return 1/(alpha_m+beta_m)

def h_tau(V):
    alpha_h, beta_h = h_rates(V)
    return 1/(alpha_h+beta_h)

def I_Na(V, h):
    return g_Na*h*m_inf(V)*(V - E_Na)

def I_K(V):
    return g_K*(V - E_K)


def dY_dt(Y, t=0):

    V, h = Y
    d_V = (-I_Na(V, h)-I_K(V))/C_m
    alpha_h, beta_h = h_rates(V)
    d_h = alpha_h*(1-h) - h*beta_h;

    return [d_V, d_h]


def dVdt_scalar(V):

    h_ss = h_inf(V);
    dV_dt = dY_dt([V, h_ss], 0)[0]

    
    return dV_dt

def compute_steady_state(V_guess):

    from scipy.optimize import bisect, newton
    #V_ss = bisect(dVdt_scalar, E_K, E_Na);

    try:
        V_ss = newton(dVdt_scalar, V_guess)
        h_ss = h_inf(V_ss);
    except RuntimeError:
        print('Newton solver failed when starting at '+ str(V_guess))
        V_ss = -999.
        h_ss = -9.
        
    return V_ss, h_ss


def solve(time, V0_l, h0_l, Vam_l, Vbm_l, Vah_l, Vbh_l):


    global  V0, h0, Vam, Vbm, Vah, Vbh
    V0 = V0_l
    h0 = h0_l
    Vam = Vam_l
    Vbm = Vbm_l
    Vah = Vah_l
    Vbh = Vbh_l

    Y = odeint(dY_dt, [V0,h0], time)
    
    V = Y[:, 0]
    h = Y[:, 1]

    return V, h 





def compute_Jacobian(Y0):
    # Compute Jacobian with finite difference:
    J = np.zeros((2,2))
    eps = 1.e-4;
    for i in range(2):  # perturb in direction i:
        dY = np.array([0.,0.]);
        dY[i] = eps;
        Yp = Y0 + dY; Fp = np.array(dY_dt(Yp))
        Ym = Y0 - dY; Fm = np.array(dY_dt(Ym))
        J[i,:] = (Fp-Fm)/(2*eps)
                
    return J

def compute_eigenvalues(J):

    from numpy import linalg 
    w, v = linalg.eig(J)
    return w

def check_stability(V0):

        
    V_eq, h_eq = compute_steady_state(V0)

    J = compute_Jacobian([V_eq, h_eq]);
    w = compute_eigenvalues(J);
    lambda_max = w.real.max()

    return lambda_max, V_eq, h_eq

def plot_scalar(V, color = 'b'):


    dV_dt =  dVdt_scalar(V)
    m_ss =  m_inf(V)
    h_ss =  h_inf(V)
    
    mh_max = max(m_ss*h_ss);
    I_Na_full = g_Na*mh_max*(Vp - E_Na)
    I_K_full = g_K*(Vp - E_K)

    
    plt.rcParams["figure.figsize"] = (10,5)
    plt.figure(3);
    plt.clf()
    plt.plot(V, C_m*dV_dt, color, V,  -I_K_full, 'k', V,  -I_Na_full -I_K_full,'r')
    plt.legend(['$dV/dt$','$I_K$','$I_{K}+I_{Na,\max}$'])
    #plt.ylim(-0.5,0.5)
    plt.grid()

    print("V0", "lambda_max", "V_eq", "h_eq")
    for V0 in range(-80,-40,10):
        lambda_max, V_eq, h_eq = check_stability(V0)
        print(V0,lambda_max, V_eq, h_eq)
    
    
def plot_two_solutions(time, V1, h1, V2, h2):
    
    plt.rcParams["figure.figsize"] = (14,5)
    plt.figure(1)
    plt.clf()
    plt.subplot(1,3,1)
    plt.plot(time, V1, time, V2)
    plt.xlim(-1,time[-1])
    plt.title(r'$V(t)$')
    plt.legend(['stable','cyclic'])

    plt.subplot(1,3,2)
    plt.plot(time, h1, time, h2)
    plt.title(r'$h(t)$')

    plt.subplot(1,3,3)
    plt.plot(V1, h1,V2, h2)
    plt.xlabel(r'$V(t)$')
    plt.ylabel(r'$h(t)$')
    plt.savefig('phase.pdf')
    #plt.show()


def get_nullclines(Vp):

        h_eq =  h_inf(Vp)
        h_V = (g_K*(Vp-E_K))/(g_Na*m_inf(Vp)*(E_Na-Vp));

        return h_V, h_eq

def solve_and_plot(V0, h0, Vam, Vbm, Vah, Vbh):

    time = np.arange(0, 15, 0.001)
    V, h = solve(time, V0, h0, Vam, Vbm, Vah, Vbh)
    # Potential Plot
    plt.subplot(2,2,1)
    plt.plot(time, V, time, time*0 + E_Na, time, time*0 + E_K)
    plt.legend(['$V$','$E_{Na}$','$E_{K}$'], loc = "center right")
    plt.title(r'$V(t)$')

    plt.subplot(2,2,2)
    plt.plot(time, h)
    plt.ylim(0,1)
    plt.title(r'$h(t)$')


    plt.subplot(2,2,3)
    Vp = np.linspace(E_K-1, E_Na+1, num=1000)
    V_null, h_null = get_nullclines(Vp)
    plt.plot(Vp, V_null, Vp, h_null)
    plt.legend(['$\dot{V}=0$','$\dot{h}=0$'])
    plt.ylim(-0.2,1.2); 
    #plt.ylim(0.1,0.25); #zoom

    plt.subplot(2,2,4)
    dV_dt =  dVdt_scalar(Vp)
    m_ss =  m_inf(Vp)
    h_ss =  h_inf(Vp)
    
    mh_max = max(m_ss*h_ss);
    I_Na_full = g_Na*mh_max*(Vp - E_Na)
    I_K_full = g_K*(Vp - E_K)
    plt.plot(Vp, C_m*dV_dt, 'b', Vp,  -I_K_full, 'k', Vp,  -I_Na_full -I_K_full,'r')
    #plt.ylim(-0.2,1.2);
    plt.grid()
    plt.show()

    from IPython.display import display, Math
    for V0 in range(-80,-40,10):
        lambda_max, V_eq, h_eq = check_stability(V0)
        if h_eq>-1:
            display(Math(r'V_{{\mbox{{guess}}}}={:.1f},  V_{{\mbox{{eq}}}}={:.1f},  h_{{\mbox{{eq}}}}={:.3f}, \lambda_{{\max}}={:.3f}'.format(V0,  V_eq, h_eq, lambda_max)))

def ap_widget():
        
    interact(solve_and_plot,
                     V0 = FloatSlider(value=-50, min=-100, max=50, step=1, continuous_update=False),
                     h0 = FloatSlider(value=0.5, min=0, max=1, step=0.01, continuous_update=False),
                     Vam = FloatSlider(value=-60, min=-120, max=0, step=1, continuous_update=False),
                     Vbm = FloatSlider(value=-10, min=-100, max=30, step=1, continuous_update=False),
                     Vah = FloatSlider(value=-80, min=-100, max=0, step=1, continuous_update=False),    
                     Vbh = FloatSlider(value=-20, min=-100, max=0, step=1, continuous_update=False))



