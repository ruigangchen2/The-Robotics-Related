import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy

Positive_Angular_Displacement = np.array([55.44,106.8,118.8,121.68])
Negative_Angular_Displacement = np.array([48.48,66.24,78.48,87.2])
Acceleration_Displacement = np.array([2,6,10,14])


fig, ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax1.plot(Acceleration_Displacement, Positive_Angular_Displacement, 'b-+', label = 'Rotating Anticlockwise to Store Energy')
ax1.plot(Acceleration_Displacement, Negative_Angular_Displacement, 'r-+', label = 'Rotating Clockwise to Store Energy')
ax1.set_xlabel('Acceleration Angle [degree]', fontweight ='bold')
ax1.set_ylabel('Final Arrival Position [degree]',fontweight ='bold')
ax1.grid()
plt.title("Relationship between Acceleration Angle and Final Arrival Position")
plt.legend()
plt.show()