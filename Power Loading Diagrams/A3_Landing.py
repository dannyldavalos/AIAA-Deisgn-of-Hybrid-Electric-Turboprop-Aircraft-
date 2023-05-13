'''
A3: Landing Plots
Author: Logan Dunn

'''

# imports #
import numpy as np
import matplotlib.pyplot as plt
import math
import RequirementsAndParameters as RP
import importlib
importlib.reload(RP)

# functions #
def PlotLandingRequirements(rho, rho_sea, CL_max, S_land, S_a):
    Wland_Sref = (((float(rho) / float(rho_sea)) * CL_max) / (80 )) * float((0.6*S_land - S_a) )       # LEC 07
    
    avgWland_Wto = 0.98
    Wto_Sref = Wland_Sref / avgWland_Wto
    print('Wing Loading: {}'.format(Wto_Sref))
    return Wto_Sref

# requirements #
S_land = RP.L_length_max
#S_land = 4500           # max landing distance (ft)
S_a = 800               # estimated approach distance (ft)

# parameters #
CL_max = RP.CL_max_L
#rho_sea = RP.rho_SL
# CL_max = 1.9                                    # for landing (1.9 - 3.3) 
rho_sea = 0.0765                                # air density at sea level (lb/ft^3)
rho_5k = 0.066                                  # air density at 5000 ft (lb/ft^3)

#S_LG = (W / (mu * g * rho * S)) * (1 / ((C_d / mu) - C_l)) * math.log10(1 + ((rho * S) / (2 * W)) * ((C_d / mu) - C_l) * (V_td **2))

# plotting #
# plt.figure()
plot1 = PlotLandingRequirements(rho_5k, rho_sea, CL_max, S_land, S_a)
# plt.axvline(x = plot1, color = 'b', linestyle = '-', label = "Landing: Sea Level (CL_max_L = {})".format(str(CL_max)))
# plt.axvspan(0, plot1, alpha = 0.2)
# plt.title('Landing Requirements')
# plt.xlabel('Wing Loading (W/S)')
# plt.ylabel('Power Loading (W/P)')
# plt.xlim()
# plt.legend(loc = 'best')
# plt.show()


























