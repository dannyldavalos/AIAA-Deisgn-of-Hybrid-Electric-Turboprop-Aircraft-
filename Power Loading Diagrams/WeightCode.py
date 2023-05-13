## Test Code

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import RequirementsAndParameters as RP
import importlib
from Payload_Calculation import W_payload

# Reloads the imports in case they are updated
importlib.reload(RP)

#####################
# Defined Functions #
#####################

def Fuel_Fraction_Total(W0):
    #####################
    # Defined Functions #
    #####################

    def TSFC(C_bhp, velocity, eta_p):
        '''
        Raymer Table 3.4 (pg. 19)
        '''
        C = (C_bhp * velocity) / (550 * eta_p)
        return C

    def IndividualPhase(Wj_Wi, W_i, phi):
        '''
        P1: Start, Warmup, Taxi
        P2: Takeoff
        P3: Climb
        P4: Cruise
        P5: Loiter
        P6: Descent
        P7: Landing
        '''
        # specific energies
        e_fuel = 12_000                                         # Whr/kg
        e_batt = 1_750                                          # Whr/kg

        # calculate energy needed for segment
        W_j = Wj_Wi * W_i                                       # lbf
        W_fuel_conv = W_i - W_j                                 # lbf
        m_fuel_conv = W_fuel_conv                               # lbm   "Edit: no conversion needed"
        E_need_conv = e_fuel * m_fuel_conv * 0.454              # Whr

        # split energy using hybridization ratio
        E_fuel_hybr = (1 - phi) * E_need_conv                   # Whr
        E_batt_hybr = phi * E_need_conv                         # Whr

        # get mass of fuel and battery
        m_fuel_hybr = (E_fuel_hybr / e_fuel) * 2.20462          # lbm
        m_batt_hybr = (E_batt_hybr / e_batt) * 2.20462          # lbm

        # get weight of fuel and battery
        W_fuel_hybr = m_fuel_hybr                               # lbf   "Edit: no conversion needed"
        W_batt_hybr = m_batt_hybr                               # lbf   "Edit: no conversion needed"

        return W_fuel_hybr, W_batt_hybr

    ###################
    # Constant Values #
    ###################

    V = 590.7                   # velocity (ft/sec)
    R = 1000*6076.12 / 2           # range (nmi -> ft)
    # R = 0
    L_D_max = 14                # based on fig. 3.6 in Raymer
    L_D = 0.94 * L_D_max
    e_fuel = 12_000             # Whr/kg

    C_bhp_cruise = 0.5          # turboprop (power specific fuel consumption)
    eta_p_cruise = 0.8          # turboprop (propeller efficiency)
    C_T_cruise = TSFC(C_bhp_cruise, V, eta_p_cruise) / 3600     # turboprop (thrust specific fuel consumption)

    w_powertrain = 1984

    # rho_wing = 2.6
    # span = RP.b
    # w_wing = span * rho_wing

    #################
    # Initial Guess #
    #################


    phases = [
        'Start, Warmup, Taxi',
        'Takeoff',
        'Climb',
        'Cruise',
        'Loiter',
        'Descent',
        'Landing'
        ]

    # hybridizations = [1,1,.25,0,0.5,1,1]
    # hybridizations = [1,.5,.1,0.05,0,1,1]
    # hybridizations = [1,1,0.75,0.01,0.85,1,1]
    # hybridizations = [0,0.5,0.3,0,0.3,0,0]
    # hybridizations = [0.05,0.05,0.05,0.05,0.05,0.05,0.05]
    hybridizations = [0.2,0.2,0.45,0.01,0.85,1,1]

    fuel_frac_array = []        # initialize
    fuel_weight_array = []      # Initialize
    battery_weight_array = []   # initialize
    

    #######################
    # Start, Warmup, Taxi #
    #######################

    Power_Max = 19390                   # Power Requirements from power loading diagram
    num_eng = 4                     # number of engines
    P_max_takeoff = Power_Max/num_eng            # engine max power @ sea level (shp)
    P_idle = P_max_takeoff * 0.05   # 5% of total power
    time_idle = 1/4                 # hr
    time_takeoff = 1/60             # hr
    start_weight_array = []         # initialize array
    start_weight_array.append(W0)   # add initial weight guess to array
    c_bhp_idle = 0.5                   # possible units (lbm/hr/shp)    |--------------------------|
    c_bhp_takeoff = 0.5                # possible units (lbm/hr/shp)    | SHOULD VERIFY IF 103-106 |     
    eta_idle = 0.8                     # unitless (-)                   |        ARE CORRECT       | 
    eta_takeoff = 0.8                  # unitless (-)                   |--------------------------|

    j = 20                          # number of subdivisions

    for i in range(0,j+1):
        Wi = start_weight_array[i]
        Wi1_Wi = 1 - (time_idle / j) * (c_bhp_idle / eta_idle) * ((P_idle * num_eng) / Wi)
        W_fuel, W_batt = IndividualPhase(Wi1_Wi, Wi, hybridizations[0])
        Wi1 = Wi - W_fuel
        battery_weight_array.append(W_batt)
        start_weight_array.append(Wi1)
        fuel_weight_array.append(W_fuel)

    W_fuel_Taxi = sum(fuel_weight_array)
    W_fuel_total = W_fuel_Taxi
    print(W_fuel_Taxi)

    W1_W0 = start_weight_array[-1] / start_weight_array[0]
    fuel_frac_array.append(W1_W0)

    ###########
    # Takeoff #
    ###########

    takeoff_weight_array = []
    takeoff_weight_array.append(start_weight_array[-1])

    for i in range(0,j+1):
        Wi = takeoff_weight_array[i]
        Wi1_Wi = 1 - (time_takeoff / j) * (c_bhp_takeoff / eta_takeoff) * ((P_max_takeoff * num_eng) / Wi)
        W_fuel, W_batt = IndividualPhase(Wi1_Wi, Wi, hybridizations[1])
        Wi1 = Wi - W_fuel
        battery_weight_array.append(W_batt)
        takeoff_weight_array.append(Wi1)
        fuel_weight_array.append(W_fuel)

    # print('\nTakeoff Weights:')
    # print(takeoff_weight_array)
    # print(f'Final Takeoff Weight: {round(takeoff_weight_array[-1])} lbf')

    W_fuel_Takeoff = sum(fuel_weight_array) - W_fuel_total
    W_fuel_total += W_fuel_Takeoff
    print(W_fuel_Takeoff)
    

    W2_W1 = takeoff_weight_array[-1] / takeoff_weight_array[0]
    fuel_frac_array.append(W2_W1)

    #########
    # Climb #
    #########

    # Constants
    g = 32.174              # Gravitational acceleration [ft/s^2]
    b = RP.b                # Wing span [ft]
    S_ref = RP.wingArea     # Wing area [ft^2] POSSIBLY INCREASE THIS VALUE????
    #S_ref = 600     # Wing area [ft^2] POSSIBLY INCREASE THIS VALUE????
    AR = b**2/S_ref         # Aspect ratio
    h_i = 5000              # Initial altitude [ft]
    h_f = 28000             # Final altitude [ft]

    segment = 20
    h = np.linspace(h_i, h_f, segment)
    time = np.linspace(0,5*60,segment)
    # V = np.linspace(230*1.688,350*1.688,segment)
    effFactor = RP.e_TO_GU

    # Initialize variables
    V = []
    climb_weight_array = []
    C_L = []
    C_D = []
    D = []
    C_bhp = []
    deltah_e = []
    fuel_fraction = []
    V_v = []


    V_i = 230*1.688 # 200-250
    n_p = RP.n_p
    V.append(V_i)
    climb_weight_array.append(takeoff_weight_array[-1])

    C_D0 = RP.CDO_TO_GU
    N_engine = 4
    c_t = 0.25                           # [/hr] "Should be correct value" 
    P_max = Power_Max
    T_max = 550 * P_max * n_p / V_i     # Equation 17.5 from Raymer
    T_max_cont = 0.94 * T_max
    T = T_max_cont

    K = 1 / (np.pi * AR * effFactor)
    C = c_t/3600                        # [/s]
    rho_SL = 0.0023769                  # Sea level density [slug/ft^3]
    T_SL = 15000

    def ISA_density_altitude(h):
        # Calculate density in slugs
        temp = 59 - .00356*h
        press = 2116 * ( (temp+459.7) / 518.6 )**5.256
        rho = press / ( 1718 * (temp + 459.7) )
        return rho

    rho = ISA_density_altitude(h)

    # P_min = 10000*4
    # P_min = 1000*4

    for i in range(0,segment-1):

        #T = (T_SL* (np.sqrt(rho[i]/rho_SL) ))
        # Equations from Lecture 2, slides 56-57
        Wi = climb_weight_array[i]
        V.append(np.sqrt( (2*Wi/(rho[i]*S_ref)) * np.sqrt(K/(3*C_D0)) ))
        C_L.append((2 * climb_weight_array[i]) / (rho[i] * (V[i]) ** 2 * S_ref))  # 0.4 to 0.7
        C_D.append(C_D0 + (K * ((C_L[i]) ** 2)))                 # 0.02 to 0.06
        D.append((rho[i] * ((V[i]) ** 2) * S_ref * C_D[i]) / 2)
        # V_v.append((550*P_min*n_p/climb_weight_array[i] ) - (D[i]*V[i]/climb_weight_array[i]))
        deltah_e.append(((h[i+1]) + ((V[i+1])**2) / (2 * g))   -   (h[i]) + ((V[i])**2) / (2 * g))
        Wi1_Wi = (np.exp(-C * deltah_e[i] / (V[i] * (1 - (D[i] / T)))))
        # print(Wi1_Wi)
        W_fuel, W_batt = IndividualPhase(Wi1_Wi, Wi, hybridizations[2])
        Wi1 = Wi - W_fuel
        battery_weight_array.append(W_batt)
        climb_weight_array.append(Wi1)

        fuel_fraction.append(climb_weight_array[i+1] / climb_weight_array[i])
        fuel_weight_array.append(W_fuel)

    W_fuel_climb = sum(fuel_weight_array) - W_fuel_total
    W_fuel_total += W_fuel_climb
    print(W_fuel_climb)

    # Remove first fuel fraction
    fuel_fraction.pop(0)
    # Find the product of the entire climb fuel fractions
    product = np.prod(np.array(fuel_fraction))  

    # print('Number of segments: {}'.format(segment))
    # print('Individual fuel fractions for each segment: {}'.format(fuel_fraction))
    # print('Entire climb segment fuel fraction: {}'.format(product))
    # print('\n')

    W3_W2 = product

    fuel_frac_array.append(product)

    ##########
    # Cruise #
    ##########

    # Data for checking if it runs
    S_ref = 491.2                               # area
    e_clean = 0.85                              # oswald span efficiency
    rho = 0.000958                              # slug/ft^3
    CDO_cruise = 0.0297                         #
    vel_cruise_sec = 350 * 1.688
    Vel_cruise_hr = vel_cruise_sec * 3600       # knots-->ft/s --> ft/hr
    Vel_inf = Vel_cruise_hr                     #
    c_t = 0.6713636                             # Raymer Table 3.4 _ thrust specific fuel consumption _  lbm/ (hour *lbf )
    # c_t = 0.006
    # C = c_t/3600
    C = c_t
    b = 78.74                                   # Wingspan [ft] maximum for the Target length
    b_adj = 118.1                               # 36 m --> mandatory restriction
    # wingArea = 480.18905                        # Wing area [ft^2]
    wingArea = S_ref
    AR = (b**2)/wingArea
    K = 1/ (np.pi * AR * e_clean)
    R_cruise = R * 7/8                          # ft

    #initialized variable
    cruise_weight_array = []                                     #
    cruise_weight_array.append(climb_weight_array[-1])           #
    ### Cruise Segments
    j = 20
    for i in range(0,j):
        Wi = cruise_weight_array[i]
        C_L = (2 * Wi ) / ( rho * (vel_cruise_sec**2) * S_ref )
        L_D = C_L / (CDO_cruise + (K * (C_L ** 2)))
        exponent = (-((R_cruise / j) * C)/(Vel_inf * L_D))
        Wi1_Wi = (np.e ** exponent)
        W_fuel, W_batt = IndividualPhase(Wi1_Wi, Wi, hybridizations[3])
        Wi1 = Wi - W_fuel
        battery_weight_array.append(W_batt)
        cruise_weight_array.append(Wi1)
        fuel_weight_array.append(W_fuel)

    W_fuel_cruise = sum(fuel_weight_array) - W_fuel_total
    W_fuel_total += W_fuel_cruise
    print(W_fuel_cruise)

    W4_W3 = cruise_weight_array[-1] / cruise_weight_array[0]
    fuel_frac_array.append(W4_W3)

    ##########
    # Loiter #
    ##########

    Wi = cruise_weight_array[-1]
    V_inf = 200 * 1.687809858           # 275 - 350 KTAS (ft/s)

    C_d0_loiter = CDO_cruise
    K_loiter = K
    E_loiter = 30 * 60                  # min --> sec
    eta_p_loiter = 0.8                  # turboprop (propeller efficiency)
    C_bhp_loiter = 0.6 / 3600 / 550     # turboprop (power specific fuel consumption) (lbm/s/shp)


    #C_loiter = C_bhp_loiter * V_inf / (550 * eta_p_loiter)
    C_loiter = 0.6196E-6    # just used to get reasonable fuel fraction [!!!ERROR!!!]

    C_l_loiter = (C_d0_loiter / K_loiter) ** 0.5
    C_d_loiter = C_d0_loiter + (K_loiter * (C_l_loiter ** 2))
    Lift_Drag_loiter = C_l_loiter / C_d_loiter

    Wi1_Wi = np.e ** ((-E_loiter * V_inf * C_bhp_loiter) / (eta_p_loiter * Lift_Drag_loiter))
    # Wi1_Wi = 0.997  # Comparable Aircraft
    W_fuel, W_batt = IndividualPhase(Wi1_Wi, Wi, hybridizations[4])
    Wi1 = Wi - W_fuel
    battery_weight_array.append(W_batt)
    W5_W4 = Wi1 / Wi

    fuel_frac_array.append(W5_W4)
    fuel_weight_array.append(W_fuel)

    W_fuel_Loiter = sum(fuel_weight_array) - W_fuel_total
    W_fuel_total += W_fuel_Loiter
    print(W_fuel_Loiter)

    ###########
    # Descent #
    ###########
    Wi = Wi1
    Wi1_Wi = 0.998           # estimated from Raymer 3.2 (should change???)
    W_fuel, W_batt = IndividualPhase(Wi1_Wi, Wi, hybridizations[5])
    Wi1 = Wi - W_fuel
    battery_weight_array.append(W_batt)
    W6_W5 = Wi1 / Wi
    fuel_frac_array.append(W6_W5)
    fuel_weight_array.append(W_fuel)
    W_fuel_Descent = sum(fuel_weight_array) - W_fuel_total
    W_fuel_total += W_fuel_Descent
    print(W_fuel_Descent)

    ###########
    # Landing #
    ###########
    Wi = Wi1
    Wi1_Wi = 0.998           # Raymer Table 3.2
    W_fuel, W_batt = IndividualPhase(Wi1_Wi, Wi, hybridizations[6])
    Wi1 = Wi - W_fuel
    battery_weight_array.append(W_batt)
    W7_W6 = Wi1 / Wi
    fuel_frac_array.append(W7_W6)
    fuel_weight_array.append(W_fuel)
    W_fuel_Landing = sum(fuel_weight_array) - W_fuel_total
    W_fuel_total += W_fuel_Landing
    print(W_fuel_Landing)

    ###################
    # Total Fractions #
    ###################

    W7_W0 = np.prod(np.array(fuel_frac_array))      # landing weight / takeoff weight
    # Wf_W0 = (1 - W7_W0) * 1.06                      # total fuel fraction accounting for 6% fuel in pipes
    Wf_W0 = sum(fuel_weight_array) / W0  * 1.06     # total fuel fraction accounting for 6% fuel in pipes
    Wb_W0 = sum(battery_weight_array) / W0          # total battery weight fraction

    ###########
    # Results #
    ###########

    # print('------------------------------------')
    # print(f'Takeoff Weight Guess (W0): {W0} lbf')
    # print('------------------------------------')


    for phase in phases:
        i = phases.index(phase)
        print('-' * len(phase) + '-----------------------------')
        print(f'{phase} Fuel Fraction (W{i+1}/W{i}): {round(fuel_frac_array[i], 4)}')
        print('-' * len(phase) + '-----------------------------')

    print('==================================')
    print(f'Total Fuel Fraction (Wf/W0): {round(Wf_W0, 4)}')
    print(f'Total Fuel Weight (Wf): {round(Wf_W0 * W0)} lbf')
    print('==================================')
    print('============================================')
    print(f'Total Battery Weight Fraction (Wb/W0): {round(Wb_W0, 4)}')
    print(f'Total Battery Weight (Wb): {round(Wb_W0 * W0)} lbf')
    print('============================================')


    return Wf_W0, Wb_W0


