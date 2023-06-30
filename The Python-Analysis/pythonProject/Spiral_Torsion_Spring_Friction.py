import numpy as np
import matplotlib.pyplot as plt
import math


Angular_Displacement = np.array([19.6, 26.3, 37.4, 38.3, 46.3, 53.5, 55.3, 57.1, 60.8, 64.5])
Acceleration_Displacement = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
Energy = np.array([0.0 for i in range(10)])
Friction = np.array([0.0 for i in range(10)])

def power(theta):
    k = 108.6 * 0.001 * 0.0263
    return 0.5 * k * ((theta * math.pi / 180)**2)

def calcualte_friction(theta,energy):
    return energy / theta

for i in range(10):
    # print(integral(i))
    Energy[i] = power(30) - power(30 - Acceleration_Displacement[i])
    Friction[i] = calcualte_friction((Angular_Displacement[i] + 30) * math.pi / 180,Energy[i])


fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax1.plot(Acceleration_Displacement, Energy, 'r-+')
ax1.set_xlabel('Acceleration Displacement [degree]', fontweight ='bold')
ax1.set_ylabel('Potential Energy Consumed [ J ]',fontweight ='bold')
ax1.grid()
plt.xticks(range(0,22,2))
plt.title("Relationship between Acceleration Angle and Potential Energy Consumption")
plt.bar(Acceleration_Displacement,Energy)

fig, ax2 = plt.subplots(figsize=(8, 4), dpi=200)
ax2.plot(Acceleration_Displacement, Friction, 'r-+')
ax2.set_xlabel('Acceleration Displacement [degree]', fontweight ='bold')
ax2.set_ylabel('Friction Moment [ N*m ]',fontweight ='bold')
ax2.grid()
plt.xticks(range(0,22,2))
plt.title("Relationship between Acceleration Displacement and Friction Moment")
plt.bar(Acceleration_Displacement,Friction)

plt.show()