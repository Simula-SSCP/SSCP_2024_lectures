from math import exp, log, sqrt, pi

def grandi_bers(y, t, Pd):

    #unpack the solution vector
    m,     h,     j,     d,     f,     fcaBj,     fcaBsl,    xtos,     ytos,     xtof,     ytof,     xkr,     xks,     RyRr,    RyRo,    RyRi,    NaBj,    NaBsl,    TnCL,     TnCHc,    TnCHm,    CaM,     Myoc,     Myom,     SRB,     SLLj,     SLLsl,     SLHj,     SLHsl,     Csqnb,     Ca_sr,    Naj,     Nasl,     Nai,     Ki,     Caj,     Casl,    Cai,     Vm  = y
    
    #unpack the passed parameter set and calculate constants
    # Constants
    R = Pd['R']
    Frdy = Pd['Frdy']
    Temp = Pd['Temp']
    FoRT = Frdy/R/Temp
    Qpow = (Temp-310)/10
    Cmem = Pd['Cmem']

    # Cell geometry
    Vcell = pi*Pd['cellRadius']**2*Pd['cellLength']*1e-15 
    Vmyo = Pd['Vmyo_ratio']*Vcell
    Vsr = Pd['Vsr_ratio']*Vcell
    Vsl = Pd['Vsl_ratio']*Vcell
    Vjunc = Pd['Vjunc_ratio']*Vcell

    # Fractional currents in compartments
    Fjunc = Pd['Fjunc']
    Fsl = 1-Fjunc
    Fjunc_CaL = Pd['Fjunc_CaL'] 
    Fsl_CaL = 1-Fjunc_CaL

    # Fixed ion concentrations     
    Cli = Pd['Cli']
    Clo = Pd['Clo']
    Ko = Pd['Ko']
    Nao = Pd['Nao']
    Cao = Pd['Cao']
    Mgi = Pd['Mgi']

    # Buffering parameters
    # koff: [1/s] = 1e-3*[1/ms]  kon: [1/uM/s] = [1/mM/ms]
    Bmax_Naj = Pd['Bmax_Naj']
    Bmax_Nasl = Pd['Bmax_Nasl']
    koff_na = Pd['koff_na']
    kon_na = Pd['kon_na']
    Bmax_TnClow = Pd['Bmax_TnClow']
    koff_tncl = Pd['koff_tncl']
    kon_tncl = Pd['kon_tncl'] 
    Bmax_TnChigh = Pd['Bmax_TnChigh']
    koff_tnchca = Pd['koff_tnchca']
    kon_tnchca = Pd['kon_tnchca'] 
    koff_tnchmg = Pd['koff_tnchmg']
    kon_tnchmg = Pd['kon_tnchmg'] 
    Bmax_CaM = Pd['Bmax_CaM'] 
    koff_cam = Pd['koff_cam'] 
    kon_cam = Pd['kon_cam'] 
    Bmax_myosin = Pd['Bmax_myosin']
    koff_myoca = Pd['koff_myoca']
    kon_myoca = Pd['kon_myoca']
    koff_myomg = Pd['koff_myomg']
    kon_myomg = Pd['kon_myomg']
    Bmax_SR = Pd['Bmax_SR']
    koff_sr = Pd['koff_sr']
    kon_sr = Pd['kon_sr']
    Bmax_SLlowsl = Pd['Bmax_SLlowsl']*Vmyo/Vsl        # [mM]    # SL buffering
    Bmax_SLlowj = Pd['Bmax_SLlowj']*Vmyo/Vjunc    # [mM]   
    koff_sll = Pd['koff_sll']    # [1/ms]
    kon_sll = Pd['kon_sll']          # [1/mM/ms]
    Bmax_SLhighsl = Pd['Bmax_SLhighsl']*Vmyo/Vsl       # [mM] 
    Bmax_SLhighj = Pd['Bmax_SLhighj']*Vmyo/Vjunc  # [mM] 
    koff_slh = Pd['koff_slh']     # [1/ms]
    kon_slh = Pd['kon_slh']          # [1/mM/ms]
    Bmax_Csqn = Pd['Bmax_Csqn']*Vmyo/Vsr  # [mM] # Bmax_Csqn = 2.6      # Csqn buffering
    koff_csqn = Pd['koff_csqn']
    kon_csqn = Pd['kon_csqn']

    #########################33

    # Nernst Potentials
    ena_junc = (1/FoRT)*log(Nao/Naj)     # [mV]
    ena_sl = (1/FoRT)*log(Nao/Nasl)       # [mV]
    ek = (1/FoRT)*log(Ko/Ki)	        # [mV]
    eca_junc = (1/FoRT/2)*log(Cao/Caj)   # [mV]
    eca_sl = (1/FoRT/2)*log(Cao/Casl)     # [mV]
    ecl = (1/FoRT)*log(Cli/Clo)            # [mV]

    #CURRENTS
    #INa ten Tusscher formulation
    mss = 1 / ((1 + exp( -(56.86 + Vm) / 9.03 ))**2)
    taum = 0.1292 * exp(-((Vm+45.79)/15.54)**2) + 0.06487 * exp(-((Vm-4.823)/51.12)**2)                 
    ah = 0.0 if (Vm >= -40) else (0.057 * exp( -(Vm + 80) / 6.8 )) 
    bh =  (0.77 / (0.13*(1 + exp( -(Vm + 10.66) / 11.1 )))) if (Vm >= -40) else ((2.7 * exp( 0.079 * Vm) + 3.1*10**5 * exp(0.3485 * Vm))) 
    tauh = 1 / (ah + bh) 
    hss = 1 / ((1 + exp( (Vm + 71.55)/7.43 ))**2)
    aj = (0) if (Vm >= -40) else (((-2.5428 * 10**4*exp(0.2444*Vm) - 6.948*10**-6 * exp(-0.04391*Vm)) * (Vm + 37.78)) /(1 + exp( 0.311 * (Vm + 79.23) )))
    bj =  ((0.6 * exp( 0.057 * Vm)) / (1 + exp( -0.1 * (Vm + 32) ))) if (Vm >= -40) else ((0.02424 * exp( -0.01052 * Vm )) / (1 + exp( -0.1378 * (Vm + 40.14) ))) 
    tauj = 1 / (aj + bj)
    jss = 1 / ((1 + exp( (Vm + 71.55)/7.43 ))**2)         
    d_m = (mss - m) / taum
    d_h = (hss - h) / tauh
    d_j = (jss - j) / tauj
    I_Na_junc = Fjunc*Pd['GNa']*m**3*h*j*(Vm-ena_junc)
    I_Na_sl = Fsl*Pd['GNa']*m**3*h*j*(Vm-ena_sl)
    I_Na = I_Na_junc+I_Na_sl

    # I_nak: Na/K Pump Current
    sigma = (exp(Nao/67.3)-1)/7
    fnak = 1/(1+0.1245*exp(-0.1*Vm*FoRT)+0.0365*sigma*exp(-Vm*FoRT))
    I_nak_junc = 1*Fjunc*Pd['IbarNaK']*fnak*Ko/(1+(Pd['KmNaip']/Naj)**4)/(Ko+Pd['KmKo'])
    I_nak_sl = 1*Fsl*Pd['IbarNaK']*fnak*Ko/(1+(Pd['KmNaip']/Nasl)**4)/(Ko+Pd['KmKo'])
    I_nak = I_nak_junc+I_nak_sl

    ## I_kr: Rapidly Activating K Current
    gkr = Pd['Gkr']*sqrt(Ko/5.4)
    xrss = 1/(1+exp(-(Vm+10)/5))
    tauxr = 550/(1+exp((-22-Vm)/9))*6/(1+exp((Vm-(-11))/9))+230/(1+exp((Vm-(-40))/20))
    d_xkr = (xrss-xkr)/tauxr
    rkr = 1/(1+exp((Vm+74)/24))
    I_kr = gkr*xkr*rkr*(Vm-ek)

    ## I_ks: Slowly Activating K Current
    eks = (1/FoRT)*log((Ko+Pd['pNaK']*Nao)/(Ki+Pd['pNaK']*Nai))
    gks_junc=1*0.0035
    gks_sl=1*0.0035 #FRA
    xsss = 1 / (1+exp(-(Vm + 3.8)/14.25)) # fitting Fra
    tauxs=990.1/(1+exp(-(Vm+2.436)/14.12))
    d_xks = (xsss-xks)/tauxs
    I_ks_junc = Fjunc*Pd['Gks']*xks**2*(Vm-eks)
    I_ks_sl = Fsl*Pd['Gks']*xks**2*(Vm-eks)      
    I_ks = I_ks_junc+I_ks_sl
     
    # I_kp: Plateau K current
    kp_kp = 1/(1+exp(7.488-Vm/5.98))
    I_kp_junc = Fjunc*Pd['Gkp']*kp_kp*(Vm-ek)
    I_kp_sl = Fsl*Pd['Gkp']*kp_kp*(Vm-ek)
    I_kp = I_kp_junc+I_kp_sl

    ## I_to: Transient Outward K Current (slow and fast components)
    I_tos = Pd['GtoSlow']*xtos*ytos*(Vm-ek)   
    I_tof = Pd['GtoFast']*xtof*ytof*(Vm-ek)
    xtoss = 1/(1+exp(-(Vm-19.0)/13))
    ytoss = 1/(1+exp((Vm+19.5)/5))
    tauxtos = 9/(1+exp((Vm+3.0)/15))+0.5
    tauytos = 800/(1+exp((Vm+60.0)/10))+30
    d_xtos = (xtoss-xtos)/tauxtos
    d_ytos = (ytoss-ytos)/tauytos
    tauxtof = 11*exp(-((Vm+45)/60)**2)+1.0 
    tauytof = 85*exp((-(Vm+40)**2/220))+7
    d_xtof = (xtoss-xtof)/tauxtof
    d_ytof = (ytoss-ytof)/tauytof
    I_to = I_tos + I_tof

    ## I_ki: Time-Independent K Current
    aki = 1.02/(1+exp(0.2385*(Vm-ek-59.215)))
    bki =(0.49124*exp(0.08032*(Vm+5.476-ek)) + exp(0.06175*(Vm-ek-594.31))) /(1 + exp(-0.5143*(Vm-ek+4.753)))
    kiss = aki/(aki+bki)
    I_ki = Pd['Gki']*sqrt(Ko/5.4)*kiss*(Vm-ek)

    # I_ClCa: Ca-activated Cl Current, I_Clbk: background Cl Current
    I_ClCa_junc = Fjunc*Pd['GClCa']/(1+Pd['KdClCa']/Caj)*(Vm-ecl)
    I_ClCa_sl = Fsl*Pd['GClCa']/(1+Pd['KdClCa']/Casl)*(Vm-ecl)
    I_ClCa = I_ClCa_junc+I_ClCa_sl  
    
    ## I_Ca: L-type Calcium Current  
    dss = 1/(1+exp(-(Vm+5)/6.0))
    fss = 1/(1+exp((Vm+35)/9))+0.6/(1+exp((50-Vm)/20))
    taud = dss*(1-exp(-(Vm+5)/6.0))/(0.035*(Vm+5))
    tauf = 1/(0.0197*exp( -(0.0337*(Vm+14.5))**2 )+0.02)
    d_d = (dss-d)/taud
    d_f = (fss-f)/tauf
    d_fcaBj = 1.7*Caj*(1-fcaBj)-11.9e-3*fcaBj # fCa_junc   koff!!!!!!!!
    d_fcaBsl = 1.7*Casl*(1-fcaBsl)-11.9e-3*fcaBsl # fCa_sl
    fcaCaMSL= 0.1/(1+(0.01/Casl))
    fcaCaj= 0.1/(1+(0.01/Caj))
    fcaCaMSL=0
    fcaCaj= 0
    ibarca_j = Pd['pCa']*4*(Vm*Frdy*FoRT) * (0.341*Caj*exp(2*Vm*FoRT)-0.341*Cao) /(exp(2*Vm*FoRT)-1)
    ibarca_sl = Pd['pCa']*4*(Vm*Frdy*FoRT) * (0.341*Casl*exp(2*Vm*FoRT)-0.341*Cao) /(exp(2*Vm*FoRT)-1)
    ibark = Pd['pK']*(Vm*Frdy*FoRT)*(0.75*Ki*exp(Vm*FoRT)-0.75*Ko) /(exp(Vm*FoRT)-1)
    ibarna_j = Pd['pNa']*(Vm*Frdy*FoRT) *(0.75*Naj*exp(Vm*FoRT)-0.75*Nao)  /(exp(Vm*FoRT)-1)
    ibarna_sl = Pd['pNa']*(Vm*Frdy*FoRT) *(0.75*Nasl*exp(Vm*FoRT)-0.75*Nao)  /(exp(Vm*FoRT)-1)
    I_Ca_junc = (Fjunc_CaL*ibarca_j*d*f*((1-fcaBj)+fcaCaj)*Pd['Q10CaL']**Qpow)*0.45*1
    I_Ca_sl = (Fsl_CaL*ibarca_sl*d*f*((1-fcaBsl)+fcaCaMSL)*Pd['Q10CaL']**Qpow)*0.45*1
    I_Ca = I_Ca_junc+I_Ca_sl
    I_CaK = (ibark*d*f*(Fjunc_CaL*(fcaCaj+(1-fcaBj))+Fsl_CaL*(fcaCaMSL+(1-fcaBsl)))*Pd['Q10CaL']**Qpow)*0.45*1
    I_CaNa_junc = (Fjunc_CaL*ibarna_j*d*f*((1-fcaBj)+fcaCaj)*Pd['Q10CaL']**Qpow)*0.45*1
    I_CaNa_sl = (Fsl_CaL*ibarna_sl*d*f*((1-fcaBsl)+fcaCaMSL)*Pd['Q10CaL']**Qpow)*.45*1
    I_CaNa = I_CaNa_junc+I_CaNa_sl
    I_Catot = I_Ca+I_CaK+I_CaNa

    # I_ncx: Na/Ca Exchanger flux
    Ka_junc = 1/(1+(Pd['Kdact']/Caj)**2)
    Ka_sl = 1/(1+(Pd['Kdact']/Casl)**2)
    s1_junc = exp(Pd['nu']*Vm*FoRT)*Naj**3*Cao
    s1_sl = exp(Pd['nu']*Vm*FoRT)*Nasl**3*Cao
    s2_junc = exp((Pd['nu']-1)*Vm*FoRT)*Nao**3*Caj
    s3_junc = Pd['KmCai']*Nao**3*(1+(Naj/Pd['KmNai'])**3) + Pd['KmNao']**3*Caj*(1+Caj/Pd['KmCai'])+Pd['KmCao']*Naj**3+Naj**3*Cao+Nao**3*Caj
    s2_sl = exp((Pd['nu']-1)*Vm*FoRT)*Nao**3*Casl
    s3_sl = Pd['KmCai']*Nao**3*(1+(Nasl/Pd['KmNai'])**3) + Pd['KmNao']**3*Casl*(1+Casl/Pd['KmCai'])+Pd['KmCao']*Nasl**3+Nasl**3*Cao+Nao**3*Casl
    I_ncx_junc = Fjunc*Pd['IbarNCX']*Pd['Q10NCX']**Qpow*Ka_junc*(s1_junc-s2_junc)/s3_junc/(1+Pd['ksat']*exp((Pd['nu']-1)*Vm*FoRT))
    I_ncx_sl = Fsl*Pd['IbarNCX']*Pd['Q10NCX']**Qpow*Ka_sl*(s1_sl-s2_sl)/s3_sl/(1+Pd['ksat']*exp((Pd['nu']-1)*Vm*FoRT))
    I_ncx = I_ncx_junc+I_ncx_sl

    # I_pca: Sarcolemmal Ca Pump Current
    I_pca_junc = Fjunc*Pd['Q10SLCaP']**Qpow*Pd['IbarSLCaP']*Caj**1.6/(Pd['KmPCa']**1.6+Caj**1.6)
    I_pca_sl = Fsl*Pd['Q10SLCaP']**Qpow*Pd['IbarSLCaP']*Casl**1.6/(Pd['KmPCa']**1.6+Casl**1.6)
    I_pca = I_pca_junc+I_pca_sl

    ## SR fluxes: Calcium Release, SR Ca pump, SR Ca leak
    MaxSR = 15 
    MinSR = 1
    kCaSR = MaxSR - (MaxSR-MinSR)/(1+(Pd['ec50SR']/Ca_sr)**2.5)
    koSRCa = Pd['koCa']/kCaSR
    kiSRCa = Pd['kiCa']*kCaSR
    RI = 1-RyRr-RyRo-RyRi
    d_RyRr = (Pd['kim']*RI-kiSRCa*Caj*RyRr)-(koSRCa*Caj**2*RyRr-Pd['kom']*RyRo)   # R
    d_RyRo = (koSRCa*Caj**2*RyRr-Pd['kom']*RyRo)-(kiSRCa*Caj*RyRo-Pd['kim']*RyRi)# O
    d_RyRi = (kiSRCa*Caj*RyRo-Pd['kim']*RyRi)-(Pd['kom']*RyRi-koSRCa*Caj**2*RI)   # I
    J_SRCarel = Pd['ks']*RyRo*(Ca_sr-Caj)          # [mM/ms]
    J_serca = 1*Pd['Q10SRCaP']**Qpow*Pd['Vmax_SRCaP']*((Cai/Pd['Kmf'])**Pd['hillSRCaP']-(Ca_sr/Pd['Kmr'])**Pd['hillSRCaP'])/(1+(Cai/Pd['Kmf'])**Pd['hillSRCaP']+(Ca_sr/Pd['Kmr'])**Pd['hillSRCaP'])
    J_SRleak = 5.348e-6*(Ca_sr-Caj)           #   [mM/ms]

    # BACKROUND CURRENTS
    # I_nabk: Na Background Current
    I_nabk_junc = Fjunc*Pd['GNaB']*(Vm-ena_junc)
    I_nabk_sl = Fsl*Pd['GNaB']*(Vm-ena_sl)
    I_nabk = I_nabk_junc+I_nabk_sl
    
    # I_cabk: Ca Background Current
    I_cabk_junc = Fjunc*Pd['GCaB']*(Vm-eca_junc)
    I_cabk_sl = Fsl*Pd['GCaB']*(Vm-eca_sl)
    I_cabk = I_cabk_junc+I_cabk_sl
    
    # I_Clbk: Chloride Background Current
    I_Clbk = Pd['GClB']*(Vm-ecl) 

    # BUFFERS
    # Sodium and Calcium Buffering
    d_NaBj = kon_na*Naj*(Bmax_Naj-NaBj)-koff_na*NaBj        # NaBj      [mM/ms]
    d_NaBsl = kon_na*Nasl*(Bmax_Nasl-NaBsl)-koff_na*NaBsl       # NaBsl     [mM/ms]

    # Cytosolic Ca Buffers
    d_TnCL = kon_tncl*Cai*(Bmax_TnClow-TnCL)-koff_tncl*TnCL            # TnCL      [mM/ms]
    d_TnCHc = kon_tnchca*Cai*(Bmax_TnChigh-TnCHc-TnCHm)-koff_tnchca*TnCHc # TnCHc     [mM/ms]
    d_TnCHm = kon_tnchmg*Mgi*(Bmax_TnChigh-TnCHc-TnCHm)-koff_tnchmg*TnCHm   # TnCHm     [mM/ms]
    d_CaM = kon_cam*Cai*(Bmax_CaM-CaM)-koff_cam*CaM                 # CaM       [mM/ms]
    d_Myoc = kon_myoca*Cai*(Bmax_myosin-Myoc-Myom)-koff_myoca*Myoc    # Myosin_ca [mM/ms]
    d_Myom = kon_myomg*Mgi*(Bmax_myosin-Myoc-Myom)-koff_myomg*Myom      # Myosin_mg [mM/ms]
    d_SRB = kon_sr*Cai*(Bmax_SR-SRB)-koff_sr*SRB                    # SRB       [mM/ms]
    J_CaB_cytosol = d_TnCL + d_TnCHc + d_TnCHm + d_CaM + d_Myoc + d_Myom + d_SRB

    # Junctional and SL Ca Buffers
    d_SLLj = kon_sll*Caj*(Bmax_SLlowj-SLLj)-koff_sll*SLLj       # SLLj      [mM/ms]
    d_SLLsl = kon_sll*Casl*(Bmax_SLlowsl-SLLsl)-koff_sll*SLLsl      # SLLsl     [mM/ms]
    d_SLHj = kon_slh*Caj*(Bmax_SLhighj-SLHj)-koff_slh*SLHj      # SLHj      [mM/ms]
    d_SLHsl = kon_slh*Casl*(Bmax_SLhighsl-SLHsl)-koff_slh*SLHsl     # SLHsl     [mM/ms]
    J_CaB_junction = d_SLLj+d_SLHj
    J_CaB_sl = d_SLLsl+d_SLHsl

    ## Ion concentrations
    # SR Ca Concentrations
    d_Csqnb = kon_csqn*Ca_sr*(Bmax_Csqn-Csqnb)-koff_csqn*Csqnb       # Csqn      [mM/ms]
    d_Ca_sr = J_serca-(J_SRleak*Vmyo/Vsr+J_SRCarel)-d_Csqnb         # Ca_sr     [mM/ms] #Ratio 3 leak current
    # d_Ca_sr=0

    # Sodium Concentrations
    I_Na_tot_junc = I_Na_junc+I_nabk_junc+3*I_ncx_junc+3*I_nak_junc+I_CaNa_junc   # [uA/uF]
    I_Na_tot_sl = I_Na_sl+I_nabk_sl+3*I_ncx_sl+3*I_nak_sl+I_CaNa_sl   # [uA/uF]
    I_Na_tot_sl2 = 3*I_ncx_sl+3*I_nak_sl+I_CaNa_sl   # [uA/uF]
    I_Na_tot_junc2 = 3*I_ncx_junc+3*I_nak_junc+I_CaNa_junc   # [uA/uF]
    d_Naj = -I_Na_tot_junc*Cmem/(Vjunc*Frdy)+Pd['J_na_juncsl']/Vjunc*(Nasl-Naj)-d_NaBj
    d_Nasl = -I_Na_tot_sl*Cmem/(Vsl*Frdy)+Pd['J_na_juncsl']/Vsl*(Naj-Nasl)+Pd['J_na_slmyo']/Vsl*(Nai-Nasl)-d_NaBsl

    #FluxNaSL=d_Nasl
    d_Nai = Pd['J_na_slmyo']/Vmyo*(Nasl-Nai)             # [mM/msec] 
    
    # Potassium Concentration
    I_K_tot = I_to+I_kr+I_ks+I_ki-2*I_nak+I_CaK+I_kp     # [uA/uF]
    d_Ki =0 # -I_K_tot*Cmem/(Vmyo*Frdy)

    # Calcium Concentrations
    I_Ca_tot_junc = I_Ca_junc+I_cabk_junc+I_pca_junc-2*I_ncx_junc                   # [uA/uF]
    I_Ca_tot_sl = I_Ca_sl+I_cabk_sl+I_pca_sl-2*I_ncx_sl            # [uA/uF]
    d_Caj = -I_Ca_tot_junc*Cmem/(Vjunc*2*Frdy)+Pd['J_ca_juncsl']/Vjunc*(Casl-Caj)   -J_CaB_junction+(J_SRCarel)*Vsr/Vjunc+J_SRleak*Vmyo/Vjunc  # Ca_j
    d_Casl = -I_Ca_tot_sl*Cmem/(Vsl*2*Frdy)+Pd['J_ca_juncsl']/Vsl*(Caj-Casl)  + Pd['J_ca_slmyo']/Vsl*(Cai-Casl)-J_CaB_sl   # Ca_sl
    d_Cai = -J_serca*Vsr/Vmyo-J_CaB_cytosol +Pd['J_ca_slmyo']/Vmyo*(Casl-Cai)

    ## Summing the current components
    I_Na_tot = I_Na_tot_junc + I_Na_tot_sl          # [uA/uF]
    I_Cl_tot = I_ClCa+I_Clbk                        # [uA/uF]
    I_Ca_tot = I_Ca_tot_junc+I_Ca_tot_sl
    I_tot = I_Na_tot+I_Cl_tot+I_Ca_tot+I_K_tot
    I_app = Pd['I_app'] if (t<5) else 0.0
    d_Vm = -(I_tot-I_app)

    ydot = [d_m,d_h, d_j, d_d, d_f,d_fcaBj, d_fcaBsl, d_xtos, d_ytos,d_xtof, d_ytof, d_xkr, d_xks, d_RyRr, d_RyRo, d_RyRi, d_NaBj, d_NaBsl, d_TnCL, d_TnCHc, d_TnCHm, d_CaM, d_Myoc, d_Myom,   d_SRB, d_SLLj, d_SLLsl, d_SLHj, d_SLHsl, d_Csqnb, d_Ca_sr, d_Naj, d_Nasl, d_Nai, d_Ki, d_Caj, d_Casl, d_Cai, d_Vm]

    ydot = list(map(lambda x,y:x*y, ydot, Pd['dynamic']))

    return ydot


