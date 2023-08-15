import matplotlib.pyplot as plt
import numpy as np

x = np.array([40, 45, 50, 55, 60])

a = [40.68,40.86]
b = [45.36,44.82]
c = [50.04,50.76]
d = [54.72,56.16]
e = [60.84,60.66]
y = np.array([np.mean(a), np.mean(b), np.mean(c), np.mean(d), np.mean(e)])

error = np.array([np.std(a), np.std(b), np.std(c), np.std(d), np.std(e)])


plt.figure(figsize=[4, 2.5])
plt.plot(x, x, 'r', label='Ideal Result')
plt.errorbar(x, y, error, marker='o', ecolor='b', color='b', linestyle='--', markersize=2, label='Experimental Result')
plt.xlabel(r'Target angle [$^{\circ}$]')
plt.ylabel(r'Reached angle [$^{\circ}$]')
plt.tight_layout()
plt.legend()
plt.savefig('temp.pdf')
plt.show()

