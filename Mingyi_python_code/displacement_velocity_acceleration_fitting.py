import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy

data = pd.read_csv("robotic_arm.csv")

time = np.array(data['Time'].ravel())
time = np.around(time, 2)/1000
dispment = np.array(data['Degree'].ravel())
dispment = np.around(dispment, 2)
velocity = np.array(data['Velocity'].ravel())
velocity = np.around(velocity, 2)
startline = 1195
endline = 1770
velocity_from_disp = np.divide(dispment[startline:endline] - dispment[startline-1:endline-1],
                               (time[startline:endline] - time[startline-1:endline-1]))
time = time[startline:endline] - time[startline]
dispment = dispment[startline:endline]
velocity = velocity[startline:endline]


plt.figure(figsize=(11, 4), dpi=100)
plt.subplot(121)
plt.plot(time, dispment, 'k-*', label='Angular Displacement [degree]')
plt.xlabel('Time [s]')
plt.ylabel('Angular Displacement')
plt.grid()
plt.legend()
plt.ylim([-180, 180])
plt.subplot(122)
velocity_smooth = scipy.signal.savgol_filter(velocity, 20, 4)
plt.plot(time, velocity, 'b-*', label='Angular Velocity')
plt.plot(time, velocity_smooth, 'r-*', label='Fitting Angular Velocity')
plt.plot(time, velocity_from_disp, 'k-+', label='Calculated Angular Velocity')
plt.xlabel('Time [s]')
plt.ylabel('Angular Velocity [degree/s]')
plt.ylabel('Fitting Angular Velocity [degree/s]')
plt.grid()
plt.legend()
plt.ylim([-300, 300])
plt.ylim([-300, 300])
plt.savefig('The Angular Velocity & Fitting Angular Velocity.pdf')
plt.show()
