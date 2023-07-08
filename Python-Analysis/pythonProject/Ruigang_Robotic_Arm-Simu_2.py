import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy import signal


inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
omega = 5.28
stiffness = inertia * omega ** 2  # I * w^2
slope = 0.108
torque_friction = slope * np.pi * stiffness / 2 / omega

startline = 600
endline = 700
data = pd.read_excel("./20230703/data.xlsx")
temp = np.around(np.array(data['Time'].ravel()), 2)
time = (temp[startline:endline] - temp[startline]) * 0.001
angle = np.around(np.array(data['Degree'].ravel()) * np.pi / 180, 2)[startline:endline]
velocity = np.around(np.array(data['Velocity'].ravel()) * np.pi / 180, 2)[startline:endline]


def eom(_t, y):
    return [y[1], - torque_friction / inertia]


sol_ivp = solve_ivp(eom, [0, 0.076], [angle[0], velocity[0]], max_step=0.001)

order = 12
z = np.polyfit(time, angle, order)
p = np.poly1d(z)
angle_fit = p(time)
z = np.polyfit(time, velocity, order)
p = np.poly1d(z)
velocity_fit = p(time)

b, a = signal.butter(8, 0.02, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
data_filter = signal.filtfilt(b, a, velocity)  # data为要过滤的信号

plt.figure(figsize=(6, 5), dpi=100)
plt.subplot(211)
plt.plot(time, angle * 180 / np.pi, 'b-+', label=r'$\theta_{exp}$')
plt.plot(time, angle_fit * 180 / np.pi, 'c-+', label=r'$\theta_{fit}$')
plt.plot(sol_ivp.t, sol_ivp.y[0] * 180 / np.pi, 'r-*', label=r"$\theta_{Simu}$")
plt.grid()
plt.xlabel('Time [s]')
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.legend()
plt.subplot(212)
plt.plot(time, data_filter, 'b-*', label=r'$\dot{\theta}_{exp}$')
plt.plot(sol_ivp.t, sol_ivp.y[1], 'r-*', label=r"$\dot{\theta}_{simu}$")
plt.xlabel('Time [s]')
plt.ylabel('Velocity [rad/s]')
plt.grid()
plt.legend()
plt.tight_layout()
plt.ylim([3, 7])
plt.savefig('Sim.pdf')
plt.show()
