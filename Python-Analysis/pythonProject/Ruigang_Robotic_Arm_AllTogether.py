import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("./20230731/1_150.xlsx")
one = 396

time = np.array(data['Time'].ravel())[one:-5]*0.001-np.array(data['Time'].ravel())[one]*0.001
angle = np.array(data['Degree'].ravel())[one:-5]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-5]*np.pi/180
plt.figure(figsize=(7, 6), dpi=100)
ax = plt.subplot(211)
plt.plot(time, angle * 180 / np.pi, 'b')
plt.subplot(212, sharex=ax)
plt.plot(time, velocity, 'b')

data = pd.read_excel("./20230731/2_150.xlsx")
one = 392
time = np.array(data['Time'].ravel())[one:-5]*0.001-np.array(data['Time'].ravel())[one]*0.001
angle = np.array(data['Degree'].ravel())[one:-5]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-5]*np.pi/180
ax = plt.subplot(211)
plt.plot(time, angle * 180 / np.pi, 'r')
plt.subplot(212, sharex=ax)
plt.plot(time, velocity, 'r')

data = pd.read_excel("./20230731/3_150.xlsx")
one = 390
time = np.array(data['Time'].ravel())[one:-5]*0.001-np.array(data['Time'].ravel())[one]*0.001
angle = np.array(data['Degree'].ravel())[one:-5]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-5]*np.pi/180
ax = plt.subplot(211)
plt.plot(time, angle * 180 / np.pi, 'c')
plt.subplot(212, sharex=ax)
plt.plot(time, velocity, 'c')

ax = plt.subplot(211)
plt.xlabel('Time [s]')
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.ylim([-110, 100])
plt.legend()
plt.subplot(212, sharex=ax)
plt.xlabel('Time [s]')
plt.ylabel(r'$\dot{\theta}$ [rad/s]')
plt.legend()
plt.tight_layout()
plt.ylim([-2, 7])
plt.savefig('Sim.pdf')
plt.show()
