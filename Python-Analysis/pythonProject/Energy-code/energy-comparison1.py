import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt

start_point = 122750
end_point = 132500

data = pd.read_csv("/Users/cotychen/Downloads/20231204/Uba.csv", low_memory=False)
data1 = pd.read_csv("/Users/cotychen/Downloads/20231204/Uca.csv", low_memory=False)
data2 = pd.read_csv("/Users/cotychen/Downloads/20231204/Ib.csv", low_memory=False)
data3 = pd.read_csv("/Users/cotychen/Downloads/20231204/Ic.csv", low_memory=False)
data4 = pd.read_csv("/Users/cotychen/Downloads/20231204/A.csv", low_memory=False)
data5 = pd.read_csv("/Users/cotychen/Downloads/20231204/B.csv", low_memory=False)
step = np.array(data['time'].ravel())[start_point:end_point]
Uba = np.array(data['voltage'].ravel())[start_point:end_point]
Uca = np.array(data1['voltage'].ravel())[start_point:end_point]
Vb = np.array(data2['voltage'].ravel())[start_point:end_point]
Vc = np.array(data3['voltage'].ravel())[start_point:end_point]
A = np.array(data4['voltage'].ravel())[start_point:end_point]
B = np.array(data5['voltage'].ravel())[start_point:end_point]

N = len(step)
motion = np.zeros(N)
sample_freq = 16000
dt = 1/sample_freq
time = np.linspace(dt, dt*N, N)

pre_A = 0
pre_time = 0
for i in range(len(A)):
    if pre_A > 2 > A[i]:
        if B[i] > 2:
            motion[i] = motion[i-1] + (360 / 512)
        else:
            motion[i] = motion[i-1] - (360 / 512)
        pre_time = time[i]
    else:
        motion[i] = motion[i-1]
    pre_A = A[i]

# change back from the voltage to the current
Ib = -(3.3 - 2 * Vb) / 40 / 0.0005
Ic = -(3.3 - 2 * Vc) / 40 / 0.0005

Ib = 2.3 * (Ib - np.mean(Ib[len(Vb)-1000:]))
Ic = 2.0 * (Ic - np.mean(Ic[len(Ib)-1000:]))


b, a = signal.butter(8, 0.01, 'lowpass')
Uba_filtered = signal.filtfilt(b, a, Uba)
Uca_filtered = signal.filtfilt(b, a, Uca)
b, a = signal.butter(8, 0.01, 'lowpass')
Ib_filtered = signal.filtfilt(b, a, Ib)
Ic_filtered = signal.filtfilt(b, a, Ic)

# fit the motion and calculate the velocity
z1 = np.polyfit(time, motion, 7)
p1 = np.poly1d(z1)
dot_p1 = np.polyder(p1, 1)
theta_fitted = p1(time)
dtheta_fitted = dot_p1(time) * np.pi / 180
ignore_front = 10
ignore_end = 500
dtheta_fitted = dtheta_fitted[ignore_front:-ignore_end]
dtheta_fitted = np.append([dtheta_fitted[0]]*ignore_front, dtheta_fitted)
dtheta_fitted = np.append(dtheta_fitted, [dtheta_fitted[-1]]*ignore_end)

J = (1 / 3 * (9.2 * 0.001) * ((123.5 * 0.001) ** 2)
     + (100 * 0.001) * ((0.5 * ((8.9 * 0.001) ** 2)) + (108.8 * 0.001) ** 2))
Electric_Power = (Uba_filtered*Ib_filtered+Uca_filtered*Ic_filtered)
Electric_Energy = np.zeros(N)
Mechanical_Power = np.zeros(N)
Mechanical_Energy = np.zeros(N)
Efficiency = np.zeros(N)

