import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_excel("demo_tracker.xlsx")

time= list(data.iloc[4:, 0] / 100) #convert to second
displacement_mm= list(data.iloc[4:, 7])
displacement_m= list(data.iloc[4:, 7] / 1000)


velocity = [0 for i in range(np.size(time))]
acceleration = [0 for i in range(np.size(time))]

for i in range(np.size(time)-1):
    velocity[i] = (displacement_m[i+1] - displacement_m[i]) / (time[i+1] - time[i])
for i in range(np.size(velocity)-1):
    acceleration[i] = (velocity[i+1] - velocity[i]) / (time[i+1] - time[i])


plt.figure(figsize=(20, 8), dpi=100)
plt.subplot(311)
plt.plot(time, displacement_mm, 'b-+', label='Distance')
plt.ylabel('Displacement [mm]')
plt.grid()
plt.legend()
plt.ylim([0, 1200])

plt.subplot(312)
plt.plot(time, velocity, 'r-', label='Velocity')
plt.grid()
plt.legend()
plt.ylabel('Displacement [m/s]')

plt.subplot(313)
plt.plot(time, acceleration, 'g-', label='Acceleration')
plt.xlabel('Time [s]')
plt.ylabel('Displacement [m/s^2]')
plt.grid()
plt.legend()
plt.savefig('Information.pdf')
plt.show()
