import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import math


data = pd.read_excel("./20230628/robotic_arm1.xlsx")

time = np.array(data['Time'].ravel())
time = np.around(time, 2)
degree = np.array(data['Degree'].ravel())
degree = np.around(degree, 2)
velocity = np.array(data['Velocity'].ravel()) * math.pi / 180
velocity = np.around(velocity, 2)
Electromagnet_1_Clutch = np.array(data['Electromagnet_Clutch_1'].ravel())
Electromagnet_1_Clutch = np.around(Electromagnet_1_Clutch, 2)
Electromagnet_2_Clutch = np.array(data['Electromagnet_Clutch_2'].ravel())
Electromagnet_2_Clutch = np.around(Electromagnet_2_Clutch, 2)
Electromagnet_3_Clutch = np.array(data['Electromagnet_Clutch_3'].ravel())
Electromagnet_3_Clutch = np.around(Electromagnet_3_Clutch, 2)
Electromagnet_4_Clutch = np.array(data['Electromagnet_Clutch_4'].ravel())
Electromagnet_4_Clutch = np.around(Electromagnet_4_Clutch, 2)


startline = 7000
endline = None

time = time[startline:endline] - time[startline]
time = time * 0.001
degree = degree[startline:endline]
velocity = velocity[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]


'''
Filtered Angular Displacement [degree] & Derivated Velocity [Python]
'''
data_number = len(degree)
b, a = signal.butter(8, 0.02, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filtered_degree = signal.filtfilt(b, a, degree)  # data为要过滤的信号
for i in range(data_number-1):
    velocity[i] = (filtered_degree[i+1] - filtered_degree[i]) / (time[i+1]-time[i])

fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax2 = ax1.twinx()
ax1.plot(time, filtered_degree, 'k-', label='Angular Displacement [degree]')
ax2.plot(time, velocity, 'r-', label='Angular Velocity [degree/s]')
ax1.set_xlabel('Time [s]', fontweight='bold')
ax1.set_ylabel('Angular Displacement [degree]', fontweight='bold')
ax2.set_ylabel('Angular Velocity [degree/s]', fontweight='bold')
ax1.grid()
fig.legend()
ax1.set_ylim([-100, 100])
ax2.set_ylim([-500, 500])
fig.savefig('./PDF-File/Angular Displacement & Velocity.pdf')

'''
Angular Displacement [rad] & Filtered Velocity  
'''
# b, a = signal.butter(8, 0.05, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, velocity)  # data为要过滤的信号
#
# startline_filter = 1
# endline_filter = None
# time = time[startline_filter:endline_filter] - time[startline_filter]
# degree = degree[startline_filter:endline_filter]
# filtedData = filtedData[startline_filter:endline_filter]
#
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, degree, 'k-', label='Angular Displacement [rad]')
# ax2.plot(time, filtedData, 'r-', label='Filtered Angular Velocity [rad/s]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Angular Displacement [rad]', fontweight='bold')
# ax2.set_ylabel('Filtered Angular Velocity [rad/s]', fontweight='bold')
# ax1.grid()
# fig.legend()
# # ax1.set_ylim([-1, 1])
# # ax2.set_ylim([-10, 10])
# fig.savefig('The Filtered.pdf')

'''
Angular Displacement [degree] & Filtered Velocity 
'''
# b, a = signal.butter(8, 0.05, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, velocity)  # data为要过滤的信号
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, degree, 'k-+', label='Angular Displacement [degree]')
# ax2.plot(time, filtedData, 'r-+', label='Filtered Angular Velocity [rad/s]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Angular Displacement [degree]', fontweight='bold')
# ax2.set_ylabel('Filtered Angular Velocity [rad/s]', fontweight='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-100, 100])
# ax2.set_ylim([-10, 10])
# fig.savefig("./PDF-File/The Filtered.pdf")


'''
Angular Displacement & Velocity
'''
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, degree, 'k-+', label='Angular Displacement [degree]')
# ax2.plot(time, velocity,'r-+', label='Angular Velocity [degree/s]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Displacement [degree]',fontweight ='bold')
# ax2.set_ylabel('Angular Velocity [degree/s]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-100, 100])
# ax2.set_ylim([-500, 500])
# fig.savefig('./PDF-File/Angular Displacement & Velocity.pdf')

'''
Filter
'''
# b, a = scipy.signal.butter(8, 0.025, 'lowpass')   #配置滤波器 8 表示滤波器的阶数
# filtedData = scipy.signal.filtfilt(b, a, velocity)  #data为要过滤的信号
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, velocity, 'k-', label='Angular Velocity [degree/s]')
# ax2.plot(time, filtedData, 'r-', label='Filtered Angular Velocity [degree/s]')
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
# ax1.plot(time, degree, 'k-', label='Angular Displacement [degree]')
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
# ax1.plot(time, velocity, 'k-', label='Angular Velocity [degree/s]')
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
# ax1.plot(time, velocity, 'b-', label='Angular Velocity [degree/s]')
# ax2.plot(time, velocity_smooth,'r-', label='Fitting Angular Velocity [degree/s]')
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
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, Electromagnet_1_Clutch, 'b-', label='Electromagnet_1_Clutch State [On/Off]')
# ax2.plot(time, Electromagnet_2_Clutch, 'r-', label='Electromagnet_2_Clutch State [On/Off]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Electromagnet_1_Clutch State [On/Off]', fontweight='bold')
# ax2.set_ylabel('Electromagnet_2_Clutch State [On/Off]', fontweight='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-2, 2])
# ax2.set_ylim([-2, 2])
# fig.savefig('./PDF-File/The Electromagnet_1 & Electromagnet_2 State.pdf')
#
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, Electromagnet_3_Clutch, 'b-', label='Electromagnet_3_Clutch State [On/Off]')
# ax2.plot(time, Electromagnet_4_Clutch, 'r-', label='Electromagnet_4_Clutch State [On/Off]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Electromagnet_3_Clutch State [On/Off]', fontweight='bold')
# ax2.set_ylabel('Electromagnet_4_Clutch State [On/Off]', fontweight='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-2, 2])
# ax2.set_ylim([-2, 2])
# fig.savefig('./PDF-File/The Electromagnet_3 & Electromagnet_4 State.pdf')

plt.show()
