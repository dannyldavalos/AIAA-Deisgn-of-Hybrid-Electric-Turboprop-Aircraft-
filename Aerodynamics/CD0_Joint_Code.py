import numpy as np
import math
import importlib
import RequirementsAndParameters as RP

# Reloads the imports in case they are updated
importlib.reload(RP)

CD0_LNDGR = 0.002748


##### FUSELAGE #####
# Requirements and Parameters
l_c = RP.fuseLength
R = RP.R
Q = 1
A_max = RP.area_fuse                    # Maximum cross-sectional area of the fuselage [ft^2]
f = l_c / np.sqrt( 4*A_max / np.pi )    # Fineness ratio [-]
# FF = 1 + (60/f**3) + (f/400)
FF = 0.9 + (5/f**1.5) + (f/400)
S_wet = RP.S_wet_fuse                   # Fuselage wetted area [ft^2] 
frontal_area = 1000                     # Frontal area of aircraft [ft^2]
S_ref = RP.wingArea                     # Wing area [ft^2]

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

def Reynolds_number(rho,V,l_c,mu):

    Re = rho*V*l_c/mu

    return Re

def find_CD0(h_array,V,FF,Q):

    h = np.average(h_array)
    rho, mu, temp = earth_atmosphere_model(h)
    Re = Reynolds_number(rho,V,l_c,mu)
    a_a = np.sqrt(1.4*R*temp*32.17)
    Ma = V/a_a

    C_f_laminar = 1.328 / np.sqrt(Re)
    C_f_turbulent = 0.455 / (  ((np.log10(Re))**2.58)*((1 + 0.144*(Ma**2))**0.65)  )
    C_f = C_f_laminar*.05 + C_f_turbulent*.95
    product = C_f*FF*Q*S_wet
    CD0 = product

    return CD0


N = 10

# Takeoff flaps, gear down, h = 0-1500 ft
h_array = np.linspace(0,1500,N)
V = 250*1.688 # knots --> [ft/s]
CD0 = find_CD0(h_array,V,FF,Q)
print('Takeoff flaps, gear down')
print('CD0: {:,.8f}'.format(CD0))
CD0_1_FUS = CD0

# Takeoff flaps, gear up, h = 1500 - 10,000 ft
h_array = np.linspace(1500,10000,N)
V = RP.V_cruise_min     # Minimum cruise speed
CD0 = find_CD0(h_array,V,FF,Q)
print('\nTakeoff flaps, gear up')
print('CD0: {:,.8f}'.format(CD0))
CD0_2_FUS = CD0

# Clean, cruise h = 28,000 ft
h_array = np.linspace(28000,28000,N)
V = RP.V_cruise_target  # Target cruise speed
CD0 = find_CD0(h_array,V,FF,Q)
print('\nClean, cruise')
print('CD0: {:,.8f}'.format(CD0))
CD0_3_FUS = CD0

# Landing flaps, gear up h = 15,000 - 3000 ft
h_array = np.linspace(15000,3000,N)
V_approach = 200*1.688
CD0 = find_CD0(h_array,V,FF,Q)
print('\nLanding flaps, gear up')
print('CD0: {:,.8f}'.format(CD0))
CD0_4_FUS = CD0

# Landing flaps, gear down, h =  3000 - 0 ft
h_array = np.linspace(3000,0,N)
V_approach = RP.V_approach  # Approach speed
CD0 = find_CD0(h_array,V,FF,Q)
print('\nLanding flaps, gear down')
print('CD0: {:,.8f}'.format(CD0))
CD0_5_FUS = CD0
CD0_FUS = [CD0_1_FUS,CD0_2_FUS,CD0_3_FUS,CD0_4_FUS,CD0_5_FUS]

'''####################################################################'''
# Wing Code

