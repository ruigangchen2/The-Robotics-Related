import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from scipy.integrate import odeint, solve_ivp
import math


data = pd.read_excel("./20230628/robotic_arm1.xlsx")
# data = pd.read_excel("./20230703/data.xlsx")
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


theta_acceleration = 10 * math.pi / 180
theta_goal = 150 * math.pi / 180
omega = 9.05
rotation_interia_magnet = 0.5 * (14.6 * 0.001) * ((15 * 0.001)**2)  # 0.5 * M * R^2
rotation_interia_plate = 0.5 * (4.5 * 0.001) * ((25 * 0.001)**2)  # 0.5 * M * R^2
rotation_interia_arm = 1/3 * (14.7 * 0.001) * ((123.6 * 0.001)**2)  # 0.5 * M * R^2
rotation_interia_total = rotation_interia_magnet + rotation_interia_plate + rotation_interia_arm
stiffness = rotation_interia_total * (omega**2)  # I * w^2

stiffness = stiffness * 0.39
rotation_interia_total = rotation_interia_total * 0.97


'''
First area
'''
# startline = 515
# endline = 595

startline = 8705
endline = 8800

time = time[startline:endline] - time[startline]
time = time * 0.001
angle = angle[startline:endline]
velocity = velocity[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]

initial_speed = velocity[0]
initial_theta = angle[0]


def ode_first_area_odeint(y, _x):
	y1, y2 = y
	return np.array([y2, -1*stiffness/rotation_interia_total * y1])


sol_odeint = odeint(ode_first_area_odeint, [initial_speed, initial_theta], time)


def ode_first_area_ivp(_t, y):
	return [y[1], -1*stiffness/rotation_interia_total * y[0]]


sol_ivp = solve_ivp(ode_first_area_ivp, [0, 0.09], [initial_theta, initial_speed], max_step=0.001, method='LSODA')

b, a = signal.butter(8, 0.05, 'lowpass')
data_filter = signal.filtfilt(b, a, velocity)

plt.figure(figsize=(8, 6), dpi=100)
plt.plot(time, angle, 'b-*', label='Angular Displacement [angle]')
plt.plot(sol_ivp.t, sol_ivp.y[0], 'r-*', label="Angular Displacement Simulation through ivp [angle]")
# plt.plot(time,soli[:,1],'r-*',label="Angular Displacement Simulation through odeint [angle]")
# plt.plot(time, angle - soli[:,1], 'k--', label="Error [angle]")
plt.grid()
plt.xlabel('Time [s]', fontweight='bold')
plt.ylabel('Angular Displacement [angle]', fontweight='bold')
plt.legend()
# plt.ylim([-100, -70])
plt.savefig("./PDF-File/The Filtered.pdf")

plt.figure(figsize=(8, 6), dpi=100)
plt.plot(time, data_filter, 'r-*', label='Filtered Angular Velocity [rad/s]')
plt.plot(sol_ivp.t, sol_ivp.y[1] * math.pi / 180, 'b-*', label="Angular Velocity Simulation through ivp [rad/s]")
# plt.plot(sol.t, data_filter - sol.y[1] * math.pi / 180, 'k--', label='Error [rad/s]')
plt.xlabel('Time [s]', fontweight='bold')
plt.ylabel('Angular Velocity [rad/s]', fontweight='bold')
plt.grid()
plt.legend()
plt.ylim([-10, 10])
plt.savefig("./PDF-File/The Filtered1.pdf")

plt.show()


'''
Second area
'''
# startline = 623
# endline = 1130
#
# time = time[startline:endline] - time[startline]
# time = time * 0.001
# angle = angle[startline:endline]
# velocity = velocity[startline:endline]
# Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
# Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
# Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
# Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]
#
# initial_speed = velocity[0]
# initial_theta = angle[0]
# def ODE_Firstarea_ivp(t, y):
#     return [y[1], -1*(stiffness)/rotation_interia_total * y[0]]
# sol_ivp = solve_ivp(ODE_Firstarea_ivp, [0,0.4], [initial_theta, initial_speed],max_step = 0.001, method = 'LSODA')
#
# b, a = signal.butter(8, 0.05, 'lowpass')  # low-path filtering
# data_filter = signal.filtfilt(b, a, velocity) # data为要过滤的信号
#
# plt.figure(figsize=(8, 6), dpi=100)
# plt.plot(time, angle, 'b-*', label='Angular Displacement [angle]')
# plt.plot(sol_ivp.t, sol_ivp.y[0], 'r-*', label="Angular Displacement Simulation through ivp [angle]")
#
# plt.grid()
# plt.xlabel('Time [s]', fontweight='bold')
# plt.ylabel('Angular Displacement [angle]', fontweight='bold')
# plt.legend()
# plt.ylim([-90, 90])
# plt.savefig("./PDF-File/The Filtered.pdf")
#
# plt.figure(figsize=(8, 6), dpi=100)
# plt.plot(time, data_filter, 'r-*', label='Filtered Angular Velocity [rad/s]')
# plt.plot(sol_ivp.t, sol_ivp.y[1] * math.pi / 180, 'b-*', label="Angular Velocity Simulation through ivp [rad/s]")
# plt.xlabel('Time [s]', fontweight='bold')
# plt.ylabel('Angular Velocity [rad/s]', fontweight='bold')
# plt.grid()
# plt.legend()
# plt.ylim([-10, 10])
# plt.savefig("./PDF-File/The Filtered1.pdf")
#
# plt.show()


# '''
# Third area
# '''
# startline = 1130
# endline = 1298

# time = time[startline:endline] - time[startline]
# time = time * 0.001
# angle = angle[startline:endline]
# velocity = velocity[startline:endline]
# Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
# Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
# Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
# Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]
#
# b, a = signal.butter(8, 0.05, 'lowpass')  # low-path filtering
# data_filter = signal.filtfilt(b, a, velocity) # data为要过滤的信号
# fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
#
# ax2 = ax1.twinx()
# ax1.plot(time, angle, 'k--', label='Angular Displacement [angle]')
# ax2.plot(time, velocity, 'g--', label='Original Angular Velocity [rad/s]')
# ax2.plot(time, data_filter, 'b--', label='Filtered Angular Velocity [rad/s]')
#
# ax1.set_xlabel('Time [s]', fontweight='bold')
# ax1.set_ylabel('Angular Displacement [angle]', fontweight='bold')
# ax2.set_ylabel('Filtered Angular Velocity [rad/s]', fontweight='bold')
# ax1.grid()
# fig.legend()
# ax1.set_ylim([-100, 100])
# ax2.set_ylim([-10, 10])
# fig.savefig("./PDF-File/The Filtered.pdf")
# plt.show()
