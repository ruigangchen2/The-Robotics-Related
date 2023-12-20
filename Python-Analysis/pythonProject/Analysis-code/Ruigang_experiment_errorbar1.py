import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import numpy as np

x = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]) + 90

zero_degree = [-0.9, -1.08, 0.18, -0.72, -0.54, -0.18, -0.54]
five_degree = [5.22, 6.84, 4.86, 6.66, 5.4, 5.94, 6.3]
ten_degree = [9.72, 9.36, 9.18, 9.18, 10.62, 9.36, 11.52]
fifteen_degree = [15.48, 16.38, 13.14, 14.4, 15.12, 16.2, 14.58]
twenty = [19.44, 20.7, 21.06, 21.24, 19.98, 20.7, 20.34]
twentyfive_degree = [26.28, 23.58, 25.92, 25.02, 25.92, 26.82, 25.2]
thirty_degree = [30.96, 30.42, 28.62, 29.52, 28.8, 31.32, 30.96]
thirtyfive_degree = [36, 35.46, 34.2, 34.02, 34.56, 34.56, 35.1]
forty = [40.86, 40.68, 40.86, 39.96, 39.06, 39.78, 40.32]
fortyfive_degree = [44.82, 45.36, 46.26, 45.72, 45.54, 45.72, 44.64]
fifty_degree = [50.04, 50.22, 49.68, 50.76, 50.4, 50.04, 51.48]
fiftyfive_degree = [54.72, 54.72, 56.16, 54.9, 54.18, 56.7, 56.7]
sixty_degree = [60.84, 60.66, 59.58, 60.3, 60.3, 62.46, 59.4]

energy_saved = [95.53, 93.73, 91.96, 90.20, 88.46, 86.65, 84.85, 83.08, 81.23, 79.5, 77.69, 75.91, 74.06]


y = np.array([np.mean(zero_degree), np.mean(five_degree), np.mean(ten_degree),
              np.mean(fifteen_degree), np.mean(twenty), np.mean(twentyfive_degree),
              np.mean(thirty_degree), np.mean(thirtyfive_degree), np.mean(forty),
              np.mean(fortyfive_degree), np.mean(fifty_degree), np.mean(fiftyfive_degree), np.mean(sixty_degree)]) + 90

std_dev = np.array([np.std(zero_degree), np.std(five_degree), np.std(ten_degree),
                    np.std(fifteen_degree), np.std(twenty), np.std(twentyfive_degree),
                    np.std(thirty_degree), np.std(thirtyfive_degree), np.std(forty),
                    np.std(fortyfive_degree), np.std(fifty_degree), np.std(fiftyfive_degree), np.std(sixty_degree)])

error = x - y

plt.figure(figsize=(8, 6), dpi=100)
host = host_subplot(111, axes_class=axisartist.Axes)
plt.subplots_adjust(right=0.8)

par1 = host.twinx()
par2 = host.twinx()

par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(60, 0))
par1.axis["right"].toggle(all=True)
par2.axis["right"].toggle(all=True)

p1, = host.plot(x, x, 'r', label='Ideal Result')
plt.errorbar(x, y, std_dev, marker='o', ecolor='b', color='b', elinewidth=2, capsize=2,
             capthick=1.5, linestyle=':', markersize=2, label='Experimental Result')
p2, = par1.plot(x, error, 'ok--', markersize=5, label="Error Angle")
p3, = par2.plot(x, energy_saved, '*g-.', markersize=6, label='Energy Saved')

plt.xticks(range(90, 155, 5))
plt.yticks(range(90, 155, 5))

par1.set_yticks(range(-6, 7, 1))
par1.set_ylim(-7, 7)
par2.set_yticks(range(70, 102, 2))
par2.set_ylim(70, 100)

host.set_xlabel(r'Target Angle [$^{\circ}$]')
host.set_ylabel(r'Reached Angle [$^{\circ}$]')
par1.set_ylabel(r'Error Angle [$^{\circ}$]')
par2.set_ylabel(r'Saved Energy [%]')
host.legend()
host.grid()

plt.savefig("The Error.pdf")
plt.show()
