# Daniela L. Davalos
# EAE 130B
# V-n diagram
# May 2, 2023

import math
import numpy as np
import importlib
import matplotlib.pyplot as plt
import RequirementsAndParameters as RP
from intersect import intersection
np.set_printoptions(threshold=np.inf)
# Reloads the imports in case they are updated
importlib.reload(RP) 

# COnstants
N = 100
g = RP.g            # Acceleration due to gravity [ft/s^2]

# Imports
W = RP.WTO          #  Maximum take-off weight [lbf]
S = RP.wingArea     # Wing area [ft^2]
rho_o = 0.0023769     # Sea level density [slug/ft^23]
c = RP.MAC_w        # Mean aerodynamic chord [ft]
CL_aoa_deg = .1        # From CL vs alpha MSES curve
CL_aoa_rad = CL_aoa_deg*(180/np.pi)
CL_max = 2.13          # Max lift coefficient [-] (from MSES)
CL_min = -2       # Min lift coefficient [-] (from MSES)
n_max = 2.5         # Max load factor [-]
n_min = -1          # Min load factor [-]
h_c = 28000        # Cruising altitude [ft]
to_knots = 1.688

def earth_atmosphere_model(h):

    'Input altitude (ft) and output density [slug/ft^3]'
    'Dynamic viscosity [lbf*s/ft^2]'
    'temp [R]'
    T_o = 518.7    # R
    mu_o = 3.62e-7 # [lbf*s/ft^2]

    temp = 59 - .00356*h
    press = 2116 * ( (temp+459.7) / 518.6 )**5.256
    rho = press / ( 1718 * (temp + 459.7) )

    tempR = temp + 459.67 # convert degree F to R
    mu = mu_o*((tempR/T_o)**1.5)*( (T_o+198.72)/(tempR+198.72) ) # Sutherland's formula

    return rho, mu, tempR

def EAS(rho,rho_o,IAS):

    'EAS is the equivalent airspeed'
    'IAS is the indicated airspeed'
    'rho is the density of the air at the altitude you are flying at'
    'rho_o is the density of the air at sea level'

    EAS = IAS * np.sqrt( rho/rho_o )
    return EAS

rho_c,_,_ = earth_atmosphere_model(h_c)

'--------------------------------------------------------------'
'--------------------- Max takeoff weight ---------------------'
'--------------------------------------------------------------'

# Stalling speed at normal level flight
V_S1 = (np.sqrt( 2*W / ( rho_o*S*CL_max ) ))
n_S1 = 1                                # 1g
n_S1_array = np.linspace(0,n_max,N)
V_S1_array = (np.sqrt(n_S1_array))*V_S1             # [knots]

# Design maneuvering speed or corner speed
V_S_1 = (np.sqrt( -2*W / ( rho_o*S*CL_min ) ))
n_S_1 = -1                              # -1g
n_S_1_array = np.linspace(-1,0,N)
V_S_1_array = (np.sqrt( 2*W*n_S_1_array / ( rho_o*S*CL_min ) ))

# Design maneuvering speed or corner speed
V_A = (np.sqrt(n_max))*V_S1 # [knots]
n_A = n_max
n_A_array = np.linspace(1,n_max,N)

# Design speed for maximum gust intensity
mu = 2 * (W/S) / ( rho_o*c*CL_aoa_rad*g)
K_g = 0.88*mu / ( 5.3 + mu )
U_de_C = 56     # FAR 25: Reference gust at sea level, EAS [ft/s]
V_cruise = (RP.V_cruise_target )    
V_C_EAS = EAS(rho_c,rho_o,V_cruise)            # EAS [ft/s]
V_B = V_S1 * ( 1 + ( K_g*U_de_C*V_cruise*rho_o*CL_aoa_rad / ( 2*W/S) ) )  # [ft/s]

# Design cruising speed ## FIX THIS????? DELTAV?
deltaV = 100    # [knots]
V_C = V_B + deltaV  # [knots]
n_C = n_min

# Design dive speed
V_D = 1.13*V_C  # [knots]
n_D = 0
n_D2 = n_max

'Gust loads'

# V_B
U_de_B = U_de_C
V_B_array = (np.linspace(0,V_B,N))    # [knots]
n_g_B = 1 + ( K_g*U_de_B*V_B_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]
n_g_B_neg = 1 - ( K_g*U_de_B*V_B_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]

# V_C
V_C_array = (np.linspace(0,V_C,N))    # [knots]
n_g_C = 1 + ( K_g*U_de_C*V_C_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]
n_g_C_neg = 1 - ( K_g*U_de_C*V_C_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]

