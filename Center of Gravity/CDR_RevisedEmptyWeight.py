## Duncan Koelzer, Steven Martinez, Kimberly Moreno
## Empty weight code for A1
## Eqs 15.25 - 15.31

import numpy as np
from matplotlib import pyplot as plt
import math
import RequirementsAndParameters as RP
import importlib
importlib.reload(RP) 

# Output Results?
show = True

# Input Values  
'First set' 
W_dg = RP.WTO               # Design gross weight (lbf)
N_z = 3.5                   # Ultimate load factor (= 1.5*limit load factor) (Taken from table 14.2 Raymer, pg 337)
S_w = RP.wingArea           # Trapezoidal wing area (aka reference area)
A = RP.AR                   # Aspect Ratio
tc_root_wing = RP.tc_wing   # thickness to chord length ratio at root
lamda = RP.lamda_w          # Wing taper ratio
Gamma = RP.Gamma_w          # Sweep at 25% MAC (NOT SURE OF UNITS)
S_csw = 10*2.5 + 4.5*1.65 + 4.5*0.75 + 8.9*0.67      # Control Surface Area for wing

K_uht = 1                   # we do NOT have unit (all-moving) horizontal tail
F_w = RP.F_w                # Fuselage width at horizontal tail intersection (ft)
B_h = 26                    # Span of horizontal tail (ft)
S_ht = 136.5                # Area of horizontal tail (ft^2)
L_t = 52                    # Tail length (Wing MAC to Tail MAC) (ft)
K_y = 0.3*L_t               # Aircraft pitching radius of gyration (~0.3*L_t) (ft)
Gamma_ht = 10 * np.pi/180   # Horizontal tail sweep angle at 25% MAC
A_h = 4.95                  # Horizontal tail Aspect Ratio
S_e = 11.7*1.14             # Elevator Area (ft^2)

H_t = 15.5                  # Height of horizontal tail above fuselage (ft)
H_v = 7.8                   # Height of Vertical Tail above fuselage (ft)
S_vt = 134.2                # Area of Vertical Tail (ft^2)
K_z = L_t                   # Arcraft Yawing radius of gyration (~L_t) (ft)
Gamma_vt = 80 * np.pi/180   # Vertical tail sweep at 25% MAC
A_v = 1.26                  # Aspect ratio of vertical tail
tc_root_tail = 0.25         # thickness to chord length ratio of vertical tail

K_door = 1.25               # 1.0 if no cargo door; = 1.06 if one side cargo door; = 1.12 if two side cargo doors; = 1.12 if aft clamshell door; = 1.25 if two side cargo and one aft clamshell doors
K_Lg = 1.12                 # 1.12 if fuselage-mounted main landing gear; = 1.0 otherwise
L = 75.0                    # Fuselage structural length (ft)
S_f = 2294                  # Fuselage wetted area (ft^2)
B_w = 83.0                  # Wing span (ft)
D = 10                      # Fuselage structural depth (I looked at height) (ft)
K_ws = 0.75 * ((1+2*lamda)/(1+lamda)) * B_w*np.tan(Gamma/L)   # Given formula

K_mp = 1.126                # 1.126 for kneeling gear; = 1.0 otherwise
W_l = W_dg-10000            # Landing Gross weight (lbf)  (Comparable aircrafts carry about 10000lbf of fuel)
N_gear = 2.85               # Gear load factors (Raymer table 11.5 gives range from 2.7-3 for commercial aircraft)
N_l = 1.5*N_gear            # Ultimate landing load factor (given eq)
L_m = 4.17*12               # Length of main landing gear (in)
N_mw = 4                    # Number of main wheels
N_mss = 4                   # Number of main gear shock struts
V_stall = 181.8             # Stall speed (ft/s)

K_np = 1.15                 # 1.15 for kneeling gear; = 1.0 otherwise
L_n = 3.75*12               # Length of nose landing gear (in)
N_nw = 1                    # Number of nose landing gear

