## Kimberly Moreno
## A3: Cruise Speed Plots

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

    # Plot
    plt.plot(W_S,w_p_TO)
    # plt.plot(W_S,t_w)

    return w_p

# W_S array
N = 300
W_S = np.linspace(1,300,N)

# Input known parameters
V_cr = 287*1.68781              # maximum cruise velocity of Dash 8 (kts*1.68781 = ft/s)
cd0 = 0.02590592                    # from zero lift drag calculation
AR = 11.28224                   # From OpenVSP
dens = 0.0010567523             # density at 28,000 ft (slug/ft3)
n_p = 0.75                      # propeller efficiency during cruise from Table 3.3 in Gudmundsson
densSL = 2.3769e-3              # density at sea level (slug/ft3)
densRatio = dens/densSL         # density ratio

# Calculated parameters
q = (1/2)*dens*(V_cr**2)           # dynamic pressure (lbf/ft2)

W_P = PlotCruiseSpeedRequirements(W_S,V_cr,q,cd0,AR,n_p,densRatio)
# Plot
# plt.figure()
# plt.plot(W_S, W_P)
# plt.title('Cruise Speed')
# plt.xlabel(' Wing Loading W/S')
# plt.ylabel('Power Loading W/P')
# plt.show()