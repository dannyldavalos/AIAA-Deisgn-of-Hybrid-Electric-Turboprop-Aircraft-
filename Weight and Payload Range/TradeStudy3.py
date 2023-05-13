## Trade Study


import numpy as np

from matplotlib import pyplot as plt

# Variable to be changed
N = 5
cruisehybr = np.linspace(0,1.0,N)                # non-dimensional
clmbhybr = np.linspace(0,1.0,N)                  # non-dimensional



# Input data (hardcode from weight file)
# intial ratios tha work hybridizations = [0.2,0.2,0.05,0.02,0.75,1,1]

#climb alterations    [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08] wtih curise at 0.01, 0.02, 0.03
#totclmb =np.array([])  
#first 3 row are climb, second 3 are fuelweightcruise
'''
fuelWeightclimb = np.array([[5362, 5322, 5317, 5312, 5307, 5303, 5298, 5293],
                            [5315, 5311, 5306, 5301, 5296, 5292, 5287, 5282],
                            [5304, 5300, 5295, 5290, 5285, 5281, 5276, 5271],
                            [5312, 5301, 5290, 5279, 5268, 5257, 5247, 5236],
                            [5307, 5296, 5285, 5275, 5264, 5253, 5242, 5231],
                            [5303, 5292, 5281, 5270, 5259, 5248, 5237, 5226]])  

#frist 3 rows are battery climb, last 3 rowas are battery cruise
batteryWeightclimb = np.array([[6358, 6477, 6596, 6716, 6836, 6958, 7081, 7204],
                               [6602, 6721, 6841, 6963, 7085, 7208, 7331, 7456],
                               [6846, 6967, 7089, 7211, 7334, 7459, 7584, 7710],
                               [6716, 6963, 7211, 7461, 7713, 7967, 8222, 8479],
                               [6836, 7085, 7334, 7586, 7839, 8094, 8351, 8609],
                               [6958, 7208, 7459, 7711, 7966, 8222, 8480, 8740]])  '''


                    #climb   0.02, 0.03, 0.04, 0.05, 0.06, 0.07         cruise
'''fuelWeightclimb = np.array([[5322, 5317, 5312, 5307, 5303, 5298],       #0.01
                            [5311, 5306, 5301, 5296, 5292, 5287],       #0.02
                            [5300, 5295, 5290, 5285, 5281, 5276],       #0.03
                            [5278, 5273, 5268, 5264, 5259, 5254],       #0.05
                            [5256, 5251, 5247, 5242, 5237, 5232],        #0.07
                            [5224, 5219, 5214, 5209, 5205, 5200]])       #0.10

                   #cruise                                             #climb
                            [5301, 5290, 5279, 5268, 5257, 5247],       #0.04
                            [5296, 5285, 5275, 5264, 5253, 5242],       #0.05
                            [5292, 5281, 5270, 5259, 5248, 5237]])      #0.06

Tw =   np.array([[62776, 62910, 63045, 63180, 63317, 63455],
                          [63049, 63184, 63320, 63458, 63596, 63735],
                          [63324, 63461, 63598, 63737, 63786, 64017],
                          [63601, 63739, 63878, 64018, 64159, 64301],
                          [63879, 64019, 64159, 64301, 64443, 64587],
                          [64160, 64301, 64443, 64586, 64730, 64875]])
                     #climb 0.02, 0.03, 0.04, 0.05, 0.06, 0.07        loiter
fuel =        np.array([[],
                          [],
                          [],
                          [],
                          [],
                          []])


#frist 3 rows are battery climb, last 3 rowas are battery cruise
                     #climb     0.02, 0.03, 0.04, 0.05, 0.06, 0.07         cruise
batteryWeightclimb = np.array([[6477, 6596, 6716, 6836, 6958, 7081],        #0.01
                               [6721, 6841, 6963, 7085, 7208, 7331],        #0.02
                               [6967, 7089, 7211, 7334, 7459, 7584],        #0.03
                               [7215, 7338, 7461, 7586, 7711, 7838],        #
                               [7464, 7588, 7713, 7839, 7966, 8094],        #0.05
                               [7715, 7840, 7967, 8094, 8222, 8351]])

[7967, 8094, 8222, 8351, 8480, 8611],        #0.07
                               [8735, 8866, 8998, 9131, 9265, 9400]])       #0.10

                    #cruise                                                climb
                               [6963, 7211, 7461, 7713, 7967, 8222],        #0.04
                               [7085, 7334, 7586, 7839, 8094, 8351],        #0.05
                               [7208, 7459, 7711, 7966, 8222, 8480]])       #0.06

'''


            #climb         0.01 0.02, 0.03, 0.04, 0.05, 0.06   loiter
