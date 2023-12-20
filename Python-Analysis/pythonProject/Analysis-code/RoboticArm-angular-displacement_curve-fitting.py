import math
import numpy as np
import pandas as pd
from sympy import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2

def damped_oscillation(t, a, lambda1, omega1, phi1, c1):
    return a * np.exp((-1) * lambda1 * t) * np.sin(omega1 * t + phi1) + c1

data = pd.read_excel("./hairspring_flywheel/45degree.xlsx")

angle = (np.array(list(data.iloc[0:, 1]))) * math.pi / 180
velocity = np.array(list(data.iloc[0:, 2])) * math.pi / 180
time = np.array(list(data.iloc[0:, 0]))


startline = 300
endline = 6000

time = time[startline:endline] - time[startline]
velocity = velocity[startline:endline]
angle = angle[startline:endline]
time = time * 0.001

A, B, C, D, E = curve_fit(damped_oscillation, time, angle, maxfev = 50000)[0]
fitted_angle = A * np.exp((-1) * B * time) * np.sin(C * time + D) + E
zeta = Symbol('zeta')
omega = Symbol('omega')
solved_value = solve([zeta * omega - B, omega * ((1 - (zeta*zeta))**0.5) - C],
                     [zeta, omega])

zeta = solved_value[0][0]
omega = solved_value[0][1]
frequency = omega / 2 / np.pi
stiffness = inertia * (omega ** 2)
Damp = (2 * zeta * ((inertia * stiffness)**0.5))
print("Zeta is: %.5f" % zeta)
print("Omega is: %.5f" % omega)
print("Frequency is: %.5f" % frequency)
print("Damp is: %.5f" % Damp)
print("EOM is: F(t) = %.7f * X2 + %.7f * X1 + %.7f * X" % (inertia, Damp, stiffness))

fig, ax1 = plt.subplots(figsize=(10, 8), dpi=100)
ax1.plot(time, angle, 'b-', label='Experiment')
ax1.plot(time, fitted_angle, 'r--', label='Fitting')
ax1.plot(time, angle-fitted_angle, 'k-', label='Fitting error')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel(r'$\theta$ [rad]')
latex = r'$\theta(t) = %.2f\/e^{-%.2f t}\/sin(%.2f t+%.2f) + %.2f$' % (A, B, C, D, E)
plt.title(latex)
ax1.grid()
plt.legend()
plt.subplots_adjust(bottom=0.15)
fig.savefig('./PDF-File/curve-fitting.pdf')
plt.show()
