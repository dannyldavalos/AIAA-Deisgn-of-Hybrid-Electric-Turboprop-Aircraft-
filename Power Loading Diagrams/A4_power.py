## Daniela L. Davalos
## A4: Power

# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.linalg import solve
import importlib
import RequirementsAndParameters
import A3_Stall
import A4_Takeoff
import A3_maneuver
import A3_Landing
import A3_CruiseSpeed
import A3_Climb
import A3_Ceiling
from shapely.geometry import LineString

# Reloads the imports in case they are updated
importlib.reload(RequirementsAndParameters)
importlib.reload(A3_Stall)
importlib.reload(A4_Takeoff)
importlib.reload(A3_Climb)
importlib.reload(A3_CruiseSpeed)
importlib.reload(A3_Ceiling)
importlib.reload(A3_maneuver)
importlib.reload(A3_Landing)

# Get power loadings from each mission phase/constraint
PW_stall = np.linspace(0,40,100)
PW_takeoff_1 = 1/A4_Takeoff.plottedValues1
PW_takeoff_2 = 1/A4_Takeoff.plottedValues2
PW_climb_1 = 1/A3_Climb.W_P1
PW_climb_2 = 1/A3_Climb.W_P2
PW_climb_3 = 1/A3_Climb.W_P3
PW_climb_4 = 1/A3_Climb.W_P4
PW_climb_5 = 1/A3_Climb.W_P5
PW_climb_6 = 1/A3_Climb.W_P6
PW_cruise = 1/A3_CruiseSpeed.W_P
PW_ceiling = 1/A3_Ceiling.plottedValues1
PW_maneuver = 1/A3_maneuver.w_p
PW_landing = 1/A3_Landing.plot1

# Serial architecutres efficiencies and power ratios
n_GT = 0.4
n_GB = 0.97
n_EM1 = 0.9
n_EM2 = 0.9
n_P1 = 0.8
n_P2 = 0.8
n_PM = 0.95

# Supplied and shaft power ratios
# SU (Phi), SH (phi)
pr_su_cruise = 0.05     # Supplied power ratio during cruise
pr_sh_cruise = 0.9      # Shaft power ratio during cruise
pr_su_takeoff = 0.1     # Supplied power ratio during takeoff
pr_sh_takeoff = 0.7     # Shaft power ratio during takeoff
pr_su_climb = 0.1       # Supplied power ratio during climb
pr_sh_climb = 0.5       # Shaft power ratio during climb

# Variables
hp = 550                # Conversion factor
N = 300
GT_index = 1
E1_index = 4
BAT_index = 5
W_S_max = 100
W_S_stall = A3_Stall.W_s_ref

W_S_landing = A3_Landing.plot1
W_S = np.linspace(0,W_S_max,N)
W_S_stall_threshold = np.linspace(0,W_S_stall,N)
W_S_stall_array = np.empty(N); 
W_S_stall_array.fill(W_S_stall)
W_S_landing_array = np.empty(N); 
W_S_landing_array.fill(W_S_landing)
W_S_0 = np.zeros(N)
W_P = np.linspace(0,50,N)

# Functions
def getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su,pr_sh,PW):
    
    # Create an 8x8 matrix for serial architecture
    #                1     2      3      4        5          6        7        8      
    A = np.array([[-n_GT,  1  ,   0  ,   0  ,     0     ,    0   ,    0    ,   0   ], # 1
                  [  0  ,-n_GB,   1  ,   0  ,     0     ,    0   ,    0    ,   0   ], # 2
                  [  0  ,  0  ,-n_EM1,   1  ,     0     ,    0   ,    0    ,   0   ], # 3
                  [  0  ,  0  ,   0  , -n_PM,   -n_PM   ,    1   ,    0    ,   0   ], # 4
                  [  0  ,  0  ,   0  ,   0  ,     0     , -n_EM2 ,    1    ,   0   ], # 5
                  [  0  ,  0  ,   0  ,   0  ,     0     ,    0   ,  -n_P2  ,   1   ], # 6
                  [pr_su,  0  ,   0  ,   0  , (pr_su-1) ,    0   ,    0    ,   0   ], # 7
                  [  0  ,  0  ,   0  ,   0  ,     0     ,    0   ,    0    ,   1   ]])# 8
    
    b = np.zeros((8, N))
    b_last_row = PW  # Generate the values for the last row of b
    b[-1, :] = b_last_row

    # Solve the equation Ax=b using NumPy's linalg.solve function
    x = np.linalg.solve(A, b)

    return x

def getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su,pr_sh,PW):
    
    # Create an 9x9 matrix for PTE architecture
    #                1     2      3      4        5          6        7        8       9
    A = np.array([[-n_GT,  1  ,   0  ,   0  ,     0     ,    0   ,    0    ,   0   ,   0   ], # 1
                  [  0  ,-n_GB,   1  ,   1  ,     0     ,    0   ,    0    ,   0   ,   0   ], # 2
                  [  0  ,  0  ,   0  , -n_P1,     0     ,    0   ,    0    ,   1   ,   0   ], # 3
                  [  0  ,  0  ,-n_EM1,   0  ,     1     ,    0   ,    0    ,   0   ,   0   ], # 4
                  [  0  ,  0  ,   0  ,   0  ,   -n_PM   ,    1   ,    0    ,   0   ,   0   ], # 5
                  [  0  ,  0  ,   0  ,   0  ,     0     , -n_EM2 ,    1    ,   0   ,   0   ], # 6
                  [  0  ,  0  ,   0  ,   0  ,     0     ,    0   ,  -n_P2  ,   0   ,   1   ], # 7
                  [  0  ,  0  ,   0  , pr_sh,     0     ,    0   ,(pr_sh-1),   0   ,   0   ], # 8
                  [  0  ,  0  ,   0  ,   0  ,     0     ,    0   ,    0    ,   1   ,   1   ]])# 9
    
    b = np.zeros((9, N))
    b_last_row = PW  # Generate the values for the last row of b
    b[-1, :] = b_last_row

    # Solve the equation Ax=b using NumPy's linalg.solve function
    x = np.linalg.solve(A, b)

    return x

'###########################################################################################################################'
'                                     PARTIAL TURBOELECTRIC ARCHITECTURE                                                    '
'###########################################################################################################################'

x_PW_takeoff_1 = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_takeoff,pr_sh_takeoff,PW_takeoff_1)
x_PW_takeoff_2 = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_takeoff,pr_sh_takeoff,PW_takeoff_2)
x_PW_climb_1 = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_1)
x_PW_climb_2 = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_2)
x_PW_climb_3 = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_3)
x_PW_climb_4 = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_4)
x_PW_climb_5 = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_5)
x_PW_climb_6 = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_6)
x_PW_cruise = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_cruise,pr_sh_cruise,PW_cruise)
x_PW_ceiling = getPTECompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_cruise,pr_sh_cruise,PW_ceiling)
# #x_PW_maneuver = getCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_man,pr_sh_cruise,PW_cruise)

# Gas turbine power loadings W/P
GT_takeoff_1_x = (1/x_PW_takeoff_1[GT_index, :])
GT_takeoff_2_x = (1/x_PW_takeoff_2[GT_index, :])
GT_climb_1_x = (1/x_PW_climb_1[GT_index, :])*hp
GT_climb_2_x = (1/x_PW_climb_2[GT_index, :])*hp
GT_climb_3_x = (1/x_PW_climb_3[GT_index, :])*hp
GT_climb_4_x = (1/x_PW_climb_4[GT_index, :])*hp
GT_climb_5_x = (1/x_PW_climb_5[GT_index, :])*hp
GT_climb_6_x = (1/x_PW_climb_6[GT_index, :])*hp
GT_cruise_x = (1/x_PW_cruise[GT_index, :])*hp
GT_ceiling_x = (1/x_PW_ceiling[GT_index, :])*hp
# #GT_maneuver_x = 1/x_PW_maneuver[1, :]