K_ng = 1.017                # 1.017 for pylon-mounted nacelle; = 1.0 otherwise
N_Lt = 10.4                 # Nacelle length (ft)
N_w = 3.0                   # Nacelle width (ft)
N_en = 4                    # Number of engines
S_n = 284.3                 # Nacelle wetted area (ft^2)
K_p = 1.4                   # 1.4 for engine with propeller or 1.0 otherwise
K_tr = 1                    # 1.18 for jet with thrust reverser or 1.0 otherwise
W_en = 1580                 # Weight of engine, each (lbf)
W_ec = 2.331 * W_en**0.901 * K_p * K_tr     # Weight of engine and contents, per nacelle (lbf) 

'Second Set'
L_ec = 4*27.5               # length from engine front to cockpit, sum total for multiple engines
V_t = 10000/6.9             # total fuel volume, gal
V_i = V_t                   # integral tank volume, gal
V_p = 0                     # self-sealing "protected" tanks volume, gal
N_t = 2                     # number of fuel tanks
N_f = 5                     # number of functions performed by controls (usually 4-7)
N_m = 1                     # number of mechanical functions (usually 0-2)

S_cs = S_csw+S_e+8.3*1.5    # total area of control surfaces, ft^2
W_APUuninstalled = 0        # weight of auxiliary power unit alone
K_r = 1.0                   # 1.133 for reciprocating engine, 1.0 otherwise
K_tp = 0.793                # 0.793 for turboprop engines
L_f =  75                   # total fuselage length, ft
g = 32.17                   # acceleration of gravity, ft/s^2
R_z = (0.45 + 0.38) / 2     # nondimensional radius of gyration, yawing (z) - taken as average of twin turboprop transport and 4 engine jet transport 
I_y = ((B_w + L)/2)**2 * (W_dg * R_z ** 2) / (4 * g) # yawing moment of inertia, lb-ft^2

'Third Set'
R_kva = 50                  #system electrical rating, kv*A (typically 40-60 for transports, 110-160 for fighters and bombers); assumption
L_a = 120500                #electrical routing distance, generators to avionics to cockpit, ft; estimate
N_gen = 4                   #number of generators (typically = N_en)
W_uav = 1100                #uninstalled avionics weight, lb (typically = 800-1400 lb); assumption
N_c = 3                     #number of crew
W_c = 2000                  #maximum cargo weight, lb
N_p = 53                    #number of personnel onboard (crew and passengers)
V_pr =  1150                #volume of pressurized section, ft^3
Cargofloorarea = 50         #cargo floor area, ft^2


'-----------'
' First Set '
'-----------'
# Eq 15.25: Wing weight
W_wing = 0.0051 * (W_dg * N_z)**0.557 * S_w**0.649 * A**0.5 * (tc_root_wing)**-0.4 * (1+lamda)**0.1 * \
    np.cos(Gamma)**0.1 * S_csw**0.1

# Eq 15.26: Horizontal Tail weight
W_HorizontalTail = 0.0379 * K_uht * (1+F_w/B_h)**-0.25 * W_dg**0.639 * N_z**0.1 * S_ht**0.75 * L_t**-1 * \
    K_y**0.704 * np.cos(Gamma_ht)**-1 * A_h**0.166 * (1+S_e/S_ht)**0.1

# Eq 15.27: Vertical Tail weight
W_VerticalTail = 0.0026 * (1+H_t/H_v)**0.225 * W_dg**0.556 * N_z**0.536 * L_t**-0.5 * S_vt**0.5 * K_z**0.875 * \
    np.cos(Gamma_vt)**-1 * A_v**0.35 * (tc_root_tail)**-0.5

# Eq 15.28: Fuselage weight
W_fuselage = 0.3280 * K_door * K_Lg * (W_dg*N_z)**0.5 * L**0.25 * S_f**0.302 * (1+K_ws)**0.04 * (L/D)**0.10

# Eq 15.29: Main Landing Gear weight
W_mainLandingGear = 0.0106 * K_mp * W_l**0.888 * N_l**0.25 * L_m**0.4 * N_mw**0.321 * N_mss**-0.5 * V_stall**0.1

# Eq 15.30: Nose landing gear weight
W_noseLandingGear = 0.032 * K_np * W_l**0.646 * N_l**0.2 * L_n**0.5 * N_nw**0.45

