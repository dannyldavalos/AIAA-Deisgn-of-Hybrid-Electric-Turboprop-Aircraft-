import matplotlib.pyplot as plot
import math
import numpy as np
import RequirementsAndParameters as RP
import importlib
importlib.reload(RP)

def Plot_Climb_Requirements(W_S):

    # Aircraft Specifications
    AR = RP.AR                       # Aspect Ratio
    S = RP.wingArea                  # Planform Area
    V_stall = RP.V_stall             # Stall velocity at 5000 ft
    #S = 1185.2649                                          # Planform Area
    #V_stall = 236.293/1.3                                  # Stall Speed at 5000ft
    e_flaps_down = RP.e_L_GU         # Oswald Span Efficiency
    e_flaps_up = RP.e_TO_GU          # Oswald Span Efficiency
    #e_flaps_down = 0.75                                    # Oswald Span Efficiency
    #e_flaps_up = 0.8                                       # Oswald Span Efficiency
    K_flaps_down = 1/(math.pi*e_flaps_down*AR)              # Lift-induced drag coefficient, flaps down
    K_flaps_up = 1/(math.pi*e_flaps_up*AR)                  # Lift-induced drag coefficient, flaps up
    C_D0_clean = RP.CDO_cruise       # Zero lift drag coefficient, flaps up and landing gear retracted
    C_D0_flaps = RP.CDO_TO_GU        # Zero lift drag coefficient, flaps down and landing gear retracted
    C_D0_gear_flaps = RP.CDO_L_GU    # Zero lift drag coefficient, flaps down and landing gear down
    W_TO = RP.WTO                    # Maximum takeoff weight, pound force
    #C_D0_clean = 0.0297                              # Zero lift drag coefficient, flaps up and landing gear retracted
    #C_D0_flaps = 0.0447                              # Zero lift drag coefficient, flaps down and landing gear retracted
    #C_D0_gear_flaps = 0.0637                         # Zero lift drag coefficient, flaps down and landing gear down
    #W_TO = 53000                                     # Maximum takeoff weight, pound force
    W_L = RP.WTO - RP.W_fuel_initial

    # define function to calculate all power loading, given a known stall velocity
    def Calculate_Climb_Requirements_V(S,W,rho,K,K_s,C_D0,V_stall,G):
        V_climb = K_s*V_stall
        C_Lmax = K_s**2*2*W/(rho*V_climb**2*S)
        T_W = K_s**2*C_D0/C_Lmax + K*C_Lmax/K_s**2 + G
        return T_W
    def Convert_T_W_to_W_P(T_W,V_stall,K_s,Eta_p,rho,W_S):
        # V_climb = K_s*V_stall
        V_climb = np.sqrt((2/(rho*1.9))*W_S)
        W_P = 1/(T_W)*Eta_p/V_climb
        return W_P
    
    # Conditions for Take-off climb at sea level
    rho_SL = 0.002377       # Air Density
    K_s_TO = 1.2
    G_TO = 0.017            # Climb Gradient
    Eta_p_TO = 0.65         # Propeller Efficiency
    T_W_TO = (1/0.8)*(4/3)*Calculate_Climb_Requirements_V(S,W_TO,rho_SL,K_flaps_down,K_s_TO,C_D0_flaps,V_stall,G_TO)
    # W_P_TO = Convert_T_W_to_W_P(T_W_TO,V_stall,K_s_TO,Eta_p_TO)
    W_P_TO = Convert_T_W_to_W_P(T_W_TO,V_stall,K_s_TO,Eta_p_TO,rho_SL,W_S)

    # Conditions for Transition Segment Climb
    rho_transition = rho_SL     # Air Density (assuming change in density is negligible)
    K_s_transition = 1.15       # Stall Speed
    G_transition = 0.005        # Climb Gradient
    Eta_p_transition = 0.75     # Propeller Efficiency
    T_W_transition = (1/0.8)*(4/3)*Calculate_Climb_Requirements_V(S,W_TO,rho_transition,K_flaps_down,K_s_transition,C_D0_gear_flaps,V_stall,G_transition)
    W_P_transition = Convert_T_W_to_W_P(T_W_transition,V_stall,K_s_transition,Eta_p_transition,rho_transition,W_S)

    # Conditions for Second Segment Climb (30-400ft)
    rho_2nd = 0.00236322        # Air Density
    K_s_2nd = 1.2
    G_2nd = 0.03                # Climb Gradient
    Eta_p_2nd = 0.75            # Propeller Efficiency
    T_W_2nd = (1/0.8)*(4/3)*Calculate_Climb_Requirements_V(S,W_TO,rho_2nd,K_flaps_down,K_s_2nd,C_D0_flaps,V_stall,G_2nd)
    W_P_2nd = Convert_T_W_to_W_P(T_W_2nd,V_stall,K_s_2nd,Eta_p_2nd,rho_2nd,W_S)

    # Conditions for En-Route Climb
    rho_ER = 0.00270727     # Air Density
    K_s_ER = 1.25
    G_ER = 0.017            # Climb Gradient 
    Eta_p_ER = 0.75         # Propeller Efficiency
    T_W_ER = (1/0.8)*(4/3)*0.94*Calculate_Climb_Requirements_V(S,W_TO,rho_ER,K_flaps_up,K_s_ER,C_D0_clean,V_stall,G_ER)
    W_P_ER = Convert_T_W_to_W_P(T_W_ER,V_stall,K_s_ER,Eta_p_ER,rho_ER,W_S)

    # Conditions for Balked landing, All Engines Operative (AEO)
    rho_BAEO = 0.002377     # Air Density
    K_s_BAEO = 1.3
    G_BAEO = 0.032          # Climb gradient
    Eta_p_BAEO = 0.75       # Propeller Efficiency
    T_W_BAEO = (1/0.8)*(W_L/W_TO)*Calculate_Climb_Requirements_V(S,W_L,rho_BAEO,K_flaps_down,K_s_BAEO,C_D0_gear_flaps,V_stall,G_BAEO)
    W_P_BAEO = Convert_T_W_to_W_P(T_W_BAEO,V_stall,K_s_BAEO,Eta_p_BAEO,rho_BAEO,W_S)

    # Conditions for Balked landing, One Engine Inoperative (OEI)
    rho_BOEI = 0.002377     # Air Density
    K_s_BOEI = 1.5
    G_BOEI = 0.027          # Climb gradient
    Eta_p_BOEI = 0.75       # Propeller Efficiency
    T_W_BOEI = (1/0.8)*(4/3)*(W_L/W_TO)*Calculate_Climb_Requirements_V(S,W_L,rho_BOEI,K_flaps_down,K_s_BOEI,C_D0_gear_flaps,V_stall,G_BOEI)
    W_P_BOEI = Convert_T_W_to_W_P(T_W_BOEI,V_stall,K_s_BOEI,Eta_p_BOEI,rho_BOEI,W_S)
   
    # Convert constants to vectors for plotting and apply correcting factors
    W_P1 = W_P_TO*np.ones(len(W_S))           
    W_P2 = W_P_transition*np.ones(len(W_S))                               
    W_P3 = W_P_2nd*np.ones(len(W_S))                         
    W_P4 = ((rho_ER/rho_SL)**0.75)*W_P_ER*np.ones(len(W_S))     # Applied correction for change in density
    W_P5 = W_P_BAEO*np.ones(len(W_S))
    W_P6 = W_P_BOEI*np.ones(len(W_S))

    # plot.plot(W_S,W_P1,label = "Take-Off Climb")
    # plot.plot(W_S,W_P2,label = "Transition Segment Climb")
    # plot.plot(W_S,W_P3,label = "Second Segment Climb")
    # plot.plot(W_S,W_P4,label = "En-Route Climb")
    # plot.plot(W_S,W_P5,label = "Balked Take-off Climb, AEO")
    # plot.plot(W_S,W_P6,label = "Balked Take-off Climb, OEI")

    return W_P1, W_P2, W_P3, W_P4, W_P5, W_P6
    
N = RP.N
W_S = np.linspace(1,300,N)

# plot.figure()
W_P1, W_P2, W_P3, W_P4, W_P5, W_P6  = Plot_Climb_Requirements(W_S)
# plot.title('Climb Requirements')
# plot.xlabel('Wing Loading W/S')
# plot.ylabel('Power Loading W/P')
# plot.legend()
# plot.show()