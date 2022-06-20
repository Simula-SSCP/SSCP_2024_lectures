import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from math import exp, log, sqrt, pi, fsum
#import numpy.linalg as lin

def HH(y,t,V,P):

    # m-gate
    m = y[0]
    alpha_m = (P[0] + P[1]*V)/(1+P[2]*exp(P[3]*V))
    beta_m = P[4]*exp(P[5]*V)
    m_inf = alpha_m/(alpha_m+beta_m)
    
    # h-gate
    h = y[1]
    if type(V)==np.ndarray:
        alpha_h = 0*V
        idx = np.nonzero(V<-40)
        alpha_h = 0*V
        alpha_h[idx] = P[6]*exp(P[7]*V[idx])
        beta_h = (1.0/(P[8] + P[9]*exp(P[10]*V)));
        beta_h[idx] = P[11]*exp(0.35*V[idx]) + P[12]*exp(P[13]*V[idx])
    else:
        alpha_h = (0 if V >= -40 else P[6]*exp(P[7]*V))
        beta_h = (1.0/(P[8] + P[9]*exp(P[10]*V)) if V >= -40 else P[11]*exp(0.35*V) + P[12]*exp(P[13]*V))
        
    h_inf = alpha_h/(alpha_h+beta_h)
    
    dm = alpha_m*(1-m) - m*beta_m;
    dh = alpha_h*(1-h) - h*beta_h;
    
    dy = [dm,dh]
    
    return dy

def Markov_Na_Matrix(V,P):
    
    # A Markov state model for the fast sodium current (INa)
    # Grandi et al. 2007
    
    # state indices for mass matrix
    O = int(0)
    IF = int(1)
    IM1 = int(2)
    IM2 = int(3)
    C3 = int(4)
    C2 = int(5)
    C1 = int(6)
    IC3 = int(7)
    IC2 = int(8)
  
    n = 9 # number of states
    A = np.zeros((n,n)) # initialize rate mass matrix for output
    
    alpha1 = P[0]/(P[1]*exp(-(V+P[2])/P[3])+ P[6]*exp(-(V+P[2])/150));
    alpha2 = P[0]/(P[1]*exp(-(V+P[2])/P[4])+ P[7]*exp(-(V+P[2])/150));
    alpha3 = P[0]/(P[1]*exp(-(V+P[2])/P[5])+ P[8]*exp(-(V+P[2])/150));
    beta1 = P[9]*exp(-(V+P[2])/P[10]);
    beta2 = P[11]*exp(-(V-P[12])/P[10]);
    beta3 = P[13]*exp(-(V-P[14])/P[10]);
    alpha4 = 1/(P[15]*exp(-(V+7)/P[16])+P[17]);
    alpha5 = P[18]*exp(-(V+7)/P[19]);
    beta5 = P[20] + P[21]*(V+7);
    beta4 = (alpha3*alpha4*alpha5)/(beta3*beta5);
    alpha6 = alpha4/P[22];
    beta6 = P[23]*exp(-V/P[24]);
    alpha7 = P[25]*exp(V/P[26]);
    beta7 = P[28]*exp(-V/P[29]);
    #alpha8 = P[30];
    #beta8 = P[31];
    
    #Assign transitions
    A[C3, C2] = beta1
    A[C2, C3] = alpha1
    A[C2, C1] = beta2
    A[C1, C2] = alpha2
    A[C1, O]  = beta3
    A[O, C1]  = alpha3
    A[O, IF]  = beta4
    A[IF,O] = alpha4
    A[IF,C1] = beta5
    A[C1,IF] = alpha5
    A[IC2,C2] = beta5
    A[C2,IC2] = alpha5
    A[IC3,C3] = beta5
    A[C3,IC3] = alpha5
    A[IF,IM1] = beta6
    A[IM1,IF] = alpha6
    A[IM1,IM2] = beta7
    A[IM2,IM1] = alpha7    
    
    for i in range(n):
        A[i,i] = -fsum(A[:,i])
    
    return A

def Markov_Na_Init(V,P):
    b = np.zeros(9)
    A = Markov_Na_Matrix(P,V)
    A[-1,:] = 1;
    b[-1] = 1
    
    return np.linalg.solve(A,b)

def Markov_Na(y,t,V,P):
    # Initialize the output vector
    dim = y.shape
    dy = np.zeros((dim))
    A = Markov_Na_Matrix(V,P)
    
    dy = A.dot(y)
    return dy