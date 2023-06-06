import numpy as np
import matplotlib.pyplot as plt
import math

class Jafri_model_parts():
    # parameters
    R = 8.3145e3
    T = 310
    F = 9.6845e4
    Cm = 0.01
    stim_start = 100
    stim_end = 10100
    stim_period = 500
    stim_duration = 1
    stim_amplitude = 0.516289
    g_Na = 0.128
    Nao = 140
    P_Ca = 33.75e-6
    P_K = 1e-9
    i_Ca_L_Ca_half = -4.58e-3
    a = 2
    b = 2
    g = 2
    f = 0.3
    g_ = 0
    f_ = 0
    omega = 0.01
    Cao = 1.8
    g_K_max = 0.001128
    P_NaK = 0.01833
    g_K1_max = 7.5e-3
    g_Kp = 8.28e-5
    k_NaCa = 50
    K_mNa = 87.5
    K_mCa = 1.38
    k_sat = 0.1
    eta = 0.35
    K_mpCa = 0.5e-3
    I_pCa = 1.15e-2
    g_Nab = 1.41e-5
    g_Cab = 6.032e-5
    I_NaK = 0.013
    K_mNai = 10
    K_mKo = 1.5
    K_m_ns_Ca = 1.2e-3
    P_ns_Ca = 1.75e-9
    Am = 546.69
    V_myo = 0.92
    v1 = 1.8
    v2 = 0.58e-4
    v3 = 1.8e-3
    nCa = 4
    mCa = 3
    k_a_plus = 1.215e10
    k_a_minus = 0.1425
    k_b_plus = 4.05e7
    k_b_minus = 1.93
    k_c_plus = 0.018
    k_c_minus = 0.0008
    k_htrpn_plus = 20
    k_htrpn_minus = 0.066e-3
    k_ltrpn_plus = 40
    k_ltrpn_minus = 0.04
    tau_tr = 34.48
    K_mup = 0.5e-3
    K_mCMDN = 2.38e-3
    K_mCSQN = 0.8
    tau_xfer = 3.125
    HTRPN_tot = 0.14
    LTRPN_tot = 0.07
    CSQN_tot = 15
    CMDN_tot = 0.05
    V_SS =  5.828e-05*V_myo
    V_NSR =  0.081*V_myo
    V_JSR =  0.00464*V_myo
    
    @property
    def parameters(self):
        return (self.R, self.T, self.F, self.Cm, self.stim_start, self.stim_end, self.stim_period,
                self.stim_duration, self.stim_amplitude, self.g_Na, self.Nao, self.P_Ca, self.P_K, 
                self.i_Ca_L_Ca_half, self.a, self.b, self.g, self.f, self.g_, self.f_, self.omega, 
                self.Cao, self.g_K_max, self.P_NaK, self.g_K1_max, self.g_Kp, self.k_NaCa, self.K_mNa, 
                self.K_mCa, self.k_sat, self.eta, self.K_mpCa, self.I_pCa, self.g_Nab, self.g_Cab, 
                self.I_NaK, self.K_mNai, self.K_mKo, self.K_m_ns_Ca, self.P_ns_Ca, self.Am, self.V_myo, 
                self.v1, self.v2, self.v3, self.nCa, self.mCa, self.k_a_plus, self.k_a_minus, 
                self.k_b_plus, self.k_b_minus, self.k_c_plus, self.k_c_minus, self.k_htrpn_plus, 
                self.k_htrpn_minus, self.k_ltrpn_plus, self.k_ltrpn_minus, self.tau_tr, self.K_mup, 
                self.K_mCMDN, self.K_mCSQN, self.tau_xfer, self.HTRPN_tot, self.LTRPN_tot, self.CSQN_tot, 
                self.CMDN_tot, self.V_SS, self.V_NSR, self.V_JSR)

    def test_class(self, t, V):
        print(f"It is time {t} and voltage {V}")
        
    
    def currents_concentrations(self, V, m, h, j, Nai, X, Ko, Ki, Cai, y, C0, C1, C2, C3, C4, \
                                C_Ca0, C_Ca1, C_Ca2, C_Ca3, C_Ca4, O, O_Ca, Ca_SS, Ca_JSR, Ca_NSR,\
                                HTRPNCa, LTRPNCa ):
        #fast_Na_current
        E_Na =  ((self.R*self.T)/self.F)*math.log(self.Nao/Nai)
        i_Na =  self.g_Na*(m**3.0)*h*j*(V - E_Na)

        alpha_m = (0.32*(V + 47.13))/(1.0 - math.exp(-0.1*(V + 47.13)))
        beta_m =  0.08*math.exp( - V/11.0)
    
        if V< - 40.0:
            alpha_h = 0.135*math.exp((80.0 + V)/-6.80)
            beta_h = 3.56*math.exp(0.079*V)+ 310000.*math.exp(0.35*V)
            alpha_j = ((-127140.*math.exp(0.244400*V) -  3.474e-05*math.exp(-0.04391*V))*(V + 37.78))/(1.0 + math.exp(0.311*(V + 79.23)))
            beta_j = (0.121200*math.exp(-0.0105200*V))/(1.0 + math.exp(-0.1378*(V + 40.14)))
        else:
            alpha_h = 0.0
            beta_h = 1.0/( 0.13*(1.0 + math.exp((V + 10.66)/-11.1)))
            alpha_j = 0.0
            beta_j = ( 0.3*math.exp(-2.535e-07*V))/(1.0 + math.exp(-0.1*(V+32.0)))
    
        dm_dt =  alpha_m*(1.0 - m) - beta_m*m
        dh_dt =  alpha_h*(1.0 - h) - beta_h*h
        dj_dt =  alpha_j*(1.0 - j) - beta_j*j
        
        
        # Time dependent K current IK
        alpha_X = (7.19e-05*(V + 30.0))/(1.0 - math.exp(-0.1480*(V + 30.0)))
        beta_X = (0.000131*(V + 30.0))/(-1.0 + math.exp(0.0687*(V + 30.0)))
        dX_dt = alpha_X*(1.0 - X) - beta_X*X

        g_K = self.g_K_max*math.sqrt(Ko/5.4)
        E_K = ((self.R*self.T)/self.F)*math.log((Ko + self.P_NaK*self.Nao)/(Ki + self.P_NaK*Nai))
        Xi = 1.0/(1.0 + math.exp((V - 56.26)/32.10))
        i_K = g_K*Xi*(X**2.0)*(V - E_K)
        
        
        ## Time dependent K current I_K1
        E_K1 = ((self.R*self.T)/self.F)*math.log(Ko/Ki)
        g_K1 = self.g_K1_max*math.sqrt(Ko/5.4)
        alpha_K1 = 1.02/(1.0 + math.exp( 0.2385*(V - E_K1 - 59.215)))
        beta_K1 = (0.491240*math.exp( 0.08032*(V + 5.476 - E_K1)) + math.exp( 0.06175*(V - (E_K1 + 594.310))))/(1.0 + math.exp(-0.5143*(V - E_K1 + 4.753)))
        K1_infinity = alpha_K1/(alpha_K1+beta_K1)
        i_K1 = g_K1*K1_infinity*(V - E_K1)
    
    
        ## Plateau current I_Kp
        E_Kp = E_K1
        Kp = 1.0/(1.0 + math.exp((7.488 - V)/5.98))
        i_Kp = self.g_Kp*Kp*(V - E_Kp)
        
        ## Na K pump
        sigma = (1.0/7.0)*(math.exp(self.Nao/67.3) - 1.0)
        f_NaK = 1.0/(1.0 + 0.1245*math.exp((-0.10*V*self.F)/(self.R*self.T)) + 0.0365*sigma*math.exp((-V*self.F)/(self.R*self.T)))
        i_NaK = (((self.I_NaK*f_NaK*1.0)/(1.0 + ((self.K_mNai/Nai)**1.5)))*Ko)/(Ko + self.K_mKo)
        
        ## Nonspecific Ca activated current I_nsCa
        EnsCa = ((self.R*self.T)/self.F)*math.log((Ko + self.Nao)/(Ki + Nai))
        VnsCa = V - EnsCa
        I_ns_Na = (((self.P_ns_Ca*(1.0**2.0)*VnsCa*(self.F**2.0))/(self.R*self.T))*(0.75*Nai*math.exp((VnsCa*self.F)/(self.R*self.T)) - 0.75*self.Nao))/(math.exp((VnsCa*self.F)/(self.R*self.T)) - 1.0)
        i_ns_Na = (I_ns_Na*1.0)/(1.0 + ((self.K_m_ns_Ca/Cai)**3.0))
        I_ns_K = (((self.P_ns_Ca*(1.0**2.0)*VnsCa*(self.F**2.0))/(self.R*self.T))*(0.75*Ki*math.exp((VnsCa*self.F)/(self.R*self.T)) - 0.75*Ko))/(math.exp((VnsCa*self.F)/(self.R*self.T)) - 1.0)
        i_ns_K = (I_ns_K*1.0)/(1.0 + ((self.K_m_ns_Ca/Cai)**3.00000))
        i_ns_Ca = i_ns_Na+i_ns_K
        
        
        ## Sarcolemmal Ca pump current I_pCa
        i_p_Ca = (self.I_pCa*Cai)/(self.K_mpCa + Cai)

    
        ## Calcium background current I_Cab
        E_CaN = ((self.R*self.T)/(2.0*self.F))*math.log(self.Cao/Cai)
        i_Ca_b = self.g_Cab*(V - E_CaN)
    

        ## Calcium background current I_Nab
        E_NaN = E_Na
        i_Na_b = self.g_Nab*(V - E_NaN)
   
    
        ## L type calcium channel
        alpha = 0.40*math.exp((V + 12.0)/10.0)
        beta = 0.05*math.exp((V + 12.0)/-13.0)
        gamma = 0.1875*Ca_SS
        alpha_a = alpha*self.a
        beta_b = beta/self.b

        y_infinity = 1.0/(1.0 + math.exp((V + 55.0)/7.5))+0.1/(1.0 + math.exp((-V + 21.0)/6.0))
        tau_y = 20.0 + 600.0/(1.0 + math.exp((V + 30.0)/9.5))
        dy_dt = (y_infinity - y)/tau_y

        dC0_dt = (beta*C1 + self.omega*C_Ca0) - (4.0*alpha + gamma)*C0
        dC1_dt = (4.0*alpha*C0 + 2.0*beta*C2 + (self.omega/self.b)*C_Ca1) - (beta + 3.0*alpha + gamma*self.a)*C1
        dC2_dt = (3.0*alpha*C1 + 3.0*beta*C3 + (self.omega/(self.b**2.0))*C_Ca2) - (beta*2.0 + 2.0*alpha + gamma*(self.a**2.0))*C2
        dC3_dt = (2.0*alpha*C2 + 4.0*beta*C4 + (self.omega/(self.b**3.0))*C_Ca3) - (beta*3.0 + alpha + gamma*(self.a**3.0))*C3
        dC4_dt = (alpha*C3 + self.g*O+ (self.omega/(self.b**4.0))*C_Ca4) -  (beta*4.0 + self.f + gamma*(self.a**4.0))*C4
        dC_Ca0_dt = (beta_b*C_Ca1+ gamma*C_Ca0) - (4.0*alpha_a+self.omega)*C_Ca0
        dC_Ca1_dt = (4.0*alpha_a*C_Ca0 + 2.0*beta_b*C_Ca2 + gamma*self.a*C1) -  (beta_b + 3.0*alpha_a + self.omega/self.b)*C_Ca1
        dC_Ca2_dt = (3.0*alpha_a*C_Ca1 + 3.0*beta_b*C_Ca3 + gamma*(self.a**2.0)*C2) - (beta_b*2.0 + 2.0*alpha_a + self.omega/(self.b**2.0))*C_Ca2
        dC_Ca3_dt = (2.0*alpha_a*C_Ca2 + 4.0*beta_b*C_Ca4 + gamma*(self.a**3.0)*C3) - (beta_b*3.0 + alpha_a + self.omega/(self.b**3.0))*C_Ca3
        dC_Ca4_dt = (alpha_a*C_Ca3 + self.g_*O_Ca + gamma*(self.a**4.0)*C4) - (beta_b*4.0 + self.f_ + self.omega/(self.b**4.0))*C_Ca4
        dO_dt = self.f*C4 - self.g*O
        dO_Ca_dt = self.f_*C_Ca4 - self.g_*O_Ca

        i_Ca_L_Ca_max = (((self.P_Ca*4.0*V*(self.F**2.0))/(self.R*self.T))*(0.001*math.exp((2.0*V*self.F)/(self.R*self.T)) -  0.341*self.Cao))/(math.exp((2.0*V*self.F)/(self.R*self.T)) - 1.0)
        i_Ca_L_Ca = i_Ca_L_Ca_max*y*(O + O_Ca)

        p_k = self.P_K/(1.0 + i_Ca_L_Ca_max/self.i_Ca_L_Ca_half)
        i_Ca_L_K = (((p_k*y*(O + O_Ca)*V*(self.F**2.0))/(self.R*self.T))*(Ki*math.exp((V*self.F)/(self.R*self.T)) - Ko))/(math.exp((V*self.F)/(self.R*self.T)) - 1.0)


        ## Calcium buffered troponin
        J_htrpn =  self.k_htrpn_plus*Cai*(self.HTRPN_tot - HTRPNCa) -  self.k_htrpn_minus*HTRPNCa
        dHTRPNCa_dt = J_htrpn
        J_ltrpn =  self.k_ltrpn_plus*Cai*(self.LTRPN_tot - LTRPNCa) -  self.k_ltrpn_minus*LTRPNCa
        dLTRPNCa_dt = J_ltrpn
        J_trpn = J_htrpn + J_ltrpn

        return dm_dt, dh_dt, dj_dt, i_Na, dX_dt, i_K, i_K1, i_Kp, i_NaK, i_ns_Ca, i_ns_Na,\
    i_ns_K, i_p_Ca, i_Ca_b, i_Na_b, dy_dt, dC0_dt, dC1_dt, dC2_dt, dC3_dt, dC4_dt,\
    dC_Ca0_dt, dC_Ca1_dt, dC_Ca2_dt, dC_Ca3_dt, dC_Ca4_dt, dO_dt, dO_Ca_dt,\
    dHTRPNCa_dt,dLTRPNCa_dt, i_Ca_L_Ca, i_Ca_L_K, J_trpn

