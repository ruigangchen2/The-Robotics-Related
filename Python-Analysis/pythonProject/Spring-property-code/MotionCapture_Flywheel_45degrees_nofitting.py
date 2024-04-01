import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

data = pd.read_excel("../Data/hairspring_flywheel/135degree.xlsx")

Angle = np.array(list(data.iloc[4:, 4])) * 180 / np.pi
time = np.array(list(data.iloc[4:, 0]))

startline = 830
endline = -1

time = time[startline:endline] - time[startline]
Angle = Angle[startline:endline]
time = time * 0.01

fig, ax1 = plt.subplots(figsize=(10, 6), dpi=100)
ax1.plot(time, Angle, 'b-', label='Experiment')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel(r'$\theta$ [$^\circ$]')
ax1.grid()
plt.legend()
plt.subplots_adjust(bottom=0.15)
fig.savefig('../Output/MotionCapture_Flywheel_45degrees.pdf')
plt.show()
