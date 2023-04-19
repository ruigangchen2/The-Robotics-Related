import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# 按列标题读取每列数据
data = pd.read_csv("robotic_arm.csv")

time = np.array(data['Time'].ravel())
time = np.around(time,2)
degree = np.array(data['Degree'].ravel())
degree = np.around(degree,2)
velocity = np.array(data['Velocity'].ravel())
velocity = np.around(velocity,2)
Electromagnet_1_Clutch = np.array(data['Electromagnet_1_Clutch'].ravel())
Electromagnet_1_Clutch = np.around(Electromagnet_1_Clutch,2)
Electromagnet_2_Clutch = np.array(data['Electromagnet_2_Clutch'].ravel())
Electromagnet_2_Clutch = np.around(Electromagnet_2_Clutch,2)
Electromagnet_3_Clutch = np.array(data['Electromagnet_3_Clutch'].ravel())
Electromagnet_3_Clutch = np.around(Electromagnet_3_Clutch,2)
Electromagnet_4_Clutch = np.array(data['Electromagnet_4_Clutch'].ravel())
Electromagnet_4_Clutch = np.around(Electromagnet_4_Clutch,2)




fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax2 = ax1.twinx()
ax1.plot(time, degree, 'k-*', label='Angular Displacement [degree]')
ax2.plot(time, velocity,'r-*', label='Angular Velocity [degree/s]')
ax1.set_xlabel('Time [ms]', fontweight ='bold')
ax1.set_ylabel('Angular Displacement [degree]',fontweight ='bold')
ax2.set_ylabel('Angular Velocity [degree/s]',fontweight ='bold')
ax1.grid()
fig.legend()
ax1.set_ylim([-180, 180])
ax2.set_ylim([-1200, 1200])
plt.show()

fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax1.plot(time, degree, 'k-*', label='Angular Displacement [degree]')
ax1.set_xlabel('Time [ms]', fontweight ='bold')
ax1.set_ylabel('Angular Displacement [degree]',fontweight ='bold')
ax1.grid()
fig.legend()
ax1.set_ylim([-180, 180])
fig.savefig('The Angular Displacement.pdf')

fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax1.plot(time, velocity, 'k-*', label='Angular Velocity [degree/s]')
ax1.set_xlabel('Time [ms]', fontweight ='bold')
ax1.set_ylabel('Angular Velocity [degree/s]',fontweight ='bold')
ax1.grid()
fig.legend()
ax1.set_ylim([-1200, 1200])
fig.savefig('The Angular Velocity.pdf')


fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax2 = ax1.twinx()
ax1.plot(time, Electromagnet_1_Clutch, 'b-*', label='Electromagnet_1_Clutch State [On/Off]')
ax2.plot(time, Electromagnet_2_Clutch,'r-*', label='Electromagnet_2_Clutch State [On/Off]')
ax1.set_xlabel('Time [ms]', fontweight ='bold')
ax1.set_ylabel('Electromagnet_1_Clutch State [On/Off]',fontweight ='bold')
ax2.set_ylabel('Electromagnet_2_Clutch State [On/Off]',fontweight ='bold')
ax1.grid()
fig.legend()
ax1.set_ylim([-2, 2])
ax2.set_ylim([-2, 2])
fig.savefig('The Electromagnet_1 & Electromagnet_2 State.pdf')

fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax2 = ax1.twinx()
ax1.plot(time, Electromagnet_3_Clutch, 'b-*', label='Electromagnet_3_Clutch State [On/Off]')
ax2.plot(time, Electromagnet_4_Clutch,'r-*', label='Electromagnet_4_Clutch State [On/Off]')
ax1.set_xlabel('Time [ms]', fontweight ='bold')
ax1.set_ylabel('Electromagnet_3_Clutch State [On/Off]',fontweight ='bold')
ax2.set_ylabel('Electromagnet_4_Clutch State [On/Off]',fontweight ='bold')
ax1.grid()
fig.legend()
ax1.set_ylim([-2, 2])
ax2.set_ylim([-2, 2])
fig.savefig('The Electromagnet_3 & Electromagnet_4 State.pdf')