fuel =        np.array([[5428, 5417, 5406, 5395, 5384, 5373],     #0.35
                          [5398, 5387, 5376, 5365, 5354, 5343],     #0.45
                          [5368, 5357, 5346, 5335, 5324, 5313],   #0.55
                          [5338, 5327, 5316, 5305, 5294, 5283],   #0.65
                          [5307, 5296, 5285, 5275, 5264, 5253],   #0.75
                          [5277, 5266, 5255, 5244, 5233, 5222]])  #0.85
            #climb       0.01 0.02, 0.03, 0.04, 0.05, 0.06   loiter
battery =         np.array([[4466, 4696, 4927, 5159, 5393, 5628],
                          [5040, 5274, 5509, 5746, 5984, 6224],
                          [5626, 5864, 6104, 6346, 6589, 6834],
                          [6225, 6468, 6713, 6959, 7207, 7457],
                          [6836, 7085, 7334, 7586, 7839, 8094],
                          [7462, 7715, 7970, 8227, 8485, 8746]])


#crusie alterations with climb at 0.04, 0.05, 0.06
#totcruise = np.array([1.0,2,3,4,5])                        
               
#fuelWeightcruise = np.array([[5312, 5301, 5290, 5279, 5268, 5257, 5247, 5236],
                            # [5307, 5296, 5285, 5275, 5264, 5253, 5242, 5231],
                            # [5303, 5292, 5281, 5270, 5259, 5248, 5237, 5226]])                                                    # [lbf]
                       
#batteryWeightcruise = np.array([[6716, 6963, 7211, 7461, 7713, 7967, 8222, 8479],
                              #  [6836, 7085, 7334, 7586, 7839, 8094, 8351, 8609],
                               # [6958, 7208, 7459, 7711, 7966, 8222, 8480, 8740]])                                                # [lbf]




#crusie alterations

plt.figure(figsize=(5,5))
plt.plot(battery[:,0],fuel[:,0], color = 'r', label='Constant Cruise \n Hybrid. Ratio')
plt.plot(battery[0,:],fuel[0,:], color = 'b', label='Constant Loiter \n Hybrid. Ratio')
plt.plot(battery[:,5],fuel[:,5], color = 'r')
plt.plot(battery[5,:],fuel[5,:], color = 'b')
plt.scatter(4466,5428 , color = 'k')
plt.scatter( 5628, 5373, color = 'k')
plt.scatter( 7462, 5277, color = 'k')
plt.scatter( 8746, 5222, color = 'k')

# for i in range(0,len(battery)):
#     plt.plot(battery[:,0],fuel[:,0], color = 'r', label='Constant Cruise Hybrid. Ratio')
#     plt.plot(battery[0,:],fuel[0,:], color = 'b', label='Constant Loiter Hybrid. Ratio')
#     plt.plot(battery[:,5],fuel[:,5], color = 'r')
#     plt.plot(battery[5,:],fuel[5,:], color = 'b')
    # plt.plot(battery[:,i],fuel[:,i], color = 'r', label='fuel')
    # plt.plot(battery[i,:],fuel[i,:], color = 'b', label='battery')
    # plt.plot(batteryWeightclimb[:,i],Tw[:,i], color = 'r', label='fuel')
    # plt.plot(batteryWeightclimb[i,:],Tw[i,:], color = 'b', label='battery')

# for i in range(0,4):
#      plt.plot(batteryWeightclimb[i,:],fuelWeightclimb[i,:], color = 'b', label='battery')
#plt.xlim([6490,7250])
#plt.ylim([5280,5325])
# f, (ax, ax2) = plt.subplots(1, 2, sharey=True, facecolor='w')

# ax.set_xlim(6500,7250 ) 
# ax2.set_xlim(8250, 9000)  

# ax.spines['right'].set_visible(False)
# ax2.spines['left'].set_visible(False)
# ax.yaxis.tick_left()
# ax.tick_params(labelright=False)  # don't put tick labels at the top
# ax2.yaxis.tick_right()

# plt.plot(batteryWeightclimb[:,0],fuelWeightclimb[:,0], color = 'k', label='fuel')
# plt.plot(batteryWeightclimb[:,5],fuelWeightclimb[:,5], color = 'k', label='fuel')
# plt.xlabel('Battery Weight [lbf]')
# plt.ylabel('Fuel Weight [lbf]')
# plt.xlim([6490,7250])
# plt.ylim([5280,5325])
# plt.plot(batteryWeightclimb[0,:],fuelWeightclimb[0,:], color = 'k', label='battery')
# plt.plot(batteryWeightclimb[5,:],fuelWeightclimb[5,:], color = 'k', label='battery')

plt.text(5166, 5400+10,'Cruise = 0.01,\n Loiter = 0.35')
plt.text(6028,5390-10,'Cruise = 0.06,\n Loiter = 0.35')
plt.text(5962, 5250+20,'Cruise = 0.01,\n Loiter = 0.85')
plt.text(6846,5222,'Cruise = 0.06,\n Loiter = 0.85')
plt.xlabel('Battery Weight [lbf]')
plt.ylabel('Fuel Weight [lbf]')
plt.legend(loc='lower left')
plt.savefig('Hybridization.pdf') 
plt.close('Hybridization.pdf')


plt.show()


