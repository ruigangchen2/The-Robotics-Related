import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

m1 = 190.6 / 1000
m2 = 593.1 / 1000
g = 9.81
length = 216.48 / 1000
max_step = 0.01
dt = 0.01
alpha = 22.5 * np.pi / 180
A = (1 / (np.cos(2 * alpha)) ** 2) - 1
# gamma = np.arcsin(A / (np.sqrt(((2 + A) * np.sin(alpha)) ** 2 + (A * np.cos(alpha)) ** 2))) \
#         - np.arcsin(A * np.cos(alpha) / (np.sqrt(((2 + A) * np.sin(alpha)) ** 2 + (A * np.cos(alpha)) ** 2)))
gamma = 0.12
initial_speed = np.sqrt((2 * (m1 + m2) * g * length * (np.cos(0.087) - np.cos(alpha + gamma))) /
                        ((3 / 2) * m2 * length ** 2 - (1 / 3) * m2 * length ** 2 *
                         (np.sin(22.5 * np.pi / 180)) ** 2 + m1 * length ** 2)) * np.cos(2 * alpha) * 1.1
initial_theta = -(alpha - gamma)


def octagon(_t, y):
    return [y[1], ((m1 + m2) * g * length * np.sin(y[0]))
            / (3 / 2 * m2 * length ** 2 - 1 / 3 * m2 * (length ** 2) *
               ((np.sin(22.5 * np.pi / 180)) ** 2) + m1 * length ** 2)]


def terminate_condition(_t, y):
    return y[0] - (alpha + gamma)


terminate_condition.terminal = True
sol = solve_ivp(octagon,
                [0, 1], [0.077, 0.69],
                max_step=max_step,
                events=terminate_condition)
sol1 = solve_ivp(octagon,
                 [0, 1], [initial_theta, initial_speed],
                 max_step=max_step,
                 events=terminate_condition)
plt.figure(figsize=(8, 6), dpi=100)
data = pd.read_csv("615.csv")
exp_start = 1680
exp_end = 1800
temp = np.array(data['RX'].ravel())
RX = temp[exp_start:exp_end]
temp = np.array(data['TZ'].ravel())
TZ = temp[exp_start:exp_end] / 1000
temp = np.array(data['TY'].ravel())
TY = temp[exp_start:exp_end] / 1000
N = np.size(TZ)
time = np.linspace(0, dt * (N - 1), N)

velocity = [0 for i in range(120)]
for i in range(119):
    velocity[i] = -(RX[i + 1] - RX[i]) / 0.01

plt.subplot(311)
plt.plot(sol.t, sol.y[0] - sol.y[0][0], 'b--', linewidth=2)
plt.plot(sol1.t + sol.t[-1], sol1.y[0] - sol1.y[0][0]
         + (sol.y[0] - sol.y[0][0])[-1] - (sol1.y[0] - sol1.y[0][0])[0], 'b--', linewidth=2, label=r'$\theta_{'
                                                                                                   r'sim}$')
plt.plot(time, -(RX - RX[0]), 'r--', label=r'$\theta_{exp}$')
plt.ylabel(r'Rotation angle [rad]')
plt.grid()
plt.legend()
plt.subplot(312)
plt.plot(sol.t, sol.y[1] - sol.y[1][0], 'b--', linewidth=2)
plt.plot(sol1.t + sol.t[-1], sol1.y[1] - sol1.y[1][0]
         + ((sol.y[1] - sol.y[1][0])[-1] * np.cos(2*alpha) - (sol1.y[1] - sol1.y[1][0])[0]),
         'b--', linewidth=2, label=r'$\ Velocity_{sim}$')
plt.plot(time, velocity, 'r--', linewidth=2, label=r'$\ Velocity_{exp}$')
plt.ylabel(r'Rotation velocity [rad/s]')
plt.grid()
plt.legend()
plt.subplot(313)
plt.plot(sol.t, length * (-np.cos(0.077) + np.cos(sol.y[0])) -
         (length * (-np.cos(0.077) + np.cos(sol.y[0])))[0], 'b--', linewidth=2)
plt.plot(sol1.t + sol.t[-1], length * (-np.cos(0.077) + np.cos(sol1.y[0]))
         + length * (-np.cos(0.077) + np.cos(sol.y[0]))[-1] -
         length * (-np.cos(0.077) + np.cos(sol1.y[0]))[0], 'b--', linewidth=2, label=r'$Z_{sim}$')
plt.plot(time, TZ - TZ[0], 'r--', label=r'$Z_{exp}$')
plt.ylabel('Disp [m]')
plt.grid()
plt.legend()
plt.savefig('octagon simulation.pdf')
plt.show()