for i in range(len(dtheta_fitted)-1):
    Mechanical_Power[i+1] = 0.5 * J * ((dtheta_fitted[i+1]**2)
                                       - (dtheta_fitted[i]**2)) / (time[i+1]-time[i])
    Mechanical_Energy[i+1] = 0.5 * J * (dtheta_fitted[i+1] ** 2)  # from the velocity
    Electric_Energy[i+1] = Electric_Energy[i] + Electric_Power[i+1] * (time[i+1] - time[i])


Efficiency = Mechanical_Energy / Electric_Energy * 100

fig_num = 3
plt.subplots(figsize=(8, 4))
ax = plt.subplot(fig_num, 2, 1)
plt.plot(time, motion, 'b')
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.subplot(fig_num, 2, 3, sharex=ax)
plt.plot(time, Electric_Power, 'r--', label='Input')
plt.plot(time, Mechanical_Power, 'b-', label='Mechanical')
plt.plot(time, np.zeros(np.shape(time)), 'k:')
plt.legend()
plt.ylabel('Power [W]')
plt.legend()
plt.subplot(fig_num, 2, 5, sharex=ax)
plt.plot(time, Electric_Energy*1000, 'r--', label='Input')
plt.plot(time, Mechanical_Energy*1000, 'b', label='Mechanical')
plt.plot(time, np.zeros(np.shape(time)), 'k:')
plt.xlabel('Time [s]')
plt.ylabel('Energy [mJ]')
plt.legend()

# the other program ------------------------------------

J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((0.5 * ((3 * 0.001) ** 2)) + (110 * 0.001) ** 2)
J_load = (1 / 3 * (11.2 * 0.001) * ((123.5 * 0.001) ** 2) + (50 * 0.001) * ((((8.9 * 0.001) ** 2) / 12) + ((108.8 * 0.001) ** 2)))   # rotation inertia

w1 = 8.4
w2 = 6.5
k1 = J * (w1 ** 2)
k2 = J * (w2 ** 2)
print(k1)
print(k2)

data = pd.read_excel("../Data/20240128/20240128.xlsx")
time = np.array(data['Time'].ravel())
angle = np.array(data['Degree'].ravel()) * np.pi / 180
Electromagnet_1_Clutch = np.array(data['Electromagnet_Clutch_1'].ravel())
Electromagnet_2_Clutch = np.array(data['Electromagnet_Clutch_2'].ravel())
Electromagnet_3_Clutch = np.array(data['Electromagnet_Clutch_3'].ravel())
Electromagnet_4_Clutch = np.array(data['Electromagnet_Clutch_4'].ravel())

startline = 1234
endline = -220

time = time[startline:endline] - time[startline]
time = time * 0.001
angle = angle[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]

z = np.polyfit(time, angle, 30)
p = np.poly1d(z)
dot_p = np.polyder(p, 1)
theta_fitted = p(time)
dtheta_fitted = dot_p(time)

startpoint = 1
endpoint = None

Electromagnet_1_Clutch = Electromagnet_1_Clutch[startpoint:endpoint]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startpoint:endpoint]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startpoint:endpoint]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startpoint:endpoint]

time_fitted = time[startpoint:endpoint]
theta_fitted = theta_fitted[startpoint:endpoint]
dtheta_fitted = dtheta_fitted[startpoint:endpoint]

Upper_Elastic_Energy_Matrix = np.zeros(len(time_fitted))
Lower_Elastic_Energy_Matrix = np.zeros(len(time_fitted))
Total_Elastic_Energy_Matrix = np.zeros(len(time_fitted))
Kinetic_Energy_Matrix = np.zeros(len(time_fitted))
Total_Energy_Matrix = np.zeros(len(time_fitted))


def upper_elastic_energy(current_angle):
    return 0.5 * k1 * (current_angle ** 2)


def lower_elastic_energy(current_angle):
    return 0.5 * k2 * (current_angle ** 2)


def kinetic_energy(current_velocity):
    return 0.5 * J_load * (current_velocity ** 2)


