import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy import signal


inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
omega1 = 5.28
omega2 = 5.22
stiffness1 = inertia * omega1 ** 2  # I * w^2
stiffness2 = inertia * omega2 ** 2
slope1 = 0.108
slope2 = 0.163
torque_friction1 = slope1 * np.pi * stiffness1 / 2 / omega1
torque_friction2 = slope2 * np.pi * stiffness2 / 2 / omega2

data = pd.read_excel("./20230703/data.xlsx")

startline1 = 515
endline1 = 580
temp1 = np.around(np.array(data['Time'].ravel()), 2)
time1 = (temp1[startline1:endline1] - temp1[startline1]) * 0.001
angle1 = np.around(np.array(data['Degree'].ravel()) * np.pi / 180, 2)[startline1:endline1]
velocity1 = np.around(np.array(data['Velocity'].ravel()) * np.pi / 180, 2)[startline1:endline1]

startline2 = 600
endline2 = 700
temp2 = np.around(np.array(data['Time'].ravel()), 2)
time2 = (temp2[startline1:endline1] - temp2[startline1]) * 0.001
angle2 = np.around(np.array(data['Degree'].ravel()) * np.pi / 180, 2)[startline2:endline2]
velocity2 = np.around(np.array(data['Velocity'].ravel()) * np.pi / 180, 2)[startline2:endline2]

startline3 = 600
endline3 = 700
temp3 = np.around(np.array(data['Time'].ravel()), 2)
time3 = (temp3[startline1:endline1] - temp3[startline1]) * 0.001
angle3 = np.around(np.array(data['Degree'].ravel()) * np.pi / 180, 2)[startline3:endline3]
velocity3 = np.around(np.array(data['Velocity'].ravel()) * np.pi / 180, 2)[startline3:endline3]


def eom1(_t, y):
    return [y[1], - stiffness1 / inertia * y[0]]

def eom2(_t, y):
    return [y[1], - torque_friction1 / inertia]

def eom3(_t, y):
    return [y[1], - stiffness2 / inertia * y[0]]


sol_ivp = solve_ivp(eom, [0, 0.15], [angle[0], velocity[0]], max_step=0.001)

order = 15
z = np.polyfit(time, angle, order)
p = np.poly1d(z)
angle_fit = p(time)
z = np.polyfit(time, velocity, order)
p = np.poly1d(z)
velocity_fit = p(time)

b, a = signal.butter(8, 0.06, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
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
plt.plot(time, velocity_fit, 'b-*', label=r'$\dot{\theta}_{exp}$')
plt.plot(sol_ivp.t, sol_ivp.y[1], 'r-*', label=r"$\dot{\theta}_{simu}$")
plt.xlabel('Time [s]')
plt.ylabel('Velocity [rad/s]')
plt.grid()
plt.legend()
plt.tight_layout()
# plt.ylim([3, 7])
plt.savefig('Sim.pdf')
plt.show()
