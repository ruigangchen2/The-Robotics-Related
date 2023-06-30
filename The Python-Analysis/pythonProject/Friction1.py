import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_excel("torsion spring Force Displacement1.xlsx")

rotation = list(data.iloc[0:, 0])  # convert to second
weight = list(data.iloc[0:, 1])

rotation1 = list(data.iloc[0:5, 2])  # convert to second
weight1 = list(data.iloc[0:5, 3])

print(rotation1)
order = 3
z = np.polyfit(rotation, weight, order)
p = np.poly1d(z)
weight_fit = p(rotation)

z1 = np.polyfit(rotation1, weight1, order)
p1 = np.poly1d(z1)
weight_fit1 = p(rotation1)

plt.figure(figsize=(6, 4), dpi=100)
plt.plot(rotation, weight, 'b-+', label='original curve')
plt.plot(rotation, weight_fit, 'r-+', label='fitting curve')
plt.plot(rotation1, weight1, 'b-+', label='original curve')
plt.plot(rotation1, weight_fit1, 'r-+', label='fitting curve')
plt.xlabel('Rotation [degree]')
plt.ylabel('Wight [g]')
plt.grid()
plt.legend()
plt.savefig('torsion spring Force Displacement.pdf')
plt.show()
