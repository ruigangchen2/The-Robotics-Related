import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import math

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



## the other program

J = (1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)
     + (5.5 * 0.001) * ((0.5 * ((3 * 0.001) ** 2)) + (110 * 0.001) ** 2))
J_load = (1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)
          + (50 * 0.001) * ((0.5 * ((8.9 * 0.001) ** 2)) + (108.8 * 0.001) ** 2))


w1 = 5.2
w2 = 7.0
k1 = J * (w1 ** 2)
k2 = J * (w2 ** 2)

data = pd.read_excel("../Data/back-and-forth-50g/20231220.xlsx")
time = np.array(data['Time'].ravel())
angle = np.array(data['Degree'].ravel()) * math.pi / 180
Electromagnet_1_Clutch = np.array(data['Electromagnet_Clutch_1'].ravel())
Electromagnet_2_Clutch = np.array(data['Electromagnet_Clutch_2'].ravel())
Electromagnet_3_Clutch = np.array(data['Electromagnet_Clutch_3'].ravel())
Electromagnet_4_Clutch = np.array(data['Electromagnet_Clutch_4'].ravel())

startline = 572
endline = 1300

time = time[startline:endline] - time[startline]
time = time * 0.001
angle = angle[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]

start_point0 = 0
end_point0 = 600
z = np.polyfit(time[start_point0:end_point0], angle[start_point0:end_point0], 99)
p = np.poly1d(z)
dot_p = np.polyder(p, 1)
theta_fitted0 = p(time[start_point0:end_point0])
velocity_fitted0 = dot_p(time[start_point0:end_point0])

start_point1 = 600
end_point1 = None
z = np.polyfit(time[start_point1:end_point1], angle[start_point1:end_point1], 99)
p = np.poly1d(z)
dot_p = np.polyder(p, 1)
theta_fitted1 = p(time[start_point1:end_point1])
velocity_fitted1 = dot_p(time[start_point1:end_point1])


time_final = time[start_point0:end_point1]
angle_final = angle[start_point0:end_point1]
fitangle_final = np.append(theta_fitted0, theta_fitted1)
fitvelocity_final = np.append(velocity_fitted0, velocity_fitted1)
# fitvelocity_final[599] = (fitvelocity_final[599] + fitvelocity_final[601])*0.65
# fitvelocity_final[600] = (fitvelocity_final[599] + fitvelocity_final[601])*0.5
# fitvelocity_final[601] = (fitvelocity_final[599] + fitvelocity_final[601])*0.5


Upper_Elastic_Energy = np.zeros(len(time_final))
Lower_Elastic_Energy = np.zeros(len(time_final))
Total_Elastic_Energy = np.zeros(len(time_final))
Kinetic_Energy = np.zeros(len(time_final))
Total_Energy = np.zeros(len(time_final))


upper_stage = 0
upper_matrix_number = 0
for i in range(len(time_final)):
    if Electromagnet_2_Clutch[i] == 1 and upper_stage == 0:
        Upper_Elastic_Energy[i] = 0.5 * k1 * (fitangle_final[i])**2
        upper_matrix_number = i
    elif Electromagnet_2_Clutch[i] == 1 and upper_stage == 1:
        Upper_Elastic_Energy[i] = 0.5 * k1 * (fitangle_final[i] + 5 * np.pi / 180)**2
    else:
        Upper_Elastic_Energy[i] = Upper_Elastic_Energy[upper_matrix_number]
        upper_stage = 1

lower_matrix_number = 0
lower_Energy_Calculate_State = 0
for i in range(len(time_final)):
    if Electromagnet_3_Clutch[i] == 1:
        if lower_Energy_Calculate_State == 0:
            lower_matrix_start_number = i
            lower_Energy_Calculate_State = 1
        Lower_Elastic_Energy[i] = 0.5 * k2 * (abs(fitangle_final[i]) - abs(fitangle_final[lower_matrix_start_number]))**2
        lower_matrix_number = i
    if Electromagnet_4_Clutch[i] == 1:
        Lower_Elastic_Energy[i] = Lower_Elastic_Energy[lower_matrix_number]

for i in range(len(time_final)):
    Kinetic_Energy[i] = 0.5 * J_load * (fitvelocity_final[i])**2

# modify
Lower_Elastic_Energy = np.append(Lower_Elastic_Energy[:-5], [Lower_Elastic_Energy[-5]]*5)
Kinetic_Energy = np.append(Kinetic_Energy[:-5], [Kinetic_Energy[-5]]*5)
Upper_Elastic_Energy = np.append(Upper_Elastic_Energy[:-5], [Upper_Elastic_Energy[-5]]*5)

Total_Elastic_Energy = Upper_Elastic_Energy + Lower_Elastic_Energy
Total_Energy = Upper_Elastic_Energy + Lower_Elastic_Energy + Kinetic_Energy



start_point = 0
end_point = None

Kinetic_Power = np.insert((Kinetic_Energy[1:] - Kinetic_Energy[0:-1])
                          / (time[1:] - time[0:-1]), 0, 0)
Elastic_Power = np.insert((Total_Elastic_Energy[1:] - Total_Elastic_Energy[0:-1])
                          / (time[1:] - time[0:-1]), 0, 0)



plt.subplot(fig_num, 2, 2)
plt.plot(time[start_point:end_point], angle[start_point:end_point]/np.pi*180, 'b')
plt.subplot(fig_num, 2, 4)
plt.plot(time[start_point:end_point], -Elastic_Power[start_point:end_point]/np.pi*180, 'r--', label='Input')
plt.plot(time[start_point:end_point], Kinetic_Power[start_point:end_point]/np.pi*180, 'b', label='Mechanical')
plt.legend(ncol=2)
plt.subplot(fig_num, 2, 6)
temp = np.array(Total_Elastic_Energy)[start_point:end_point]*1000
energy_input = temp[0]-temp
plt.plot(time[start_point:end_point], energy_input, 'r--', label='Input')
plt.plot(time[start_point:end_point],
         np.array(Kinetic_Energy)[start_point:end_point]*1000, 'b-', label='Mechanical')
plt.legend(ncol=2)
plt.xlabel('Time [s]')
plt.ylabel('Energy [mJ]')
plt.ylim([-0.1, 1.4])
plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
