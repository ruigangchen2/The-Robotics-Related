import matplotlib.pyplot as plt
import numpy as np

x = np.array([60]) + 90

degree = [58.86, 62.28, 60.12, 59.94, 61.56, 60.3, 61.38]


y = np.array([np.mean(degree)]) + 90

std_dev = np.array([np.std(degree)])

error = x - y

fig, ax1 = plt.subplots(figsize=(8, 6), dpi=100)
ax2 = ax1.twinx()
ax1.plot(150, 150, 'r-*', label='Ideal Result')
ax1.errorbar(x, y, std_dev, marker='o', ecolor='b', color='b',
             elinewidth=2, capsize=2, capthick=1.5,
             linestyle=':', markersize=2, label='Experimental Result')
ax2.plot(x, error, 'g-*', label='Error Angle')
ax1.set_xlabel(r'Target Angle [$^{\circ}$]')
ax1.set_ylabel(r'Reached Angle [$^{\circ}$]')
ax2.set_ylabel(r'Error Angle [$^{\circ}$]')
ax1.grid()
fig.legend()
ax1.set_ylim([140, 160])
ax2.set_ylim([-7, 7])
fig.savefig("./PDF-File/The Error.pdf")
plt.show()
