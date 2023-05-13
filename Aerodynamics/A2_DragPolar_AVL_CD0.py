# Daniela L. Davalos
# EAE 130B
# Drag Polar Estimate
# April 18, 2023

import math
import numpy as np
import importlib
import array
import matplotlib.pyplot as plt
import CD0_Joint_Code as CD0
import CD_i_Raw_Data as CDi
np.set_printoptions(threshold=np.inf)

# Reloads the imports in case they are updated
importlib.reload(CD0)
importlib.reload(CDi)

N = 10

# Imports
CD0 = CD0.CD0

CL_top = np.arange(start=0, stop=2.3, step=0.1)
CL_bot = (-CL_top) + .1
CL_bot = np.delete(CL_bot, [0])

CD0_LNDGR = 0.002748
# Take-off, gear down
CD0_TO_GD = CD0[0] + CD0_LNDGR
CDi_TO_GD = CDi.CD_i_TO1
CD_TO_GD = CD0_TO_GD + CDi_TO_GD
CD_TO_GD_top = CD_TO_GD
CD_TO_GD_bot = np.delete(CD_TO_GD, [0]) 
# CD_TO_GD_n = CD_TO_GD_p
# CD_TO_GD_min = np.min(CD_TO_GD_p)
# CD_TO_GD_n = np.delete(CD_TO_GD_n, 0)
# CD_TO_GD_n = -1*(np.delete(CD_TO_GD_n, 0))
# CD_TO_GD_n = np.flip(CD_TO_GD_n)
# CD_TO_GD = np.append(CD_TO_GD_n,CD_TO_GD_p)
# CD_TO_GD = list(CD_TO_GD_n)
# CD_TO_GD_p = list(CD_TO_GD_p)
# CD_TO_GD.append(CD_TO_GD_p)
# new = list(np.concatenate(CD_TO_GD))
# CD_TO_GD = np.array(CD_TO_GD)

# Take-off, gear up
CD0_TO_GU = CD0[1] 
CDi_TO_GU = CDi.CD_i_TO2
CD_TO_GU = CD0_TO_GU + CDi_TO_GU
CD_TO_GU_top = CD_TO_GU
CD_TO_GU_bot = np.delete(CD_TO_GU, [0]) 

# Cruise
CD0_clean = CD0[2]
CDi_clean = CDi.CD_i_Cruise
CD_clean = CD0_clean + CDi_clean
CD_clean_top = CD_clean
CD_clean_bot = np.delete(CD_clean, [0])

# Landing, gear up
CD0_L_GU = CD0[3]
CDi_L_GU = CDi.CD_i_L1
CD_L_GU = CD0_L_GU + CDi_L_GU
CD_L_GU_top = CD_L_GU
CD_L_GU_bot = np.delete(CD_L_GU, [0]) 

# Landing, gear down
CD0_L_GD = CD0[4] + CD0_LNDGR
CDi_L_GD = CDi.CD_i_L2
CD_L_GD = CD0_L_GD + CDi_L_GD
CD_L_GD_top = CD_L_GD
CD_L_GD_bot = np.delete(CD_L_GD, [0]) 

# Plot drag polar
lw = 1      # linewidth
plt.figure()
# plt.title('Drag Polar')

plt.plot(CD_TO_GU_top[CL_top<2.07], CL_top[CL_top<2.07], label = 'Take-off flaps, gear up',linewidth = lw,color='green')
plt.plot(CD_TO_GU_bot[CL_bot>-2.07], CL_bot[CL_bot>-2.07],linewidth = lw,color='green')

plt.plot(CD_TO_GD_top[CL_top<2.07], CL_top[CL_top<2.07], label = 'Take-off flaps, gear down', linewidth = lw,color='blue')
plt.plot(CD_TO_GD_bot[CL_bot>-2.07], CL_bot[CL_bot>-2.07], linewidth = lw,color='blue')

plt.plot(CD_clean_top[CL_top<1.5], CL_top[CL_top<1.5], label = 'Cruise', linewidth = lw,color='c')
plt.plot(CD_clean_bot[CL_bot>-1.5], CL_bot[CL_bot>-1.5], linewidth = lw,color='c')

plt.plot(CD_L_GU_top[CL_top<2.13], CL_top[CL_top<2.13], label = 'Landing flaps, gear up', linewidth = lw,color='red')
plt.plot(CD_L_GU_bot[CL_bot>-2.13], CL_bot[CL_bot>-2.13], linewidth = lw,color='red')

plt.plot(CD_L_GD_top[CL_top<2.13], CL_top[CL_top<2.13], label = 'Landing flaps, gear down', linewidth = lw,color='m')
plt.plot(CD_L_GD_bot[CL_bot>-2.13], CL_bot[CL_bot>-2.13], linewidth = lw,color='m')


plt.xlabel("$C_D$")
plt.ylabel("$C_L$")
# plt.xlim([0,0.45])
# plt.ylim([-2,3])
plt.legend(loc='best')
plt.savefig('Figures/dragPolar.pdf') 
plt.close('Figures/dragPolar.pdf')
plt.show()

