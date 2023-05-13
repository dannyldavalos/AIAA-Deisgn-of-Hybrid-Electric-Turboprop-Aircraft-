# Daniela L. Davalos
# EAE 130A
# Cost Analysis
# March 11, 2023
# Updated 5/12/2023

import math
import numpy as np
import RequirementsAndParameters
import importlib
np.set_printoptions(threshold=np.inf)
importlib.reload(RequirementsAndParameters) 

WTO = RequirementsAndParameters.WTO

def cost_analysis(W,V_H,Q,Q_M,Q_PROTO,N_motor,N_engine,P_ICE,P_EM,P_EM_total,E_BAT,N_Prop,Dp,P_SHP):

    # Factors for hybrid-electric propulsion [unitless]
    F_HyE_ENG = 1.5     # Engineering cost
    F_HyE_TOOL = 1.10   # Tooling cost
    F_HyE_MFG = 1.10    # Manufacturing cost
    F_HyE_DEV = 1.05    # Development support cost
    F_HyE_FT = 1.50     # Flight test operations cost
    F_HyE_QC = 1.50     # Quality control cost
    F_HyE_MAT = 1.05    # Materials cost

    # Labor rates [$/hr]
    R_ENG = 92
    R_TOOL = 61
    R_MFG = 53

    # Consumer price index
    CPI = 1.31 # adjusted for 2022

    # Engineering cost
    # C_ENG = (0.083*(W**0.791)*(V_H**1.521)*(Q**0.183)*F_HyE_ENG*R_ENG*CPI)/Q
    # # Tooling cost
    # C_TOOL = (2.1036*(W**0.764)*(V_H**0.899)*(Q**0.178)*(Q_M**0.066)*F_HyE_TOOL*R_TOOL*CPI)/Q
    # # Manufacturing cost
    # C_MFG = (20.2588*(W**0.74)*(V_H**0.543)*(Q**0.524)*(F_HyE_MFG)*(R_MFG)*CPI)/Q
    # # Development support cost
    # C_DEV = (0.06458*(W**0.873)*(V_H**1.89)*(Q_PROTO**0.346)*CPI*F_HyE_DEV)/Q
    # #C_DEV = 45.42*(W**0.630)*(V_H**1.3)*CPI*F_HyE_DEV
    # # Flight test operations cost
    # C_FT = (0.009646*(W**1.16)*(V_H**1.3718)*(Q_PROTO**1.281)*CPI*F_HyE_FT)/Q
    # # Quality control cost
    # C_QC = (0.13*C_MFG*F_HyE_QC)/Q
    # # Materials cost
    # C_MAT = (24.896*(W**0.689)*(V_H**0.624)*(Q**0.792)*CPI*F_HyE_MAT)/Q
    C_ENG = (0.083*(W**0.791)*(V_H**1.521)*(Q**0.183)*F_HyE_ENG*R_ENG*CPI)/Q
    # Tooling cost
    C_TOOL = (2.1036*(W**0.764)*(V_H**0.899)*(Q**0.178)*(Q_M**0.066)*F_HyE_TOOL*R_TOOL*CPI)/Q
    # Manufacturing cost
    C_MFG = (20.2588*(W**0.74)*(V_H**0.543)*(Q**0.524)*(F_HyE_MFG)*(R_MFG)*CPI)/Q
    # Development support cost
    C_DEV = (0.06458*(W**0.873)*(V_H**1.89)*(Q_PROTO**0.346)*CPI*F_HyE_DEV)/Q
    #C_DEV = 45.42*(W**0.630)*(V_H**1.3)*CPI*F_HyE_DEV
    # Flight test operations cost
    C_FT = (0.009646*(W**1.16)*(V_H**1.3718)*(Q_PROTO**1.281)*CPI*F_HyE_FT)
    # Quality control cost
    C_QC = (0.13*C_MFG*F_HyE_QC)/Q
    # Materials cost
    C_MAT = (24.896*(W**0.689)*(V_H**0.624)*(Q**0.792)*CPI*F_HyE_MAT)/Q
    #C_MAT = 11*(W**0.921)*(V_H**0.621)*(Q**0.799)
    # Piston engine cost
    C_ICE = (174*N_engine*P_ICE*CPI)
    # Electric motor cost
    C_EM = (174*N_motor*P_EM*CPI)
    # Power management cost
    C_PMS = (150*P_EM_total*CPI)
    # Battery cost
    C_BAT = (200*(E_BAT)*CPI)
    # Propeller cost
    C_CS_Prop = (210*N_Prop*CPI*(Dp**2)*( (P_SHP/Dp)**0.12 ))

    # Crew Cost
    bCEF = 5.17053 + 0.104981*(1989 - 2006)
    tCEF = 5.17053 + 0.104981*(2035 - 2006)
    CEF = tCEF/bCEF
    time = 3 # hours
    AF = 0.8
    P_elec = 500
    e_elec = 600
    K = 2.75
    K_dep = 2.75
    n_attd = 2
    p_elec = 500
    p_oil = 4.15
    rho_oil = 7.39
    n = 20
    t_b = 3
    W_b = 1000
    W_f = 4500
    # Ccrew = (440 + 0.532*WTO/1000)*CEF*time
    

    C_civil = C_ENG + C_TOOL + C_MFG + C_DEV + C_FT + C_QC + C_MAT + C_ICE + C_EM + C_PMS + C_BAT + C_CS_Prop
    insur = .15
    C_insur = insur*(C_civil) 
    profit = .15    
    C_profit = profit*(C_civil + C_insur)
    salesPrice = C_civil + C_insur + C_profit

    C_crew = AF*K*WTO**0.4*t_b*CEF
    C_attd = 60*n_attd*CEF*t_b
    C_fuel = 1.05*W_b*P_elec/e_elec
    W_oil = 0.0125*W_f*t_b/100
    C_oil = 1.02*W_oil*p_oil/rho_oil
    C_airport = 1.5*WTO/1000*CEF

    # FOC
    C_unit = salesPrice
    U_annual = 1.5e3*(3.4546*t_b + 2.994 - (12.289*t_b**2 - 5.6626*t_b + 8.964)**0.5)

    C_insur2 = .02*salesPrice*t_b/U_annual
    C_dep = C_unit*(1+K_dep)*t_b/(n*U_annual)
    C_COC = C_crew + C_attd + C_fuel + C_oil + C_airport
    C_reg = (.001+1e-8*WTO)*C_COC

    C_COC = C_crew + C_attd + C_fuel + C_oil + C_airport
    C_FOC = C_insur2+C_dep+C_reg

    C_DOC = C_COC + C_FOC

    print('Engineering cost:             ${:,.2f}'.format(C_ENG))
    print('Tooling cost:                 ${:,.2f}'.format(C_TOOL))
    print('Manufacturing:                ${:,.2f}'.format(C_MFG))
    print('Development support cost:     ${:,.2f}'.format(C_DEV))
    print('Flight test operations cost:  ${:,.2f}'.format(C_FT))
    print('Quality control cost:         ${:,.2f}'.format(C_QC))
    print('Materials cost:               ${:,.2f}'.format(C_MAT))
    print('Piston engine cost ({} eng.):  ${:,.2f}'.format(N_engine,C_ICE))
    print('Electric motor cost ({} EMs):  ${:,.2f}'.format(N_motor,C_EM))
    print('Power management cost:        ${:,.2f}'.format(C_PMS))
    print('Battery cost:                 ${:,.2f}'.format(C_BAT))
    print('Propeller cost ({} prop.):     ${:,.2f}'.format(N_Prop,C_CS_Prop))
    print('Production cost:              ${:,.2f}'.format(C_civil))
    print('Insurance ({}%):            ${:,.2f}'.format(insur*100,C_insur))
    print('Profit ({}%):               ${:,.2f}'.format(profit*100,C_profit))
    print('Sales Price:                  ${:,.2f}'.format(salesPrice))
    print('C_insur:                  ${:,.2f}'.format(C_insur))
    print('C_dep:                  ${:,.2f}'.format(C_dep))
    print('C_reg:                  ${:,.2f}'.format(C_reg))
    print('COC:                  ${:,.2f}'.format(C_COC))
    print('FOC:                  ${:,.2f}'.format(C_FOC))
    print('DOC:                  ${:,.2f}'.format(C_DOC))
    print('CEF:                  {:,.2f}'.format(CEF))
    
    return C_civil , C_ENG, C_TOOL , C_MFG , C_DEV , C_FT , C_QC , C_MAT , C_ICE, C_EM , C_PMS , C_BAT , C_CS_Prop, C_DOC