# define constants
h_cruise = 28000
x_c_m_wing = 0.37                                      # chordwise location of max thickness
t_c_m_wing = 0.18937                                   # chordwise maximum thickness
Lambda = RP.Gamma_w
gamma = 1.4                                       # assumed constant specific heat ratio
S_wet_wing = 2 * RP.wingArea - 123.6473938        # wetted wing area, minus area within fuselage, ft^2
Re_transition = 10 ** 6
Q_c_wing = 1.0                                    # wing interference factor, 1.0 for high wing
C_flap_to_wing = 0.25                             # flap to wing chord ratio
del_f = 15                                        # flap deflection angle, degrees
S_flapped = 57.88                                 # flapped wing area, ft^2

def earth_atmosphere_model(h):
    T_o = 518.7    # R
    mu_o = 3.62e-7 # [lbf*s/ft^2]

    temp = 59 - .00356*h
    press = 2116 * ( (temp+459.7) / 518.6 )**5.256
    rho = press / ( 1718 * (temp + 459.7) )

    tempR = temp + 459.67 # convert degree F to R
    mu = mu_o*((tempR/T_o)**1.5)*( (T_o+198.72)/(tempR+198.72) ) # Sutherland's formula
    return rho, mu, tempR
x = earth_atmosphere_model(10000)


def reynolds_number(rho, mu, V,l):
    Re = rho*V*l/mu
    return Re

V_stage = [250*1.688, RP.V_cruise_min, RP.V_cruise_target, 200*1.688, 140*1.688]
h_stage = [1500/2, (28000-1500)/2 + 1500, 28000, (28000-3000)/2 + 3000, 3000/2]
Rho = []
Mu = []
Temp = []
a_a = []
Re_stage = []
FF = []
M_stage = []
C_f = []
CD0_WNG = []
delCD_flaps = 0.9*(C_flap_to_wing)**1.38 * (S_flapped/RP.wingArea) * (math.sin(math.radians(del_f))**2)

# calculate rho, mu, and Temp for given altitude and velocity
for i in range(5):
    data = earth_atmosphere_model(h_stage[i])   # index goes from sea level to cruise altitude in increments of h_cruise/n
    Rho.append(data[0])
    Mu.append(data[1])
    Temp.append(data[2])

for i in range(5):
    Re_stage.append(reynolds_number(Rho[i],Mu[i],V_stage[i],RP.MAC_w))
    a_a.append(math.sqrt(gamma * RP.R * Temp[i]))

for i in range(5):
    M_stage.append(V_stage[i] / a_a[i])
    FF.append((1 + 0.6 / x_c_m_wing * t_c_m_wing + 100 * (t_c_m_wing)**4) * (1.34 * (M_stage[i])**0.18 * (np.cos(Lambda))**0.28))


for i in range(5):

    if Re_stage[i] > Re_transition:
        C_f.append(0.455/(math.log10(Re_stage[i])**2.58 * (1 + 0.144 * M_stage[i]**2)**0.65))

    else:
        C_f.append(1.328 / math.sqrt(Re_stage))
    
    if i == 3:
        CD0_WNG.append(C_f[i] * FF[i] * Q_c_wing * S_wet_wing)

    else:
        CD0_WNG.append(C_f[i] * FF[i] * Q_c_wing * S_wet_wing + delCD_flaps)


print(CD0_WNG)





'''####################################################################'''
# Horizontal Tail Code
# Reloads the imports in case they are updated
#importlib.reload(RP)


# Requirements and Parameters
h_cruise = 28000
x_c_m_ht = 0.5*6.034                                   # chordwise location of max thickness
t_c_m_ht = 0.903/6.034                                 # chordwise maximum thickness
Lambda = RP.Gamma_ht
gamma = 1.4                                       # assumed constant specific heat ratio
S_wet_ht = 2 * RP.S_horiz_tail - 123.6473938        # wetted ht area, minus area within fuselage, ft^2
Re_transition = 10 ** 6
Q_c_ht = 1.03
l_c = RP.B_h                                # length of horizontal tail
R = RP.R                               # Gas constant [ft*lbf/ ( lbm*R )]
Q = 1



def earth_atmosphere_model(h):
    T_o = 518.7    # R
    mu_o = 3.62e-7 # [lbf*s/ft^2]

    temp = 59 - .00356*h
    press = 2116 * ( (temp+459.7) / 518.6 )**5.256
    rho = press / ( 1718 * (temp + 459.7) )

    tempR = temp + 459.67 # convert degree F to R
    mu = mu_o*((tempR/T_o)**1.5)*( (T_o+198.72)/(tempR+198.72) ) # Sutherland's formula
    return rho, mu, tempR
