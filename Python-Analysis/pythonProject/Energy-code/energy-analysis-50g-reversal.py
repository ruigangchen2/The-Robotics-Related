import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((0.5 * ((3 * 0.001) ** 2)) + (110 * 0.001) ** 2)
J_load = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (50 * 0.001) * ((0.5 * ((8.9 * 0.001) ** 2)) + (108.8 * 0.001) ** 2)
print("rotation inertia: %.8lf km*m^2" % J_load)

w1 = 5.6
w2 = 7.4
k1 = J * (w1 ** 2)
k2 = J * (w2 ** 2)

data = pd.read_excel("../Data/20231219/20231219.xlsx")
time = np.array(data['Time'].ravel())
angle = np.array(data['Degree'].ravel()) * math.pi / 180
Electromagnet_1_Clutch = np.array(data['Electromagnet_Clutch_1'].ravel())
Electromagnet_2_Clutch = np.array(data['Electromagnet_Clutch_2'].ravel())
Electromagnet_3_Clutch = np.array(data['Electromagnet_Clutch_3'].ravel())
Electromagnet_4_Clutch = np.array(data['Electromagnet_Clutch_4'].ravel())

startline = 391
endline = -40

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

startpoint = 0
endpoint = None

time_fitted = time[startpoint:endpoint]
theta_fitted = theta_fitted[startpoint:endpoint]
dtheta_fitted = dtheta_fitted[startpoint:endpoint]


Upper_Elastic_Energy_Matrix = np.zeros(len(time_fitted))
Lower_Elastic_Energy_Matrix = np.zeros(len(time_fitted))
Total_Elastic_Energy_Matrix = np.zeros(len(time_fitted))
Kinetic_Energy_Matrix = np.zeros(len(time_fitted))
Total_Energy_Matrix = np.zeros(len(time_fitted))

def upper_elastic_energy(angle):
    return (0.5 * k1 * (angle ** 2))


def lower_elastic_energy(angle):
    return (0.5 * k2 * (angle ** 2))


def kinetic_energy(velocity):
    return (0.5 * J_load * (velocity ** 2))


upper_stage = 0
for i in range(len(theta_fitted)):
    if Electromagnet_2_Clutch[i] == 1 and upper_stage == 0:
        Upper_Elastic_Energy_Matrix[i] = upper_elastic_energy(abs(theta_fitted[i]))
        upper_matrix_number = i
    elif Electromagnet_2_Clutch[i] == 1 and upper_stage == 1:
        Upper_Elastic_Energy_Matrix[i] = upper_elastic_energy(abs(theta_fitted[i] + 5 * np.pi / 180))
    else:
        Upper_Elastic_Energy_Matrix[i] = Upper_Elastic_Energy_Matrix[upper_matrix_number]
        upper_stage = 1


lower_Energy_Calculate_State = 0
for i in range(len(theta_fitted)):
    if Electromagnet_3_Clutch[i] == 1:
        if lower_Energy_Calculate_State == 0:
            lower_matrix_start_number = i
            lower_Energy_Calculate_State = 1
        Lower_Elastic_Energy_Matrix[i] = lower_elastic_energy(abs(theta_fitted[i]) - abs(theta_fitted[lower_matrix_start_number]))
        lower_matrix_number = i
    if Electromagnet_4_Clutch[i] == 1:
        Lower_Elastic_Energy_Matrix[i] = Lower_Elastic_Energy_Matrix[lower_matrix_number]

for i in range(len(theta_fitted)):
    Kinetic_Energy_Matrix[i] = kinetic_energy(abs(dtheta_fitted[i]))

for i in range(len(theta_fitted)):
    Total_Elastic_Energy_Matrix[i] = Upper_Elastic_Energy_Matrix[i] + Lower_Elastic_Energy_Matrix[i]
    Total_Energy_Matrix[i] = Upper_Elastic_Energy_Matrix[i] + Lower_Elastic_Energy_Matrix[i] + Kinetic_Energy_Matrix[i]

print("Totay Energy: %lf J" % Total_Energy_Matrix[0])
print("Harvested Energy: %lf J" % Total_Energy_Matrix[-10])


fig = plt.figure(figsize=(10, 8))
ax1 = plt.subplot(3, 1, 1)
ax2 = ax1.twinx()
ax1.plot(time, angle * 180 / np.pi, 'b-*', label='angle')
ax1.plot(time_fitted, theta_fitted * 180 / np.pi, 'r-', label='angle')
ax2.plot(time_fitted, dtheta_fitted, 'g-', label='velocity')
ax1.set_ylabel(r'$\theta$ [$^\circ$]')
ax2.set_ylabel(r'$\dot{\theta}$ [rad/s]')
ax2.set_ylim([-5, 5])
ax1.get_xaxis().set_visible(False)
lines, labels = ax1.get_legend_handles_labels()
lines_1, labels_1 = ax2.get_legend_handles_labels()
ax2.legend(lines+lines_1, labels+labels_1)

ax = plt.subplot(3, 1, 2, sharex=ax1)
plt.plot(time_fitted, np.array(Kinetic_Energy_Matrix)*1000, 'b-', label=r'$E_{kinetic}$')
plt.plot(time_fitted, np.array(Upper_Elastic_Energy_Matrix)*1000, 'r--', label=r'$E_{upper}$')
plt.plot(time_fitted, np.array(Lower_Elastic_Energy_Matrix)*1000, 'r-.', label=r'$E_{lower}$')
plt.plot(time_fitted, np.array(Total_Energy_Matrix)*1000, 'k', label=r'$E_{total}$')
ax.get_xaxis().set_visible(False)
plt.ylabel('Energy [mJ]')
plt.legend()

plt.subplot(3, 1, 3, sharex=ax1)
plt.plot(time, Electromagnet_1_Clutch, 'b--', label='Clutch 1')
plt.plot(time, Electromagnet_2_Clutch, 'r--', label='Clutch 2')
plt.plot(time, Electromagnet_3_Clutch, 'c--', label='Clutch 3')
plt.plot(time, Electromagnet_4_Clutch, 'k--', label='Clutch 4')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('ON / OFF')
plt.tight_layout()
plt.savefig('../Output/temp.pdf')
plt.show()