# E1 power loadings W/P
E1_takeoff_1_x = (1/x_PW_takeoff_1[E1_index, :])
E1_takeoff_2_x = (1/x_PW_takeoff_2[E1_index, :])
E1_climb_1_x = (1/x_PW_climb_1[E1_index, :])*hp
E1_climb_2_x = (1/x_PW_climb_2[E1_index, :])*hp
E1_climb_3_x = (1/x_PW_climb_3[E1_index, :])*hp
E1_climb_4_x = (1/x_PW_climb_4[E1_index, :])*hp
E1_climb_5_x = (1/x_PW_climb_5[E1_index, :])*hp
E1_climb_6_x = (1/x_PW_climb_6[E1_index, :])*hp
E1_cruise_x = (1/x_PW_cruise[E1_index, :])*hp
E1_ceiling_x = (1/x_PW_ceiling[E1_index, :])*hp

# Battery power loadings W/P
BAT_takeoff_1_x = (1/x_PW_takeoff_1[BAT_index, :])
BAT_takeoff_2_x = (1/x_PW_takeoff_2[BAT_index, :])
BAT_climb_1_x = (1/x_PW_climb_1[BAT_index, :])*hp
BAT_climb_2_x = (1/x_PW_climb_2[BAT_index, :])*hp
BAT_climb_3_x = (1/x_PW_climb_3[BAT_index, :])*hp
BAT_climb_4_x = (1/x_PW_climb_4[BAT_index, :])*hp
BAT_climb_5_x = (1/x_PW_climb_5[BAT_index, :])*hp
BAT_climb_6_x = (1/x_PW_climb_6[BAT_index, :])*hp
BAT_cruise_x = (1/x_PW_cruise[BAT_index, :])*hp
BAT_ceiling_x = (1/x_PW_ceiling[BAT_index, :])*hp

a = np.minimum(GT_takeoff_2_x, GT_cruise_x,GT_climb_4_x)

line_1 = LineString(np.column_stack((W_S_landing_array,W_P)))
line_2 = LineString(np.column_stack((W_S,GT_takeoff_1_x)))
intersection = line_1.intersection(line_2)

# line_1_1 = LineString(np.column_stack((W_S,E1_cruise_x)))
# line_2_1 = LineString(np.column_stack((W_S,E1_takeoff_2_x)))
# intersection_1 = line_1_1.intersection(line_2_1)         

GT_x = 18.71
EM1_x = 21.75

