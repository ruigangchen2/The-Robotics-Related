import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import math

# 0.5 * M * R^2
# J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((110 * 0.001) ** 2) + (18.9 * 0.001) * ((88.6 * 0.001) ** 2)
J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((110 * 0.001) ** 2)
print(J)
# w1 = 5.22
# w2 = 9.12
w1 = 5.2
w2 = 8.0
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
endline = -8

time = time[startline:endline] - time[startline]
time = time * 0.001
angle = angle[startline:endline]
velocity = velocity[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]

b, a = signal.butter(8, 0.2, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filtedangle = signal.filtfilt(b, a, angle)  # data为要过滤的信号

b, a = signal.butter(8, 0.1, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filtedvelocity = signal.filtfilt(b, a, velocity)  # data为要过滤的信号
startline_filter0 = -725
endline_filter0 = -675
time0 = time[startline_filter0:endline_filter0] - time[startline_filter0]
angle0 = filtedangle[startline_filter0:endline_filter0]
velocity0 = velocity[startline_filter0:endline_filter0]
filtedData0 = filtedvelocity[startline_filter0:endline_filter0]

b, a = signal.butter(8, 0.06, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filtedvelocity = signal.filtfilt(b, a, velocity)  # data为要过滤的信号
startline_filter_1 = -675
endline_filter_1 = -639
time1 = time[startline_filter_1:endline_filter_1] - time[startline_filter0]
angle1 = filtedangle[startline_filter_1:endline_filter_1]
velocity1 = velocity[startline_filter_1:endline_filter_1]
filtedData1 = filtedvelocity[startline_filter_1:endline_filter_1]

b, a = signal.butter(8, 0.1, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filtedvelocity = signal.filtfilt(b, a, velocity)  # data为要过滤的信号
startline_filter_2 = -639
endline_filter_2 = -30
time2 = time[startline_filter_2:endline_filter_2] - time[startline_filter0]
angle2 = filtedangle[startline_filter_2:endline_filter_2]
velocity2 = velocity[startline_filter_2:endline_filter_2]
filtedData2 = filtedvelocity[startline_filter_2:endline_filter_2]

b, a = signal.butter(8, 0.4, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filtedvelocity = signal.filtfilt(b, a, velocity)  # data为要过滤的信号
startline_filter_3 = -30
endline_filter_3 = -3
time3 = time[startline_filter_3:endline_filter_3] - time[startline_filter0]
angle3 = filtedangle[startline_filter_3:endline_filter_3]
velocity3 = velocity[startline_filter_3:endline_filter_3]
filtedData3 = filtedvelocity[startline_filter_3:endline_filter_3]

time = np.concatenate((time0, time1, time2, time3), axis=0)
angle = np.concatenate((angle0, angle1, angle2, angle3), axis=0)
velocity = np.concatenate((velocity0, velocity1, velocity2, velocity3), axis=0)
filted_velocity = np.concatenate((filtedData0, filtedData1, filtedData2, filtedData3), axis=0)

Upper_Elastic_Energy_Matrix = [0 for i in range(len(angle))]
Lower_Elastic_Energy_Matrix = [0 for i in range(len(angle))]
Total_Elastic_Energy_Matrix = [0 for i in range(len(angle))]
Kinetic_Energy_Matrix = [0 for i in range(len(angle))]
Total_Energy_Matrix = [0 for i in range(len(angle))]


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


fig = plt.figure(figsize=(5, 3))
# fig = plt.figure(figsize=(10, 8))
plt.plot(time, np.array(Kinetic_Energy_Matrix)*1000, 'b-', label=r'$E_{kinetic}$')
plt.plot(time, np.array(Upper_Elastic_Energy_Matrix)*1000, 'r--', label=r'$E_{upper}$')
plt.plot(time, np.array(Lower_Elastic_Energy_Matrix)*1000, 'r-.', label=r'$E_{lower}$')
plt.plot(time, np.array(Total_Energy_Matrix)*1000, 'k', label=r'$E_{total}$')
plt.xlabel('Time [s]')
plt.ylabel('Energy [mJ]')
plt.ylim([-0.2, 3.1])
# plt.xticks(np.arange(0, 1, 0.1))
plt.legend(loc=(0.4, 0.23))
plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
