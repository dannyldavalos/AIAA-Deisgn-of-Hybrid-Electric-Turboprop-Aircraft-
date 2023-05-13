# Daniela L. Davalos, Duncan Koelzer
# EAE 130A
# Center of Gravity
# April 13, 2023
# Updated 5/10/2023

import math
import numpy as np
import RequirementsAndParameters as RP
import CDR_NeutralPoint as NP
import CDR_RevisedEmptyWeight as REW
import importlib
from matplotlib import pyplot as plt
importlib.reload(RP) 
importlib.reload(NP) 
importlib.reload(REW) 
np.set_printoptions(threshold=np.inf)

WTO = RP.WTO

'----------------------------------------------'
'              Airframe Structure              '
'----------------------------------------------'

# Wing
S_w = RP.wingArea
MAC_w = RP.MAC_w
# W_wing = (2.5*S_w) # [lbf/ft^2*ft^2v = lbf] # Table 15.2 from Raymer
W_wing = REW.W_wing
x_wing = 26 + 0.4*RP.MAC_w       # ft
xw_wing = W_wing*x_wing

# Horizontal tail
S_horiz_tail = RP.S_horiz_tail
MAC_ht = RP.MAC_ht
# W_horiz_tail = 2*S_horiz_tail # Table 15.2 from Raymer
W_horiz_tail = REW.W_HorizontalTail
x_ht = 74
xw_ht = W_horiz_tail*x_ht

# Vertical tail
S_vert_tail = RP.S_vert_tail
MAC_vt = RP.MAC_vt
# W_vert_tail = 2*S_vert_tail # Table 15.2 from Raymer
W_vert_tail = REW.W_VerticalTail
x_vt = 60
xw_vt = W_vert_tail*x_vt

# Fuselage
S_wet_fuse = RP.S_wet_fuse
# W_fuse = (1.4*S_wet_fuse) # Table 15.2 from Raymer
W_fuse = REW.W_fuselage
fuseLength = RP.fuseLength
x_fuse = .4*fuseLength
xw_fuse = W_fuse*x_fuse

# Landing gear nose
# W_LGN = .15*.057*WTO
W_LGN = REW.W_noseLandingGear
x_LGN = 7
xw_LGN = W_LGN*x_LGN

# Landing gear main
# W_LGM = .85*.057*WTO
W_LGM = REW.W_mainLandingGear
x_LGM = 40
xw_LGM = W_LGM*x_LGM

'-------------x*w of airframe structure---------------'
xw_airframestructure = xw_wing + xw_ht + xw_vt + xw_fuse + xw_LGN + xw_LGM
W_airframestructure = W_wing + W_horiz_tail + W_vert_tail + W_fuse + W_LGN + W_LGM
x_airframestructure = x_wing + x_ht + x_vt + x_fuse + x_LGN + x_LGM
'----------------------------------------------'
'                Propulsion                    '
'----------------------------------------------'

# Engine
W_engine = RP.W_engine
W_install_eng = 1.4*W_engine
x_eng = 26
xw_eng = W_engine*x_eng

# Fuel
W_fuel_max = RP.W_fuel_initial
W_fuel_min = RP.W_fuel_final
W_fuel = W_fuel_max
x_fuel = x_wing     # Assumption based on fuel being stored in the wing
xw_fuel = W_fuel*x_fuel

'--------------x*w of propulsion----------------'
xw_propulsion = xw_eng + xw_fuel
w_propulsion = W_install_eng + W_fuel
x_propulsion = x_eng + x_fuel

'----------------------------------------------'
'             Control Systems                  '
'----------------------------------------------'

W_airconditioning = REW.W_airconditioning
x_airconditioning = 15
xw_airconditioning = x_airconditioning*W_airconditioning

W_APUinstalled = REW.W_APUinstalled
x_APUinstalled = RP.fuseLength - 5 # Near tail of aircraft
xw_APUinstalled = x_APUinstalled*W_APUinstalled

W_hydraulics = REW.W_hydraulics
x_hydraulics = x_LGM - 10
xw_hydraulics = x_hydraulics*W_hydraulics

W_enginecontrols = REW.W_enginecontrols
x_enginecontrols = 5 # In cockpit
xw_enginecontrols = x_enginecontrols*W_enginecontrols

W_flightcontrols = REW.W_flightcontrols
x_flightcontrols = 5 # In cockpit
xw_flightcontrols = x_flightcontrols*W_flightcontrols

'------------x*w of control systems------------------'
xw_controlsystems = xw_airconditioning + xw_APUinstalled + xw_hydraulics + xw_enginecontrols + xw_flightcontrols
w_controlsystems = W_airconditioning + W_APUinstalled + W_hydraulics + W_enginecontrols + W_flightcontrols
x_controlsystems = x_airconditioning + x_APUinstalled + x_hydraulics + x_enginecontrols + x_flightcontrols
'----------------------------------------------'
'                Systems                       '
'----------------------------------------------'

W_antiice = REW.W_antiice
x_antiice = x_wing
xw_antiice = x_antiice*W_antiice

W_avionics = REW.W_avionics
x_avionics = 3  # In the nose of the aircraft
xw_avionics = x_avionics*W_avionics

W_electrical = REW.W_electrical
x_electrical = x_wing   # a lot of wiring needed in the wings, before/after wings will approx. balance
xw_electrical = x_electrical*W_electrical

