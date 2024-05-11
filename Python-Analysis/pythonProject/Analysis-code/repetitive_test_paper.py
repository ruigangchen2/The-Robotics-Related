import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

one = 397
two = 393
three = 391
data1 = pd.read_excel("../Data/20230731/1_150.xlsx")
data2 = pd.read_excel("../Data/20230731/2_150.xlsx")
data3 = pd.read_excel("../Data/20230731/3_150.xlsx")
time1 = np.array(data1['Time'].ravel())[one:-11]*0.001-np.array(data1['Time'].ravel())[one]*0.001
time2 = np.array(data2['Time'].ravel())[two:-9]*0.001-np.array(data2['Time'].ravel())[two]*0.001
time3 = np.array(data3['Time'].ravel())[three:-9]*0.001-np.array(data3['Time'].ravel())[three]*0.001
angle1 = np.array(data1['Degree'].ravel())[one:-11]*np.pi/180
angle2 = np.array(data2['Degree'].ravel())[two:-9]*np.pi/180
angle3 = np.array(data3['Degree'].ravel())[three:-9]*np.pi/180
velocity1 = np.array(data1['Velocity'].ravel())[one:-11]*np.pi/180
velocity2 = np.array(data2['Velocity'].ravel())[two:-9]*np.pi/180
velocity3 = np.array(data3['Velocity'].ravel())[three:-9]*np.pi/180


fig = plt.figure(figsize=(4, 3))
ax1 = plt.subplot(211)
ax1.plot(time1, angle1 * 180 / np.pi, 'b', label="Trial 1")
ax1.plot(time2, angle2 * 180 / np.pi, 'r--', label="Trial 2")
ax1.plot(time3, angle3 * 180 / np.pi, 'k:', label="Trial 3")
ax1.legend(fontsize=8)
ax1.set_ylabel(r'$\theta$ [$^\circ$]')
ax1.get_xaxis().set_visible(False)

ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(time1, velocity1, 'b', label="Trial 1")
ax2.plot(time2, velocity2, 'r--', label="Trial 2")
ax2.plot(time3, velocity3, 'k:', label="Trial 3")
ax2.legend(ncol=3, fontsize=8)
ax2.set_ylabel(r'$\dot{\theta}$ [rad/s]')
ax2.set_xlabel('Time [s]')

plt.tight_layout()
plt.savefig('Sim.pdf')
plt.show()
