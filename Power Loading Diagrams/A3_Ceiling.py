## Daniela L. Davalos
## A3: Absolute Ceiling Plot

# Imports
import numpy as np
import matplotlib.pyplot as plt
import math
import RequirementsAndParameters as RP
import importlib
importlib.reload(RP)

def PlotAbsCeilingRequirements(W_S,W_T,n_p,V_cruise,densRatio):
    # Plot
    
    w_p = ( n_p*W_T ) / V_cruise

    # Convert to takeoff power
    conv = densRatio**(3/4)
    w_p_TO = w_p*conv

    # plt.plot(W_S,w_p_TO)

    return w_p_TO

# Arrays
N = RP.N
W_S = np.linspace(1,300,N)
T_W = np.empty(N)

# Requirements
V_cruise = RP.V_cruise_target    # Target cruise speed [knots --> ft/s]
CL_max = RP.CL_max_cruise
#V_cruise = 350*1.688    # Target cruise speed [knots --> ft/s]
rho = 0.00095801        # Air density [slugs/ft^3]
V = np.sqrt(2*W_S/(rho*CL_max))

# Parameters
CD0 = RP.CDO_TO_GU            # From drag polar for take-off flaps gear up, calculated previously
e = 0.85                # Span efficiency for clean-cruise, from Table 3.6 (page 127) in Roskam
AR = RP.AR           # From OpenVSP
n_p = 0.75              # Propeller efficieny during climb, from Table 3.3 in Gudmundsson
dens = 0.00107          # density (slug/ft3)
densSL = 2.3769e-3      # density at sea level (slug/ft3)
densRatio = dens/densSL # density ratio

# Calculations
k = 1 / ( np.pi*e*AR )
T_W_constant = 2*(np.sqrt(k*CD0))
T_W.fill(T_W_constant)
W_T = 1 / T_W

print('k:  {:,.2f}'.format(k))

# Plot range for absolute ceiling
# plt.figure()
plottedValues1 = PlotAbsCeilingRequirements(W_S,W_T,n_p,V,densRatio)
# plt.title('Absolute Ceiling Requirements')
# plt.xlabel('Wing loading W/S')
# plt.ylabel('Power Loading W/P')

# plt.figure()
# plt.plot(W_S,T_W)
# plt.title('Absolute Ceiling Requirements')
# plt.xlabel('W/S')
# plt.ylabel('T/W')
# plt.show()

