import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2

omega = 5.28
stiffness1 = inertia * (omega ** 2)  # I * w^2
stiffness2 = inertia * (omega ** 2)


friction1 = 0.00025
friction2 = 0.00025 * 0.5
friction3 = 0.00025

data = pd.read_excel("../Data/In_paper_data/150degrees.xlsx")

one = 566
two = 59
three = 617
four = 752
five = 758

time = np.array(data['Time'].ravel())[one:-15]*0.001
angle = np.array(data['Degree'].ravel())[one:-15]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-15]*np.pi/180
time_append = np.array([11153.17, 11296.64, 11328.51, 11342.01, 11351.21]) * 0.001 - time[0]
time_append1 = np.array([854, 867, 885, 897, 907]) * 0.001
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
time4 = time[four:five]
angle4 = angle[four+1:five]
velocity4 = velocity_filtered[four+1:five]

angle_append1 = np.array([-90.72, -90.54, -90.36, -90.18, -90]) * np.pi/180
velocity_append1 = np.array([-0.46, 1.25, 5.65, 13.33, 19.56]) * np.pi/180
time = np.append(time_append, time)
angle = np.append(angle_append1, angle)
velocity = np.append(velocity_append1, velocity)
velocity_filtered = np.append(velocity_append1, velocity_filtered)


def eom1(_t, y):
    return [y[1],  - (stiffness1 * (y[0] + angle1[0] * np.pi / 180) - friction1) / inertia]


def eom2(_t, y):
    return [y[1], - friction2 / inertia]


def eom3(_t, y):
    return [y[1],  - (stiffness2 * y[0] - friction3) / inertia]


def eom4(_t, y):
    return [y[1],  - friction3 / inertia]


sol_ivp1 = solve_ivp(eom1, [time1[0], time1[-1]], [angle1[0], velocity1[0]], max_step=0.001)
sol_ivp2 = solve_ivp(eom2, [time2[0], time2[-1]], [angle2[0], velocity2[0]], max_step=0.001)
sol_ivp3 = solve_ivp(eom3, [time3[0], time3[-1]], [angle3[0], velocity3[0]], max_step=0.001)
sol_ivp4 = solve_ivp(eom4, [time4[0], time4[-1]], [angle4[0], velocity4[0]], max_step=0.001)

###############################################################
fig = plt.figure(figsize=(6, 3))
ax1 = plt.subplot(211)
ax1.plot(time, angle * 180 / np.pi, 'b', label='experimental')
ax1.plot(sol_ivp1.t, sol_ivp1.y[0] * 180 / np.pi, 'r--')
ax1.plot(sol_ivp2.t, sol_ivp2.y[0] * 180 / np.pi, 'r--')
ax1.plot(sol_ivp3.t, sol_ivp3.y[0] * 180 / np.pi, 'r--', label='simulation')
ax1.plot(sol_ivp4.t, sol_ivp4.y[0] * 180 / np.pi, 'r--')
ax1.set_ylabel(r'$\theta$ [$^\circ$]', fontsize=12)
ax1.set_ylim([-100, 100])
ax1.get_xaxis().set_visible(False)
ax1.legend(prop={'size': 10})

ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(time, velocity_filtered, 'b', label='experimental')
ax2.plot(sol_ivp1.t, sol_ivp1.y[1], 'r--')
ax2.plot(sol_ivp2.t, sol_ivp2.y[1], 'r--')
ax2.plot(sol_ivp3.t, sol_ivp3.y[1], 'r--', label='simulation')
ax2.plot(sol_ivp4.t, sol_ivp4.y[1], 'r--')
ax2.set_xlabel("Time [s]")
ax2.set_ylabel(r'$\dot{\theta}$ [rad/s]', fontsize=12)
ax2.legend(prop={'size': 10})
ax2.set_ylim([-0.7, 7.7])
plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