# V_D
U_de_D = 0.5*U_de_C
V_D_array = (np.linspace(0,V_D,N))    # [knots]
n_g_D = 1 + ( K_g*U_de_D*V_D_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]
n_g_D_neg = 1 - ( K_g*U_de_D*V_D_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]

# Maximum weight V-n diagram
lw = 1
fig, ax = plt.subplots()
ax.plot(V_S1_array/to_knots, n_S1_array, c = 'b')
ax.plot(V_S_1_array/to_knots, n_S_1_array, c = 'b')

x_VCD = [V_C/to_knots, V_D/to_knots]
y_VCD = [n_min, 0]
ax.plot(x_VCD,y_VCD, c = 'b')
ax.hlines(y = n_max, xmin = V_A/to_knots, xmax = V_D/to_knots, colors = 'b')
ax.hlines(y = n_min, xmin = V_S_1/to_knots, xmax = V_C/to_knots, colors = 'b')
ax.vlines(x = V_D/to_knots, ymin = 0, ymax = n_max, colors = 'b')
ax.vlines(x = V_S1/to_knots, ymin = 0, ymax = n_S1, colors = 'k',linestyles='dashed',linewidth = lw)
ax.vlines(x = V_S_1/to_knots, ymin = n_min, ymax = 0, colors = 'k',linestyles='dashed',linewidth = lw)
ax.vlines(x = V_A/to_knots, ymin = n_min, ymax = n_max, colors = 'k',linestyles='dashed',linewidth = lw)
ax.vlines(x = V_B/to_knots, ymin = n_min, ymax = n_max, colors = 'k',linestyles='dashed',linewidth = lw)
ax.vlines(x = V_C/to_knots, ymin = n_min, ymax = n_max, colors = 'k',linestyles='dashed',linewidth = lw)
ax.hlines(y = 1, xmin = 0, xmax = V_D/to_knots, colors = 'k',linestyles='dashed',linewidth = lw)
ax.axhline(y=0, color='k')
'Gust Lines'
# V_B
ax.plot(V_B_array/to_knots,n_g_B, c = 'r', linestyle='-',linewidth = lw,label='$U_B$ gust = %.0f ft/s' %(U_de_B)) 
ax.plot(V_B_array/to_knots,n_g_B_neg, c = 'r', linestyle='-',linewidth = lw) 
# V_C
ax.plot(V_C_array/to_knots,n_g_C, c = 'r', linestyle='--',linewidth = lw,label='$U_C$ gust = %.0f ft/s' %(U_de_C)) 
ax.plot(V_C_array/to_knots,n_g_C_neg,c = 'r', linestyle='--',linewidth = lw)
# V_D
ax.plot(V_D_array/to_knots,n_g_D, c = 'r', linestyle='-.',linewidth = lw,label='$U_D$ gust = %.0f ft/s' %(U_de_D)) 
ax.plot(V_D_array/to_knots,n_g_D_neg,c = 'r', linestyle='-.',linewidth = lw)

# Connecting lines
# BD pos
x_VBD_gp = [V_B_array[-1]/to_knots, V_D_array[-1]/to_knots]
y_VBD_gp = [n_g_B[-1], n_g_D[-1]]
ax.plot(x_VBD_gp,y_VBD_gp, c = 'r',linestyle='-',linewidth = lw)
# BD neg
x_VBD_gn = [V_B_array[-1]/to_knots, V_D_array[-1]/to_knots]
y_VBD_gn = [n_g_B_neg[-1], n_g_D_neg[-1]]
ax.plot(x_VBD_gn,y_VBD_gn, c = 'r',linestyle='-',linewidth = lw)
# CD pos
x_VCD_gp = [V_C_array[-1]/to_knots, V_D_array[-1]/to_knots]
y_VCD_gnp = [n_g_C[-1], n_g_D[-1]]
ax.plot(x_VCD_gp,y_VCD_gnp, c = 'r',linestyle='dashed',linewidth = lw)
# CD neg
x_VCD_gn = [V_C_array[-1]/to_knots, V_D_array[-1]/to_knots]
y_VCD_gn = [n_g_C_neg[-1], n_g_D_neg[-1]]
ax.plot(x_VCD_gn,y_VCD_gn, c = 'r',linestyle='dashed',linewidth = lw)