x = earth_atmosphere_model(10000)


def reynolds_number(rho, mu, V,l):
    Re = rho*V*l/mu
    return Re

V_stage = [250*1.688, RP.V_cruise_min, RP.V_cruise_target, 200*1.688, 140*1.688]
h_stage = [1500/2, (28000-1500)/2 + 1500, 28000, (28000-3000)/2 + 3000, 3000/2]
Rho = []
Mu = []
Temp = []
a_a = []
Re_stage = []
FF = []
M_stage = []
C_f = []
CD0_HT = []

# calculate rho, mu, and Temp for given altitude and velocity
for i in range(5):
    data = earth_atmosphere_model(h_stage[i])   # index goes from sea level to cruise altitude in increments of h_cruise/n
    Rho.append(data[0])
    Mu.append(data[1])
    Temp.append(data[2])

for i in range(5):
    Re_stage.append(reynolds_number(Rho[i],Mu[i],V_stage[i],RP.MAC_w))
    a_a.append( math.sqrt(gamma * RP.R * Temp[i]))

for i in range(5):
    M_stage.append(V_stage[i] / a_a[i])
    FF.append((1 + 0.6 / x_c_m_ht * t_c_m_ht + 100 * (t_c_m_ht)**4) * (1.34 * (M_stage[i])**0.18 * (np.cos(Lambda))**0.28))


for i in range(5):

    if Re_stage[i] > Re_transition:
        C_f.append(0.455/(math.log10(Re_stage[i])**2.58 * (1 + 0.144 * M_stage[i]**2)**0.65))

    else:
        C_f.append(1.328 / math.sqrt(Re_stage))
    
    if i == 3:
        CD0_HT.append(C_f[i] * FF[i] * Q_c_ht * S_wet_ht)

    else:
        CD0_HT.append(C_f[i] * FF[i] * Q_c_ht * S_wet_ht)


print(CD0_HT)


'''####################################################################'''
# Vertical Tail Code
# Requirements and Parameters
h_cruise = 28000
x_c_m_vt = 0.5*6.034                                   # chordwise location of max thickness
t_c_m_vt = 0.903/6.034                                 # chordwise maximum thickness
Lambda = RP.Gamma_vt
gamma = 1.4                                       # assumed constant specific heat ratio
S_wet_vt = 2 * RP.S_vert_tail - 123.6473938        # wetted vt area, minus area within fuselage, ft^2
Re_transition = 10 ** 6
Q_c_vt = 1.03                                    # vt interference factor, 1.0 for high vt
l_c = RP.B_h                                # length of horizontal tail
R = RP.R                               # Gas constant [ft*lbf/ ( lbm*R )]
Q = 1.03



def earth_atmosphere_model(h):
    T_o = 518.7    # R
    mu_o = 3.62e-7 # [lbf*s/ft^2]

    temp = 59 - .00356*h
    press = 2116 * ( (temp+459.7) / 518.6 )**5.256
    rho = press / ( 1718 * (temp + 459.7) )

    tempR = temp + 459.67 # convert degree F to R
    mu = mu_o*((tempR/T_o)**1.5)*( (T_o+198.72)/(tempR+198.72) ) # Sutherland's formula
    return rho, mu, tempR
x = earth_atmosphere_model(10000)


def reynolds_number(rho, mu, V,l):
    Re = rho*V*l/mu
    return Re

V_stage = [250*1.688, RP.V_cruise_min, RP.V_cruise_target, 200*1.688, 140*1.688]
h_stage = [1500/2, (28000-1500)/2 + 1500, 28000, (28000-3000)/2 + 3000, 3000/2]
Rho = []
Mu = []
Temp = []
a_a = []
Re_stage = []
FF = []
M_stage = []
C_f = []
CD0_VT = []

