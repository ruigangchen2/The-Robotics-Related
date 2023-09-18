import numpy as np

# J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
#           + (5.5 * 0.001) * ((110 * 0.001) ** 2)
J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2) + (5.5 * 0.001) * ((110 * 0.001) ** 2) + (18.9 * 0.001) * ((88.6 * 0.001) ** 2)
print("rotation inertia is: %.8f Kg·m²" % J)

w1 = 5.22
w2 = 7.8
print("omega1 is: %f rad/s" % w1)
print("omega2 is: %f rad/s" % w2)

k1 = J * (w1 ** 2)
k2 = J * (w2 ** 2)
print("stiffness1 is: %f N/m" % k1)
print("stiffness2 is: %f N/m" % k2)

theta_start = 70 * np.pi / 180
print("start angle is: %.2f degrees" % (theta_start * 180 / np.pi))

theta_goal = 60
theta_goal = (theta_goal + 90) * np.pi / 180
print("goal angle is: %.2f degrees" % (theta_goal * 180 / np.pi))

theta_acc = 10 * np.pi / 180
print("acceleration angle is: %.2f degrees" % (theta_acc * 180 / np.pi))

slope1 = 0.108
slope2 = 0.182
t1 = slope1 * np.pi * k1 / 2 / w1
t3 = slope2 * np.pi * k2 / 2 / w2
t2 = 0.962 * J

theta_clutch = (- (t3 + t2 - k2 * theta_goal) / k2) - \
               ((((0.5 * k1 * (2 * theta_start * theta_acc - (theta_acc ** 2)) \
                 - t1 * theta_acc \
                 + t3 * theta_goal \
                 + t2 * theta_acc \
                 - 0.5 * k2 * (theta_goal ** 2)) \
                 / (0.5 * k2)) \
                 + (((t3 + t2 - k2 * theta_goal) / k2) ** 2))
                ** 0.5)

print("clutching theta is: %.2f degrees" % (theta_clutch * 180 / np.pi - 90))