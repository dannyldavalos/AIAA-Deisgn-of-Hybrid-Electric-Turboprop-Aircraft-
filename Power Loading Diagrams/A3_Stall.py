##Kyle Dennis
## A3: Stall Velocity Plots
#imoports
import numpy as np
import matplotlib.pyplot as plt
import math
import RequirementsAndParameters as RP


####        Stall Velocity      ####


def PlotV_StallRequirments(p_s, cl_max,v_stall):
    #calculation

    W_s_ref = 0.5 * p_s * v_stall**2 *cl_max

    N = 100
    T_W = np.linspace(0,0.5,N)
    #w_p = np.ones(N)*W_s_ref
    w_p = np.linspace(0,100,N)
    w_p_from_s = np.linspace(0,100,N)*W_s_ref
    w_s = np.ones(N)*W_s_ref

    # plt.figure()
    # plt.plot(w_s,w_p)
    #plot
    # g = plt.plot(w_p,T_W)
    #plt.axvline(x=W_s_ref, linestyle='--')

    return W_s_ref,w_p

#Arrays
N = 100
T_W = np.linspace(0,0.5,N)

#Parameters
W = 53000.0                 # based on initial estimate + battery estimate
p_s = 0.0020481             # 5000ft density slug/s value from RFP
s_ref = RP.wingArea           # wing area
cl_max = RP.CL_max_cruise 
v_stall = (140/1.3)*1.68781    # kts*1.68781  = ft/s    <141 vapp

#Plot
# plt.figure()
W_s_ref,w_p_stall = PlotV_StallRequirments(p_s, cl_max,v_stall)
# plt.title('Stall Velocity Feasibility')
# plt.xlabel(' Wing Loading W/S')
# plt.ylabel('Power Loading W/P')
#plt.show()