# Scatter Points
os = 20
ax.scatter(V_S1/to_knots,1,c = 'b',zorder=os)
ax.scatter(V_A/to_knots,n_max,c = 'b',zorder=os)
ax.scatter(V_C/to_knots,n_min,c = 'b',zorder=os)
ax.scatter(V_D/to_knots,n_max,c = 'b',zorder=os)
ax.scatter(V_S_1/to_knots,-1,c = 'b',zorder=os)

# Bound annotations
bf = 9
ax.annotate('$G$', ((V_S_1/to_knots) +7, n_S_1 + .1), color='b', fontsize=bf)
ax.annotate('$A$', ((V_A/to_knots) -18 , n_max - .05 ), color='b', fontsize=bf)
ax.annotate('$B$', ((V_B/to_knots) -12 , n_max - .17 ), color='k', fontsize=bf)
ax.annotate('$-C$', ((V_C/to_knots) +8 , n_min - .05 ), color='b', fontsize=bf)
ax.annotate('$D$', ((V_D/to_knots) +8 , n_max - .05 ), color='b', fontsize=bf)
ax.annotate('$V_S$', ((V_S1/to_knots) +7 , n_S1 - .2 ), color='b', fontsize=bf)

# Legend
pf = 7
ax.annotate('$V_{{S}} = {0:.0f}$ kts'.format( V_S1/to_knots ), xy=(0.05, 0.95), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{A}} = {0:.0f}$ kts'.format( V_A/to_knots ), xy=(0.05, 0.95-.05), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{B}} = {0:.0f}$ kts'.format( V_B/to_knots ), xy=(0.05, 0.95-.05*2), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{C}} = {0:.0f}$ kts'.format( V_C/to_knots ), xy=(0.05, 0.95-.05*3), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{D}} = {0:.0f}$ kts'.format( V_D/to_knots ), xy=(0.05, 0.95-.05*4), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{G}} = {0:.0f}$ kts'.format( V_S_1/to_knots ), xy=(0.05, 0.95-.05*5), xycoords='axes fraction',fontsize=pf)
plt.xlabel("Equivalent air speed (knots)")
plt.ylabel("$n$")
plt.xlim(0, 460)
plt.ylim(-1.5, 3)
ax.set_xticks([100,200,300,400])
plt.legend(loc='lower left',fontsize=pf,frameon=False)
ax.set_xlim(left=0)
plt.savefig('V-n_diagram_MAX.pdf') 
plt.close('V-n_diagram_MAX.pdf')

'--------------------------------------------------------------'
'--------------------- Min takeoff weight ---------------------'
'--------------------------------------------------------------'
W = RP.W_min
# Stalling speed at normal level flight
V_S1 = (np.sqrt( 2*W / ( rho_o*S*CL_max ) ))
n_S1 = 1                                # 1g
n_S1_array = np.linspace(0,n_max,N)
V_S1_array = (np.sqrt(n_S1_array))*V_S1             # [knots]

# Design maneuvering speed or corner speed
V_S_1 = (np.sqrt( -2*W / ( rho_o*S*CL_min ) ))
n_S_1 = -1                              # -1g
n_S_1_array = np.linspace(-1,0,N)
V_S_1_array = (np.sqrt( 2*W*n_S_1_array / ( rho_o*S*CL_min ) ))

# Design maneuvering speed or corner speed
V_A = (np.sqrt(n_max))*V_S1 # [knots]
n_A = n_max
n_A_array = np.linspace(1,n_max,N)

# Design speed for maximum gust intensity
mu = 2 * (W/S) / ( rho_o*c*CL_aoa_rad*g)
K_g = 0.88*mu / ( 5.3 + mu )
U_de_C = 56     # FAR 25: Reference gust at sea level, EAS [ft/s]
V_cruise = (RP.V_cruise_target )    
V_C_EAS = EAS(rho_c,rho_o,V_cruise)            # EAS [ft/s]
V_B = V_S1 * ( 1 + ( K_g*U_de_C*V_cruise*rho_o*CL_aoa_rad / ( 2*W/S) ) )  # [ft/s]

# Design cruising speed ## FIX THIS????? DELTAV?
deltaV = 50    # [knots]
V_C = V_B + deltaV  # [knots]
n_C = n_min

# Design dive speed
V_D = 1.13*V_C  # [knots]
n_D = 0
n_D2 = n_max

'Gust loads'

# V_B
U_de_B = U_de_C
V_B_array = (np.linspace(0,V_B,N))    # [knots]
n_g_B = 1 + ( K_g*U_de_B*V_B_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]
n_g_B_neg = 1 - ( K_g*U_de_B*V_B_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]

