import numpy as np
import matplotlib.pylab as plt
import scipy.optimize as opt
import math
from scipy.integrate import odeint
import numpy.linalg as lin


def f(y,t,P,V):
    
    alpha = math.exp((V-P[0])/P[1]);
    beta = math.exp((V-P[2])/P[3])*math.exp(-(V+P[4])/P[5])/(P[6]+P[7]*math.exp(-(V+P[8])/P[9]))
    
    C1 = int(0)
    C2 = int(1)
    C3 = int(2)
    C4 = int(3)
    O = int(4)
    I = int(5) 
    
    n = 6 # number of states
    A = np.zeros((n,n)) # initialize rate mass matrix for initialization
    b = np.zeros(n)
    
    # fill the rate matrix
    A[C1, C2] = beta
    A[C2, C1] = 4*alpha
    A[C2, C3] = 2*beta
    A[C3, C2] = 3*alpha
    A[C3, C4] = 3*beta
    A[C4, C3] = 2*alpha
    A[O, C4] = alpha
    A[C4, O] = 4*beta
    A[O, I] = P[10] # k1
    A[I, O] = P[11] # k2 
    
    for i in range(n):
        A[i,i] = -math.fsum(A[:,i])
    
    A[-1,:] = 1
    b[-1] = 1
    
    y0 = lin.solve(A,b)
    
    return y0
## --------------------------------------------------------------------------
    C1, C2, C3, C4, O = y
    
    alpha = math.exp((V-P[0])/P[1])
    beta = math.exp((V-P[2])/P[3])*math.exp(-(V+P[4])/P[5])/(P[6]+P[7]*math.exp(-(V+P[8])/P[9]))
    
    # first conserve mass
    I = 1-(O+C4+C3+C2+C1)
    # then calculate transitions
    dC1 = beta*C2 - 4*alpha*C1
    dC2 = 4*alpha*C1 + 2*beta*C3 - C2*(beta + 3*alpha)
    dC3 = 3*alpha*C2 + 3*beta*C4 - C3*(2*beta + 2*alpha)
    dC4 = 2*alpha*C3 + 4*beta*O - C4*(alpha + 3*beta)
    dO = P[11]*I + alpha*C4 - O*(P[10] + 4*beta)
    
    dy = [dC1, dC2, dC3, dC4, dO]
    return dy

def Activation(V,P,step_length):
    
    # Fixed parameters
    g_K = 0.3
    V_hold = -90
    
    #step through the test potentials in your reference data
    for n,i in enumerate(V):        
        # First reset your initial conditions to the holding potential at the beginning of each step
        # Question: Is this always a good idea? Why or why not?     
        V_hold = -90
        
        #y0 = Init(V_hold,P) 
        y0 = [0.44,0.40,0.14,0.0198,0.001]
        # time vector
        t = np.linspace(0,step_length,step_length*10)
        
        # solve the time-varying system
        Y = odeint(f,y0,t,(P,i))
      
        #    O = int(0)
#    I = int(1)
#    C4 = int(2)
#    C3 = int(3)
#    C2 = int(4)
#    C1 = int(5)
##    B = int(6)
        
        #store the open probability data and calculate the error metrics
        Po = np.zeros((len(t),len(V)))
        peaks = np.zeros((len(V)))
        
        Po[:,n] = Y[:,4]
        peaks[n] = g_K*Po.max()
        out = {'t':t, 'Po':Po,'I_peak':peaks}        
        
    return out


def Init(V,P):
    alpha = math.exp((V-P[0])/P[1]);
    beta = math.exp((V-P[2])/P[3])*math.exp(-(V+P[4])/P[5])/(P[6]+P[7]*math.exp(-(V+P[8])/P[9]))
    
    C1 = int(0)
    C2 = int(1)
    C3 = int(2)
    C4 = int(3)
    O = int(4)
    I = int(5) 
    
    n = 6 # number of states
    A = np.zeros((n,n)) # initialize rate mass matrix for initialization
    b = np.zeros(n)
    
    # fill the rate matrix
    A[C1, C2] = beta
    A[C2, C1] = 4*alpha
    A[C2, C3] = 2*beta
    A[C3, C2] = 3*alpha
    A[C3, C4] = 3*beta
    A[C4, C3] = 2*alpha
    A[O, C4] = alpha
    A[C4, O] = 4*beta
    A[O, I] = P[10] # k1
    A[I, O] = P[11] # k2 
    
    for i in range(n):
        A[i,i] = -math.fsum(A[:,i])
    
    A[-1,:] = 1
    b[-1] = 1
    
    y0 = lin.solve(A,b)
    
    return y0

# import data
SSA_data = np.loadtxt("SS.txt",dtype='float')
V = SSA_data[:,0]
I = SSA_data[:,1]

init_params = [48.4, 49.2, 48.4, 49.2, 48.4, 
               13.6, 1, 0.023, 48.4, 13.6, 
               0.00001, 0.00001]
step_length = 1000

dats = Activation(V, init_params, step_length)
model_I = dats['I_peak']
Po = dats['Po']
t = dats['t']

V = SSA_data[:,0]
I = SSA_data[:,1]
plt.figure()
plt.plot(V,I,'b-')
plt.plot(V,model_I,'r-')
plt.xlabel('Step potential [mV]')
plt.ylabel('Current (A/F)')

