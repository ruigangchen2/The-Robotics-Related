import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy import signal


inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
omega1 = 5.28
omega2 = 5.22
stiffness1 = inertia * omega1 ** 2  # I * w^2
stiffness2 = inertia * omega2 ** 2
slope1 = 0.108
slope2 = 0.163
torque_friction1 = slope1 * np.pi * stiffness1 / 2 / omega1
torque_friction2 = slope2 * np.pi * stiffness2 / 2 / omega2

data = pd.read_excel("./20230703/data.xlsx")

startline1 = 515
endline1 = 580
temp1 = np.around(np.array(data['Time'].ravel()), 2)
time1 = (temp1[startline1:endline1] - temp1[startline1]) * 0.001
angle1 = np.around(np.array(data['Degree'].ravel()) * np.pi / 180, 2)[startline1:endline1]
velocity1 = np.around(np.array(data['Velocity'].ravel()) * np.pi / 180, 2)[startline1:endline1]

startline2 = 651
endline2 = 1130
temp2 = np.around(np.array(data['Time'].ravel()), 2)
time2 = (temp2[startline2:endline2] - temp2[startline2]) * 0.001
angle2 = np.around(np.array(data['Degree'].ravel()) * np.pi / 180, 2)[startline2:endline2]
velocity2 = np.around(np.array(data['Velocity'].ravel()) * np.pi / 180, 2)[startline2:endline2]

startline3 = 1200
endline3 = 1295
temp3 = np.around(np.array(data['Time'].ravel()), 2)
time3 = (temp3[startline3:endline3] - temp3[startline3]) * 0.001
angle3 = np.around(np.array(data['Degree'].ravel()) * np.pi / 180, 2)[startline3:endline3]
velocity3 = np.around(np.array(data['Velocity'].ravel()) * np.pi / 180, 2)[startline3:endline3]

time = np.append(time1, time2 + time1[-1])
time_ = np.append(time, time3 + time[-1])

angle = np.append(angle1, angle2)
angle_ = np.append(angle, angle3)

velocity = np.append(velocity1, velocity2)
velocity_ = np.append(velocity, velocity3)

def eom1(_t, y):
    return [y[1], - stiffness1 / inertia * y[0]]

def eom2(_t, y):
    return [y[1], - torque_friction1 / inertia]

def eom3(_t, y):
    return [y[1], - stiffness2 / inertia * y[0]]

sol_ivp1 = solve_ivp(eom1, [0, 0.09], [angle1[0], velocity1[0]], max_step=0.001)
sol_ivp2 = solve_ivp(eom2, [0, 0.38], [angle2[0], velocity2[0]], max_step=0.001)
sol_ivp3 = solve_ivp(eom3, [0, 0.15], [angle3[0], velocity3[0]], max_step=0.001)


y_list = []
def y(t):
    for i in t:
        if i >= 0 and i <= time1[-1]:
            y_list = np.append(0, sol_ivp1.y[0] * 180 / np.pi)
        elif i > time1[-1] and i <= time[-1]:
            y_list = np.append(y_list, sol_ivp2.y[0] * 180 / np.pi)
        elif i > time[-1]:
            y_list = np.append(y_list, sol_ivp3.y[0] * 180 / np.pi)
y(time_)

order = 15
z = np.polyfit(time1, velocity1, order)
p = np.poly1d(z)
velocity_fit1 = p(time1)

z = np.polyfit(time2, velocity2, order)
p = np.poly1d(z)
velocity_fit2 = p(time2)

z = np.polyfit(time3, velocity3, order)
p = np.poly1d(z)
velocity_fit3 = p(time3)

plt.figure(figsize=(6, 5), dpi=100)
plt.subplot(211)
plt.plot(time_, angle_ * 180 / np.pi, 'b-+', label=r'$\theta_{exp}$')
plt.plot(time, y_list, 'r-*', label=r"$\theta_{Simu}$")
plt.grid()
plt.xlabel('Time [s]')
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.legend()
# plt.subplot(212)
# plt.plot(time, velocity_fit, 'b-*', label=r'$\dot{\theta}_{exp}$')
# plt.plot(sol_ivp.t, sol_ivp.y[1], 'r-*', label=r"$\dot{\theta}_{simu}$")
# plt.xlabel('Time [s]')
# plt.ylabel('Velocity [rad/s]')
# plt.grid()
# plt.legend()
# plt.tight_layout()
# plt.ylim([3, 7])
plt.savefig('Sim.pdf')
plt.show()
