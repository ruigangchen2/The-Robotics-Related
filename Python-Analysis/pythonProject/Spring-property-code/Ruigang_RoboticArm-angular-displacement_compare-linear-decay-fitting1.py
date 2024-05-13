import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
def exp_model(t, A, omega, phi, zeta):
    return A * np.sin(omega*t+phi)*np.exp(-zeta * t)


def linear_model(t, x0, F, omega):
    return (x0-2*F/np.pi/(inertia * (omega ** 2))*omega*t)*np.cos(omega*t) + 2*F/np.pi/(inertia * (omega ** 2))*np.sin(omega*t)


data = pd.read_excel("../Data/20230713_clutch/only_lower_electromagnet_clutch.xlsx")
start_point = 514
end_point = 5453
temp = np.around(np.array(data['Time'].ravel())) * 0.001
time = temp[start_point:end_point] - temp[start_point]
angle = np.around(np.array(data['Degree'].ravel()))[start_point:end_point] * np.pi / 180
[A_, omega_, phi_, zeta_] = curve_fit(exp_model, time, angle)[0]
exp_fit = exp_model(time, A_, omega_, phi_, zeta_)
[x0, F, omega] = curve_fit(linear_model, time, angle, [-1.57079633,0.0002222461477312496,5.28])[0]
print("Force is:%f" % F)
print("omega is:%f" % omega)
linear_fit = linear_model(time,x0, F, omega)
line = -2*F/np.pi/(inertia * (omega ** 2))*omega*time + x0
plt.subplots(figsize=(8.2, 2))
plt.subplot(121)
plt.plot(time, angle, 'k', label=r'Data')
plt.plot(time, exp_fit, 'r--', label=r'Exp. fit')
plt.plot(time, linear_fit, 'b:', label=r'Lin. fit')
plt.plot(time, line, 'b:', label=r'line')
plt.xlabel('Time [s]')
plt.ylabel(r'$\theta$ [rad]')
plt.legend(ncol=3)
plt.subplot(122)
plt.plot(time, exp_fit-angle, 'r--', label=r'Exp. fit error')
plt.plot(time, linear_fit-angle, 'b:', label=r'Lin. fit error')
plt.xlabel('Time [s]')
plt.legend(ncol=3)
plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
