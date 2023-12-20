import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
omega1 = 5.28
omega2 = 5.22
stiffness1 = inertia * omega1 ** 2  # I * w^2
stiffness2 = inertia * omega2 ** 2
slope = 0.108
torque_friction = slope * np.pi * stiffness1 / 2 / omega1

data = pd.read_excel("./20230703/data.xlsx")
one = 515
two = 66
three = 620
four = 780
time = np.array(data['Time'].ravel())[one:]*0.001
angle = np.array(data['Degree'].ravel())[one:]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:]*np.pi/180

[b, a] = signal.butter(8, 0.05, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
velocity_filtered = signal.filtfilt(b, a, velocity)
# plt.plot(velocity, 'b')
# plt.plot(velocity_filtered, 'r--')

time1 = time[:two]
angle1 = angle[:two]
velocity1 = velocity_filtered[:two]
time2 = time[two:three]
angle2 = angle[two+1:three]
velocity2 = velocity_filtered[two+1:three]
time3 = time[three:four]
angle3 = angle[three+1:four]
velocity3 = velocity_filtered[three+1:four]


def eom1(_t, y):  # y =  - k/J * (90 + y0)
    return [y[1], - stiffness1 / inertia * y[0]]


def eom2(_t, y):
    return [y[1], - torque_friction / inertia]


def eom3(_t, y):
    return [y[1], - stiffness2 / inertia * y[0]]


sol_ivp1 = solve_ivp(eom1, [time1[0], time1[-1]], [angle1[0], velocity1[0]], max_step=0.001)
sol_ivp2 = solve_ivp(eom2, [time2[0], time2[-1]], [angle2[0], velocity2[0]], max_step=0.001)
sol_ivp3 = solve_ivp(eom3, [time3[0], time3[-1]], [angle3[0], velocity3[0]], max_step=0.001)

plt.figure(figsize=(7, 6), dpi=100)
plt.subplot(211)
plt.plot(time, angle * 180 / np.pi, 'b', label='original')
plt.plot(sol_ivp1.t, sol_ivp1.y[0] * 180 / np.pi, 'r--')
plt.plot(sol_ivp2.t, sol_ivp2.y[0] * 180 / np.pi, 'r--')
plt.plot(sol_ivp3.t, sol_ivp3.y[0] * 180 / np.pi, 'r--', label='modeling')
plt.xlabel('Time [s]')
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.ylim([-110, 100])
plt.legend()
plt.subplot(212)
plt.plot(time, velocity, 'k-', alpha=0.2, label='original')
plt.plot(time, velocity_filtered, 'b', label='filtered')
plt.plot(sol_ivp1.t, sol_ivp1.y[1], 'r--')
plt.plot(sol_ivp2.t, sol_ivp2.y[1], 'r--')
plt.plot(sol_ivp3.t, sol_ivp3.y[1], 'r--', label='modeling')
plt.xlabel('Time [s]')
plt.ylabel('Velocity [rad/s]')
plt.legend()
plt.tight_layout()
plt.ylim([-2, 7])
plt.savefig('Sim.pdf')
plt.show()