# Eq 15.31: Nacelle Group weight
W_nacelleGroup = 0.6724 * K_ng * N_Lt**0.10 * N_w**0.294 * N_z**0.119 * W_ec**0.611 * N_en**0.984 * S_n**0.224

# Sum empty weights
W_empty1 = W_wing + W_HorizontalTail + W_VerticalTail + W_fuselage + W_mainLandingGear + W_noseLandingGear + W_nacelleGroup

# Print
if show==True:
    print('W_wing=',W_wing)
    print('W_HTail=',W_HorizontalTail)
    print('W_VTail=',W_VerticalTail)
    print('W_fuselage=',W_fuselage)
    print('W_mainLanding=',W_mainLandingGear)
    print('W_noseLanding=',W_noseLandingGear)
    print('W_nacelle=',W_nacelleGroup)
    print('EMPTY1=',W_empty1)
    print(' ')


'-----------'
' Second Set'
'-----------'
W_enginecontrols = 5.0 * N_en + 0.8 * L_ec # calculate weight of engine controls
W_starterpneumatic = 49.19 * ((N_en * W_en) / 1000)**0.541 # calculate weight of pneumatic starter
W_fuelsystem = 2.405 * V_t**0.606 * (1 + V_i / V_t)**-1.0 * (1 + V_p/V_t) * N_t**0.5 # calculate weight of fuel system
W_flightcontrols = 145.9 * N_f**0.554 * (1 + N_m/N_f)**-1.0 * S_cs**0.20 * (I_y * 10**-6)**0.07 # calculate weight of flight controls
W_APUinstalled = 2.2 * W_APUuninstalled # calculate weight of auxiliary power unit once installed
W_instruments = 4.509 * K_r * K_tp * N_c**0.541 * N_en * (L_f + B_w)**0.5 # calculate weight of flight instruments
W_hydraulics = 0.2673 * N_f * (L_f + B_w)**0.937 # calcualte weight of hydraulics system
W_empty2 = W_enginecontrols + W_starterpneumatic + W_fuelsystem + W_flightcontrols + W_APUinstalled + W_instruments + W_hydraulics

if show == True:
    print('W_engControls=',W_enginecontrols)
    print('W_pneumaticStarter=',W_starterpneumatic)
    print('W_fuelSystem=',W_fuelsystem)
    print('W_flightControls=',W_flightcontrols)
    print('W_APU=',W_APUinstalled)
    print('W_instruments=',W_instruments)
    print('W_hydraulics=',W_hydraulics)
    print('EMPTY2=',W_empty2)
    print(' ')


'-----------'
' Third Set '
'-----------'
#weight estimation equations
W_electrical = 7.291 * (R_kva ** 0.782) * (L_a ** 0.346) * (N_gen ** 0.10)
W_avionics = 1.73 * (W_uav ** 0.983)
W_furnishings = 0.0577 * (N_c ** 0.1) * (W_c ** 0.393) * (S_f ** 0.75)
W_airconditioning = 62.36 * (N_p ** 0.25) * ((V_pr/1000) ** 0.604) * (W_uav ** 0.10)
W_antiice = 0.002 * W_dg
W_handlinggear =  0.00030 * W_dg
W_militarycargohandlingsystem = 2.4 * Cargofloorarea 
W_empty3 = W_electrical + W_avionics + W_furnishings + W_airconditioning + W_antiice + W_handlinggear + W_militarycargohandlingsystem

if show==True:
    print ("W_electrical:",  W_electrical)
    print ("W_avionics:", W_avionics)
    print ("W_furnishings:", W_furnishings)
    print ("W_airconditioning:", W_airconditioning)
    print ("W_antiice:", W_antiice)
    print ("W_handlinggear:", W_handlinggear)
    print ("W_militarycargohandlingsystem:", W_militarycargohandlingsystem)
    print ("EMPTY3:",W_empty3)



# Total Empty Weight
W_empty = W_empty1 + W_empty2 + W_empty3
if show == True: 
    print('Total empty=',W_empty)


