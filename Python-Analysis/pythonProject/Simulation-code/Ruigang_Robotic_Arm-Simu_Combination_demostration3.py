import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2

omega1 = 5.28
omega2 = 5.45
stiffness1 = inertia * (omega1 ** 2)  # I * w^2
stiffness2 = inertia * (omega2 ** 2)

damp1 = 0.0000405
damp2 = 0.00003780
damp3 = 0.0001869

data = pd.read_excel("../Data/In_paper_data/150degrees.xlsx")

one = 566
two = 59
three = 617
four = 754

time = np.array(data['Time'].ravel())[one:-15]*0.001
angle = np.array(data['Degree'].ravel())[one:-15]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-15]*np.pi/180
time_append1 = np.array([11153.17, 11296.64, 11328.51, 11342.01, 11351.21]) * 0.001 - time[0]
time = time - time[0]


[b, a] = signal.butter(8, 0.05, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数

velocity_filtered = signal.filtfilt(b, a, velocity)

time1 = time[:two]
angle1 = angle[:two]
velocity1 = velocity_filtered[:two]
time2 = time[two:three]
angle2 = angle[two+1:three]
velocity2 = velocity_filtered[two+1:three]
time3 = time[three:four]
angle3 = angle[three+1:four]
velocity3 = velocity_filtered[three+1:four]

clutch1 = np.array(data['Electromagnet_Clutch_1'].ravel())[one:-15]
clutch2 = np.array(data['Electromagnet_Clutch_2'].ravel())[one:-15]
clutch3 = np.array(data['Electromagnet_Clutch_3'].ravel())[one:-15]
clutch4 = np.array(data['Electromagnet_Clutch_4'].ravel())[one:-15]


angle_append1 = np.array([-90.72, -90.54, -90.36, -90.18, -90]) * np.pi/180
velocity_append1 = np.array([-0.46, 1.25, 5.65, 13.33, 19.56]) * np.pi/180
time = np.append(time_append1, time)
angle = np.append(angle_append1, angle)
velocity = np.append(velocity_append1, velocity)
velocity_filtered = np.append(velocity_append1, velocity_filtered)

clutch1 = np.append([1, 1, 1, 1, 1], clutch1)
clutch2 = np.append([0, 0, 0, 0, 0], clutch2)
clutch3 = np.append([0, 0, 0, 0, 0], clutch3)
clutch4 = np.append([0, 0, 0, 0, 0], clutch4)


def eom1(_t, y):
    return [y[1],  - (stiffness1 * (y[0] + angle1[0] * np.pi / 180) - damp1 * y[1]) / inertia]


def eom2(_t, y):
    return [y[1], - damp2 * y[1] / inertia]


def eom3(_t, y):
    return [y[1],  - (stiffness2 * y[0] - damp3 * y[1]) / inertia]


sol_ivp1 = solve_ivp(eom1, [time1[0], time1[-1]], [angle1[0], velocity1[0]], max_step=0.001)
sol_ivp2 = solve_ivp(eom2, [time2[0], time2[-1]], [angle2[0], velocity2[0]], max_step=0.001)
sol_ivp3 = solve_ivp(eom3, [time3[0], time3[-1]], [angle3[0], velocity3[0]], max_step=0.001)

# for energy analysis #########################################

time_EA = time[5:four-5]
angle_EA = angle[5:four-5]
print(time_EA)

z = np.polyfit(time_EA, angle_EA, 30)
p = np.poly1d(z)
dot_p = np.polyder(p, 1)
theta_fitted = p(time_EA)
dtheta_fitted = dot_p(time_EA)

Electromagnet_1_Clutch = clutch1[5:four-5]
Electromagnet_2_Clutch = clutch2[5:four-5]
Electromagnet_3_Clutch = clutch3[5:four-5]
Electromagnet_4_Clutch = clutch4[5:four-5]

Upper_Elastic_Energy = np.zeros(len(time_EA))
Lower_Elastic_Energy = np.zeros(len(time_EA))
Total_Elastic_Energy = np.zeros(len(time_EA))
Kinetic_Energy = np.zeros(len(time_EA))
Total_Energy = np.zeros(len(time_EA))


upper_matrix_number = 0
for i in range(len(time_EA)):
    if Electromagnet_2_Clutch[i] == 1:
        Upper_Elastic_Energy[i] = 0.5 * stiffness1 * ((theta_fitted[i]) ** 2)
        upper_matrix_number = i
    else:
        Upper_Elastic_Energy[i] = Upper_Elastic_Energy[upper_matrix_number]

lower_Energy_Calculate_State = 0
lower_matrix_number = 0
lower_matrix_start_number = 0
for i in range(len(time_EA)):
    if Electromagnet_3_Clutch[i] == 1:
        if lower_Energy_Calculate_State == 0:
            lower_matrix_start_number = i
            lower_Energy_Calculate_State = 1
        Lower_Elastic_Energy[i] = 0.5 * stiffness2 * ((abs(theta_fitted[i]) - abs(theta_fitted[lower_matrix_start_number])) ** 2)
        lower_matrix_number = i
    if Electromagnet_4_Clutch[i] == 1:
        Lower_Elastic_Energy[i] = Lower_Elastic_Energy[lower_matrix_number]

for i in range(len(time_EA)):
    Kinetic_Energy[i] = 0.5 * inertia * ((dtheta_fitted[i]) ** 2)

Total_Elastic_Energy = Upper_Elastic_Energy + Lower_Elastic_Energy
Total_Energy = Upper_Elastic_Energy + Lower_Elastic_Energy + Kinetic_Energy

upper_elastic_energy_append = np.array([Upper_Elastic_Energy[0]]*5)
lower_elastic_energy_append = np.array([Lower_Elastic_Energy[0]]*5)
total_energy_append = np.array([Total_Energy[0]]*5)
kinetic_energy_append = np.array([Kinetic_Energy[0]]*5)

time_EA = np.append(time_append1, time_EA)
Upper_Elastic_Energy = np.append(upper_elastic_energy_append, Upper_Elastic_Energy)
Lower_Elastic_Energy = np.append(lower_elastic_energy_append, Lower_Elastic_Energy)
Total_Energy = np.append(total_energy_append, Total_Energy)
Kinetic_Energy = np.append(kinetic_energy_append, Kinetic_Energy)
###############################################################
fig = plt.figure(figsize=(6, 5), dpi=100)
ax1 = plt.subplot(411)
ax1.plot(time, angle * 180 / np.pi, 'b', label='experimental')
ax1.plot(sol_ivp1.t, sol_ivp1.y[0] * 180 / np.pi, 'r--')
ax1.plot(sol_ivp2.t, sol_ivp2.y[0] * 180 / np.pi, 'r--')
ax1.plot(sol_ivp3.t, sol_ivp3.y[0] * 180 / np.pi, 'r--', label='simulation')
ax1.set_ylabel(r'$\theta$ [$^\circ$]')
ax1.set_ylim([-100, 100])
ax1.get_xaxis().set_visible(False)
ax1.legend()

ax2 = plt.subplot(412, sharex=ax1)
ax2.plot(time, velocity_filtered, 'b', label='experimental')
ax2.plot(sol_ivp1.t, sol_ivp1.y[1], 'r--')
ax2.plot(sol_ivp2.t, sol_ivp2.y[1], 'r--')
ax2.plot(sol_ivp3.t, sol_ivp3.y[1], 'r--', label='simulation')
ax2.plot(time, np.zeros(np.shape(time)), 'k:')
ax2.set_ylabel(r'$\dot{\theta}$ [rad/s]')
ax2.legend(ncol=3)
ax2.get_xaxis().set_visible(False)
ax2.set_ylim([-0.7, 7.7])

ax3 = plt.subplot(413, sharex=ax1)
ax3.plot(time, clutch1, 'b-', label='Up1')
ax3.plot(time, clutch2, 'r--', label='Up2')
ax3.plot(time, clutch3, 'k-.', label='Low1')
ax3.plot(time, clutch4, 'c:', label='Low2')
ax3.set_yticks([0, 1], ['OFF', 'ON'])
ax3.get_xaxis().set_visible(False)
ax3.legend()

ax4 = plt.subplot(414, sharex=ax1)
plt.plot(time_EA, np.array(Kinetic_Energy)*1000, 'b-', label=r'$E_{kinetic}$')
plt.plot(time_EA, np.array(Upper_Elastic_Energy)*1000, 'r--', label=r'$E_{upper}$')
plt.plot(time_EA, np.array(Lower_Elastic_Energy)*1000, 'c-.', label=r'$E_{lower}$')
plt.plot(time_EA, np.array(Total_Energy)*1000, 'k', label=r'$E_{total}$')
ax4.set_ylabel('Energy [mJ]')
ax4.set_xlabel('Time [s]')
ax4.legend()

plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
