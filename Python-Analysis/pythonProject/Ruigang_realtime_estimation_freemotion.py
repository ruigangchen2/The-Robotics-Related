import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


damp = 0.0000326

data = pd.read_excel("./20230712_1torque/1_150degrees.xlsx")
one = 570
two = 55
three = 613
time = np.array(data['Time'].ravel())[one:-5]*0.001
angle = np.array(data['Degree'].ravel())[one:-5]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-5]*np.pi/180


[b, a] = signal.butter(8, 0.05, 'lowpass')
velocity_filtered = signal.filtfilt(b, a, velocity)

time1 = time[two:three]
angle1 = angle[two:three]
velocity1 = velocity_filtered[two:three]


def eom(_t, y):
    return [y[1], - damp * y[1] / inertia]

error = 1
a = 0.000141407104*0.1
b = 0.000141407104*3

plt.figure(figsize=(11, 8))
plt.subplot(211)
plt.plot(time1, angle1 * 180 / np.pi, 'b-*', label='exp')

while abs(error) > 0.0005:
    inertia = (a+b)/2
    sol = solve_ivp(eom, [time1[0], time1[-1]], [angle1[0], velocity1[0]], t_eval=time1)
    error = np.sum(angle[two:three] - sol.y[0])
    if error > 0:
        a = inertia
    else:
        b = inertia
    print(inertia)
    plt.subplot(211)
    plt.plot(sol.t, sol.y[0] * 180 / np.pi, '-', label=inertia)
    plt.subplot(212)
    plt.plot(sol.t, (angle1 - sol.y[0]) * 180 / np.pi, label=inertia)
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
