import numpy as np
import importlib
import  matplotlib.pyplot as plt
import RequirementsAndParameters as RP


# Reloads the imports in case they are updated
importlib.reload(RP)

# hybridizations = [0.2,0.2,0.05,0.02,0.75,1,1]

# RP imports
AR = RP.AR                              # aspect ratio (-)
e = RP.e_clean                          # oswald efficiency factor (-)
rho = RP.rho_25                         # air density (slug/ft^3)
C_D0 = 0.029
S = RP.wingArea
eta_p = RP.n_p

V = 590.8                               # ft/s
C_bhp = 0.5
c = C_bhp * eta_p / 3600 / 550

payload = 12000                         # lbf
crew = 660                              # lbf

fuel_taxi = 127.36107652537503          # lbf
fuel_takeoff = 169.81476870048834       # lbf
fuel_climb = 877.5454733320721          # lbf
fuel_cruise = 1652.0556739937508        # lbf
fuel_loiter = 131.1456546637096         # lbf
fuel_descent = 0                        # lbf
fuel_landing = 0                        # lbf

fuel_used = fuel_taxi + fuel_takeoff + fuel_climb + fuel_cruise + fuel_loiter + fuel_descent + fuel_landing
fuel_reserve = fuel_used * 0.06
fuel_total = fuel_used + fuel_reserve


MRW = 67193                         # max ramp weight
MTOW = round(MRW - fuel_taxi)       # max takeoff weight

OEW = MRW - fuel_total - payload
print(OEW)

MFW = 5027                          # max fuel weight -- fuel needed for 1000nmi 



def GetRange(W0, W1):

    a2_a1 = (1 / (0.5 * rho * (V ** 2) * S)) * ((1 / (C_D0 * np.pi * AR * e)) ** 0.5)

    a1a2 = (C_D0 / (np.pi * AR * e)) ** 0.5

    R = (eta_p / c) * (1 / (a1a2)) * (np.arctan(W0 * (a2_a1)) - np.arctan(W1 * (a2_a1)))

    return R

# Point A #
Range_A = 0
Payload_A = payload

# Point B #
W0_B = OEW + payload + fuel_total
W1_B = OEW + payload
Range_B = GetRange(W0_B, W1_B)
Payload_B = payload

# Point C #
W0_C = MRW
W1_C = MRW - MFW + fuel_reserve
Range_C = GetRange(W0_C, W1_C)
Payload_C = MRW - MFW - OEW

# Point D #
W0_D = OEW - payload + MFW
W1_D = OEW - payload
Range_D = GetRange(W0_D, W1_D)
Payload_D = 0

# Plot #
RangeArray = [Range_A/6076.12, Range_B/6076.12, Range_C/6076.12, Range_D/6076.12]
PayloadArray = [Payload_A, Payload_B, Payload_C, Payload_D]

plt.plot(RangeArray,PayloadArray)
plt.scatter(RangeArray,PayloadArray)

plt.annotate(f'({round(RangeArray[0],1)} nmi, {round(PayloadArray[0],1)} lbf)', fontsize = 8, xy=(RangeArray[0], PayloadArray[0]), xytext=(-40,Payload_A - 700))
plt.annotate(f'({round(RangeArray[1],1)} nmi, {round(PayloadArray[1],1)} lbf)', fontsize = 8, xy=(RangeArray[1], PayloadArray[1]), xytext=(280,Payload_B - 700))
plt.annotate(f'({round(RangeArray[2],1)} nmi, {round(PayloadArray[2],1)} lbf)', fontsize = 8, xy=(RangeArray[2], PayloadArray[2]), xytext=(475,Payload_C - 200))
plt.annotate(f'({round(RangeArray[3],1)} nmi, {round(PayloadArray[3],1)} lbf)', fontsize = 8, xy=(RangeArray[3], PayloadArray[3]), xytext=(750,Payload_D - 100))


plt.xlabel('Range (nmi)')
plt.ylabel('Payload (lbf)')
plt.ticklabel_format(style='plain', axis='x')

plt.show()

# Phase Range Calculation #
W_taxi_start = MRW
W_taxi_final = W_taxi_start - fuel_taxi
W_takeoff_start = W_taxi_final
W_takeoff_final = W_takeoff_start - fuel_takeoff
W_climb_start = W_takeoff_final
W_climb_final = W_climb_start - fuel_climb
W_cruise_start = W_climb_final
W_cruise_final = W_cruise_start - fuel_cruise
W_loiter_start = W_cruise_final
W_loiter_final = W_loiter_start - fuel_loiter
W_descent_start = W_loiter_final
W_descent_final = W_descent_start - fuel_descent
W_landing_start = W_descent_final
W_landing_final = W_landing_start - fuel_landing

R_taxi = 0
R_takeoff = GetRange(W_takeoff_start, W_takeoff_final)
R_climb = GetRange(W_climb_start, W_climb_final)
R_cruise = GetRange(W_cruise_start, W_cruise_final)
R_loiter = GetRange(W_loiter_start, W_loiter_final)
R_descent = GetRange(W_descent_start, W_descent_final)
R_landing = 0

phase_ranges = [R_taxi, R_takeoff, R_climb, R_cruise, R_loiter, R_descent, R_landing]
i = 0
for range in phase_ranges:
    phase_ranges[i] = range / 6076.12
    i += 1

print(phase_ranges)
print(sum(phase_ranges))