plt.figure()
# plt.figure()
#plt.suptitle('PTE Configuration')
plt.subplot(2, 1, 1)
plt.plot(*intersection.xy, 'ro',label = 'Design for min. wing size',zorder=21)
plt.scatter(GT_x,7.38,marker='v',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. GT power',zorder=22)
plt.scatter(EM1_x,6.58,marker='^',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. EM1 power',zorder=22)
# plt.plot(*intersection_1.xy, '*',label = 'Design for min. EM2 power',zorder=22)
#plt.axvline(x=W_S_stall, linestyle='--',label = 'Stall')
plt.plot(W_S,GT_takeoff_1_x, label = 'Take-Off 1',zorder=20)
plt.plot(W_S,GT_takeoff_2_x, label = 'Take-Off 2')
plt.plot(W_S,GT_climb_1_x, label = 'Take-Off Climb')
plt.plot(W_S,GT_climb_2_x, label = 'Transition Segment Climb')
plt.plot(W_S,GT_climb_3_x, label = 'Second Segment Climb')
plt.plot(W_S,GT_climb_4_x, label = 'En-Route Climb')
plt.plot(W_S,GT_climb_5_x, label = 'BSSSalked Take-off Climb, AEO')
plt.plot(W_S,GT_climb_6_x, label = 'Balked Take-off Climb, OEI')
plt.plot(W_S,GT_cruise_x, color = '#00FFFF', label = 'Cruise')
plt.plot(W_S,GT_ceiling_x, label = 'Ceiling')
plt.axvline(x=W_S_landing, linestyle='--',label = 'Landing',color='r')
plt.fill_between(W_S[W_S<W_S_landing], np.zeros(207),a[W_S<W_S_landing],color='#697EF6', alpha=.5,interpolate=True,label='Feasible Region')
plt.ylabel('Gas turbine power loading \n$W_{TO}/P_{GT}$ (lbf/hp)')
plt.ylim([0,10])
plt.xlim([0,80])
plt.grid()


b = np.minimum(E1_takeoff_2_x, E1_cruise_x,GT_climb_4_x)
line_3 = LineString(np.column_stack((W_S,E1_takeoff_1_x)))
intersection2 = line_1.intersection(line_3)

# line3_1 = LineString(np.column_stack((W_S,E1_cruise_x)))
# intersection2_2 = line3_1.intersection(line3_1)
mult = 1
plt.subplot(2, 1, 2)
plt.plot(*intersection2.xy, 'ro',label = 'Design for min. wing size',zorder=21)
plt.scatter(GT_x,9.3,marker='v',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. GT power',zorder=22)
plt.scatter(EM1_x,10,marker='^',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. EM1 power',zorder=22)
# plt.plot(intersection2_2.xy, 'ro',label = 'Design for min. EM2 power',zorder=22)
#plt.axvline(x=W_S_stall, linestyle='--',label = 'Stall')
plt.plot(W_S,E1_takeoff_1_x, label = 'Take-Off 1')
plt.plot(W_S,E1_takeoff_2_x, label = 'Take-Off 2')
plt.plot(W_S,E1_climb_1_x*mult, label = 'Take-Off Climb')
plt.plot(W_S,E1_climb_2_x*mult, label = 'Transition Segment Climb')
plt.plot(W_S,E1_climb_3_x*mult, label = 'Second Segment Climb')
plt.plot(W_S,E1_climb_4_x*mult, label = 'En-Route Climb')
plt.plot(W_S,E1_climb_5_x*mult, label = 'Balked Take-off Climb, AEO')
plt.plot(W_S,E1_climb_6_x*mult, label = 'Balked Take-off Climb, OEI')
plt.plot(W_S,E1_cruise_x*mult, color = '#00FFFF',label = 'Cruise')
plt.plot(W_S,E1_ceiling_x*mult, label = 'Ceiling')
plt.axvline(x=W_S_landing, linestyle='--',label = 'Landing',color='r')
plt.fill_between(W_S[W_S<W_S_landing], np.zeros(207),b[W_S<W_S_landing],color='#697EF6', alpha=.5,interpolate=True,label='Feasible Region')
plt.ylabel('EM1 power loading \n$W_{TO}/P_{EM1}$ (lbf/hp)')
plt.xlabel('Wing loading W/S (psf)')
plt.xlim([0,80])
plt.ylim([0,12])
plt.grid()
plt.savefig('PTE.pdf') 
plt.close('PTE.pdf')
# plt.legend(bbox_to_anchor =(0.5,-1.95),loc='lower center',facecolor='white', framealpha=1,ncol=2)
# plt.tight_layout()

#plt.legend(bbox_to_anchor =(0.5,-2),loc='lower center',facecolor='white', framealpha=1,ncol=2)
# plt.legend(loc='best',facecolor='white', framealpha=1,ncol=2)

c = np.minimum(BAT_takeoff_1_x, BAT_cruise_x,BAT_climb_4_x)
line_4 = LineString(np.column_stack((W_S,E1_takeoff_1_x)))
intersection3 = line_1.intersection(line_4)

# plt.subplot(3, 1, 3)
# plt.plot(*intersection3.xy, 'ro',label = 'Design for min. wing size',zorder=21)
# plt.scatter(EM2_x,5.96,marker='^',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. EM2 power',zorder=22)
# plt.scatter(BAT_x,6.31,marker='H',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. bat. power',zorder=23)
# plt.axvline(x=W_S_stall, linestyle='--',label = 'Stall')
# plt.plot(W_S,BAT_takeoff_1_x, label = 'Take-Off 1')
# plt.plot(W_S,BAT_takeoff_2_x, label = 'Take-Off 2')
# plt.plot(W_S,BAT_climb_1_x, label = 'Take-Off Climb')
# plt.plot(W_S,BAT_climb_2_x, label = 'Transition Segment Climb')
# plt.plot(W_S,BAT_climb_3_x, label = 'Second Segment Climb')
# plt.plot(W_S,BAT_climb_4_x, label = 'En-Route Climb')
# plt.plot(W_S,BAT_climb_5_x, label = 'Balked Take-off Climb, AEO')
# plt.plot(W_S,BAT_climb_6_x, label = 'Balked Take-off Climb, OEI')
# plt.plot(W_S,BAT_cruise_x, color = '#00FFFF', label = 'Cruise')
# plt.plot(W_S,BAT_ceiling_x, label = 'Ceiling')
# plt.axvline(x=W_S_landing, linestyle='--',label = 'Landing',color='r')
# plt.fill_between(W_S[W_S<W_S_stall], np.zeros(193),b[W_S<W_S_stall],color='blue', alpha=.2,interpolate=True,label='Feasible Region')
# plt.xlabel('Wing loading W/S (psf)')
# plt.ylabel('Battery power loading \n$W_{TO}/P_{bat}$ (lbf/hp)')
# plt.xlim([0,80])
# plt.ylim([0,20])
# plt.grid()
#plt.legend(bbox_to_anchor =(0.5,-2), loc='lower center')

'##########################################################################################################################'
'                                            SERIAL ARCHITECTURE                                                           '
'##########################################################################################################################'

x_PW_takeoff_1 = getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_takeoff,pr_sh_takeoff,PW_takeoff_1)
x_PW_takeoff_2 = getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_takeoff,pr_sh_takeoff,PW_takeoff_2)
x_PW_climb_1 = getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_1)
x_PW_climb_2 = getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_2)
x_PW_climb_3 = getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_3)
x_PW_climb_4 = getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_4)
x_PW_climb_5 = getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_5)
x_PW_climb_6 = getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_climb,pr_sh_climb,PW_climb_6)
x_PW_cruise = getSerialCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_cruise,pr_sh_cruise,PW_cruise)
#x_PW_maneuver = getCompPowerLoading(n_GT,n_GB,n_EM1,n_EM2,n_P1,n_P2,n_PM,pr_su_man,pr_sh_cruise,PW_cruise)

