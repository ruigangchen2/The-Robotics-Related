import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

data = pd.read_excel("torsion spring Force Displacement3.xlsx")

rotation = list(np.array(data.iloc[0:, 0]) * math.pi / 180)
weight = list((np.array(data.iloc[0:, 1]) - 23.55) * 0.001 * 9.8)


rotation1 = list(np.array(data.iloc[0:6, 2]) * math.pi / 180)
weight1 = list((np.array(data.iloc[0:6, 3]) - 23.55) * 0.001 * 9.8)


order = 2
z = np.polyfit(rotation, weight, order)
p = np.poly1d(z)
weight_fit = p(rotation)

z1 = np.polyfit(rotation1, weight1, order)
p1 = np.poly1d(z1)
weight_fit1 = p1(rotation1)

print(z)
print(z1)


plt.figure(figsize=(6, 4), dpi=100)
plt.plot(rotation, weight, 'b-+', label='original tightening curve')
plt.plot(rotation, weight_fit, 'r-+', label='fitting tightening curve')

plt.plot(rotation1, weight1, 'g-+', label='original releasing curve')
plt.plot(rotation1, weight_fit1, 'k-+', label='fitting releasing curve')

plt.xlabel('Rotation [rad]')
plt.ylabel('Force [N]')

# latex = r'$Tightening: Y(t) = (%.7f) X^{3} + (%.7f) X^{2} + (%.7f) X + (%.7f)$' % (z[0],z[1],z[2],z[3])
# latex1 = r'$Releasing: Y(t) = (%.7f) X^{3} + (%.7f) X^{2} + (%.7f) X + (%.7f)$' % (z1[0],z1[1],z1[2],z1[3])

latex = r'$Tightening: Y(t) = (%.7f) X + (%.7f)$' % (z[0],z[1])
latex1 = r'$Releasing: Y(t) = (%.7f) X + (%.7f)$' % (z1[0],z1[1])
plt.title(latex + '\n' + latex1, size = 'large')


plt.grid()
plt.legend()
plt.savefig('torsion spring Force Displacement.pdf')
plt.show()
