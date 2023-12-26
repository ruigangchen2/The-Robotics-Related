import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy import signal

# 15 degrees of acceleration

J = (1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)
     + (5.5 * 0.001) * ((0.5 * ((3 * 0.001) ** 2)) + (110 * 0.001) ** 2))
J_load = (1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)
          + (50 * 0.001) * ((0.5 * ((8.9 * 0.001) ** 2)) + (108.8 * 0.001) ** 2))

w1 = 5.2
w2 = 7
k1 = J * (w1 ** 2)
k2 = J * (w2 ** 2)

data = pd.read_excel("../Data/20231226-accelerationangle-55/data.xlsx")
time = np.array(data['Time'].ravel())
angle = np.array(data['Degree'].ravel()) * math.pi / 180
Electromagnet_1_Clutch = np.array(data['Electromagnet_Clutch_1'].ravel())
Electromagnet_2_Clutch = np.array(data['Electromagnet_Clutch_2'].ravel())
Electromagnet_3_Clutch = np.array(data['Electromagnet_Clutch_3'].ravel())
Electromagnet_4_Clutch = np.array(data['Electromagnet_Clutch_4'].ravel())

startline = 390
endline = -27

time = time[startline:endline] - time[startline]
time = time * 0.001
angle = angle[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]

start_point0 = 0
end_point0 = 1000
z = np.polyfit(time[start_point0:end_point0], angle[start_point0:end_point0], 20)
p = np.poly1d(z)
dot_p = np.polyder(p, 1)
theta_fitted0 = p(time[start_point0:end_point0])
velocity_fitted0 = dot_p(time[start_point0:end_point0])

start_point1 = 1000
end_point1 = None
z = np.polyfit(time[start_point1:end_point1], angle[start_point1:end_point1], 20)
p = np.poly1d(z)
dot_p = np.polyder(p, 1)
theta_fitted1 = p(time[start_point1:end_point1])
velocity_fitted1 = dot_p(time[start_point1:end_point1])

time_final = time[start_point0:end_point1]
angle_final = angle[start_point0:end_point1]
fitangle_final = np.append(theta_fitted0, theta_fitted1)
fitvelocity_final = np.append(velocity_fitted0, velocity_fitted1)
# fitvelocity_final[727] = (fitvelocity_final[726] + fitvelocity_final[730])*0.65
# fitvelocity_final[728] = (fitvelocity_final[726] + fitvelocity_final[730])*0.5
# fitvelocity_final[729] = (fitvelocity_final[726] + fitvelocity_final[730])*0.5


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


plt.figure(figsize=(5, 4))
ax1 = plt.subplot(3, 1, 1)
ax2 = ax1.twinx()
ax1.plot(time_final, angle_final * 180 / np.pi, 'b-*', label='angle')
ax1.plot(time_final, fitangle_final * 180 / np.pi, 'r-', label='angle')
ax2.plot(time_final, fitvelocity_final, 'g-', label='velocity')
ax1.set_ylabel(r'$\theta$ [$^\circ$]')
ax2.set_ylabel(r'$\dot{\theta}$ [rad/s]')
ax2.set_ylim([-5, 5])
ax1.get_xaxis().set_visible(False)
lines, labels = ax1.get_legend_handles_labels()
lines_1, labels_1 = ax2.get_legend_handles_labels()
ax2.legend(lines+lines_1, labels+labels_1)

ax = plt.subplot(3, 1, 2, sharex=ax1)
plt.plot(time_final, np.array(Kinetic_Energy)*1000, 'b-', label=r'$E_{kinetic}$')
plt.plot(time_final, np.array(Upper_Elastic_Energy)*1000, 'r--', label=r'$E_{upper}$')
plt.plot(time_final, np.array(Lower_Elastic_Energy)*1000, 'c-.', label=r'$E_{lower}$')
plt.plot(time_final, np.array(Total_Energy)*1000, 'k', label=r'$E_{total}$')
ax.get_xaxis().set_visible(False)
plt.ylabel('Energy [mJ]')
plt.legend()
plt.xlabel('Time [s]')
plt.tight_layout()

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
