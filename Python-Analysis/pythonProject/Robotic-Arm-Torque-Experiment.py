import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal


data = pd.read_excel("./20230619/robotic_arm4.xlsx")

time = np.array(data['Time'].ravel())
time = np.around(time, 2)
degree = np.array(data['Degree'].ravel()-1.44)
degree = np.around(degree, 2)
velocity = np.array(data['Velocity'].ravel())
velocity = np.around(velocity, 2)
Force = (np.array(data['Weight'].ravel()) + 17.04) * 0.001 * 9.8
Force = np.around(Force, 2)
Electromagnet_1_Clutch = np.array(data['Electromagnet_Clutch_1'].ravel())
Electromagnet_1_Clutch = np.around(Electromagnet_1_Clutch, 2)
Electromagnet_2_Clutch = np.array(data['Electromagnet_Clutch_2'].ravel())
Electromagnet_2_Clutch = np.around(Electromagnet_2_Clutch, 2)
Electromagnet_3_Clutch = np.array(data['Electromagnet_Clutch_3'].ravel())
Electromagnet_3_Clutch = np.around(Electromagnet_3_Clutch, 2)
Electromagnet_4_Clutch = np.array(data['Electromagnet_Clutch_4'].ravel())
Electromagnet_4_Clutch = np.around(Electromagnet_4_Clutch, 2)


startline = 1
endline = None

time = time[startline:endline] - time[startline]
time = time * 0.001
degree = degree[startline:endline]
velocity = velocity[startline:endline]
Force = Force[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]


'''
Force & Filtered Force
'''
# b, a = signal.butter(8, 0.01, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, Weight)  # data为要过滤的信号
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, Weight, 'k--', label='Weight [g]')
# ax2.plot(time, filtedData, 'r--', label='Filtered Weight [g]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Weight [g]', fontweight='bold')
# ax2.set_ylabel('Filtered Weight [g]', fontweight='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-20, 20])
# ax2.set_ylim([-20, 20])
# fig.savefig('The Filtered.pdf')

'''
Angular Displacement & Filtered Force
'''
b, a = signal.butter(8, 0.01, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filtedData = signal.filtfilt(b, a, Force)  # data为要过滤的信号
fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax2 = ax1.twinx()
ax1.plot(time, degree, 'k--', label='Angular Displacement [degree]')
ax2.plot(time, filtedData, 'r--', label='Force [N]')
ax1.set_xlabel('Time [s]', fontweight='bold')
ax1.set_ylabel('Angular Displacement [degree]', fontweight='bold')
ax2.set_ylabel('Force [N]', fontweight='bold')
ax1.grid()
fig.legend()
ax1.set_ylim([-150, 150])
ax2.set_ylim([-0.1, 0.1])
fig.savefig('The Filtered.pdf')

'''
Angular Displacement & Filtered Velocity
'''
# b, a = signal.butter(8, 0.05, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, velocity)  # data为要过滤的信号
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, degree, 'k--', label='Angular Displacement [degree]')
# ax2.plot(time, filtedData, 'r--', label='Filtered Angular Velocity [degree/s]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Angular Displacement [degree]', fontweight='bold')
# ax2.set_ylabel('Filtered Angular Velocity [degree/s]', fontweight='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-150, 150])
# ax2.set_ylim([-400, 400])
# fig.savefig('The Filtered.pdf')


'''
Angular Displacement & Velocity
'''
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, degree, 'k--', label='Angular Displacement [degree]')
# ax2.plot(time, velocity,'r--', label='Angular Velocity [degree/s]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Displacement [degree]',fontweight ='bold')
# ax2.set_ylabel('Angular Velocity [degree/s]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-250, 250])
# ax2.set_ylim([-1200, 1200])
# fig.savefig('Angular Displacement & Velocity.pdf')

'''
Filter
'''
# b, a = scipy.signal.butter(8, 0.025, 'lowpass')   #配置滤波器 8 表示滤波器的阶数
# filtedData = scipy.signal.filtfilt(b, a, velocity)  #data为要过滤的信号
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, velocity, 'k--', label='Angular Velocity [degree/s]')
# ax2.plot(time, filtedData, 'r--', label='Filtered Angular Velocity [degree/s]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Velocity [degree/s]',fontweight ='bold')
# ax2.set_ylabel('Filtered Angular Velocity [degree/s]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-1200, 1200])
# ax2.set_ylim([-1200, 1200])
# fig.savefig('The Filtered Angular Velocity.pdf')


'''
Angular Displacement
'''
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax1.plot(time, degree, 'k--', label='Angular Displacement [degree]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Displacement [degree]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-250, 250])
# fig.savefig('The Angular Displacement.pdf')

'''
Angular Velocity
'''
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax1.plot(time, velocity, 'k--', label='Angular Velocity [degree/s]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Velocity [degree/s]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-1200, 1200])
# fig.savefig('The Angular Velocity.pdf')

'''
Fitting Angular Velocity 
'''
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# velocity_smooth = scipy.signal.savgol_filter(velocity,20,4)
# ax1.plot(time, velocity, 'b-*', label='Angular Velocity [degree/s]')
# ax2.plot(time, velocity_smooth,'r-*', label='Fitting Angular Velocity [degree/s]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Velocity [degree/s]',fontweight ='bold')
# ax2.set_ylabel('Fitting Angular Velocity [degree/s]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-300, 300])
# ax2.set_ylim([-300, 300])
# fig.savefig('The Angular Velocity & Fitting Angular Velocity.pdf')

'''
Electromagnet Clutch State
'''
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, Electromagnet_1_Clutch, 'b-*', label='Electromagnet_1_Clutch State [On/Off]')
# ax2.plot(time, Electromagnet_2_Clutch,'r-*', label='Electromagnet_2_Clutch State [On/Off]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Electromagnet_1_Clutch State [On/Off]',fontweight ='bold')
# ax2.set_ylabel('Electromagnet_2_Clutch State [On/Off]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-2, 2])
# ax2.set_ylim([-2, 2])
# fig.savefig('The Electromagnet_1 & Electromagnet_2 State.pdf')
#
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, Electromagnet_3_Clutch, 'b-*', label='Electromagnet_3_Clutch State [On/Off]')
# ax2.plot(time, Electromagnet_4_Clutch,'r-*', label='Electromagnet_4_Clutch State [On/Off]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Electromagnet_3_Clutch State [On/Off]',fontweight ='bold')
# ax2.set_ylabel('Electromagnet_4_Clutch State [On/Off]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-2, 2])
# ax2.set_ylim([-2, 2])
# fig.savefig('The Electromagnet_3 & Electromagnet_4 State.pdf')

plt.show()
