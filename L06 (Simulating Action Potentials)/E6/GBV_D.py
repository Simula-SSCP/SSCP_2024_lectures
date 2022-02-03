from math import pi

Pd = {}
## Model Parameters
## EPI or ENDO?
Pd['epi']=1

Pd['I_app'] = 6

# Constants
Pd['R'] = 8314       # [J/kmol*K]  
Pd['Frdy'] = 96485   # [C/mol]  
Pd['Temp'] = 310     # [K]
Pd['Cmem'] = 1.3810e-10   # [F] membrane capacitance

# Cell geometry
Pd['cellLength'] = 100     # cell length [um]
Pd['cellRadius'] = 10.25   # cell radius [um]
Pd['Vmyo_ratio'] = 0.65
Pd['Vsr_ratio'] = 0.035
Pd['Vsl_ratio'] = 0.02
Pd['Vjunc_ratio'] = 0.00539

# Inter-compartmental fluxes
Pd['J_ca_juncsl'] =1/1.2134e12 # [L/msec] = 8.2413e-13
Pd['J_ca_slmyo'] = 1/2.68510e11 # [L/msec] = 3.2743e-12
Pd['J_na_juncsl'] = 1/(1.6382e12/3*100) # [L/msec] = 6.1043e-13
Pd['J_na_slmyo'] = 1/(1.8308e10/3*100)  # [L/msec] = 5.4621e-11

# Fractional currents in compartments
Pd['Fjunc'] = 0.11   
Pd['Fjunc_CaL'] = 0.9 

# Fixed ion concentrations     
Pd['Cli'] = 15   # Intracellular Cl  [mM]
Pd['Clo'] = 150  # Extracellular Cl  [mM]
Pd['Ko']= 5.4   # Extracellular K   [mM]
Pd['Nao'] = 140  # Extracellular Na  [mM]
Pd['Cao'] = 1.8  # Extracellular Ca  [mM]1.8
Pd['Mgi'] = 1.    # Intracellular Mg  [mM]

# Na transport parameters
Pd['GNa']=23;
Pd['GNaB'] = 0.597e-3    # [mS/uF] 0.897e-3
Pd['IbarNaK'] = 1.0*1.8#1.90719;     # [uA/uF]
Pd['KmNaip'] = 11        # [mM]11
Pd['KmKo'] =1.5         # [mM]1.5
Pd['Q10NaK'] = 1.63  
Pd['Q10KmNai'] = 1.39

## K current parameters
Pd['pNaK'] = 0.01833      
Pd['Gkp'] = 2*0.001
Pd['Gkr'] = 0.035
Pd['Gki'] = 0.35
Pd['Gks'] = 0.0035
if Pd['epi']==1:
    Pd['GtoSlow'] = 1.0*0.13*0.12 #epi
    Pd['GtoFast'] = 1.0*0.13*0.88 #epi0.88
else:
    Pd['GtoSlow'] = 0.13*0.3*0.964 #endo
    Pd['GtoFast'] = 0.13*0.3*0.036 #endo
Pd['markov_iks'] = 0  

# Cl current parameters
Pd['GClCa'] =0.5*0.109625   # [mS/uF]
Pd['GClB'] = 1*9e-3        # [mS/uF]
Pd['KdClCa'] = 100e-3    # [mM]

# I_Ca parameters
Pd['pNa'] = 0.50*1.5e-8       # [cm/sec]
Pd['pCa'] = 0.50*5.4e-4       # [cm/sec]
Pd['pK'] = 0.50*2.7e-7        # [cm/sec]
Pd['Q10CaL'] = 1.8       

## Ca transport parameters
Pd['IbarNCX'] = 1.0*4.5  # [uA/uF] - 9 in rabbit
Pd['KmCai'] = 3.59e-3    # [mM]
Pd['KmCao'] = 1.3        # [mM]
Pd['KmNai'] = 12.29      # [mM]
Pd['KmNao'] = 87.5       # [mM]
Pd['ksat'] = 0.32        # [none]  
Pd['nu'] = 0.27          # [none]
Pd['Kdact'] = 0.150e-3   # [mM] 
Pd['Q10NCX'] = 1.57      # [none]
Pd['IbarSLCaP'] = 0.0673 # IbarSLCaP FEI changed [uA/uF](2.2 umol/L cytosol/sec)[uA/uF]
Pd['KmPCa'] = 0.5e-3     # [mM] 
Pd['GCaB'] = 5.513e-4    # [uA/uF] 3
Pd['Q10SLCaP'] = 2.35    # [none]

# SR flux parameters
Pd['Q10SRCaP'] = 2.6          # [none]
Pd['Vmax_SRCaP'] = 1.0*5.3114e-3  # [mM/msec] (286 umol/L cytosol/sec)
Pd['Kmf'] = 0.246e-3          # [mM] default
Pd['Kmr'] = 1.7               # [mM]L cytosol
Pd['hillSRCaP'] = 1.787       # [mM]
Pd['ks'] = 25                 # [1/ms]      
Pd['koCa'] = 10               # [mM^-2 1/ms]   #default 10   modified 20
Pd['kom'] = 0.06              # [1/ms]     
Pd['kiCa'] = 0.5              # [1/mM/ms]
Pd['kim'] = 0.005             # [1/ms]
Pd['ec50SR'] = 0.45           # [mM]

