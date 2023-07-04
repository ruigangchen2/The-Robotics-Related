import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
from scipy.optimize import curve_fit
from sympy import *

def damped_oscillation(t, A, Lambda, Omega, Phi, C):
    return A * np.exp((-1) * Lambda * t) * np.sin(Omega * t + Phi) + C

data = pd.read_excel("./MotionCapture_Pendulum1.xlsx")

TX = np.array(list(data.iloc[4:, 5]))
TX = np.around(TX,2)
time = np.array(list(data.iloc[4:, 0]))

startline = 734
endline = None

time = time[startline:endline] - time[startline]
TX = TX[startline:endline] + 186.7
time = time * 0.01
Degree = np.array([0 for i in range(len(TX))])
Degree = np.arcsin(TX * 0.001 / 0.445) * 180 / math.pi


A, B, C, D, E = curve_fit(damped_oscillation, time, Degree)[0]
print("The parameters of previous torsion spring:",curve_fit(damped_oscillation, time, Degree)[0])
fitted_angle = A * np.exp((-1) * B * time) * np.sin(C * time + D) + E
zeta = Symbol('zeta')
omega = Symbol('omega')
solved_value=solve([zeta * omega - B, omega * ((1 - (zeta*zeta))**0.5) - C], [zeta, omega])
print(solved_value)
zeta = solved_value[0][0]
omega = solved_value[0][1]
frequency = omega / 2 / math.pi


fig ,ax1 = plt.subplots(figsize=(12, 8), dpi=200)
ax1.plot(time, Degree, 'r--', label='Angular Displacement [degree]')
ax1.set_xlabel('Time [s]', fontweight ='bold')
ax1.set_ylabel('Angular Displacement [degree]',fontweight ='bold')
plt.ylim(-25,25)


plt.annotate(r'$\angle %.2f^o$' % np.max(Degree[100:200]),xy=(1.3,np.max(Degree[100:200])),xytext=(+20,+20),textcoords='offset points',fontsize=12,
             arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.max(Degree[0:5]),xy=(0,np.max(Degree[0:5])),xytext=(+20,+20),textcoords='offset points',fontsize=12,
             arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.min(Degree[0:100]),xy=(0.64,np.min(Degree[0:100])),xytext=(-20,-20),textcoords='offset points',fontsize=12,
             arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f^o$' % np.min(Degree[180:220]),xy=(1.97,np.min(Degree[180:220])),xytext=(-20,-20),textcoords='offset points',fontsize=12,
             arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.2'))

latex = r'$s(t) = \mathcal{A}\/e^{-\lambda t}\/sin(\omega t + \Phi) +\mathcal{C} \/ (\mathcal{A}:%.2f,\lambda:%.2f,\omega:%.2f,\Phi:%.2f,\mathcal{C}:%.2f)$' % (A,B,C,D,E)
plt.title(latex, size = 'large')

plt.text(4,-17,'The zeta is: %.3f' % zeta, fontsize=15)
plt.text(4,-19,'The omega is: %.3f' % omega, fontsize=15)
plt.text(4,-21,'The frequency is: %.3f' % frequency, fontsize=15)

ax1.grid()
fig.legend()
fig.savefig('The Angular Displacement.pdf')
plt.show()


