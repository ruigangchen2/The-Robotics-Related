import math
import numpy as np
import pandas as pd
from sympy import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

inertia = 0.5 * (30.5 * 0.001) * ((6.7 * 0.01) ** 2) * (1 - 2 / 3 * np.sin(np.pi / 8))

def damped_oscillation(t, a, lambda1, omega1, phi1, c1):
    return a * np.exp((-1) * lambda1 * t) * np.sin(omega1 * t + phi1) + c1


data = pd.read_excel("../Data/hairspring_flywheel/135degree.xlsx")

Angle = np.array(list(data.iloc[4:, 4])) * 180 / np.pi
time = np.array(list(data.iloc[4:, 0]))


startline = -300
endline = -220

time = time[startline:endline] - time[startline]
Angle = Angle[startline:endline]
time = time * 0.01

A, B, C, D, E = curve_fit(damped_oscillation, time, Angle)[0]
print("The parameters of previous torsion spring:",
      curve_fit(damped_oscillation, time, Angle)[0])
fitted_angle = A * np.exp((-1) * B * time) * np.sin(C * time + D) + E

Angular_damping_constant = 2 * inertia * B
Torsion_spring_constant = ((C ** 2) + ((Angular_damping_constant/(2*inertia))**2)) * inertia

print("Stiffness is:%.8f N*m*rad−1" % Torsion_spring_constant)

fig, ax1 = plt.subplots(figsize=(10, 8), dpi=100)
ax1.plot(time, Angle, 'b-', label='Experiment')
ax1.plot(time, fitted_angle, 'r--', label='Fitting')
ax1.plot(time, Angle-fitted_angle, 'k-', label='Fitting error')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel(r'$\theta$ [$^\circ$]')
latex = r'$\theta(t) = %.2f\/e^{-%.2f t}\/sin(%.2f t+%.2f) + %.2f$' % (A, B, C, D, E)
plt.title(latex)
ax1.grid()
plt.legend()
plt.subplots_adjust(bottom=0.15)
fig.savefig('../Output/MotionCapture_Flywheel_45degrees.pdf')
plt.show()
