## Duncan Koelzer
## A3: Takeoff plots

# Imports
import numpy as np
import matplotlib.pyplot as plt
import RequirementsAndParameters as RP
import importlib
importlib.reload(RP)

def PlotTakeoffRequirements(W_S,sTOG,CL_max,rho,k1,k2,cD0,mu_g):

    # Calculate
    num1 = (k1*W_S/(sTOG*rho)) + 0.72*cD0
    num2 = (num1/CL_max) + mu_g
    p_w = num2/k2
    w_p = 1/p_w




    # Plot
    plt.plot(W_S,w_p)
    # plt.plot(W_S,p_w)

    return w_p


## Arrays
N = RP.N
W_S = np.linspace(0,300,N)

# Requirements
s_TOG = 4500/1.66           # takeoff length ( /1.66 as stated in Roskam)

# Parameters
CLmax = RP.CL_max_TO                 # Max lift coeff
CD0 = 0.02671093            # 
dens1 = 2.3769e-3           # Density at SL (slug/ft3)
dens2 = 2.0482e-3           # Density at h=5000ft (slug/ft3)
sigma1 = dens1/dens1        # Density ratio at SL
sigma2 = dens2/dens1        # Densitty ratio at h=5000ft

# Equation parameters (needed for military takeoff eq in Roskam)
k1 = 0.0376                 # From Roskam
mu_g = 0.03                 # Ground friction coeff
l_p = 4.6                   # For calculation of k2
propDiskLoading = 10        # Propeller disk loading range (10-30)

# Calculate k2 at each altitude
k2_1 = l_p * (sigma1/propDiskLoading)**(1/3)
k2_2 = l_p * (sigma2/propDiskLoading)**(1/3)

# Plot range for takeoff
# plt.figure()
plottedValues1 = PlotTakeoffRequirements(W_S,s_TOG,CLmax,dens1,k1,k2_1,CD0,mu_g)
plottedValues2 = PlotTakeoffRequirements(W_S,s_TOG,CLmax,dens1,k1,k2_2,CD0,mu_g)
# plt.title('Takeoff Requirements')
# plt.xlabel(' Wing loading W/S')
# plt.ylabel('Power Loading W/P')
# plt.show()



