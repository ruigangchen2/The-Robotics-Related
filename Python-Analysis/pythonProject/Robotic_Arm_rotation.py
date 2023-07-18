import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import math


data = pd.read_excel("./20230713_clutch/only_lower_electromagnet_clutch.xlsx")

time = np.array(data['Time'].ravel())
time = np.around(time, 2)
angle = np.array(data['Degree'].ravel())
angle = np.around(angle, 2)
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


startline = 510
endline = -1

time = time[startline:endline] - time[startline]
time = time * 0.001
angle = angle[startline:endline]
velocity = velocity[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]
# print(angle)


'''
Get the friction
'''
fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax1.plot(time, angle, 'k--', label='Angular Displacement [angle]')


first_maximum_ranage = angle[900:1000]
first_maximum_time = 900 + np.argmax(first_maximum_ranage)
second_maximum_ranage = angle[2000:3000]
second_maximum_time = 2000 + np.argmax(second_maximum_ranage)
third_maximum_ranage = angle[3600:4000]
third_maximum_time = 3600 + np.argmax(third_maximum_ranage)
fourth_maximum_ranage = angle[4000:5500]
fourth_maximum_time = 4000 + np.argmax(fourth_maximum_ranage)
fifth_maximum_ranage = angle[5000:5500]
fifth_maximum_time = 5000 + np.argmax(fifth_maximum_ranage)
sisth_maximum_ranage = angle[5800:6000]
sisth_maximum_time = 5800 + np.argmax(sisth_maximum_ranage)


plt.annotate(r'$\angle %.2f^o$' % np.max(first_maximum_ranage), xy=(time[first_maximum_time], np.max(first_maximum_ranage)), xytext=(+20, -20),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.max(second_maximum_ranage), xy=(time[second_maximum_time], np.max(second_maximum_ranage)), xytext=(+20, -10),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.max(third_maximum_ranage), xy=(time[third_maximum_time], np.max(third_maximum_ranage)), xytext=(+20, -10),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.max(fourth_maximum_ranage), xy=(time[fourth_maximum_time], np.max(fourth_maximum_ranage)), xytext=(+20, -10),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.max(fifth_maximum_ranage), xy=(time[fifth_maximum_time], np.max(fifth_maximum_ranage)), xytext=(+20, -10),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.max(sisth_maximum_ranage), xy=(time[sisth_maximum_time], np.max(sisth_maximum_ranage)), xytext=(+20, -10),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))

ax1.set_xlabel('Time [s]', fontweight='bold')
ax1.grid()
fig.legend()
ax1.set_ylim([-100, 100])
fig.savefig("./PDF-File/The Filtered.pdf")


'''
Angular Displacement [angle] & Filtered Velocity [rad/s] & curve fit
'''

# b, a = signal.butter(8, 0.1, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
# data_filter = signal.filtfilt(b, a, velocity) # data为要过滤的信号
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
#
# order = 30
# z = np.polyfit(time, data_filter, order)
# p = np.poly1d(z)
# data_fit = p(time)
# print(z)
#
# ax2 = ax1.twinx()
# ax1.plot(time, angle, 'k--', label='Angular Displacement [angle]')
# ax2.plot(time, velocity, 'g--', label='Original Angular Velocity [rad/s]')
# ax2.plot(time, data_filter, 'r--', label='Filtered Angular Velocity [rad/s]')
# ax2.plot(time, data_fit, 'b--', label='Fitted Angular Velocity [rad/s]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Angular Displacement [angle]', fontweight='bold')
# ax2.set_ylabel('Filtered Angular Velocity [rad/s]', fontweight='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-100, 100])
# ax2.set_ylim([-10, 10])
# fig.savefig("./PDF-File/The Filtered.pdf")

'''
Filtered Angular Displacement [angle] & Derivated Velocity [Python]
'''
# data_number = len(angle)
# b, a = signal.butter(8, 0.02, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
# filtered_degree = signal.filtfilt(b, a, angle)  # data为要过滤的信号
# for i in range(data_number-1):
#     velocity[i] = (filtered_degree[i+1] - filtered_degree[i]) / (time[i+1]-time[i])
#
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, filtered_degree, 'k-', label='Angular Displacement [angle]')
# ax2.plot(time, velocity, 'r-', label='Angular Velocity [angle/s]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Angular Displacement [angle]', fontweight='bold')
# ax2.set_ylabel('Angular Velocity [angle/s]', fontweight='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-100, 100])
# ax2.set_ylim([-500, 500])
# fig.savefig('./PDF-File/Angular Displacement & Velocity.pdf')

