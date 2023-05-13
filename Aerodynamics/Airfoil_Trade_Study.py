## Airfoil Trade Study, adapted from Kimberly Moreno's Cruise Speed Power Loading code
## Steven Martinez

# Imports
import numpy as np
import matplotlib.pyplot as plt
import math

def PlotCruiseSpeedRequirements(W_S,V_cr,q,cd0,AR,n_p,densRatio):

    # Calculation
    t_w = ((q*cd0)/W_S)+((W_S)/(q*np.pi*AR))
    # w_p = (n_p/V_cr)*((W_S/(q*cd0))+((q*np.pi*AR)/(W_S)))
    w_p = (n_p/V_cr)/(((q*cd0)/W_S)+((W_S)/(q*np.pi*AR)))

    # Conversion to takeoff power
    conv = densRatio**(3/4)
    w_p_TO = w_p * conv

    return w_p

# W_S array
N = 100
W_S = np.linspace(1,300,N)

# Input known parameters
V_cr = 287*1.68781              # maximum cruise velocity of Dash 8 (kts*1.68781 = ft/s)
cd0 = [0.02487842, 0.02490307, 0.02476912, 0.02474757, 0.02515984]                    # from zero lift drag calculation
AR = 11.28224                   # From OpenVSP
dens = 0.0010567523             # density at 28,000 ft (slug/ft3)
n_p = 0.75                      # propeller efficiency during cruise from Table 3.3 in Gudmundsson
densSL = 2.3769e-3              # density at sea level (slug/ft3)
densRatio = dens/densSL         # density ratio

# Calculated parameters
q = (1/2)*dens*(V_cr**2)           # dynamic pressure (lbf/ft2)

# Plot
plt.figure()
plt.plot(W_S, 550*PlotCruiseSpeedRequirements(W_S,V_cr,q,cd0[0],AR,n_p,densRatio),label='Lockheed-Georgia Supercritical')
plt.plot(W_S, 550*PlotCruiseSpeedRequirements(W_S,V_cr,q,cd0[1],AR,n_p,densRatio),label='Whitcomb Integral Supercritical')
plt.plot(W_S, 550*PlotCruiseSpeedRequirements(W_S,V_cr,q,cd0[2],AR,n_p,densRatio),label='NASA SC(2)-0710')
# plt.plot(W_S, 550*PlotCruiseSpeedRequirements(W_S,V_cr,q,cd0[3],AR,n_p,densRatio),label='Sikorsky SC2110')
plt.plot(W_S, 550*PlotCruiseSpeedRequirements(W_S,V_cr,q,cd0[4],AR,n_p,densRatio),label='NASA SC(2)-0714')
# plt.legend(['Lockheed-Georgia Supercritical','Whitcomb Integral Supercritical', 'NASA SC(2)-0710', 'Sikorsky SC2110', 'NASA SC(2)-0714'])
plt.legend(loc='lower right')
plt.xlim([65,70])
plt.ylim([13.4,14.25])
plt.title('Cruise Speed Constraint')
plt.xlabel(' Wing Loading W/S')
plt.ylabel('Power Loading W/P')
plt.savefig('Airfoil_Study.pdf') 
plt.close('Airfoil_Study.pdf')
plt.show()
