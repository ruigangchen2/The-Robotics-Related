import numpy as np
from scipy.optimize import root


k = 0.00394
theta_start = 70 * np.pi / 180
theta_target = 60 * np.pi / 180
J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
friction1 = 0.000222
friction2 = 0.000133
friction3 = 0.000222
time = 0.5


def equations(x):  # disengage:x[0]; engage:x[1]
    omega2 = (((k*((theta_target-x[1])**2)+2*friction3*(theta_target-x[1]))/J)**0.5)
    omega1 = (((k*(theta_start**2-x[0]**2)-2*friction1*(theta_start-x[0]))/J)**0.5)
    return [0.5*k*(theta_start**2-x[0]**2)-0.5*k*((theta_target-x[1])**2)-friction3*(theta_target-x[1])-friction2*(x[0]+x[1])-friction1*(theta_start-x[0]),
            2*(theta_start-x[0])/omega1+2*(x[0]+x[1])/(omega1+omega2)+2*(theta_target-x[0])/omega2-time]


print(root(equations, [0, 0.01]).x * 180 / np.pi)
