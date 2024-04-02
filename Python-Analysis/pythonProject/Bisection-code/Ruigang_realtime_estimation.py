import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

inertia = 0.000141407104 * 2
delta_J = 0.000141407104 * 0.5
omega = 5.28 # constant
stiffness = 0.000141407104 * (omega ** 2)  # constant
slope = 0.108 # constant
torque_friction1 = slope * np.pi * stiffness / 2 / omega # constant
# print(torque_friction1)
data = pd.read_excel("../Data/20230712_3.5torqye/1_110degrees.xlsx")
one = 590
two = 60
time = np.array(data['Time'].ravel())[one:-5]*0.001
angle = np.array(data['Degree'].ravel())[one:-5]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-5]*np.pi/180


[b, a] = signal.butter(8, 0.05, 'lowpass')
velocity_filtered = signal.filtfilt(b, a, velocity)

time1 = time[:two]
angle1 = angle[:two]
velocity1 = velocity_filtered[:two]


def eom(_t, y):
    return [y[1],  - (stiffness * (y[0] + angle1[0] * np.pi / 180) - torque_friction1) / inertia]


error = 1
a = 0.000141407104*0.1
b = 0.000141407104*3
inertia = a

plt.figure(figsize=(11, 8))
plt.subplot(211)
plt.plot(time[:two], angle[:two] * 180 / np.pi, 'b-*', label='exp')
while abs(error) > 0.0015:
    inertia = (a+b)/2
    sol = solve_ivp(eom, [time1[0], time1[-1]], [angle1[0], velocity1[0]], t_eval=time1)
    error = np.sum(angle[:two] - sol.y[0])
    if error > 0:
        b = inertia
    else:
        a = inertia
    # print(inertia)
    plt.subplot(211)
    plt.plot(sol.t, sol.y[0] * 180 / np.pi, '-', label=inertia)
    plt.subplot(212)
    plt.plot(sol.t, (angle[:two] - sol.y[0]) * 180 / np.pi, label=inertia)
plt.subplot(211)
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.subplot(212)
plt.plot([sol.t[0], sol.t[-1]], [0, 0], 'k:')
plt.xlabel('Time [s]')
plt.ylabel(r'$\theta_{err}$ [$^\circ$]')
plt.tight_layout()
plt.savefig('Sim.pdf')
plt.show()
