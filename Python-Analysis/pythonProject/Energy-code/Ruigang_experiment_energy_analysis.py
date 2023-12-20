import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import math

J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) \
    + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
w1 = 5.22
w2 = 9.12
k1 = J * (w1 ** 2)
k2 = J * (w2 ** 2)

data = pd.read_excel("./Repetitive_Experiment/150degrees_60.3degrees.xlsx")

time = np.array(data['Time'].ravel())
time = np.around(time, 2)
angle = np.array(data['Degree'].ravel()) * math.pi / 180
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


startline = 389
endline = -5

time = time[startline:endline] - time[startline]
time = time * 0.001
angle = angle[startline:endline]
velocity = velocity[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]
Upper_Elastic_Energy_Matrix = [0 for i in range(len(angle))]
Lower_Elastic_Energy_Matrix = [0 for i in range(len(angle))]
Total_Elastic_Energy_Matrix = [0 for i in range(len(angle))]
Kinetic_Energy_Matrix = [0 for i in range(len(angle))]
Total_Energy_Matrix = [0 for i in range(len(angle))]


b, a = signal.butter(8, 0.1, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filted_velocity = signal.filtfilt(b, a, velocity)  # data为要过滤的信号


def upper_elastic_energy(current_angle):
    return 0.5 * k1 * (current_angle ** 2)


def lower_elastic_energy(current_angle):
    return 0.5 * k2 * (current_angle ** 2)


def kinetic_energy(current_velocity):
    return 0.5 * J * (current_velocity ** 2)


for i in range(len(angle)):
    if Electromagnet_2_Clutch[i] == 1:
        Upper_Elastic_Energy_Matrix[i] = upper_elastic_energy(abs(angle[i]))
        upper_matrix_number = i
    else:
        Upper_Elastic_Energy_Matrix[i] = Upper_Elastic_Energy_Matrix[upper_matrix_number]

lower_Energy_Calculate_State = 0
for i in range(len(angle)):
    if Electromagnet_3_Clutch[i] == 1:
        if lower_Energy_Calculate_State == 0:
            lower_matrix_start_number = i
            lower_Energy_Calculate_State = 1
        Lower_Elastic_Energy_Matrix[i] = lower_elastic_energy(abs(angle[i]) - abs(angle[lower_matrix_start_number]))
        lower_matrix_number = i
    if Electromagnet_4_Clutch[i] == 1:
        Lower_Elastic_Energy_Matrix[i] = Lower_Elastic_Energy_Matrix[lower_matrix_number]

for i in range(len(angle)):
    Kinetic_Energy_Matrix[i] = kinetic_energy(abs(filted_velocity[i]))

for i in range(len(angle)):
    Total_Elastic_Energy_Matrix[i] = Upper_Elastic_Energy_Matrix[i] + Lower_Elastic_Energy_Matrix[i]
    Total_Energy_Matrix[i] = Upper_Elastic_Energy_Matrix[i] + Lower_Elastic_Energy_Matrix[i] + Kinetic_Energy_Matrix[i]


fig = plt.figure(figsize=(9, 6))
ax = plt.subplot(211)
ax.plot(time, Kinetic_Energy_Matrix, 'c--', label=r'$E_{k}$')
ax.plot(time, Upper_Elastic_Energy_Matrix, 'm-.', label=r'$E_{p1}$')
ax.plot(time, Lower_Elastic_Energy_Matrix, 'k-.', label=r'$E_{p2}$')
ax.plot(time, Total_Elastic_Energy_Matrix, 'g-.', label=r'$E_{pT}$')
ax.plot(time, Total_Energy_Matrix, 'y-', label=r'$ E$')
ax.set_ylabel('Energy [J]')
# ax.set_ylim([-0.001, 0.004])

ax1 = plt.subplot(212)
ax2 = ax1.twinx()
ax1.plot(time, angle * 180 / np.pi, 'r-', label=r'$\theta_{exp.}$')
ax2.plot(time, filted_velocity, 'b-', label=r'$\dot{\theta}_{exp.}$')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel(r'$\theta$ [$^\circ$]')
ax2.set_ylabel(r'$\dot{\theta}$ [rad/s]')
ax1.set_ylim([-100, 100])
ax2.set_ylim([-5, 5])
fig.legend(loc=(14.5/16, 5.4/9))

plt.savefig('./PDF-File/energy.pdf')

plt.show()
