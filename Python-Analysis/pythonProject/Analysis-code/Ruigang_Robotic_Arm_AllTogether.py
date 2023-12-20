import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("./Data/20230802/1_140.xlsx")
one = 390

time = np.array(data['Time'].ravel())[one:-22]*0.001-np.array(data['Time'].ravel())[one]*0.001
angle = np.array(data['Degree'].ravel())[one:-22]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-22]*np.pi/180
plt.figure(figsize=(7, 5), dpi=100)
ax = plt.subplot(211)

# time = time + 0.77

plt.plot(time, angle * 180 / np.pi, 'b', label="Trial 1")
plt.subplot(212, sharex=ax)
plt.plot(time, velocity, 'b', label="Trial 1")

data = pd.read_excel("./Data/20230802/2_140.xlsx")
one = 454
time = np.array(data['Time'].ravel())[one:-10]*0.001-np.array(data['Time'].ravel())[one]*0.001
angle = np.array(data['Degree'].ravel())[one:-10]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-10]*np.pi/180

# time = time - 0.5

ax = plt.subplot(211)
plt.plot(time, angle * 180 / np.pi, 'r--', label="Trial 2")
plt.subplot(212, sharex=ax)
plt.plot(time, velocity, 'r--', label="Trial 2")

data = pd.read_excel("./Data/20230802/3_140.xlsx")
one = 391
time = np.array(data['Time'].ravel())[one:-10]*0.001-np.array(data['Time'].ravel())[one]*0.001
angle = np.array(data['Degree'].ravel())[one:-10]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-10]*np.pi/180

# time = time - 0.05

ax = plt.subplot(211)
plt.plot(time, angle * 180 / np.pi, 'k:', label="Trial 3")
plt.subplot(212, sharex=ax)
plt.plot(time, velocity, 'k:', label="Trial 3")

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