# V_C
V_C_array = (np.linspace(0,V_C,N))    # [knots]
n_g_C = 1 + ( K_g*U_de_C*V_C_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]
n_g_C_neg = 1 - ( K_g*U_de_C*V_C_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]

# V_D
U_de_D = 0.5*U_de_C
V_D_array = (np.linspace(0,V_D,N))    # [knots]
n_g_D = 1 + ( K_g*U_de_D*V_D_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]
n_g_D_neg = 1 - ( K_g*U_de_D*V_D_array*rho_o*CL_aoa_rad / ( 2*W/S) )    # [knots]

# Minimum weight V-n diagram
lw = 1
fig, ax = plt.subplots()
ax.plot(V_S1_array/to_knots, n_S1_array, c = 'b')
ax.plot(V_S_1_array/to_knots, n_S_1_array, c = 'b')
x_VCD = [V_C/to_knots, V_D/to_knots]
y_VCD = [n_min, 0]
ax.plot(x_VCD,y_VCD, c = 'b')
x_AD = np.linspace(V_A/to_knots,V_D/to_knots,N)
y_AD = np.linspace(n_max,n_max,N)
#ax.hlines(y = n_max, xmin = V_A/to_knots, xmax = V_D/to_knots, colors = 'k',linewidth = lw)
ax.plot(x_AD,y_AD, c = 'k',linewidth = lw)
ax.hlines(y = n_min, xmin = V_S_1/to_knots, xmax = V_C/to_knots, colors = 'b')
ax.vlines(x = V_D/to_knots, ymin = 0, ymax = n_max, colors = 'b')
ax.vlines(x = V_S1/to_knots, ymin = 0, ymax = n_S1, colors = 'k',linestyles='dashed',linewidth = lw)
ax.vlines(x = V_S_1/to_knots, ymin = n_min, ymax = 0, colors = 'k',linestyles='dashed',linewidth = lw)
ax.vlines(x = V_A/to_knots, ymin = n_min, ymax = n_max, colors = 'k',linestyles='dashed',linewidth = lw)
ax.vlines(x = V_B/to_knots, ymin = n_min, ymax = n_g_B[-1], colors = 'k',linestyles='dashed',linewidth = lw)
ax.vlines(x = V_C/to_knots, ymin = n_min, ymax = n_g_C[-1], colors = 'k',linestyles='dashed',linewidth = lw)
ax.hlines(y = 1, xmin = 0, xmax = V_D/to_knots, colors = 'k',linestyles='dashed',linewidth = lw)
ax.axhline(y=0, color='k')
'Gust Lines'
# V_B
ax.plot(V_B_array/to_knots,n_g_B, c = 'r', linestyle='-',linewidth = lw,label='$U_B$ gust = %.0f ft/s' %(U_de_B)) 
ax.plot(V_B_array/to_knots,n_g_B_neg, c = 'r', linestyle='-',linewidth = lw) 
# V_C
ax.plot(V_C_array/to_knots,n_g_C, c = 'r', linestyle='--',linewidth = lw,label='$U_C$ gust = %.0f ft/s' %(U_de_C)) 
ax.plot(V_C_array/to_knots,n_g_C_neg,c = 'r', linestyle='--',linewidth = lw)
# V_D
ax.plot(V_D_array/to_knots,n_g_D, c = 'r', linestyle='-.',linewidth = lw,label='$U_D$ gust = %.0f ft/s' %(U_de_D)) 
ax.plot(V_D_array/to_knots,n_g_D_neg,c = 'r', linestyle='-.',linewidth = lw)

# Red gust connecting lines
# BD pos
x_VBD_gp = [V_B_array[-1]/to_knots, V_D_array[-1]/to_knots]
y_VBD_gp = [n_g_B[-1], n_g_D[-1]]
ax.plot(x_VBD_gp,y_VBD_gp, c = 'r',linestyle='-',linewidth = lw)
# BD neg
x_VBD_gn = [V_B_array[-1]/to_knots, V_D_array[-1]/to_knots]
y_VBD_gn = [n_g_B_neg[-1], n_g_D_neg[-1]]
ax.plot(x_VBD_gn,y_VBD_gn, c = 'r',linestyle='-',linewidth = lw)
# CD pos
x_VCD_gp = [V_C_array[-1]/to_knots, V_D_array[-1]/to_knots]
y_VCD_gp = [n_g_C[-1], n_g_D[-1]]
ax.plot(x_VCD_gp,y_VCD_gp, c = 'r',linestyle='dashed',linewidth = lw)
# CD neg
x_VCD_gn = [V_C_array[-1]/to_knots, V_D_array[-1]/to_knots]
y_VCD_gn = [n_g_C_neg[-1], n_g_D_neg[-1]]
ax.plot(x_VCD_gn,y_VCD_gn, c = 'r',linestyle='dashed',linewidth = lw)