def Empty_Weight_Total(W_fuel, W0):
    # Output Results?
    show = False


    # Imput Values  
    'First set' 
    W_dg = W0                   # Design gross weight (lbf)
    N_z = 3.5                   # Ultimate load factor (= 1.5*limit load factor) (Taken from table 14.2 Raymer, pg 337)
    S_w = 491.2                 # Trapezoidal wing area (aka reference area)
    A = 12.39                   # Aspect Ratio
    tc_root_wing = 0.18937      # thickness to chord length ratio at root
    lamda = 1.5/13              # Wing taper ratio
    Gamma = 25 * np.pi/180      # Sweep at 25% MAC (NOT SURE OF UNITS)
    S_csw = 10*2.5 + 4.5*1.65 + 4.5*0.75 + 8.9*0.67      # Control Surface Area for wing

    K_uht = 1                   # we do NOT have unit (all-moving) horizontal tail
    F_w = 8                     # Fuselage width at horizontal tail intersection (ft)
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
    W_l = W_dg - W_fuel         # Landing Gross weight (lbf)  (Comparable aircrafts carry about 10000lbf of fuel)
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
    N_en = 4.0                  # Number of engines
    S_n = 284.3                 # Nacelle wetted area (ft^2)
    K_p = 1.4                   # 1.4 for engine with propeller or 1.0 otherwise
    K_tr = 1                    # 1.18 for jet with thrust reverser or 1.0 otherwise
    W_en = 1580                 # Weight of engine, each (lbf)
    W_ec = 2.331 * W_en**0.901 * K_p * K_tr     # Weight of engine and contents, per nacelle (lbf) 

    'Second Set'
    L_ec = 4*27.5               # length from engine front to cockpit, sum total for multiple engines
    V_t = W_fuel / 6.9          # total fuel volume, gal
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
    W_empty = W_empty1 + W_empty2 + W_empty3 + 4 * W_en
    if show == True: 
        print('Total empty=',W_empty)
    
    return W_empty