W_fuelsystem = REW.W_fuelsystem
x_fuelsystem = x_fuel
xw_fuelsystem = x_fuelsystem*W_fuelsystem

W_furnishings = REW.W_furnishings
x_furnishings = 10
xw_furnishings = x_furnishings*W_furnishings

W_handlinggear =  REW.W_handlinggear
x_handlinggear = 5
xw_handlinggear = x_handlinggear*W_handlinggear

W_instruments = REW.W_instruments
x_instruments = 5.8 # In cockpit
xw_instruments = x_instruments*W_instruments

# # Not needed (is multiplied by 0 to neglect)
# W_militarycargohandlingsystem = REW.W_militarycargohandlingsystem
# x_militarycargohandlingsystem = 1
# xw_militarycargohandlingsystem = x_militarycargohandlingsystem*W_militarycargohandlingsystem*0

W_starterpneumatic = REW.W_starterpneumatic
x_starterpneumatic = x_eng
xw_starterpneumatic = x_starterpneumatic*W_starterpneumatic

'---------------x*w of systems-----------------'
xw_systems = xw_antiice + xw_avionics + xw_electrical + xw_fuelsystem + xw_furnishings + xw_handlinggear + xw_instruments + xw_starterpneumatic
W_systems = W_antiice + W_avionics + W_electrical + W_fuelsystem + W_furnishings + W_handlinggear + W_instruments + W_starterpneumatic
x_systems = x_antiice + x_avionics + x_electrical + x_fuelsystem + x_furnishings + x_handlinggear + x_instruments + x_starterpneumatic
'----------------------------------------------'
'                Payload                       '
'----------------------------------------------'

# Crew
W_crew = RP.crew_W_tot
x_crew = 5
xw_crew = W_crew*x_crew

# Crew baggage
W_crew_bag= RP.crew_bag_W
x_crew_bag = 30
xw_crew_bag = W_crew_bag*x_crew_bag

# Passengers
W_pass = RP.pass_W
x_pass = 35
xw_pass = W_pass*x_pass

# Passenger baggage
W_pass_bag = RP.pass_bag_W_tot
x_pass = 25
xw_pass_bag = W_pass_bag*x_pass

'-------------x*w of payload-----------------'
xw_payload = xw_crew + xw_crew_bag + xw_pass + xw_pass_bag
w_payload = W_crew + W_crew_bag + W_pass + W_pass_bag
# # All-else empty
# W_else = 0.1*WTO
# x_else = 0.48*fuseLength
# xw_else = W_else*x_else

'-------------CG calculation------------------'
W_tot = RP.WTO
#W = W_wing+W_fuel+W_horiz_tail+W_vert_tail+W_fuse+W_LGM+W_LGN+W_install_eng+W_crew+W_pass+W_pass_bag
W = W_airframestructure + w_propulsion + w_controlsystems + W_systems + w_payload
c = RP.MAC_w

xnp = NP.xnp_nose
xcg = (xw_airframestructure + xw_propulsion + xw_controlsystems + xw_systems  + xw_payload) / W

SM = (xnp-xcg)/MAC_w

# Case 1: empty
# Case 2: crew
# Case 3: crew + fuel
# Case 4: crew + fuel + passengers/cargo

W1 = W_airframestructure + W_install_eng + w_controlsystems + W_systems
x1 = (xw_airframestructure + xw_eng + xw_systems + xw_controlsystems) / W1

W2 = W_airframestructure + W_install_eng + w_controlsystems + W_systems + W_crew + W_crew_bag 
x2 = (xw_airframestructure + xw_eng + xw_systems + xw_controlsystems + xw_crew + xw_crew_bag) / W2

W3 = W_airframestructure + W_install_eng + w_controlsystems + W_systems + W_crew + W_crew_bag + W_fuel 
x3 = (xw_airframestructure + xw_eng + xw_systems + xw_controlsystems+xw_crew + xw_crew_bag + xw_fuel) / W3

W4 = W_airframestructure + W_install_eng + w_controlsystems + W_systems + W_crew + W_crew_bag + W_fuel + W_pass + W_pass_bag
x4 = (xw_airframestructure + xw_propulsion + xw_controlsystems + xw_systems  + xw_payload) / W4

print('x_cg = ',xcg)
print('x_np = ',xnp)
print('SM = ',SM)

plt.figure()
xa = 0.01
ya = 100
pf = 8
plt.plot([x1,x2,x3,x4],[W1,W2,W3,W4])
plt.scatter([x1,x2,x3,x4],[W1,W2,W3,W4])
#plt.title(r'Center of Gravity Envelope Diagram')
plt.xlabel(r'$x_{cg}$, relative to nose (ft)')
plt.ylabel(r'Weight (lbf)')
plt.annotate('Crew + Fuel + Passengers', (x4-xa*13, W4), fontsize=pf,zorder=6)
plt.annotate('Crew + Fuel', (x3-xa*7, W3-ya*2), fontsize=pf,zorder=6)
plt.annotate('Crew', (x2+xa+xa, W2+ya+100), fontsize=pf,zorder=6)
plt.annotate('Empty', (x1-xa-xa, W1+ya+300), fontsize=pf,zorder=6)
plt.savefig('Figures/CG_envelope.pdf') 
plt.close('Figures/CG_envelope.pdf')
plt.show()