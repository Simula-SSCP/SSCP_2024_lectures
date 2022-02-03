from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from default_dict import Pd, name2index
from grandi_bers import grandi_bers

y0 = np.load('SS_ventricular_reduced.npy')

T = np.linspace(0,1000,1001);
Y = odeint(grandi_bers, y0, T, (Pd,))
plt.figure(1)
plt.plot(T,Y[:, name2index("Vmo")])
plt.figure(2)
plt.plot(T,Y[:, name2index("Caio")]*1000)

Pd['epi']=1

#INa
Pd['GNa'] *=1

#INaK
Pd['IbarNaK'] *=1 

#Ito
if Pd['epi']==1:
    Pd['GtoSlow'] *= 1 #epi
    Pd['GtoFast'] *= 1 #epi0.88
else:
    Pd['GtoSlow'] *= 2.41 #endo
    Pd['GtoFast'] *= 0.012 #endo

#IKr
Pd['Gkr'] *= 1

#IKs
Pd['Gks'] *= 1

#IKr
Pd['Gkp'] *= 1

#IK1
Pd['Gki'] *= 1

#ICaL
Pd['pNa'] *= 1       # [cm/sec]
Pd['pCa'] *= 1       # [cm/sec]
Pd['pK'] *= 1        # [cm/sec]

#INCX
Pd['IbarNCX'] *= 1 

#ICaCl
Pd['GClCa'] *= 1

#Background Currents
Pd['GNaB'] *= 1
Pd['GCaB'] *= 1
Pd['GClB'] *= 1

Y_mod = odeint(grandi_bers, y0, T, (Pd,))
plt.figure(1)
plt.plot(T,Y_mod[:, name2index("Vmo")])
plt.legend((r'Default',r'$new$'))
plt.figure(2)
plt.plot(T,Y_mod[:, name2index("Caio")]*1000)
plt.legend((r'Default',r'$new$'))

