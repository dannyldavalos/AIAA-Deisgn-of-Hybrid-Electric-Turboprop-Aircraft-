## Daniela L. Davalos
## A6: PS Diagram

# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.linalg import solve
import importlib
import RequirementsAndParameters as RP
import A3_Stall
import A4_Takeoff
import A3_maneuver
import A3_Landing
import A3_CruiseSpeed
import A3_Climb
import A3_Ceiling
import WeightCode as WC
# from shapely.geometry import LineString

# Reloads the imports in case they are updated
importlib.reload(RP)
importlib.reload(A3_Stall)
importlib.reload(A4_Takeoff)
importlib.reload(A3_Climb)
importlib.reload(A3_CruiseSpeed)
importlib.reload(A3_Ceiling)
importlib.reload(A3_maneuver)
importlib.reload(A3_Landing)

WTO = WC.W0

# Variables
hp = 550                # Conversion factor
N = 300
GT_index = 1
E1_index = 4
BAT_index = 5
W_S_max = 100
W_S_stall = A3_Stall.W_s_ref

# Get power l
mult = 1
P_stall = (np.linspace(0,40,100))*mult
P_takeoff_1 = (WTO/A4_Takeoff.plottedValues1)*mult
P_takeoff_2 = (WTO/A4_Takeoff.plottedValues2)*mult
P_climb_1 = (WTO/A3_Climb.W_P1)/hp*mult
P_climb_2 = (WTO/A3_Climb.W_P2)/hp*mult
P_climb_3 = (WTO/A3_Climb.W_P3)/hp*mult
P_climb_4 = (WTO/A3_Climb.W_P4)/hp*mult
P_climb_5 = (WTO/A3_Climb.W_P5)/hp*mult
P_climb_6 = (WTO/A3_Climb.W_P6)/hp*mult
P_cruise = (WTO/A3_CruiseSpeed.W_P)/hp*mult
P_ceiling = (WTO/A3_Ceiling.plottedValues1)/hp*mult
P_maneuver = (WTO/A3_maneuver.w_p)/hp*mult
P_landing = (WTO/A3_Landing.plot1)/hp*mult


W_S_landing = A3_Landing.plot1
S_landing = WTO/W_S_landing 
W_S = np.linspace(0,W_S_max,N)
W_S_stall_threshold = np.linspace(0,W_S_stall,N)
W_S_stall_array = np.empty(N); 
W_S_stall_array.fill(W_S_stall)
W_S_landing_array = np.empty(N); 
W_S_landing_array.fill(W_S_landing)
W_S_0 = np.zeros(N)
W_P = np.linspace(0,50,N)

# S = WTO/W_S

S = np.linspace(0,3000,N)

multf = 2
plt.figure()
WP_TO = A4_Takeoff.plottedValues1
WP_TO2 = A4_Takeoff.plottedValues2
plt.plot(W_S,WP_TO*multf, label = 'Take-Off 1')
plt.plot(W_S,WP_TO2*multf, label = 'Take-Off 2')
plt.plot(W_S,(A3_Climb.W_P1*hp)*multf, label = 'Take-Off Climb')
plt.plot(W_S,(A3_Climb.W_P2*hp)*multf, label = 'Transition Segment Climb')
plt.plot(W_S,(A3_Climb.W_P3*hp)*multf, label = 'Second Segment Climb')
plt.plot(W_S,(A3_Climb.W_P4*hp)*multf, label = 'En-Route Climb')
plt.plot(W_S,(A3_Climb.W_P5*hp)*multf, label = 'Balked Take-off Climb, AEO')
plt.plot(W_S,(A3_Climb.W_P6*hp)*multf, label = 'Balked Take-off Climb, OEI')
plt.plot(W_S,(A3_CruiseSpeed.W_P*hp)*multf, color = '#00FFFF', label = 'Cruise')
plt.plot(W_S,(A3_Ceiling.plottedValues1*hp)*multf, label = 'Ceiling')
plt.axvline(x=W_S_landing, linestyle='--',label = 'Landing',color='r')
# plt.fill_between(W_S[W_S<W_S_landing], np.zeros(207),[W_S<W_S_landing],color='#697EF6', alpha=.5,interpolate=True,label='Feasible Region')
plt.ylabel('W/P (lbf/hp)')
plt.xlabel('W/S (lbf/ft$^2$)')
plt.ylim([0,20])
plt.xlim([0,80])
plt.legend(facecolor='white', framealpha=1)
plt.grid()
plt.savefig('CDR_WP.pdf') 
plt.close('CDR_WP.pdf')

WP = 3.65
Ppoint = (1/WP)*WTO
Spoint = (1/W_S_landing)*WTO

print(Ppoint)

plt.figure()
plt.plot(S,P_takeoff_1, label = 'Take-Off 1')
plt.plot(S,P_takeoff_2, label = 'Take-Off 2')
plt.plot(S,P_climb_1, label = 'Take-Off Climb')
plt.plot(S,P_climb_2, label = 'Transition Segment Climb')
plt.plot(S,P_climb_3, label = 'A6Second Segment Climb')
plt.plot(S,P_climb_4, label = 'En-Route Climb')
plt.plot(S,P_climb_5, label = 'Balked Take-off Climb, AEO')
plt.plot(S,P_climb_6, label = 'Balked Take-off Climb, OEI')
plt.plot(S,P_cruise, color = '#00FFFF', label = 'Cruise')
plt.plot(S,P_ceiling, label = 'Ceiling')
plt.scatter(Spoint,Ppoint,marker='o',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. wing size',zorder=22)
plt.axvline(x=S_landing, linestyle='--',label = 'Landing',color='r')
# plt.fill_between(W_S[W_S<W_S_landing], np.zeros(207),a[W_S<W_S_landing],color='#697EF6', alpha=.5,interpolate=True,label='Feasible Region')
plt.ylabel('Power (hp)')
plt.xlabel('Area (ft$^2$)')
plt.ylim([0,30000])
plt.xlim([0,3000])
# plt.legend(facecolor='white', framealpha=1)
plt.grid()
plt.savefig('CDR_PS.pdf') 
plt.close('CDR_PS.pdf')
plt.show()