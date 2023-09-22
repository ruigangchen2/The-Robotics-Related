import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data1 = pd.read_csv("./different_inertia_trails/trail1.csv")
start_point1 = 391
end_point1 = 1114
time1 = np.array(data1['Time'].ravel())[start_point1:end_point1]*0.001
angle1 = np.array(data1['Degree'].ravel())[start_point1:end_point1]*np.pi/180
velocity1 = np.array(data1['Velocity'].ravel())[start_point1:end_point1]*np.pi/180

data2 = pd.read_csv("./different_inertia_trails/trail2.csv")
start_point2 = 391
end_point2 = 1120
time2 = np.array(data2['Time'].ravel())[start_point2:end_point2]*0.001
angle2 = np.array(data2['Degree'].ravel())[start_point2:end_point2]*np.pi/180
velocity2 = np.array(data2['Velocity'].ravel())[start_point2:end_point2]*np.pi/180

data3 = pd.read_csv("./different_inertia_trails/trail3.csv")
start_point3 =    390
end_point3 = 1120
time3 = np.array(data3['Time'].ravel())[start_point3:end_point3]*0.001
angle3 = np.array(data3['Degree'].ravel())[start_point3:end_point3]*np.pi/180
velocity3 = np.array(data3['Velocity'].ravel())[start_point3:end_point3]*np.pi/180


t1 = time1-time1[0]
t2 = time2-time2[0]
t3 = time3-time3[0]

print(angle1[0] * 180 / np.pi)
print(angle2[0] * 180 / np.pi)
print(angle3[0] * 180 / np.pi)

plt.figure(figsize=(5, 4))
ax = plt.subplot(211)
plt.plot(t1, angle1 * 180 / np.pi, 'b', label="Trial 1")
plt.plot(t2, angle2 * 180 / np.pi, 'r--', label="Trial 2")
plt.plot(t3, angle3 * 180 / np.pi, 'k:', label="Trial 3")

plt.subplot(212, sharex=ax)
plt.plot(t1, velocity1, 'b', label="Trial 1")
plt.plot(t2, velocity2, 'r--', label="Trial 2")
plt.plot(t3, velocity3, 'k:', label="Trial 3")


ax = plt.subplot(211)
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.ylim([-90, 100])
plt.legend()

plt.subplot(212, sharex=ax)
plt.xlabel('Time [s]')
plt.ylabel(r'$\dot{\theta}$ [rad/s]')
plt.legend()
plt.tight_layout()
plt.ylim([-1, 4])
plt.savefig('Sim.pdf')
plt.show()
