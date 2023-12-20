import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

inertia = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2

omega1 = 5.28
omega2 = 5.45
stiffness1 = inertia * (omega1 ** 2)  # I * w^2
stiffness2 = inertia * (omega2 ** 2)

damp1 = 0.0000405
damp2 = 0.00003780
damp3 = 0.0001869

data = pd.read_excel("./In_paper_data/150degrees.xlsx")
one = 570
two = 55
three = 613
four = 750
time = np.array(data['Time'].ravel())[one:-15]*0.001
angle = np.array(data['Degree'].ravel())[one:-15]*np.pi/180
velocity = np.array(data['Velocity'].ravel())[one:-15]*np.pi/180
time = time - time[0]


[b, a] = signal.butter(8, 0.05, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数

velocity_filtered = signal.filtfilt(b, a, velocity)

time1 = time[:two]
angle1 = angle[:two]
velocity1 = velocity_filtered[:two]
time2 = time[two:three]
angle2 = angle[two+1:three]
velocity2 = velocity_filtered[two+1:three]
time3 = time[three:four]
angle3 = angle[three+1:four]
velocity3 = velocity_filtered[three+1:four]

clutch1 = np.array(data['Electromagnet_Clutch_1'].ravel())[one:-15]
clutch2 = np.array(data['Electromagnet_Clutch_2'].ravel())[one:-15]
clutch3 = np.array(data['Electromagnet_Clutch_3'].ravel())[one:-15]
clutch4 = np.array(data['Electromagnet_Clutch_4'].ravel())[one:-15]




def eom1(_t, y):
    return [y[1],  - (stiffness1 * (y[0] + angle1[0] * np.pi / 180) - damp1 * y[1]) / inertia]


def eom2(_t, y):
    return [y[1], - damp2 * y[1] / inertia]


def eom3(_t, y):
    return [y[1],  - (stiffness2 * y[0] - damp3 * y[1]) / inertia]


sol_ivp1 = solve_ivp(eom1, [time1[0], time1[-1]], [angle1[0], velocity1[0]], max_step=0.001)
sol_ivp2 = solve_ivp(eom2, [time2[0], time2[-1]], [angle2[0], velocity2[0]], max_step=0.001)
sol_ivp3 = solve_ivp(eom3, [time3[0], time3[-1]], [angle3[0], velocity3[0]], max_step=0.001)

plt.figure(figsize=(6, 5), dpi=100)
plt.subplot(411)
plt.plot(time, angle * 180 / np.pi, 'b', label='experimental')
plt.plot(sol_ivp1.t, sol_ivp1.y[0] * 180 / np.pi, 'r--')
plt.plot(sol_ivp2.t, sol_ivp2.y[0] * 180 / np.pi, 'r--')
plt.plot(sol_ivp3.t, sol_ivp3.y[0] * 180 / np.pi, 'r--', label='simulation')
plt.xticks([])
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.ylim([-100, 100])
plt.legend()
plt.subplot(412)
plt.plot(time, velocity, 'k-', alpha=0.4, label='experimental')
plt.plot(time, velocity_filtered, 'b', label='filtered')
plt.plot(sol_ivp1.t, sol_ivp1.y[1], 'r--')
plt.plot(sol_ivp2.t, sol_ivp2.y[1], 'r--')
plt.plot(sol_ivp3.t, sol_ivp3.y[1], 'r--', label='simulation')
plt.plot(time, np.zeros(np.shape(time)), 'k:')
plt.xticks([])
plt.ylabel(r'$\dot{\theta}$ [rad/s]')
plt.legend(ncol=3)
plt.ylim([-0.7, 7.7])
plt.subplot(413)
plt.plot(time, clutch1, 'b-', label=r'$Clutch_{upper1}$')
plt.plot(time, clutch2, 'r--', label=r'$Clutch_{upper2}$')
plt.xticks([])
plt.yticks([0, 1], ['OFF', 'ON'])
plt.legend()
plt.subplot(414)
plt.plot(time, clutch3, 'k-.', label=r'$Clutch_{lower1}$')
plt.plot(time, clutch4, 'c:', label=r'$Clutch_{upper2}$')
plt.xlabel('Time [s]')
plt.yticks([0, 1], ['OFF', 'ON'])
plt.legend()
plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
