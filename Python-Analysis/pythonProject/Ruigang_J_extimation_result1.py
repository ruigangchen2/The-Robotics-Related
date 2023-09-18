import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data1 = pd.read_excel("./different_rotation_inertia_curve_compared/heavy.xlsx")
start_point1 = 390
end_point1 = -14
time1 = np.array(data1['Time'].ravel())[start_point1:end_point1]*0.001
angle1 = np.array(data1['Degree'].ravel())[start_point1:end_point1]*np.pi/180
velocity1 = np.array(data1['Velocity'].ravel())[start_point1:end_point1]*np.pi/180

data2 = pd.read_excel("./different_rotation_inertia_curve_compared/light.xlsx")
start_point2 = 393
end_point2 = -13
time2 = np.array(data2['Time'].ravel())[start_point2:end_point2]*0.001
angle2 = np.array(data2['Degree'].ravel())[start_point2:end_point2]*np.pi/180
velocity2 = np.array(data2['Velocity'].ravel())[start_point2:end_point2]*np.pi/180

t1 = time1-time1[0]
t2 = time2-time2[0]

plt.figure(figsize=(7, 5), dpi=100)
ax = plt.subplot(211)
plt.plot(t1, angle1 * 180 / np.pi, 'b', label="Larger Rotation Inertia")
plt.plot(t2, angle2 * 180 / np.pi, 'r', label="Original")


plt.subplot(212, sharex=ax)
plt.plot(t1, velocity1, 'b--', label="Larger Rotation Inertia")
plt.plot(t2, velocity2, 'r--', label="Original")


ax = plt.subplot(211)
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.ylim([-90, 100])
plt.legend()
plt.subplot(212, sharex=ax)
plt.xlabel('Time [s]')
plt.ylabel(r'$\dot{\theta}$ [rad/s]')
plt.legend()
plt.tight_layout()
plt.ylim([-1, 5])
plt.savefig('Sim.pdf')
plt.show()
