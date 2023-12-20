import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

# start to rotate from 30 degrees, clutch again at 10 degrees, the robotic arm stops at -64.5 degrees
# start to rotate from 30 degrees, clutch again at 12 degrees, the robotic arm stops at -56.6 degrees
# start to rotate from 30 degrees, clutch again at 14 degrees, the robotic arm stops at -57.1 degrees
# start to rotate from 30 degrees, clutch again at 16 degrees, the robotic arm stops at -47.2 degrees
# start to rotate from 30 degrees, clutch again at 18 degrees, the robotic arm stops at -53.5 degrees
# start to rotate from 30 degrees, clutch again at 20 degrees, the robotic arm stops at -46.3 degrees
# start to rotate from 30 degrees, clutch again at 22 degrees, the robotic arm stops at -38.3 degrees
# start to rotate from 30 degrees, clutch again at 24 degrees, the robotic arm stops at -37.4 degrees
# start to rotate from 30 degrees, clutch again at 26 degrees, the robotic arm stops at -26.3 degrees
# start to rotate from 30 degrees, clutch again at 28 degrees, the robotic arm stops at -19.6 degrees

Angular_Displacement = np.array([19.6, 26.3, 37.4, 38.3, 46.3, 53.5, 55.3, 57.1, 60.8, 64.5]) * math.pi/180 + math.pi/6
Acceleration_Displacement = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20]) * math.pi/180

order = 2
z = np.polyfit(Acceleration_Displacement, Angular_Displacement, order)
p = np.poly1d(z)
degree_fit = p(Acceleration_Displacement)
print(z)

fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax1.plot(Acceleration_Displacement, Angular_Displacement, 'k-+', label='original curve')
plt.plot(Acceleration_Displacement, degree_fit, 'r-+', label='fitting curve')
ax1.set_xlabel('Acceleration Displacement [rad]', fontweight ='bold')
ax1.set_ylabel('Angular Displacement [rad]',fontweight ='bold')
# latex = r'$Y(t) = (%.3f) X^{3} + (%.3f) X^{2} + (%.3f) X + (%.3f)$' % (z[0],z[1],z[2],z[3])
latex = r'$Y(\theta) = (%.3f) \theta^{2} + (%.3f) \theta + (%.3f)$' % (z[0],z[1],z[2])
plt.title(latex, size = 'large')

plt.legend()
ax1.grid()
fig.savefig('The degree-degree.pdf')

plt.show()