# GT power loadings W/P
GT_takeoff_1_x = 1/x_PW_takeoff_1[GT_index, :]
GT_takeoff_2_x = 1/x_PW_takeoff_2[GT_index, :]
GT_climb_1_x = (1/x_PW_climb_1[GT_index, :])*hp
GT_climb_2_x = (1/x_PW_climb_2[GT_index, :])*hp
GT_climb_3_x = (1/x_PW_climb_3[GT_index, :])*hp
GT_climb_4_x = (1/x_PW_climb_4[GT_index, :])*hp
GT_climb_5_x = (1/x_PW_climb_5[GT_index, :])*hp
GT_climb_6_x = (1/x_PW_climb_6[GT_index, :])*hp
GT_cruise_x = (1/x_PW_cruise[GT_index, :])*hp
# #GT_maneuver_x = 1/x_PW_maneuver[1, :]

# E1 power loadings W/P
E1_takeoff_1_x = (1/x_PW_takeoff_1[E1_index, :])
E1_takeoff_2_x = (1/x_PW_takeoff_2[E1_index, :])
E1_climb_1_x = (1/x_PW_climb_1[E1_index, :])*hp
E1_climb_2_x = (1/x_PW_climb_2[E1_index, :])*hp
E1_climb_3_x = (1/x_PW_climb_3[E1_index, :])*hp
E1_climb_4_x = (1/x_PW_climb_4[E1_index, :])*hp
E1_climb_5_x = (1/x_PW_climb_5[E1_index, :])*hp
E1_climb_6_x = (1/x_PW_climb_6[E1_index, :])*hp
E1_cruise_x = (1/x_PW_cruise[E1_index, :])*hp

# Battery power loadings W/P
BAT_takeoff_1_x = (1/x_PW_takeoff_1[BAT_index, :])
BAT_takeoff_2_x = (1/x_PW_takeoff_2[BAT_index, :])
BAT_climb_1_x = (1/x_PW_climb_1[BAT_index, :])*hp
BAT_climb_2_x = (1/x_PW_climb_2[BAT_index, :])*hp
BAT_climb_3_x = (1/x_PW_climb_3[BAT_index, :])*hp
BAT_climb_4_x = (1/x_PW_climb_4[BAT_index, :])*hp
BAT_climb_5_x = (1/x_PW_climb_5[BAT_index, :])*hp
BAT_climb_6_x = (1/x_PW_climb_6[BAT_index, :])*hp
BAT_cruise_x = (1/x_PW_cruise[BAT_index, :])*hp
BAT_ceiling_x = (1/x_PW_ceiling[BAT_index, :])*hp