# calculate rho, mu, and Temp for given altitude and velocity
for i in range(5):
    data = earth_atmosphere_model(h_stage[i])   # index goes from sea level to cruise altitude in increments of h_cruise/n
    Rho.append(data[0])
    Mu.append(data[1])
    Temp.append(data[2])

for i in range(5):
    Re_stage.append(reynolds_number(Rho[i],Mu[i],V_stage[i],RP.MAC_w))
    a_a.append(math.sqrt(gamma * RP.R * Temp[i]))

for i in range(5):
    M_stage.append(V_stage[i] / a_a[i])
    FF.append((1 + 0.6 / x_c_m_vt * t_c_m_vt + 100 * (t_c_m_vt)**4) * (1.34 * (M_stage[i])**0.18 * (np.cos(Lambda))**0.28))


for i in range(5):

    if Re_stage[i] > Re_transition:
        C_f.append(0.455/(math.log10(Re_stage[i])**2.58 * (1 + 0.144 * M_stage[i]**2)**0.65))

    else:
        C_f.append(1.328 / math.sqrt(Re_stage))
    
    if i == 3:
        CD0_VT.append(C_f[i] * FF[i] * Q_c_vt * S_wet_vt)

    else:
        CD0_VT.append(C_f[i] * FF[i] * Q_c_vt * S_wet_vt)


print(CD0_VT)

'''####################################################################'''
# Engine Parameters (PW100/150A) #
eng_length = 10.4      # (ft)
eng_height = 3         # (ft)
eng_width = 2.291667    # (ft)
eng_power = 5_000       # (shp)

# Velocities (ft/s) #
climb_velocity = RP.V_cruise_min
cruise_velocity = RP.V_cruise_target
descent_velocity = 200*1.688

#################################
# Skin Friction Coeff (C_f_eng) #
#################################
""" depends on: Reynolds #, laminar/turbulent, shape of component """
import math

def GetDensityViscosity(altitude):
    'Input altitude (ft) and output density [slug/ft^3], dynamic viscosity [lbf*s/ft^2], and temp [R]'
    T_o = 518.7    # R
    mu_o = 3.62e-7 # [lbf*s/ft^2]

    temp = 59 - .00356*altitude
    press = 2116 * ( (temp+459.7) / 518.6 )**5.256
    rho = press / ( 1718 * (temp + 459.7) )

    tempR = temp + 459.67 # convert degree F to R
    mu = mu_o*((tempR/T_o)**1.5)*( (T_o+198.72)/(tempR+198.72) ) # Sutherland's formula
    return rho, mu

def GetReynoldsNumber(air_density, velocity, characteristic_length, dynamic_viscosity):
    Re = air_density * velocity * characteristic_length / dynamic_viscosity
    return Re

def GetMachNumber(velocity):
    Ma = velocity / 1125.33
    return Ma

def GetSkinFrictionCoefficient(Re, Mach_number):
    C_f_l_array = []
    C_f_t_array = []
    for i in Re:
        C_f_laminar = 1.328 / (i ** 0.5)
        C_f_turbulent = 0.445 / ((math.log10(i) ** 2.58) * ((1 + 0.144 * (Mach_number ** 2)) ** 0.65))
        C_f_l_array.append(C_f_laminar)
        C_f_t_array.append(C_f_turbulent)
    return C_f_l_array, C_f_t_array

def GetSkinFrictionCruise(Re,Mach_number):
    C_f_laminar = 1.328 / (Re ** 0.5)
    C_f_turbulent = 0.445 / ((math.log10(Re) ** 2.58) * ((1 + 0.144 * (Mach_number ** 2)) ** 0.65))
    return C_f_laminar, C_f_turbulent


climb_altitude_array = np.linspace(0,28000,57)      # altitude (ft)
climb_density_array, climb_viscosity_array = GetDensityViscosity(climb_altitude_array)
Re_climb = GetReynoldsNumber(climb_density_array, climb_velocity, eng_length, climb_viscosity_array)
Ma_climb = GetMachNumber(climb_velocity)
# print(Re_climb)
C_f_laminar_climb, C_f_turbulent_climb = GetSkinFrictionCoefficient(Re_climb, Ma_climb)

