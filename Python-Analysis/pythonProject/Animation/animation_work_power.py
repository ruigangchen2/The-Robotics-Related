import imageio
import numpy as np
import matplotlib.pyplot as plt

N = 500
dt = 1/N

x_matrix = []
y1_matrix = []
y_matrix = []
frames = []

for i in range(N+1):
    x_matrix = np.append(x_matrix, 0.1*i)

    plt.subplots(figsize=(8, 4), dpi=200)
    plt.clf()
    plt.subplot(211)
    plt.title(f'Time = {round(i*0.1,1)} s', fontsize=12)
    plt.ylabel('Energy [J]', fontsize=12)
    plt.grid()
    y1_matrix = np.append(y1_matrix, (0.01 / 3 * ((0.1* i) ** 3)))
    plt.plot(x_matrix, y1_matrix, 'b-')
    plt.ylim([0, 500])
    plt.xlim([0, 50])

    plt.subplot(212)
    plt.ylabel('Power [W]', fontsize=12)
    plt.xlabel('time [s]', fontsize=12)
    plt.grid()
    y_matrix = np.append(y_matrix, (0.01*((0.1*i)**2)))
    plt.plot(x_matrix, y_matrix, 'r-')
    plt.ylim([0, 40])
    plt.xlim([0, 50])

    plt.savefig(f'./img_work_energy/img_{i}.png', transparent=False, facecolor='white')
    image = imageio.v2.imread(f'./img_work_energy/img_{i}.png')
    frames.append(image)
    plt.close()

imageio.mimsave('./img_work_energy/example.gif', frames, duration=20, loop=0)