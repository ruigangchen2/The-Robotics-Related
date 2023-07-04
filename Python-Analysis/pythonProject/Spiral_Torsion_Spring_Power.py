import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import math


Energy = np.array([19.6, 26.3, 37.4, 38.3, 46.3, 53.5, 55.3, 57.1, 60.8, 64.5])
Acceleration_Displacement = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])

def power(theta):
    distance = 108.6 * 0.001 * theta * math.pi / 180
    return 2.01635971e-07*(distance**3) - 2.35910531e-05*(distance**2) + 3.72788128e-03*(distance) + 2.74967755e-03

def integral(x):
    return integrate.quad(power, x, 30)[0]

for i in range(28,8,-2):
    print(integral(i))
    Energy[14 - int((i/2))] = integral(i)

fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax1.plot(Acceleration_Displacement, Energy, 'r-+')
ax1.set_xlabel('Acceleration Displacement [degree]', fontweight ='bold')
ax1.set_ylabel('Potential Energy Consumed [W]',fontweight ='bold')
plt.xticks(range(0,22,2))
ax1.grid()
plt.title("Relationship between Acceleration Angle and Potential Energy Consumption")
plt.bar(Acceleration_Displacement,Energy)
plt.show()