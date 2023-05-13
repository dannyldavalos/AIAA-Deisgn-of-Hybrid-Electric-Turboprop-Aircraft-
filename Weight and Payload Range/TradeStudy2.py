## Trade Study 2
## Duncan Koelzer

import numpy as np
from matplotlib import pyplot as plt

# Variable to be changed
N = 5
cruiseSpeed = np.linspace(275,350,N)                # [knots]
loiterSpeed = np.linspace(200,250,N)                # [knots]

# Input data (hardcode from weight file)
#            loiterSpeed = 200.0, 212.5, 225.0, 237.5, 250.0                
fuelWeight =    np.array([[6160 , 6223 , 6287 , 6352 , 6418],       # cruise speed = 275
                          [5801 , 5857 , 5914 , 5972 , 6031],       # cruise speed = 293.75
                          [5558 , 5609 , 5661 , 5714 , 5768],       # cruise speed = 312.5
                          [5397 , 5445 , 5493 , 5542 , 5592],       # cruise speed = 331.25
                          [5296 , 5341 , 5386 , 5432 , 5479]        # cruise speed = 350 
                          ])

batteryWeight = np.array([[7243 , 7547 , 7854 , 8166 , 8482],       # cruise speed = 275
                          [7177 , 7479 , 7785 , 8094 , 8407],       # cruise speed = 293.75 
                          [7132 , 7433 , 7737 , 8045 , 8357],       # cruise speed = 312.5
                          [7103 , 7403 , 7706 , 8013 , 8323],       # cruise speed = 331.25
                          [7085 , 7383 , 7686 , 7992 , 8302]        # cruise speed = 350 
                          ])       


plt.figure(figsize=(6,6))
plt.text(batteryWeight[0,4]+20,fuelWeight[0,4]-20,'Cruise Speed: \n{:.2f}kts'.format(cruiseSpeed[0]),fontsize=6)
plt.text(batteryWeight[4,0]+10,fuelWeight[4,0]-75,'Loiter Speed: \n{:.1f}kts'.format(loiterSpeed[0]),fontsize=6)
for i in range(0,len(fuelWeight)):
    plt.plot(batteryWeight[i,:],fuelWeight[i,:],color='k')
    plt.plot(batteryWeight[:,i],fuelWeight[:,i],color='k')

for i in range(1,len(fuelWeight)):
    plt.text(batteryWeight[i,N-1]+20,fuelWeight[i,N-1],'{:.2f}kts'.format(cruiseSpeed[i]),fontsize=6)
    plt.text(batteryWeight[4,i]-40,fuelWeight[4,i]-40,'{:.1f}kts'.format(loiterSpeed[N-(N-i)]),fontsize=6)


# plt.title('Fuel and Battery Weights for 500nmi mission')
plt.xlabel('Battery Weight (lbf)')
plt.ylabel('Fuel Weight (lbf)')
plt.xlim([7000,8750])
plt.ylim([5000,6600])
plt.scatter(batteryWeight[4,0],fuelWeight[4,0],c='r',label='Desired Point')
            #label='Desired Point: \nFuel = {:.0f}\nBattery = {:.0f}'.format(fuelWeight[4,0],batteryWeight[4,0]))
plt.legend(loc='upper left')
plt.hlines(fuelWeight[4,0],0,batteryWeight[4,0],colors='red',linestyles='dashed')
plt.vlines(batteryWeight[4,0],0,fuelWeight[4,0],colors='red',linestyles='dashed')
plt.savefig('CruiseLoiterTrade.pdf') 
plt.show()