# Buffering parameters
# koff: [1/s] = 1e-3*[1/ms];  kon: [1/uM/s] = [1/mM/ms]
Pd['Bmax_Naj'] = 7.561       # [mM] # Bmax_Naj = 3.7; (c-code difference?)  # Na buffering
Pd['Bmax_Nasl'] = 1.65       # [mM]
Pd['koff_na'] = 1e-3         # [1/ms]
Pd['kon_na'] = 0.1e-3        # [1/mM/ms]
Pd['Bmax_TnClow'] = 70e-3    # [mM]                      # TnC low affinity
Pd['koff_tncl'] = 19.6e-3    # [1/ms] 
Pd['kon_tncl'] = 32.7        # [1/mM/ms]
Pd['Bmax_TnChigh'] = 140e-3  # [mM]                      # TnC high affinity 
Pd['koff_tnchca'] = 0.032e-3 # [1/ms] 
Pd['kon_tnchca'] = 2.37      # [1/mM/ms]
Pd['koff_tnchmg'] = 3.33e-3  # [1/ms] 
Pd['kon_tnchmg'] = 3e-3      # [1/mM/ms]
Pd['Bmax_CaM'] = 24e-3       # [mM] **? about setting to 0 in c-code**   # CaM buffering
Pd['koff_cam'] = 238e-3      # [1/ms] 
Pd['kon_cam'] = 34           # [1/mM/ms]
Pd['Bmax_myosin'] = 140e-3   # [mM]                      # Myosin buffering
Pd['koff_myoca'] = 0.46e-3   # [1/ms]
Pd['kon_myoca'] = 13.8       # [1/mM/ms]
Pd['koff_myomg'] = 0.057e-3  # [1/ms]
Pd['kon_myomg'] = 0.0157     # [1/mM/ms]
Pd['Bmax_SR'] = 19*.9e-3     # [mM] (Bers text says 47e-3) 19e-3
Pd['koff_sr'] = 60e-3        # [1/ms]
Pd['kon_sr'] = 100           # [1/mM/ms]
Pd['Bmax_SLlowsl'] = 37.4e-3        # [mM]    # SL buffering
Pd['Bmax_SLlowj'] = 4.6e-3*0.1    # [mM]    #Fei *0.1!!! junction reduction factor
Pd['koff_sll'] = 1300e-3     # [1/ms]
Pd['kon_sll'] = 100          # [1/mM/ms]
Pd['Bmax_SLhighsl'] = 13.4e-3       # [mM] 
Pd['Bmax_SLhighj'] = 1.65e-3*0.1  # [mM] #Fei *0.1!!! junction reduction factor
Pd['koff_slh'] = 30e-3       # [1/ms]
Pd['kon_slh'] = 100          # [1/mM/ms]
Pd['Bmax_Csqn'] = 140e-3            # [mM] # Bmax_Csqn = 2.6;      # Csqn buffering
Pd['koff_csqn'] = 65         # [1/ms] 
Pd['kon_csqn'] = 100         # [1/mM/ms] 

# Mark all states as dynamic ODEs:
Pd['dynamic'] = [1]*39

# Define a default initial condition:
mo = 1.405627e-3
ho = 9.867005e-1
jo = 9.915620e-1 
do = 7.175662e-6 
fo = 1.000681 
fcaBjo = 2.421991e-2
fcaBslo = 1.452605e-2
xtoso = 4.051574e-3
ytoso = 9.945511e-1 
xtofo = 4.051574e-3 
ytofo =  9.945511e-1 
xkro = 8.641386e-3 
xkso =  5.412034e-3
RyRro = 8.884332e-1
RyRoo = 8.156628e-7 
RyRio = 1.024274e-7 
NaBjo = 3.539892
NaBslo = 7.720854e-1 
TnCLo = 8.773191e-3 
TnCHco = 1.078283e-1 
TnCHmo = 1.524002e-2 
CaMo = 2.911916e-4 
Myoco = 1.298754e-3 
Myomo = 1.381982e-1
SRBo = 2.143165e-3 
SLLjo = 9.566355e-3 
SLLslo = 1.110363e-1 
SLHjo = 7.347888e-3 
SLHslo = 7.297378e-2 
Csqnbo =  1.242988
Ca_sro = 0.1e-1 
Najo = 9.06
Naslo = 9.06
Naio = 9.06
Kio = 120. 
Cajo = 1.737475e-4 
Caslo =  1.031812e-4 
Caio = 8.597401e-5 
Vmo = -8.09763e+1 
     

y0 = [mo, ho, jo, do, fo, fcaBjo, fcaBslo, xtoso, ytoso, xtofo, ytofo, xkro, xkso,RyRro, RyRoo, RyRio, NaBjo, NaBslo, TnCLo, TnCHco, TnCHmo, CaMo, Myoco, Myomo,SRBo, SLLjo, SLLslo, SLHjo, SLHslo, Csqnbo,Ca_sro, Najo, Naslo, Naio, Kio, Cajo, Caslo, Caio, Vmo]

state_names = ["mo", "ho", "jo", "do", "fo", "fcaBjo", "fcaBslo", 
               "xtoso", "ytoso", "xtofo", "ytofo", "xkro", "xkso", "RyRro",
               "RyRoo", "RyRio", "NaBjo", "NaBslo", "TnCLo", "TnCHco", "TnCHmo",
               "CaMo", "Myoco", "Myomo", "SRBo", "SLLjo", "SLLslo", "SLHjo", 
               "SLHslo", "Csqnbo", "Ca_sro", "Najo", "Naslo", "Naio", "Kio", 
               "Cajo", "Caslo", "Caio", "Vmo"]

def name2index(name):
    """Take the name of a state in the model, return the index of that state in the solution vector y."""
    if type(name) == str:
        try:
            return state_names.index(name)
        except ValueError:
            raise ValueError("{} is not a state in the model".format(name))
    else:
        raise TypeError("Input must be the name of a state in the model as a str")

def index2name(index):
    if type(index) == int:
        return state_names[index]
    else:
        raise TypeError("Input must be the index of a state as an int")