'''
Angular Displacement [rad] & Filtered Velocity  
'''
# b, a = signal.butter(8, 0.08, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, velocity)  # data为要过滤的信号
#
# startline_filter = 1
# endline_filter = None
# time = time[startline_filter:endline_filter] - time[startline_filter]
# angle = angle[startline_filter:endline_filter]
# filtedData = filtedData[startline_filter:endline_filter]
#
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, angle, 'k-+', label='Angular Displacement [rad]')
# ax2.plot(time, filtedData, 'r-+', label='Filtered Angular Velocity [rad/s]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Angular Displacement [rad]', fontweight='bold')
# ax2.set_ylabel('Filtered Angular Velocity [rad/s]', fontweight='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-100, 100])
# ax2.set_ylim([-10, 10])
# fig.savefig("./PDF-File/The Filtered.pdf")

'''
Angular Displacement [angle] & Filtered Velocity 
'''
# b, a = signal.butter(8, 0.05, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, velocity)  # data为要过滤的信号
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, angle, 'k-+', label='Angular Displacement [angle]')
# ax2.plot(time, filtedData, 'r-+', label='Filtered Angular Velocity [rad/s]')
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Angular Displacement [angle]', fontweight='bold')
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
# ax1.plot(time, angle, 'k--', label='Angular Displacement [angle]')
# ax2.plot(time, velocity,'r--', label='Angular Velocity [angle/s]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Displacement [angle]',fontweight ='bold')
# ax2.set_ylabel('Angular Velocity [angle/s]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-150, 150])
# ax2.set_ylim([-10, 10])
# fig.savefig('./PDF-File/Angular Displacement & Velocity.pdf')

'''
Filter
'''
# b, a = scipy.signal.butter(8, 0.025, 'lowpass')   #配置滤波器 8 表示滤波器的阶数
# filtedData = scipy.signal.filtfilt(b, a, velocity)  #data为要过滤的信号
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# ax1.plot(time, velocity, 'k-', label='Angular Velocity [angle/s]')
# ax2.plot(time, filtedData, 'r-', label='Filtered Angular Velocity [angle/s]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Velocity [angle/s]',fontweight ='bold')
# ax2.set_ylabel('Filtered Angular Velocity [angle/s]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-1200, 1200])
# ax2.set_ylim([-1200, 1200])
# fig.savefig('./PDF-File/The Filtered Angular Velocity.pdf')


'''
Angular Displacement
'''
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax1.plot(time, angle * np.pi / 180, 'k-', label=r'$\theta$ [$^\circ$]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel(r'$\theta$ [$^\circ$]',fontweight ='bold')
# ax1.grid()
# # fig.legend()
# ax1.set_ylim([-5, 5])
# fig.savefig("./PDF-File/The Angular Displacement.pdf")

'''
Angular Velocity
'''
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax1.plot(time, velocity, 'k-', label='Angular Velocity [angle/s]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Velocity [angle/s]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-1200, 1200])
# fig.savefig("./PDF-File/The Angular Velocity.pdf")

'''
Fitting Angular Velocity 
'''
# fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
# ax2 = ax1.twinx()
# velocity_smooth = scipy.signal.savgol_filter(velocity,20,4)
# ax1.plot(time, velocity, 'b-', label='Angular Velocity [angle/s]')
# ax2.plot(time, velocity_smooth,'r-', label='Fitting Angular Velocity [angle/s]')
# ax1.set_xlabel('Time [s]', fontweight ='bold')
# ax1.set_ylabel('Angular Velocity [angle/s]',fontweight ='bold')
# ax2.set_ylabel('Fitting Angular Velocity [angle/s]',fontweight ='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-300, 300])
# ax2.set_ylim([-300, 300])
# fig.savefig('./PDF-File/The Angular Velocity & Fitting Angular Velocity.pdf')

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
