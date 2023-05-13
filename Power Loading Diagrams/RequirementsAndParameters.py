# Updated by Daniela L. Davalos on 4/20/2023
import numpy as np
import WeightCode as WC

#-------------------------------#
#           Constants           #
#-------------------------------#
N = 300
R = 53.35                               # Gas constant [ft*lbf/ ( lbm*R )]
g = 32.17                               # Accceleration of gravity [ft/s^2]

#-------------------------------#
#       RFP Requirements        #
#-------------------------------#
V_approach = 140*1.688 #140    
V_stall = 140*1.688/1.3                 # Stall speed [knots --> ft/s], V_approach = 1.3*V_stall     
V_cruise_target = 350*1.688             # Target cruise speed [knots --> ft/s]     
V_cruise_min = 275*1.688                # Minimum cruise speed [knots --> ft/s]    

# Performance, Take-off
TO_length_max = 4500                    # Max takepff field length [ft]
TO_height = 50                          # Takeoff clearance height [ft]

# Performance, Landing
L_length_max = 4500                     # Max landing field length [ft]

# Payload
crew_num = 3                            # Number of crew members [-]
crew_W = 190                            # Weight of each crew member [lbf]
crew_W_tot = crew_num*crew_W            # Total crew weight [lbf]
crew_bag_W = crew_num*30                # Total crew baggage weight [lbf]
pass_num = 50                           # Number of passengers [-]
pass_W = 200                            # Weight of each passenger [lbf]
pass_bag_W = 40                         # Weight of each passenger baggage [lbf]
pass_bag_W_tot = pass_num*pass_bag_W    # Total weight of passenger baggage [lbf]

#-------------------------------#
#     Atmospheric Parameters    #
#-------------------------------#
rho_25 = 0.0010567523                   # Density of air at 25,000 ft [slug/ft3]
rho_SL = 2.3769e-3                      # Density at sea level [slug/ft3]
T_cruise = 429.64                       # Temp at cruise, SEE ANDERSEN????? [R]
a_a = np.sqrt(1.4*R*T_cruise*32.17)     # Speed of sound at cruise [ft/s]
Ma = V_cruise_target/a_a                # Mach number at cruise [-]

#-------------------------------#
#      Aircrfaft Parameters     #
#-------------------------------#
WTO = 70774                            # Maximum takeoff weight [lbf]     
CL_max_TO = 2.4
CL_max_L = 3.3                          # For landing (1.9 - 3.3) 
CL_max_cruise = 2.0

# Engine/Nacelle
W_engine = 3968                         # Weight of each engine [lbf]
W_fuel_initial = 5151                   # Initial fuel weight [lbf]
W_fuel_final = 0*W_fuel_initial         # Final fuel weight [lbf]
N_Lt = 10.4                             # Nacelle length [ft]
N_w = 3.0                               # Nacelle width [ft]
N_en = 4                                # Number of engines [-]
S_n = 284.3                             # Nacelle wetted area [ft^2]
N_t = 2                                 # Number of fuel tanks [-]

# Wing
b = 83                                  # Wingspan [ft]
wingArea = 491.2                        # Wing reference area [ft^2]
AR = b**2/wingArea                      # Wing aspect ratio, from OpenVSP [-]
MAC_w = 7.6887                          # Mean aerodynamic chord of wing [ft]
tc_wing = 0.18937                       # Thickness to chord length ratio at root [-]
lamda_w = 1.5/13                        # Wing taper ratio [-]
Gamma_w = 25 * np.pi/180                # Sweep at 25% MAC [radians]

# Fuselage
fuseLength = 75                         # Total fuselage length [ft]
F_w = 8                                 # Fuselage width at horizontal tail intersection [ft]
S_wet_fuse = 2294                       # Fuselage wetted area [ft^2]  
diam_fuse = 10.5                        # Max fuselage diameter [ft]
area_fuse = np.pi*((diam_fuse/2)**2)    # Max cross-sectional area of fuselage [ft^2]
depth_fuse = 10                         # Fuselage structural depth (I looked at height) [ft]
cargo_floorarea = 50                    # Cargo floor area [ft^2]

# Tail
L_t = 52                                # Tail length (Wing MAC to Tail MAC) (ft)

# Horizontal tail
S_horiz_tail = 136.54                   # Horizontail tail area [ft^2]
MAC_ht = 5.29                           # Mean aerodynamic chord of horizontal tail [ft]
B_h = 26                                # Span of horizontal tail [ft]
H_t = 15.5                              # Height of horizontal tail above fuselage [ft]
A_h = 4.95                              # Horizontal tail aspect ratio [-]
Gamma_ht = 10 * np.pi/180               # Horizontal tail sweep angle at 25% MAC [radians]
S_e = 11.7*1.14                         # Elevator area [ft^2]

# Vertical tail
S_vert_tail = 134.23                    # Vertical tail area [ft^2]
MAC_vt = 6.4656                         # Mean aerodynamic chord of vertical tail [ft]
H_v = 7.8                               # Height of vertical tail above fuselage [ft]
Gamma_vt = 80 * np.pi/180               # Vertical tail sweep at 25% MAC [radians]
A_v = 1.26                              # Aspect ratio of vertical tail [-]
tc_v_tail = 0.25                        # Thickness to chord length ratio of vertical tail [-]

# Landing gear
L_m = 4.17*12                           # Length of main landing gear [in]
N_mw = 4                                # Number of main wheels [-]
N_mss = 4                               # Number of main gear shock struts [-]
L_n = 3.75*12                           # Length of nose landing gear [in]
N_nw = 1                                # Number of nose landing gear [-]

# Oswald Span Efficiency
e_clean = 0.85                          # Clean, cruise configuration
e_TO_GU = 0.80                          # Take-off flaps, gear up
e_TO_GD = 0.80                          # Take-off flaps, gear down
e_L_GU = 0.75                           # Landing flaps, gear up
e_L_GD = 0.75                           # Landing flaps, gear down

# Propeller
n_p = 0.75                          # Propeller efficiency during cruise from Table 3.3 in Gudmundsson

# # Zero lift drag coefficients, from dragPolar.py
CDO_cruise = 0.02590592                 # Clean, cruise configuration
CDO_TO_GU = 0.02656793                  # Take-off flaps, gear up
# CDO_TO_GD = 0.0637                  # Take-off flaps, gear down
CDO_L_GU = 0.02819714                    # Landing flaps, gear up
# CDO_L_GD = 0.1067                    # Landing flaps, gear down