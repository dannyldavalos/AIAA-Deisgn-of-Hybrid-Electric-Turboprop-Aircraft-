import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def TSFC(C_bhp, velocity, eta_p):
    """
    Raymer Table 3.4 (pg. 19)
    """
    C = (C_bhp * velocity) / (550 * eta_p)
    return C

print("---------- Conventional Aircraft ----------")


###########
# Payload #
###########

num_of_pass = 50            # number of passengers
num_of_crew = 3             # number of crew
W_sing_pass = 200           # weight of each passenger (lbs)
W_sing_pass_bag = 40        # weight of each passenger luggage (lbs)
W_sing_crew = 190           # weight of each crew (lbs)
W_sing_crew_bag = 30        # weight of each crew luggage (lbs)

W_crew = num_of_crew * (W_sing_crew + W_sing_crew_bag)      # total crew weight
W_pass = num_of_pass * (W_sing_pass + W_sing_pass_bag)      # total passenger weight
W_payload = W_crew + W_pass

print(f'Payload Weight: {W_payload} lbs')

###################
# Cruise & Loiter #
###################

V = 590.7                       # velocity (ft/sec)
L_D_max = 14                    # based on fig. 3.6 in Raymer
L_D = 0.94 * L_D_max

# ---------------------------- # CRUISE # ---------------------------- #
R = 6_076_000                                                   # range (ft)
C_bhp_cruise = 0.5                                              # turboprop
eta_p_cruise = 0.8                                              # turboprop (propeller efficiency)
C_cruise = TSFC(C_bhp_cruise, V, eta_p_cruise) / 3600           # units should be (1/hr) so /3600 for 1/sec

w3_w2 = np.exp((-R * C_cruise) / (eta_p_cruise * V * L_D))
print("Cruise Fuel Fraction (W3/W2): " + str(round(w3_w2, 3)))

# ---------------------------- # LOITER # ---------------------------- #
E = 30 * 60                                                     # min --> sec
C_bhp_loiter = 0.6                                              # turboprop
eta_p_loiter = 0.8                                              # turboprop (propeller efficiency)
C_loiter = TSFC(C_bhp_loiter, V, eta_p_loiter) / 3600           # units should be (1/hr) so /3600 for 1/sec

w4_w3 = np.exp((-E * C_loiter) / (eta_p_loiter * L_D))
print("Loiter Fuel Fraction (W4/W3): " + str(round(w4_w3, 3)))

####################
# Estimated Stages #
####################

w1_w0 = 0.970                                                   # warmup & takeoff
w2_w1 = 0.985                                                   # climb
w5_w4 = 0.998                                                   # landing

#########
# Final #
#########

w5_w0 = w5_w4 * w4_w3 * w3_w2 * w2_w1 * w1_w0
print("Final Fuel Fraction (W5/w0): " + str(round(w5_w0, 3)))

########
# Fuel #
########

Wf_W0 = (1 - w5_w0) * 1.06      # compute fuel fraction
print("Total Fuel Fraction Wf/w0: {:.3f}".format(Wf_W0))

'''
##########
# Energy #
##########


###########
# Battery #
###########

eta_bat = .95                   # battery efficiency
p_bat = 5000                    # Specific energy (Whr/kg) (5000-11000)
e_star = p_bat * 3600           # Whr/kg * sec/hr * kg/lb = Ws/lb
g = 32.174                      # (ft/s^2)
'''


###############################
# Iterative Weight Estimation #
###############################

w0 = 40_000       # lbs, initial empty weight guess
W0_history = []   # list of all w0 guesses for plot
err = 1e-6        # relative convergence tolerance
delta = 2*err     # any value greater than the tolerance

A = 0.97          # From Raymer Table 3.1
C = -0.05         # From Raymer Table 3.1

while delta > err:
    W0_history.append(w0)                                   # add latest value to list
    We_W0 = A * w0 ** C                                     # lbs, Compute empty weight ratio

    W0_new = (W_payload) / (1 - Wf_W0 - We_W0)    # lbs, compute new TOGW
    delta = abs(W0_new - w0) / abs(W0_new)                  # find difference between last guess and current guess  
    w0 = W0_new                                             # lbs, update TOGW value
    