a = np.minimum(GT_takeoff_2_x, GT_cruise_x, GT_climb_4_x)

line_1 = LineString(np.column_stack((W_S_landing_array,W_P)))
line_2 = LineString(np.column_stack((W_S,GT_takeoff_1_x)))
intersection = line_1.intersection(line_2)

line_1_1 = LineString(np.column_stack((W_S,E1_cruise_x)))
line_2_1 = LineString(np.column_stack((W_S,E1_ceiling_x)))
intersection_1 = line_1_1.intersection(line_2_1)       

GT_x = 19.96
EM2_x = 5.68
BAT_x = 18.04

plt.figure(figsize=(6.5,7.5))
mult = 1
# plt.figure()
# plt.figure()
#plt.suptitle('Serial Configuration')
plt.subplot(3, 1, 1)
plt.plot(*intersection.xy, 'ro',label = 'Design for min. wing size',zorder=21)
plt.scatter(GT_x,8.65,marker='v',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. GT power',zorder=22)
plt.scatter(EM2_x,3.25,marker='^',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. EM2 power',zorder=22)
plt.scatter(BAT_x,8.26,marker='H',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. bat. power',zorder=23)
#plt.axvline(x=W_S_stall, linestyle='--',label = 'Stall')
plt.plot(W_S,GT_takeoff_1_x, label = 'Take-Off 1',zorder=20)
plt.plot(W_S,GT_takeoff_2_x, label = 'Take-Off 2')
plt.plot(W_S,GT_climb_1_x*mult, label = 'Take-Off Climb')
plt.plot(W_S,GT_climb_2_x*mult, label = 'Transition Segment Climb')
plt.plot(W_S,GT_climb_3_x*mult, label = 'Second Segment Climb')
plt.plot(W_S,GT_climb_4_x*mult, label = 'En-Route Climb')
plt.plot(W_S,GT_climb_5_x*mult, label = 'BSSSalked Take-off Climb, AEO')
plt.plot(W_S,GT_climb_6_x*mult, label = 'Balked Take-off Climb, OEI')
plt.plot(W_S,GT_cruise_x*mult, color = '#00FFFF', label = 'Cruise')
plt.plot(W_S,GT_ceiling_x*mult, label = 'Ceiling')
plt.axvline(x=W_S_landing, linestyle='--',label = 'Landing',color='r')
plt.fill_between(W_S[W_S<W_S_landing], np.zeros(207),a[W_S<W_S_landing],color='#697EF6', alpha=.5,interpolate=True,label='Feasible Region')
plt.ylabel('Gas turbine power loading \n$W_{TO}/P_{GT}$ (lbf/hp)')
plt.ylim([0,10])
plt.xlim([0,80])
# plt.legend(loc='upper left',bbox_to_anchor=[1.0,-1.0],ncol=2,facecolor='white', framealpha=1)
plt.grid()

b = np.minimum(E1_cruise_x,E1_ceiling_x)
line_3 = LineString(np.column_stack((W_S,E1_ceiling_x)))
intersection2 = line_1.intersection(line_3)

# line3_1 = LineString(np.column_stack((W_S,E1_cruise_x)))
# intersection2_2 = line3_1.intersection(line3_1)
mult = 1
plt.subplot(3, 1, 2)
plt.plot(*intersection2.xy, 'ro',label = 'Design for min. wing size',zorder=21)
plt.scatter(GT_x,12.63,marker='v',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. GT power',zorder=22)
plt.scatter(EM2_x,23.64,marker='^',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. EM2 power',zorder=22)
plt.scatter(BAT_x,13.42,marker='H',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. bat. power',zorder=23)
# plt.plot(intersection2_2.xy, 'ro',label = 'Design for min. EM2 power',zorder=22)
#plt.axvline(x=W_S_stall, linestyle='--',label = 'Stall')
plt.plot(W_S,E1_takeoff_1_x, label = 'Take-Off 1')
plt.plot(W_S,E1_takeoff_2_x, label = 'Take-Off 2')
plt.plot(W_S,E1_climb_1_x*mult, label = 'Take-Off Climb')
plt.plot(W_S,E1_climb_2_x*mult, label = 'Transition Segment Climb')
plt.plot(W_S,E1_climb_3_x*mult, label = 'Second Segment Climb')
plt.plot(W_S,E1_climb_4_x*mult, label = 'En-Route Climb')
plt.plot(W_S,E1_climb_5_x*mult, label = 'Balked Take-off Climb, AEO')
plt.plot(W_S,E1_climb_6_x*mult, label = 'Balked Take-off Climb, OEI')
plt.plot(W_S,E1_cruise_x*mult, color = '#00FFFF',label = 'Cruise')
plt.plot(W_S,E1_ceiling_x*mult, label = 'Ceiling')
plt.axvline(x=W_S_landing, linestyle='--',label = 'Landing',color='r')
plt.fill_between(W_S[W_S<W_S_landing], np.zeros(207),b[W_S<W_S_landing],color='#697EF6', alpha=.5,interpolate=True,label='Feasible Region')
plt.ylabel('EM1 power loading \n$W_{TO}/P_{EM1}$ (lbf/hp)')
plt.xlim([0,80])
plt.ylim([0,25])
plt.grid()

c = np.minimum(BAT_takeoff_2_x, BAT_cruise_x,BAT_climb_4_x)
line_4 = LineString(np.column_stack((W_S,BAT_takeoff_1_x)))
intersection3 = line_1.intersection(line_4)
mult = 1
plt.subplot(3, 1, 3)
plt.plot(*intersection3.xy, 'ro',label = 'Design for min. wing size',zorder=21)
plt.scatter(GT_x,7.82,marker='v',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. GT power',zorder=22)
plt.scatter(EM2_x,3.42,marker='^',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. EM2 power',zorder=22)
plt.scatter(BAT_x,8.55,marker='H',facecolors='white',linewidths = 1.5,edgecolors='black',label = 'Design for min. bat. power',zorder=23)
#plt.axvline(x=W_S_stall, linestyle='--',label = 'Stall')
plt.plot(W_S,BAT_takeoff_1_x*mult, label = 'Take-Off 1')
plt.plot(W_S,BAT_takeoff_2_x*mult, label = 'Take-Off 2')
plt.plot(W_S,BAT_climb_1_x*mult, label = 'Take-Off Climb')
plt.plot(W_S,BAT_climb_2_x*mult, label = 'Transition Segment Climb')
plt.plot(W_S,BAT_climb_3_x*mult, label = 'Second Segment Climb')
plt.plot(W_S,BAT_climb_4_x*mult, label = 'En-Route Climb')
plt.plot(W_S,BAT_climb_5_x*mult, label = 'Balked Take-off Climb, AEO')
plt.plot(W_S,BAT_climb_6_x*mult, label = 'Balked Take-off Climb, OEI')
plt.plot(W_S,BAT_cruise_x*mult, color = '#00FFFF', label = 'Cruise')
plt.plot(W_S,BAT_ceiling_x*mult, label = 'Ceiling')
plt.axvline(x=W_S_landing, linestyle='--',label = 'Landing',color='r')
#plt.fill_between(W_S[W_S<W_S_landing], np.zeros(207),c[W_S<W_S_landing],color='#697EF6', alpha=.5,interpolate=True,label='Feasible Region')
plt.xlabel('Wing loading W/S (psf)')
plt.ylabel('Battery power loading \n$W_{TO}/P_{bat}$ (lbf/hp)')
plt.xlim([0,80])
plt.ylim([0,30])
plt.grid()
plt.savefig('Serial.pdf') 
plt.close('Serial.pdf')
plt.legend(bbox_to_anchor =(0.5,-1.95),loc='lower center',facecolor='white', framealpha=1,ncol=2)
plt.tight_layout()
plt.legend(loc='center left', bbox_to_anchor=(1, 0))

# plt.tight_layout()

plt.show()