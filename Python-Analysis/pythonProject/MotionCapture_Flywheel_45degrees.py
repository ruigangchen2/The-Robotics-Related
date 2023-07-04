import math
import numpy as np
import pandas as pd
from sympy import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def damped_oscillation(t, a, lambda1, omega1, phi1, c1):
    return a * np.exp((-1) * lambda1 * t) * np.sin(omega1 * t + phi1) + c1


data = pd.read_excel("./hairspring_flywheel/45degree.xlsx")

Angle = np.array(list(data.iloc[4:, 4]))
Angle = np.around(Angle, 4)
time = np.array(list(data.iloc[4:, 0]))

startline = 1200
endline = 1600

time = time[startline:endline] - time[startline]
Angle = Angle[startline:endline]
time = time * 0.01


A, B, C, D, E = curve_fit(damped_oscillation, time, Angle)[0]
print("The parameters of previous torsion spring:",
      curve_fit(damped_oscillation, time, Angle)[0])
fitted_angle = A * np.exp((-1) * B * time) * np.sin(C * time + D) + E
zeta = Symbol('zeta')
omega = Symbol('omega')
solved_value = solve([zeta * omega - B, omega * ((1 - (zeta*zeta))**0.5) - C],
                     [zeta, omega])
print(solved_value)
zeta = solved_value[0][0]
omega = solved_value[0][1]
frequency = omega / 2 / math.pi
print("Zeta is:%.5f" % zeta)
print("Omega is:%.5f" % omega)
print("Frequency is:%.5f" % frequency)

fig, ax1 = plt.subplots(figsize=(10, 8), dpi=100)
ax1.plot(time, Angle, 'b-', label='Experiment')
ax1.plot(time, fitted_angle, 'r--', label='Fitting')
ax1.plot(time, Angle-fitted_angle, 'k-', label='Fitting error')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel(r'$\theta$ [$rad$]')
latex = r'$\theta(t) = %.2f\/e^{-%.2f t}\/sin(%.2f t+%.2f) + %.2f$' % (A, B, C, D, E)
plt.title(latex)
ax1.grid()
plt.legend()
plt.subplots_adjust(bottom=0.15)
fig.savefig('MotionCapture_Flywheel_45degrees.pdf')
plt.show()

Angle = np.array(list(data.iloc[4:, 4]))
Angle = np.around(Angle, 4)
time = np.array(list(data.iloc[4:, 0]))

startline = 876
endline = None

time = time[startline:endline] - time[startline]
Angle = Angle[startline:endline] * 180 / math.pi
time = time * 0.01

fig, ax1 = plt.subplots(figsize=(10, 8), dpi=100)
ax1.plot(time, Angle, 'b-', label='Experiment')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel(r'$\theta$ [$\circ$]')
plt.ylim(-50, 50)
plt.annotate(r'$\angle %.2f^o$' % np.min(Angle[0:50]), xy=(0, np.min(Angle[0:50])), xytext=(+20, -10),
             textcoords='offset points', fontsize=12, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.min(Angle[50:100]), xy=(0.96, np.min(Angle[50:100])), xytext=(+20, -10),
             textcoords='offset points', fontsize=12, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.min(Angle[190:194]), xy=(1.92, np.min(Angle[190:194])), xytext=(+20, -10),
             textcoords='offset points', fontsize=12, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.max(Angle[0:100]), xy=(0.48, np.max(Angle[0:100])), xytext=(+20, +10),
             textcoords='offset points', fontsize=12, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.max(Angle[100:150]), xy=(1.44, np.max(Angle[100:150])), xytext=(+20, +10),
             textcoords='offset points', fontsize=12, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
ax1.grid()
plt.legend()
plt.subplots_adjust(bottom=0.15)

fig.savefig('MotionCapture_Flywheel_45degrees1.pdf')
plt.show()