# Start of iteration
W0 = 70_000         # initial guess (lbf)

W0_history = []     # list of all w0 guesses for plot
err = 1e-6          # relative convergence tolerance
delta = 2 * err     # any value greater than the tolerance

while delta > err:
    W0_history.append(W0)                           # add latest value to list
    # print(f'guess: {W0}')
    Wf_W0, Wb_W0 = Fuel_Fraction_Total(W0)
    # print(f'fuel frac: {Wf_W0}')
    W_fuel = Wf_W0 * W0
    W_empty = Empty_Weight_Total(W_fuel, W0)

    We_W0 = W_empty / W0
    # print(f'empty frac: {We_W0}')

    W0_new = (W_payload) / (1 - Wf_W0 - We_W0 - Wb_W0)      # lbf, compute new TOGW
    delta = abs(W0_new - W0) / abs(W0_new)          # find difference between last guess and current guess  
    alpha = 0.9
    W0 = alpha*W0 + (1-alpha)*W0_new
    
W0_history = np.array(W0_history)                   # convert list to array
print(f'guess: {W0}')
print(f'fuel frac: {Wf_W0}')
print(f'empty frac: {We_W0}')

print(f'MTOW (W0): {round(W0_history[-1])} lbf')

# plt.figure()
# plt.plot(list(np.linspace(0,len(W0_history), 29)), W0_history)
# plt.show()