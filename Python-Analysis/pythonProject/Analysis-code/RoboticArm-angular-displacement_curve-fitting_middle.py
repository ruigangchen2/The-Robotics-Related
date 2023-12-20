import math
import numpy as np
import pandas as pd
from sympy import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2

data = pd.read_excel("./Data/middle_freemotion/data.xlsx")

angle = (np.array(list(data.iloc[0:, 1]))) * math.pi / 180
velocity = np.array(list(data.iloc[0:, 2])) * math.pi / 180
time = np.array(list(data.iloc[0:, 0]))

startline = 300
endline = 500

time = time[startline:endline] - time[startline]
velocity = velocity[startline:endline]
angle = angle[startline:endline]
time = time * 0.001

def damped_oscillation(t, a, c):
    return velocity[0] * t + 0.5 * a * t * t + c

A, B = curve_fit(damped_oscillation, time, angle, maxfev = 50000)[0]
fitted_angle = velocity[0] * time + 0.5 * A * time * time + B

print("The acceleration is: %.8f" % A)
print("The beta is: %.8f" % B)
damp = A * inertia / np.mean(velocity)
print("The damp is: %.8f" % damp)

fig, ax1 = plt.subplots(figsize=(10, 8), dpi=100)
ax1.plot(time, angle, 'b-', label='Experiment')
ax1.plot(time, fitted_angle, 'r--', label='Fitting')
ax1.plot(time, angle-fitted_angle, 'k-', label='Fitting error')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel(r'$\theta$ [rad]')
ax1.grid()
plt.legend()
plt.subplots_adjust(bottom=0.15)
fig.savefig('curve-fitting.pdf')
plt.show()