# Concept 1: Saab 340
W_empty = 19000
W = 0.5*W_empty         # structural weight [lbs]
V_H = 283               # maximum level airspeed [KTAS]
Q = 35*5                # number of aircraft to be produced over a 5-year period (35/year*5years)
Q_M = 35/12             # number of aircraft produced in one month (35/year*1year/12months)
Q_PROTO = 1             # number of prototype aircraft to be produced
N_motor = 4             # number of motors
N_engine = N_motor      # number of engines
P_ICE = 150             # power of piston engine [hp]
P_EM = 150              # power of electric motor [hp]
P_EM_total = 0.85*P_EM  # power management system [hp], approximately 85% of the EM is assumed
E_BAT = 25              # battery energy [kWh]
N_Prop = N_motor        # number of propellers
Dp = 12.9               # propeller diameter
P_SHP = 2500            # power of propeller? [hp]

print('----------------------------')
print('Concept 1: Saab 340\n')
C_civil , C_ENG, C_TOOL , C_MFG , C_DEV , C_FT , C_QC , C_MAT , C_ICE, C_EM , C_PMS , C_BAT , C_CS_Prop, C_DOC = cost_analysis(W,V_H,Q,Q_M,Q_PROTO,N_motor,N_engine,P_ICE,P_EM,P_EM_total,E_BAT,N_Prop,Dp,P_SHP)

