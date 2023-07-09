import math
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


data = pd.read_excel("./20230703/data.xlsx")
time = np.around(np.array(data['Time'].ravel()), 2)
angle = np.around(np.array(data['Degree'].ravel()) * math.pi / 180, 2)
velocity = np.around(np.array(data['Velocity'].ravel()) * math.pi / 180, 2)

startline = 515
endline = 580

time = time[startline:endline] - time[startline]
time = time * 0.001
angle = angle[startline:endline]
velocity = velocity[startline:endline]

omega = 5.29
interia_magnet = 0.5 * (14.6 * 0.001) * ((15 * 0.001) ** 2)  # 0.5 * M * R^2
interia_plate = 0.5 * (4.5 * 0.001) * ((25 * 0.001) ** 2)  # 0.5 * M * R^2
interia_arm = 1 / 3 * ((14.7) * 0.001) * ((123.6 * 0.001) ** 2)  # 0.5 * M * R^2
interia_mass = (5.5 * 0.001) * ((110 * 0.001) ** 2)  # M * R^2
interia_total = interia_magnet + interia_plate + interia_arm + interia_mass
stiffness = interia_total * (omega ** 2)  # I * w^2

initial_speed = velocity[0]
initial_theta = angle[0]


def eom(_t, y):  # y2 =  k / J * (90 + y0)
    y1, y2 = y
    return [y2,  - stiffness / interia_total * y1]


sol_ivp = solve_ivp(eom, [0, 0.09], [initial_theta, initial_speed], max_step=0.001)

b, a = signal.butter(8, 0.05, 'lowpass')
velocity_filter = signal.filtfilt(b, a, velocity)

order = 12
z = np.polyfit(time, angle, order)
p = np.poly1d(z)
data_fit = p(time)
print(z)

plt.figure(figsize=(8, 6), dpi=100)
plt.subplot(211)
plt.plot(time, angle * 180 / math.pi, 'c-+', label=r'Displacement [$^\circ$]')
plt.plot(time, data_fit * 180 / math.pi, 'k-+', label=r'Curve Fit Displacement [$^\circ$]')
plt.plot(sol_ivp.t, sol_ivp.y[0] * 180 / math.pi, 'r-*', label="Displacement Simu [$^\circ$]")
plt.grid()
plt.xlabel('Time [s]', fontweight='bold')
plt.ylabel('Angular Displacement [$^\circ$]', fontweight='bold')
plt.legend()
# plt.ylim([-100, -60])

plt.subplot(212)
plt.plot(time, velocity_filter, 'b-*', label='Velocity [rad/s]')
plt.plot(sol_ivp.t, sol_ivp.y[1], 'r-*', label="Velocity Simu [rad/s]")
plt.xlabel('Time [s]', fontweight='bold')
plt.ylabel('Angular Velocity [rad/s]', fontweight='bold')
plt.grid()
plt.legend()
# plt.ylim([-200, 300])
plt.savefig('./PDF-File/Sim.pdf')
plt.show()