upper_matrix_number = 0
for i in range(len(theta_fitted)):
    if Electromagnet_2_Clutch[i] == 1:
        Upper_Elastic_Energy_Matrix[i] = upper_elastic_energy(abs(theta_fitted[i]))
        upper_matrix_number = i
    else:
        Upper_Elastic_Energy_Matrix[i] = Upper_Elastic_Energy_Matrix[upper_matrix_number]

lower_Energy_Calculate_State = 0
lower_matrix_number = 0
lower_matrix_start_number = 0
for i in range(len(theta_fitted)):
    if Electromagnet_3_Clutch[i] == 1:
        if lower_Energy_Calculate_State == 0:
            lower_matrix_start_number = i
            lower_Energy_Calculate_State = 1
        Lower_Elastic_Energy_Matrix[i] = lower_elastic_energy(theta_fitted[i] - theta_fitted[lower_matrix_start_number] + 90 * np.pi / 180) - lower_elastic_energy(90 * np.pi / 180)
        if Lower_Elastic_Energy_Matrix[i] < Lower_Elastic_Energy_Matrix[i-1]:
            Lower_Elastic_Energy_Matrix[i] = lower_elastic_energy(theta_fitted[lower_matrix_start_number] - theta_fitted[i] - 90 * np.pi / 180) - lower_elastic_energy(90 * np.pi / 180)
        lower_matrix_number = i
    if Electromagnet_4_Clutch[i] == 1:
        Lower_Elastic_Energy_Matrix[i] = Lower_Elastic_Energy_Matrix[lower_matrix_number]
Lower_Elastic_Energy_Matrix = Lower_Elastic_Energy_Matrix + lower_elastic_energy(90 * np.pi / 180)

for i in range(len(theta_fitted)):
    Kinetic_Energy_Matrix[i] = kinetic_energy(abs(dtheta_fitted[i]))

for i in range(len(theta_fitted)):
    Total_Elastic_Energy_Matrix[i] = Upper_Elastic_Energy_Matrix[i] + Lower_Elastic_Energy_Matrix[i]
    Total_Energy_Matrix[i] = Upper_Elastic_Energy_Matrix[i] + Lower_Elastic_Energy_Matrix[i] + Kinetic_Energy_Matrix[i]


start_point = 0
end_point = -1
Kinetic_Power = np.insert((Kinetic_Energy_Matrix[1:] - Kinetic_Energy_Matrix[0:-1]) / (time_fitted[1:] - time_fitted[0:-1]), 0, 0)
Elastic_Power = np.insert((Total_Elastic_Energy_Matrix[1:] - Total_Elastic_Energy_Matrix[0:-1]) / (time_fitted[1:] - time_fitted[0:-1]), 0, 0)


plt.subplot(fig_num, 2, 2)
plt.plot(time[start_point:end_point], angle[start_point:end_point]/np.pi*180, 'b')
plt.subplot(fig_num, 2, 4)
plt.plot(time_fitted[start_point:end_point], -Elastic_Power[start_point:end_point], 'r--', label='Input')
plt.plot(time_fitted[start_point:end_point], Kinetic_Power[start_point:end_point], 'b', label='Mechanical')
plt.legend(ncol=2)
plt.plot(time_fitted, np.zeros(np.shape(time_fitted)), 'k:')
plt.subplot(fig_num, 2, 6)
temp = np.array(Total_Elastic_Energy_Matrix)[start_point:end_point]*1000
energy_input = temp[0]-temp
plt.plot(time_fitted[start_point:end_point], energy_input, 'r--', label='Input')
plt.plot(time_fitted[start_point:end_point],
         np.array(Kinetic_Energy_Matrix)[start_point:end_point]*1000, 'b-', label='Mechanical')
plt.legend(ncol=2)
plt.plot(time_fitted, np.zeros(np.shape(time_fitted)), 'k:')
plt.xlabel('Time [s]')
plt.ylim([-5, 80])
plt.xticks([0.0,0.1,0.2,0.3,0.4,0.5,0.6])
plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