# Intersections
xi1,yi1 = intersection(x_AD,y_AD,V_B_array/to_knots,n_g_B)
#ax.scatter(xi1,yi1)
xi2,yi2 = intersection(x_AD,y_AD,x_VBD_gp,y_VBD_gp)
#ax.scatter(xi2,yi2)
xi3,yi3 = intersection(x_AD,y_AD,x_VCD_gp,y_VCD_gp)
#ax.scatter(xi3,yi3)

# Bounds
ax.hlines(y = n_max, xmin = V_A/to_knots, xmax = xi1, colors = 'b')
ax.hlines(y = n_max, xmin = xi3, xmax = V_D/to_knots, colors = 'b')

# Blue bound connecting lines
x_lin1 = [xi1, V_C/to_knots]
y_lin1 = [n_max, n_g_C[-1]]
ax.plot(x_lin1,y_lin1, c = 'b',linestyle='-')
x_lin2 = [V_C_array[-1]/to_knots, xi3]
y_lin2 = [n_g_C[-1], n_max]
ax.plot(x_lin2,y_lin2, c = 'b',linestyle='-')

# Scatter Points
os = 20
ax.scatter(V_S1/to_knots,1,c = 'b',zorder=os)
ax.scatter(V_A/to_knots,n_max,c = 'b',zorder=os)
ax.scatter(V_B/to_knots,n_g_B[-1],c = 'b',zorder=os)
ax.scatter(V_C/to_knots,n_g_C[-1],c = 'b',zorder=os)
ax.scatter(V_C/to_knots,n_min,c = 'b',zorder=os)
ax.scatter(V_D/to_knots,n_max,c = 'b',zorder=os)
ax.scatter(V_S_1/to_knots,-1,c = 'b',zorder=os)

# Bound annotations
bf = 9
ax.annotate('$G$', ((V_S_1/to_knots) +7, n_S_1 + .1), color='b', fontsize=bf)
ax.annotate('$A$', ((V_A/to_knots) -18 , n_max - .05 ), color='b', fontsize=bf)
ax.annotate('$B$', ((V_B/to_knots) -18 , n_g_B[-1] + .05 ), color='b', fontsize=bf)
ax.annotate('$-B$', ((V_B/to_knots) -22 , n_g_B_neg[-1] - .14 ), color='r', fontsize=bf)
ax.annotate('$C$', ((V_C/to_knots) +8 , n_g_C[-1] + .05 ), color='b', fontsize=bf)
ax.annotate('$-C$', ((V_C/to_knots) +8 , n_min - .05 ), color='b', fontsize=bf)
ax.annotate('$D$', ((V_D/to_knots) +8 , n_max - .05 ), color='b', fontsize=bf)
ax.annotate('$V_S$', ((V_S1/to_knots) +7 , n_S1 - .2 ), color='b', fontsize=bf)

# Legend
pf = 7
ax.annotate('$V_{{S}} = {0:.0f}$ kts'.format( V_S1/to_knots ), xy=(0.05, 0.95), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{A}} = {0:.0f}$ kts'.format( V_A/to_knots ), xy=(0.05, 0.95-.05), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{B}} = {0:.0f}$ kts'.format( V_B/to_knots ), xy=(0.05, 0.95-.05*2), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{C}} = {0:.0f}$ kts'.format( V_C/to_knots ), xy=(0.05, 0.95-.05*3), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{D}} = {0:.0f}$ kts'.format( V_D/to_knots ), xy=(0.05, 0.95-.05*4), xycoords='axes fraction',fontsize=pf)
ax.annotate('$V_{{G}} = {0:.0f}$ kts'.format( V_S_1/to_knots ), xy=(0.05, 0.95-.05*5), xycoords='axes fraction',fontsize=pf)
plt.xlabel("Equivalent air speed (knots)")
plt.ylabel("$n$")
plt.xlim(0, 430)
plt.ylim(-1.5, 3)
ax.set_xticks([100,200,300,400])
plt.legend(loc='lower left',fontsize=pf,frameon=False)
ax.set_xlim(left=0)
plt.savefig('V-n_diagram_MIN.pdf') 
plt.close('V-n_diagram_MIN.pdf')

plt.show()
