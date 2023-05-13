## Duncan Koelzer   
## Maneuver plots

# Imports
import numpy as np
import matplotlib.pyplot as plt
import math
import RequirementsAndParameters as RP
import importlib
importlib.reload(RP)

def PlotManeuverRequirements(W_S,q,cd0,AR,e,n,V,n_p,densRatio):

    # Calculation
    t_w = (q*cd0/W_S) + W_S*(n**2)/(q*np.pi*AR*e)
    w_p = (n_p/V) / t_w

    # Conversion to takeoff power
    conv = densRatio**(3/4)
    w_p_TO = w_p * conv

    # Plot
    # plt.plot(W_S,w_p_TO)
    # plt.plot(W_S,t_w)

    return w_p

# W_S array
N = RP.N
W_S = np.linspace(1,300,N)

# Input known parameters
CD0 = RP.CDO_cruise      # min drag coeff, cruise
AR = RP.AR               # Aspect ratio
e = RP.e_clean           # Oswald/span eff factor, cruise
V = RP.V_cruise_min      # Velocity (kts*1.68781 = ft/s)
n_p = RP.n_p             # Propeller eff at cruise 

#CD0 = 0.0297                    # min drag coeff
#AR = 11.28224                   # aspect ratio
#e = 0.85                        # Oswald/span eff factor
#V = 280*1.68781                 # velocity (kts*1.68781 = ft/s)
#n_p = 0.75                      # Propeller eff at cruise 
dens = 0.00107                  # density (slug/ft3)
densSL = 2.3769e-3              # density at sea level (slug/ft3)
densRatio = dens/densSL         # density ratio
turnRate = 3*np.pi/180          # angular velocity (deg/s*pi/180 = rad/s)
g = 32.17                       # gravitation accel (ft/s2)

# Calculated parameters
q = (1/2)*dens*(V**2)           # dynamic pressure (lbf/ft2)
# n = np.sqrt(1 + (turnRate*V/g)) # load factor
n = 3.2                         # load factor

# Plot
# plt.figure()
w_p = PlotManeuverRequirements(W_S,q,CD0,AR,e,n,V,n_p,densRatio)
# plt.title('Maneuver Requirements')
# plt.xlabel(' Wing Loading W/S')
# plt.ylabel('Power Loading W/P')
# plt.show()


