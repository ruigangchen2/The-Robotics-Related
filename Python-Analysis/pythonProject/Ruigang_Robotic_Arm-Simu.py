import math
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


data = pd.read_excel("./20230703/data.xlsx")
time = np.around(np.array(data['Time'].ravel()), 2)
angle = np.around(np.array(data['Degree'].ravel()), 2)
velocity = np.around(np.array(data['Velocity'].ravel()) * math.pi / 180, 2)

theta_acceleration = 10 * math.pi / 180
theta_goal = 150 * math.pi / 180
omega = 9.05
interia_magnet = 0.5 * (14.6 * 0.001) * ((15 * 0.001) ** 2)  # 0.5 * M * R^2
interia_plate = 0.5 * (4.5 * 0.001) * ((25 * 0.001) ** 2)  # 0.5 * M * R^2
interia_arm = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)  # 0.5 * M * R^2
interia_total = interia_magnet + interia_plate + interia_arm
stiffness = interia_total * (omega ** 2)  # I * w^2


startline = 515
endline = 595


time = time[startline:endline] - time[startline]
time = time * 0.005
angle = angle[startline:endline]
velocity = velocity[startline:endline]

initial_speed = velocity[0]
initial_theta = angle[0]


def EOM(_t, y):
    return [y[1], 1 * (stiffness * y[0]) / interia_total]

sol_ivp = solve_ivp(EOM, [0, 0.5], [initial_theta, initial_speed], max_step=0.001)

b, a = signal.butter(8, 0.05, 'lowpass')
velocity_filter = signal.filtfilt(b, a, velocity)

plt.figure(figsize=(8, 6), dpi=100)
plt.subplot(211)
plt.plot(time, angle, 'b-*', label=r'Displacement [$^\circ$]')
plt.plot(sol_ivp.t, sol_ivp.y[0], 'r-*', label="Displacement Simu [$^\circ$]")
plt.grid()
plt.xlabel('Time [s]', fontweight='bold')
plt.ylabel('Angular Displacement [$^\circ$]', fontweight='bold')
plt.legend()
plt.ylim([-100, -60])

plt.subplot(212)
plt.plot(time, velocity_filter, 'b-*', label='Velocity [rad/s]')
plt.plot(sol_ivp.t, sol_ivp.y[1] * math.pi / 180, 'r-*', label="Velocity Simu [rad/s]")
plt.xlabel('Time [s]', fontweight='bold')
plt.ylabel('Angular Velocity [rad/s]', fontweight='bold')
plt.grid()
plt.legend()
plt.ylim([-10, 10])
plt.show()
