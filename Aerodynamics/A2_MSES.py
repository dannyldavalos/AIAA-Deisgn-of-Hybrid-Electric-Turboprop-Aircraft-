import numpy as np
import matplotlib.pyplot as plt
import importlib
import RequirementsAndParameters as RP

# Reloads the imports in case they are updated
importlib.reload(RP)

def earth_atmosphere_model(h):

    'Input altitude (ft) and output density [slug/ft^3], dynamic viscosity [lbf*s/ft^2], and temp [R]'
    T_o = 518.7    # R
    mu_o = 3.62e-7 # [lbf*s/ft^2]

    temp = 59 - .00356*h
    press = 2116 * ( (temp+459.7) / 518.6 )**5.256
    rho = press / ( 1718 * (temp + 459.7) )

    tempR = temp + 459.67 # convert degree F to R
    mu = mu_o*((tempR/T_o)**1.5)*( (T_o+198.72)/(tempR+198.72) ) # Sutherland's formula

    return rho, mu, tempR

# Constants
N = 10
l_c = RP.MAC_w
R = RP.R

# Plot geometry of airfoil at cruise, takeoff, and landing configurations
airfoil_C = 'Data/airfoil_cruise.dat' 
airfoil_C_x, airfoil_C_y = np.loadtxt(airfoil_C, unpack = True, skiprows = 2) 
airfoil_T = 'Data/airfoil_takeoff.dat' 
airfoil_T_x, airfoil_T_y = np.loadtxt(airfoil_T, unpack = True, skiprows = 2) 
airfoil_L = 'Data/airfoil_landing.dat' 
airfoil_L_x, airfoil_L_y = np.loadtxt(airfoil_L, unpack = True, skiprows = 2) 


plt.figure(figsize=(4,1))
plt.plot(airfoil_C_x,airfoil_C_y,linewidth = 2,color='black')
plt.axis('equal')
plt.xticks([]) 
plt.yticks([])
plt.box(False)
plt.savefig('Figures/airfoil_C.pdf') 
plt.close('Figures/airfoil_C.pdf')

plt.figure(figsize=(4,1))
plt.plot(airfoil_T_x,airfoil_T_y,linewidth = 2,color='black')
plt.axis('equal')
plt.xticks([]) 
plt.yticks([])
plt.box(False)
plt.savefig('Figures/airfoil_T.pdf') 
plt.close('Figures/airfoil_T.pdf')

plt.figure(figsize=(4,1))
plt.plot(airfoil_L_x,airfoil_L_y,linewidth = 2,color='black')
plt.axis('equal')
plt.xticks([]) 
plt.yticks([])
plt.box(False)
plt.savefig('Figures/airfoil_L.pdf') 
plt.close('Figures/airfoil_L.pdf')

# Takeoff flaps, gear up, h = 1500 - 10,000 ft
# h_array = np.linspace(1500,10000,N)
# V = RP.V_cruise_min     # Minimum cruise speed
V = RP.V_approach     # Minimum cruise speed
# h = np.average(h_array)
h = 4000
rho, mu, temp = earth_atmosphere_model(h)
Re = rho*V*l_c/mu
a_a = np.sqrt(1.4*R*temp*32.17)
Ma = V/a_a

print('\nTakeoff')
print('h: {:,.2f} ft'.format(h))
print('Ma: {:,.8f}'.format(Ma))
print('Re: {:,.4e}'.format(Re))

# Landing flaps, gear down, h =  3000 - 0 ft
# h_array = np.linspace(3000,0,N)
V  = RP.V_approach  # Approach speed
# h = np.average(h_array)
h = 8000
rho, mu, temp = earth_atmosphere_model(h)
Re = rho*V*l_c/mu
a_a = np.sqrt(1.4*R*temp*32.17)
Ma_2 = V/a_a
print('\nLanding')
print('h: {:,.2f} ft'.format(h))
print('Ma: {:,.8f}'.format(Ma_2))
print('Re: {:,.4e}'.format(Re))

filename_polar_TO = 'polar_takeoff.dat'
aoa_TO,cl_TO,cd_TO,_,_,_,_,_,_,_,_ = np.loadtxt(filename_polar_TO, unpack = True, skiprows = 13)
cl_max_TO = np.max(cl_TO)
filename_polar_L = 'polar_landing.dat'
aoa_L,cl_L,cd_L,_,_,_,_,_,_,_,_ = np.loadtxt(filename_polar_L, unpack = True, skiprows = 13)
cl_max_L = np.max(cl_L)


plt.figure(figsize=(6,5))
plt.plot(aoa_TO,cl_TO,linewidth = 3, label = "Takeoff")
plt.plot(aoa_L,cl_L,linewidth = 3, label = "Landing")
# plt.scatter()
plt.ylabel('$C_l$')
plt.xlabel(r'${\alpha}$ (deg)')
plt.legend(loc='best')
plt.savefig('Figures/MSES.pdf') 
plt.close('Figures/MSES.pdf')
# plt.title('Drag Polar')
plt.show()