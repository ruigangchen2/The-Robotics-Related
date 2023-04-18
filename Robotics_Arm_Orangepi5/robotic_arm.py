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
# upper_clutch = np.array(data['Upper_Clutch'].ravel())
# upper_clutch = np.around(upper_clutch,2)
# nether_clutch = np.array(data['Nether_Clutch'].ravel())
# nether_clutch = np.around(nether_clutch,2)




fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=100)
ax2 = ax1.twinx()

ax1.plot(time, degree, 'k-*', label='Angular Displacement [°]')
ax2.plot(time, velocity,'r-*', label='Angular Velocity [°/s]')

ax1.set_xlabel('Time [ms]', fontweight ='bold')

ax1.set_ylabel('Angular Displacement [°]',fontweight ='bold')
ax2.set_ylabel('Angular Velocity [°/s]',fontweight ='bold')


ax1.grid()
fig.legend()

ax1.set_ylim([-180, 180])
ax2.set_ylim([-1200, 1200])

fig.savefig('The Angular Displacement & Velocity.pdf')
plt.show()


# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=100)
# ax2 = ax1.twinx()

# ax1.plot(time, upper_clutch, 'b-*', label='Upper Electromagnet State [On/Off]')
# ax2.plot(time, nether_clutch,'r-*', label='Upper Electromagnet State [On/Off]')

# ax1.set_xlabel('Time [ms]', fontweight ='bold')

# ax1.set_ylabel('Upper Electromagnet State [On/Off]',fontweight ='bold')
# ax2.set_ylabel('Upper Electromagnet State [On/Off]',fontweight ='bold')

# ax1.grid()
# fig.legend()

# ax1.set_ylim([-2, 2])
# ax2.set_ylim([-2, 2])

# fig.savefig('The Electromagnet State.pdf')