W0_history = np.array(W0_history)  # convert list to array

###########
# Results #
###########

#m_batt = (R * w0) / (eta_bat * e_star * L_D)
We = We_W0 * w0
#W_bat = w0 - W_crew - W_payload - We


print("Takeoff Gross Weight: " + str(round(w0)) + " lb")
print("Empty Weight: " + str(round(We, 3)) + " lb")
print("Fuel Weight: {}".format(Wf_W0 * w0))
print("Empty Weight Fraction (We_W0): {:.3f}".format(We_W0))
#print("Battery Weight: " + str(round(W_bat,3)) + " lb")
#print("Battery Weight Fraction: {:.3f}".format(W_bat / w0))

########
# Plot #
########

# plt.figure(figsize=(8,4))
# plt.title('Conventional Aircraft Weight Estimate Convergence')
# plt.xlabel("Iteration")
# plt.ylabel("w0 (lbs)")
# plt.plot(W0_history, label='w0', linestyle='-', linewidth=2, marker=None, markersize=8)
# plt.grid(True)
# plt.legend(loc='best')
# plt.show()

print("\n---------- Hybrid Aircraft (Electric Powered Cruise) ----------")
##########################
# Calculate Energy Needs #
##########################

jetFuel_A_SE = 12000 # Whr/kg
total_energy = (w0/2.20462)*jetFuel_A_SE # Whr
print('Total Required Energy: '+str(round(total_energy))+' Whrs')

w3_w2 = 1                                                           # fuel isnt used in cruise therefore ratio = 1

electric_energy = (w1_w0 * w2_w1) * (w0/2.20462) * jetFuel_A_SE    # cruise
fuel_energy = total_energy - electric_energy
print(f'Gas Required Energy: {round(fuel_energy)} Whrs')
w5_w0 = w5_w4 * w4_w3 * w3_w2 * w2_w1 * w1_w0                   # Adjusting Fuel Fraction
wf = (fuel_energy / jetFuel_A_SE) * 2.20462                    # weight of fuel (lbs)
Wf_W0 = (wf / w0) * 1.06                                        # compute fuel fraction
print(f'Fuel Weight Ratio: {Wf_W0}')


#########################
# Hybrid Implementation #
#########################

W0_history_hybrid = []                         # list of all w0 guesses for plot
err = 1e-6        # relative convergence tolerance
delta = 2*err     # any value greater than the tolerance

A = 0.97          # From Raymer Table 3.1
C = -0.05         # From Raymer Table 3.1

eta_bat = .8                                    # battery efficiency
e_star = 1750 * 3600 * 10.76                    # Whr/kg -> J/kg -> m^2/s^2 -> ft^2/s^2
g = 32.17                                       # ft/s^2                     

wb_w0 = (R * g) / (eta_bat * e_star * L_D)              # must be < 1
print(f'Battery Weight Ratio: {wb_w0}')
print(f'Resulting Battery Weight: {wb_w0 * w0} lbf')

while delta > err:
    W0_history_hybrid.append(w0)                                                                # add latest value to list
    We_W0 = A * w0 ** C                                     # lbs, Compute empty weight ratio
    
    W0_new = (W_payload) / (1 - Wf_W0 - We_W0 - (wb_w0))                                        # lbf, compute new TOGW
    delta = abs(W0_new - w0) / abs(W0_new)                                                      # find difference between last guess and current guess  
    w0 = W0_new                                                                                 # lbf, update TOGW value
    
W0_history_hybrid = np.array(W0_history_hybrid)    # convert list to array

# Plot Convergence
plt.figure(figsize=(8,4))
plt.xlabel("Iteration")
plt.ylabel("w0 (lbf)")
plt.plot(W0_history_hybrid, label='w0', linestyle='-', linewidth=2, marker=None, markersize=8)
plt.grid(True)
plt.legend(loc='best')
plt.show()

We = We_W0 * w0

print("Takeoff Gross Weight: " + str(round(w0)) + " lb")
print("Empty Weight: " + str(round(We, 3)) + " lb")
print("Fuel Weight: {}".format(Wf_W0 * w0))
print("Empty Weight Fraction (We_W0): {:.3f}".format(We_W0))