# Concept 2: ATR 72
W_empty = 28700
W = 0.5*W_empty         # structural weight [lbs]
V_H = 346               # maximum level airspeed [KTAS]
Q = 33*5                # number of aircraft to be produced over a 5-year period (15/year*5years)
Q_M = 33/12             # number of aircraft produced in one month (15/year*1year/12months)
Q_PROTO = 1             # number of prototype aircraft to be produced
N_motor = 2             # number of motors
N_engine = N_motor      # number of engines
P_ICE = 150             # power of piston engine [hp]
P_EM = 150              # power of electric motor [hp]
P_EM_total = 0.85*P_EM  # power management system [hp], approximately 85% of the EM is assumed
E_BAT = 25              # battery energy [kWh]
N_Prop = N_motor        # number of propellers
Dp = 12.9               # propeller diamete
P_SHP = 2750            # power of propeller? [hp]

print('----------------------------')
print('Concept 2: ATR 72\n')
C_civil , C_ENG, C_TOOL , C_MFG , C_DEV , C_FT , C_QC , C_MAT , C_ICE, C_EM , C_PMS , C_BAT , C_CS_Prop, C_DOC = cost_analysis(W,V_H,Q,Q_M,Q_PROTO,N_motor,N_engine,P_ICE,P_EM,P_EM_total,E_BAT,N_Prop,Dp,P_SHP)

# Concept 3: Bombardier Dash-8 Q300
W_empty = 26000
W = 0.5*W_empty         # structural weight [lbf]
V_H = 287               # maximum level airspeed [KTAS]
Q = 35*5                # number of aircraft to be produced over a 5-year period (35/year*5years)
Q_M = 35/12             # number of aircraft produced in one month (35/year*1year/12months)
Q_PROTO = 1             # number of prototype aircraft to be produced
N_motor = 4             # number of motors
N_engine = N_motor      # number of engines
P_ICE = 150             # power of piston engine [hp]
P_EM = 150              # power of electric motor [hp]
P_EM_total = 0.85*P_EM  # power management system [hp], approximately 85% of the EM is assumed
E_BAT = 25              # battery energy [kWh]
N_Prop = N_motor        # number of propellers
Dp = 12.99213           # propeller diameter [ft]
P_SHP = 2500            # power of each propeller [hp]

print('----------------------------')
print('Concept 3: Bombardier Dash-8 Q300\n')
C_civil , C_ENG, C_TOOL , C_MFG , C_DEV , C_FT , C_QC , C_MAT , C_ICE, C_EM , C_PMS , C_BAT , C_CS_Prop, C_DOC = cost_analysis(W,V_H,Q,Q_M,Q_PROTO,N_motor,N_engine,P_ICE,P_EM,P_EM_total,E_BAT,N_Prop,Dp,P_SHP)

# CoulAir
W_empty = RequirementsAndParameters.WTO
W = 0.5*(0.5*W_empty)         # structural weight [lbf]
V_H = 350               # maximum level airspeed [KTAS]
Q = 35*5                # number of aircraft to be produced over a 5-year period (35/year*5years)
Q_M = 35/12             # number of aircraft produced in one month (35/year*1year/12months)
Q_PROTO = 1             # number of prototype aircraft to be produced
N_motor = 4             # number of motors
N_engine = N_motor      # number of engines
P_ICE = 150             # power of piston engine [hp]
P_EM = 150              # power of electric motor [hp]
P_EM_total = 0.85*P_EM  # power management system [hp], approximately 85% of the EM is assumed
E_BAT = 25              # battery energy [kWh]
N_Prop = N_motor        # number of propellers
Dp = 12.99213           # propeller diameter [ft]
P_SHP = 2500            # power of each propeller [hp]

print('----------------------------')
print('CoulAir\n')
C_civil , C_ENG, C_TOOL , C_MFG , C_DEV , C_FT , C_QC , C_MAT , C_ICE, C_EM , C_PMS , C_BAT , C_CS_Prop, C_DOC = cost_analysis(W,V_H,Q,Q_M,Q_PROTO,N_motor,N_engine,P_ICE,P_EM,P_EM_total,E_BAT,N_Prop,Dp,P_SHP)

