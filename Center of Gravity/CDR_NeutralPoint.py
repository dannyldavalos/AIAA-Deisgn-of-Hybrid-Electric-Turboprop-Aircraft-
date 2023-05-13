## Daniela L. Davalos
## A5: Neutral Point
# Updated 5/10/2023

# Imports
import numpy as np
import matplotlib.pyplot as plt
import math
import RequirementsAndParameters as RP
import importlib
importlib.reload(RP)  

# Aircraft parameters
S_w = RP.wingArea    # Area of wing [ft^2]
eta = 0.97                                  # From metabook/lecture slide 42
Ma = RP.Ma
AR_w = RP.AR
fuseLength = RP.fuseLength
Kf = 0.59353 # Interpolated from Table 8.1 from Raymer

# From OpenVSP
w_f = RP.F_w          # Fuselage width [ft]
L_f = RP.fuseLength        # Fuselage length [ft]
c = RP.MAC_w          # Mean aerodynamic chord [ft]
# l_h = 40         # Positon of tail lift with respect to cg [ft]
l_h = 56.2         # Positon of tail lift with respect to cg [ft]
nose2quarter = fuseLength - l_h
# S_h = 136.5         # Area of horizontal stabilizer [ft^2]
S_h = RP.S_horiz_tail         # Area of horizontal stabilizer [ft^2]
AR_h = RP.A_h         # Aspect ratio of horizontal stabilizer [ft^2]
Lambda_w = 25       # Sweep angle of wing [degrees]
Lambda_h = 10       # Sweep angle of horizontal tail [degrees]

dClwda = 2*np.pi*AR_w/ ( 2 + np.sqrt( ( ((AR_w/eta)**2)*( 1 + (np.tan(Lambda_w*np.pi/180))**2 - Ma**2) ) + 4 ) )
dCLh_clean_da = 2*np.pi*AR_h/ ( 2 + np.sqrt( ( ((AR_h/eta)**2)*( 1 + (np.tan(Lambda_h*np.pi/180))**2 - Ma**2) ) + 4 ) )
deda = 2*dClwda/(np.pi*AR_w)
dCLhda = dCLh_clean_da*( 1 - deda )
dCmfda = Kf*w_f**2*L_f / ( S_w*c*dClwda )

xnp = (( l_h*S_h*dCLhda/(c*S_w*dClwda) ) - ( dCmfda/dClwda ))*c # [ft] quarter chord

xnp_nose = nose2quarter + xnp