# print(f'Climb (C_f_lam): {C_f_laminar_climb}')
# print(f'Climb (C_f_tur): {C_f_turbulent_climb}')

cruise_altitude = 28_000        # altitude (ft)
cruise_density, cruise_viscosity = GetDensityViscosity(cruise_altitude)
Re_cruise = GetReynoldsNumber(cruise_density, cruise_velocity, eng_length, cruise_viscosity)
Ma_cruise = GetMachNumber(cruise_velocity)
C_f_laminar_cruise, C_f_turbulent_cruise = GetSkinFrictionCruise(Re_cruise, Ma_cruise)

# print(f'Cruise (C_f_lam): {C_f_laminar_cruise}')
# print(f'Cruise (C_f_tur): {C_f_turbulent_cruise}')


descent_altitude_array = np.linspace(28000,0,57)      # altitude (ft)
descent_density_array, descent_viscosity_array = GetDensityViscosity(descent_altitude_array)
Re_descent = GetReynoldsNumber(descent_density_array, descent_velocity, eng_length, descent_viscosity_array)
Ma_descent = GetMachNumber(descent_velocity)
C_f_laminar_descent, C_f_turbulent_descent = GetSkinFrictionCoefficient(Re_descent, Ma_descent)

# print(f'Descent (C_f_lam): {C_f_laminar_descent}')
# print(f'Descent (C_f_tur): {C_f_turbulent_descent}')

avg_l_clmb = sum(C_f_laminar_climb) / len(C_f_laminar_climb)
avg_t_clmb = sum(C_f_turbulent_climb) / len(C_f_turbulent_climb)
C_f_clmb = 0.05*avg_l_clmb + 0.95*avg_t_clmb

C_f_crs = 0.05*C_f_laminar_cruise + 0.95*C_f_turbulent_cruise

avg_l_dcnt = sum(C_f_laminar_descent) / len(C_f_laminar_descent)
avg_t_dcnt = sum(C_f_turbulent_descent) / len(C_f_turbulent_descent)
C_f_dcnt = 0.05*avg_l_dcnt + 0.95*avg_t_dcnt


########################
# Form Factor (FF_eng) #
########################

def GetFormfactor(characteristic_length, max_diameter):
    f = characteristic_length / max_diameter
    FF = (1 + (0.35 / f))

    # print(f'Form Factor (FF): {FF}')

    return FF

FF = GetFormfactor(eng_length, eng_width)

###############################
# Interference Factor (Q_eng) #
###############################

Q = 1.3     # 1.0, 1.3 or 1.5 (Lec 4 pg 10)

###################################
# Wetted Surface Area (S_wet_eng) #
###################################

S_wet_eng = RP.S_n                             # Nacelle wetted area [ft^2]
S_wet_eng_total = S_wet_eng * 4

CD0_clmb_ENG = FF * C_f_clmb * Q * S_wet_eng_total
CD0_crs_ENG  = FF * C_f_crs * Q * S_wet_eng_total
CD0_decent_ENG = FF * C_f_dcnt * Q * S_wet_eng_total

CD0_ENG = [CD0_clmb_ENG,CD0_clmb_ENG,CD0_crs_ENG,CD0_decent_ENG,CD0_decent_ENG]
print(f'CD0_ENG: {CD0_ENG}')

'''####################################################################'''

print( 'CD0_FUS',CD0_FUS )
print( 'CD0_WNG',CD0_WNG )
print(  'CD0_HT',CD0_HT )
print( 'CD0_VT',CD0_VT )


CD0_components = CD0_FUS + CD0_WNG + CD0_HT + CD0_VT + CD0_ENG
CD0_components = np.array(CD0_components)

# Reshape the array into a 2D array with 5 columns
CD0_components_2d = CD0_components.reshape(-1, 5)

# Calculate the sum of each column
column_sum = np.sum(CD0_components_2d, axis=0)

# Print the reshaped array with rows after every 5th value
print('\nReshaped CD0_components array:')
print(CD0_components_2d)

# Print the sum of each column as a new row
print('\nSum of each column:')
print(column_sum)

CD0 = (1/S_ref) * column_sum




