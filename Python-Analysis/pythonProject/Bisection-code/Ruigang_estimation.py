import matplotlib.pyplot as plt
import numpy as np
data = np.array([0.5000005000, 0.5000005000, 0.2500007500, 0.1250008750 ,0.0625009375, 0.0312509687,
                 0.0156259844, 0.0078134922, 0.0039072461, 0.0019541230, 0.0009775615, 0.0004892808,
                 0.0002451404, 0.0003672106, 0.0003061755, 0.0002756579, 0.0002909167, 0.0002985461,
                 0.0002947314, 0.0002966387, 0.0002956851, 0.0002952082, 0.0002954467, 0.0002955659,
                 0.0002956255, 0.0002955957, 0.0002955808, 0.0002955882, 0.0002955919, 0.0002955901])



N = len(data)

plt.figure(figsize=[5, 3])
plt.subplot(211)
plt.plot(np.linspace(1, N, N), data, 'b-*', label='Estimation')
plt.plot(np.linspace(1, N, N), 0.000289771348*np.ones(np.size(data)), 'r--', label='Ground truth')
plt.ylabel(r'J [$kg m^2$]')
plt.ylim([-0.06, 0.55])
plt.legend()
plt.subplot(212)
plt.plot(np.linspace(1, N, N), np.log10(np.abs(data-0.000289771348)), 'b-*')
plt.xlabel('Iterations')
plt.ylabel(r'$log_{10} |Error|$')
plt.ylim([-7, 0.5])
plt.tight_layout()
plt.show()
plt.savefig('temp.pdf')
