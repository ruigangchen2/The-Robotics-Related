import imageio
import numpy as np
import matplotlib.pyplot as plt

beta = 2
length = 1
N = 50
t_end = 1
t = np.linspace(0, t_end, N+1)
dt = 1/N
phi1 = (30*np.sin(t*2*np.pi+np.arcsin(0.3))+90)*np.pi/180
phi2 = (30*np.sin(t*2*np.pi-np.arcsin(0.3))+90)*np.pi/180
theta = np.arctan((np.sin(phi1)-np.sin(phi2))/(np.cos(phi1)
                                               + np.cos(phi2)-beta))
d = length*(beta*np.cos(theta)-np.cos(phi1-theta)-np.cos(phi2+theta))


frames = []
for i in range(N+1):
    plt.figure(figsize=(4, 4), dpi=300)
    x0 = np.cos(np.pi - (phi1[i] - theta[i])) \
         + (13 < i < 38) * (d[13] - d[i])
    y0 = np.sin(np.pi-(phi1[i]-theta[i]))
    plt.plot([0 + (13 < i < 38) * (d[13] - d[i]), x0],
             [0, y0], 'r-*')
    x1 = x0 + beta*np.cos(theta[i])
    y1 = y0 + beta*np.sin(theta[i])
    plt.plot([x0, x1], [y0, y1], 'r-*')
    x2 = x1 + np.cos(theta[i]+np.pi+phi2[i])
    y2 = y1 + np.sin(theta[i]+np.pi+phi2[i])
    plt.plot([x1, x2], [y1, y2], 'r-*')
    plt.plot([-1.5, 3.5], [0, 0], 'k:')
    plt.xlabel('x [m]', fontsize=8)
    plt.ylabel('y [m]', fontsize=8)
    plt.axis('equal')
    plt.xlim([-2, 4])
    plt.ylim([-0.1, 1.7])
    plt.title(f'Time = {round(i*dt,1)} s', fontsize=8)
    plt.savefig(f'./img/img_{i}.png', transparent=False, facecolor='white')
    image = imageio.v2.imread(f'./img/img_{i}.png')
    frames.append(image)
    # plt.pause(0.1)
    plt.close()

imageio.mimsave('./img/example.gif', frames, fps=int(1/dt), loop=0)
# imageio.mimsave('./example.gif', frames, duration=20, loop=0)