import numpy as np

# inertia = 1/3 * m1 * R^2 + m2 * (1/2 * r^2 + d^2)
J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((0.5 * ((3.0 * 0.001) ** 2)) + (110 * 0.001) ** 2) + (18.9 * 0.001) * ((0.5 * ((20.0 * 0.001) ** 2)) + (88.6 * 0.001) ** 2)
print("calibration rotation inertia is: %.8f Kg·m²" % J)

w1 = 5.6
w2 = 7.4
print("omega1 is: %f rad/s" % w1)
print("omega2 is: %f rad/s" % w2)

k1 = J * (w1 ** 2)
k2 = J * (w2 ** 2)
print("stiffness1 is: %f N/m" % k1)
print("stiffness2 is: %f N/m" % k2)

slope1 = 0.108
slope2 = 0.182
F1 = slope1 * np.pi * k1 / 2 / w1
F2 = 0.962 * J
F3 = slope2 * np.pi * k2 / 2 / w2
print("t1 is:%f N" % F1)
print("t2 is:%f N" % F2)
print("t3 is:%f N" % F3)

theta_relock = -((F2 - F1 - (k1 * (13 * np.pi / 18))) / k1) - \
               (((k2 * ((np.pi / 9) ** 2) - ((k1 * ((13 * np.pi / 18) ** 2)) - (k1 * ((np.pi / 3) ** 2)) + (F1 * (7 * np.pi / 9)) + (F2 * (4 * np.pi / 9)) + (F3 * (2 * np.pi / 9)))) / k1) + (((F2 - F1 - (k1 * (13 * np.pi / 18))) / k1) ** 2)) ** 0.5

print("clutching theta is: %.2f degrees" % (theta_relock * 180 / np.pi))
