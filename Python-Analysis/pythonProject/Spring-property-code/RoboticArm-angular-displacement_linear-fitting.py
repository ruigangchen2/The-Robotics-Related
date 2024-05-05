import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def decay_curve(t, k, b):
    return k * t + b


data = pd.read_excel("../Data/20230713_clutch/only_lower_electromagnet_clutch.xlsx")

startline = 510
endline = -1
time = np.around(np.array(data['Time'].ravel()), 2) * 0.001
time = time[startline:endline] - time[startline]
angle = np.around(np.array(data['Degree'].ravel()), 2)[startline:endline] * np.pi / 180


first_maximum_ranage = angle[900:1000]
first_maximum_time = 900 + np.argmax(first_maximum_ranage)
second_maximum_ranage = angle[2000:3000]
second_maximum_time = 2000 + np.argmax(second_maximum_ranage)
third_maximum_ranage = angle[3600:4000]
third_maximum_time = 3600 + np.argmax(third_maximum_ranage)
fourth_maximum_ranage = angle[4000:5500]
fourth_maximum_time = 4000 + np.argmax(fourth_maximum_ranage)
fifth_maximum_ranage = angle[5000:5500]
fifth_maximum_time = 5000 + np.argmax(fifth_maximum_ranage)
sixth_maximum_ranage = angle[5800:6000]
sixth_maximum_time = 5800 + np.argmax(sixth_maximum_ranage)
decay_angle = [np.max(first_maximum_ranage), np.max(second_maximum_ranage), np.max(third_maximum_ranage),
               np.max(fourth_maximum_ranage), np.max(fifth_maximum_ranage), np.max(sixth_maximum_ranage)]
decay_time = [time[first_maximum_time], time[second_maximum_time], time[third_maximum_time],
              time[fourth_maximum_time], time[fifth_maximum_time], time[sixth_maximum_time]]
A, B = curve_fit(decay_curve, decay_time, decay_angle)[0]
print("The parameters of previous torsion spring:", curve_fit(decay_curve, decay_time, decay_angle)[0])
fitted_angle = A * time + B
print(A)
print(B)
fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax1.plot(time, angle, 'k--', label=r'$\theta_{exp}$ [rad]')
ax1.plot(time, fitted_angle, 'r--', label=r'$\theta_{fit}$ [rad]')

plt.annotate(r'$\angle %.2f\ rad$' % np.max(first_maximum_ranage), xy=(time[first_maximum_time], np.max(first_maximum_ranage)), xytext=(+20, 0),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f\ rad$' % np.max(second_maximum_ranage), xy=(time[second_maximum_time], np.max(second_maximum_ranage)), xytext=(+20, 0),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f\ rad$' % np.max(third_maximum_ranage), xy=(time[third_maximum_time], np.max(third_maximum_ranage)), xytext=(+20, 0),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f\ rad$' % np.max(fourth_maximum_ranage), xy=(time[fourth_maximum_time], np.max(fourth_maximum_ranage)), xytext=(+20, 0),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f\ rad$' % np.max(fifth_maximum_ranage), xy=(time[fifth_maximum_time], np.max(fifth_maximum_ranage)), xytext=(+20, 0),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
plt.annotate(r'$\angle %.2f\ rad$' % np.max(sixth_maximum_ranage), xy=(time[sixth_maximum_time], np.max(sixth_maximum_ranage)), xytext=(+20, 0),
             textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
ax1.set_xlabel('Time [s]', fontweight='bold')
ax1.set_ylabel('Angle [rad]', fontweight='bold')
ax1.grid()
plt.legend()
# ax1.set_ylim([-100, 100])
plt.savefig('figure.pdf')
plt.show()
