import matplotlib.pyplot as plt
import numpy as np
data = np.array([0.5000005000, 0.2500007500, 0.1250008750, 0.0625009375, 0.0312509687, 0.0156259844, 0.0078134922,
                 0.0039072461, 0.0019541230, 0.0009775615, 0.0004892808, 0.0002451404, 0.0001230702, 0.0001841053,
                 0.0001535877, 0.0001383290, 0.0001459584, 0.0001421437, 0.0001440510, 0.0001430973, 0.0001426205,
                 0.0001428589, 0.0001427397, 0.0001427993])

time = np.array([0.362000, 0.445000, 0.462000, 0.476000, 0.490000, 0.514000, 0.531000,
                 0.547000, 0.563000, 0.580000, 0.594000, 0.614000, 0.630000, 0.646000,
                 0.661000, 0.676000, 0.695000, 0.711000, 0.730000, 0.744000, 0.757000,
                 0.770000, 0.783000, 0.803000])

plt.figure(figsize=[5, 3])
plt.subplot(211)
plt.plot(time, data, 'b-*', label='Estimation')
plt.plot(time, 0.000141407104*np.ones(np.size(data)), 'r--', label='Ground truth')
plt.ylabel(r'J [$kg m^2$]')
plt.ylim([-0.06, 0.55])
plt.legend()
plt.subplot(212)
plt.plot(time, np.log10(np.abs(data-0.000141407104)), 'b-*')
plt.xlabel('time [ms]')
plt.ylabel(r'$log_{10} |Error|$')
plt.ylim([-7, 0.5])
plt.tight_layout()
plt.savefig('temp.pdf')
plt.show()
