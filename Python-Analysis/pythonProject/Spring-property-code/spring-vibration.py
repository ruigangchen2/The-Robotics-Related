import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import math

data = pd.read_excel("./Data/vertical_free_vibration/vertical_freevibration1.xlsx")

time = np.array(data['Time'].ravel())
time = np.around(time, 2)
angle = np.array(data['Degree'].ravel())
angle = np.around(angle, 2)
velocity = np.array(data['Velocity'].ravel()) * math.pi / 180
velocity = np.around(velocity, 2)

startline = 300
endline = -5

time = time[startline:endline] - time[startline]
time = time * 0.001
angle = angle[startline:endline]
velocity = velocity[startline:endline]

b, a = signal.butter(8, 0.05, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filtedData = signal.filtfilt(b, a, velocity)  # data为要过滤的信号

plt.subplots(figsize=(8, 4), dpi=200)
plt.subplot(211)
plt.plot(time, angle, 'b-')
plt.ylabel(r'$\theta$ [$^\circ$]')
plt.grid()

plt.subplot(212)
plt.plot(time, filtedData, 'r-')
plt.xlabel('Time [s]')
plt.ylabel(r'$\dot{\theta}$ [rad/s]')

plt.grid()
plt.ylim([-80, 80])
plt.ylim([-10, 10])
plt.savefig("./Output/The Filtered.pdf")
plt.show()
