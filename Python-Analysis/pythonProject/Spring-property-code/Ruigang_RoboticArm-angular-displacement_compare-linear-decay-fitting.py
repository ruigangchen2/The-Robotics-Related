import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def exp_model(t, A, omega, phi, zeta):
    return A * np.sin(omega*t+phi)*np.exp(-zeta * t)


def linear_model(t, x0, F, k, omega):
    return (x0-F/2/k*omega*t)*np.cos(omega*t)


data = pd.read_excel("../Data/20230713_clutch/only_lower_electromagnet_clutch.xlsx")
start_point = 510
end_point = 5453  # -1  # 5453
temp = np.around(np.array(data['Time'].ravel()), 2) * 0.001
time = temp[start_point:end_point] - temp[start_point]
angle = np.around(np.array(data['Degree'].ravel()), 2)[start_point:end_point]

[A_, omega_, phi_, zeta_] = curve_fit(exp_model, time, angle)[0]
exp_fit = exp_model(time, A_, omega_, phi_, zeta_)
[x0, F, k, omega] = curve_fit(linear_model, time, angle)[0]
linear_fit = linear_model(time,x0, F, k, omega)
print(F)
plt.subplots(figsize=(8.2, 2))
plt.subplot(121)
plt.plot(time, angle, 'k', label=r'Data')
plt.plot(time, exp_fit, 'r--', label=r'Exp. fit')
plt.plot(time, linear_fit, 'b:', label=r'Lin. fit')
plt.xlabel('Time [s]')
plt.ylabel(r'$\theta$ [$^{\circ}$]')
plt.legend(ncol=3)
plt.ylim([-160, 85])
plt.subplot(122)
plt.plot(time, exp_fit-angle, 'r--', label=r'Exp. fit error')
plt.plot(time, linear_fit-angle, 'b:', label=r'Lin. fit error')
plt.xlabel('Time [s]')
plt.legend(ncol=3)
plt.ylim([-3.5, 6])
plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
