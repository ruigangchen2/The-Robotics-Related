import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2


def exp_model(t, a, omega_, phi, zeta):
    return a * np.sin(omega_*t+phi)*np.exp(-zeta * t)


def linear_model(t, x_0, f_, omega_):
    return (x_0-2*f_/np.pi/(inertia * (omega_ ** 2))*omega_*t)*np.cos(omega_*t) + 2*f_/np.pi/(inertia * (omega_ ** 2))*np.sin(omega_*t)


data = pd.read_excel("../Data/20230713_clutch/only_lower_electromagnet_clutch.xlsx")
start_point = 514
end_point = 5453
temp = np.around(np.array(data['Time'].ravel())) * 0.001
time = temp[start_point:end_point] - temp[start_point]
angle = np.around(np.array(data['Degree'].ravel()))[start_point:end_point] * np.pi / 180
[A_, omega_, phi_, zeta_] = curve_fit(exp_model, time, angle)[0]
exp_fit = exp_model(time, A_, omega_, phi_, zeta_)
[x0, F, omega] = curve_fit(linear_model, time, angle, [-1.57079633, 0.0002222461477312496, 5.28])[0]
print("Force is:%f" % F)
linear_fit = linear_model(time, x0, F, omega)

fig = plt.figure(figsize=(5, 4))
ax1 = plt.subplot(211)
ax1.plot(time, angle, 'k', label=r'Data')
ax1.plot(time, exp_fit, 'r--', label=r'Exp. fit')
ax1.plot(time, linear_fit, 'b:', label=r'Lin. fit')
ax1.set_ylabel(r'$\theta$ [rad]')
ax1.get_xaxis().set_visible(False)
ax1.legend(ncol=3)
ax2 = plt.subplot(212)
ax2.plot(time, exp_fit-angle, 'r--', label=r'Exp. fit error')
ax2.plot(time, linear_fit-angle, 'b:', label=r'Lin. fit error')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel(r'$\theta$ [rad]')
ax2.legend(ncol=3)
plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
