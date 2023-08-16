import numpy as np


theta_start = 70 * np.pi / 180
print("start angle is: %.2f degrees" % (theta_start * 180 / np.pi))

theta_acc = 10 * np.pi / 180  # The acceleration angle
print("acceleration angle is: %f degrees" % (theta_acc * 180 / np.pi))

theta_dec = 20.17 * np.pi / 180  # The deceleration angle
print("deceleration angle is: %f degrees" % (theta_dec * 180 / np.pi))

theta_goal = 90 * np.pi / 180
print("goal angle is: %.2f degrees" % (theta_goal * 180 / np.pi))

g = 9.8
print("gravitational_acceleration is: %f m/s^2" % g)

J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
print("rotation inertia is: %f Kg·m²" % J)

w1 = 5.22
print("omega1 is: %f rad/s" % w1)

w2 = 9.12
print("omega2 is: %f rad/s" % w2)

k1 = J * (w1 ** 2)
print("stiffness1 is: %f N/m" % k1)

k2 = J * (w2 ** 2)
print("stiffness2 is: %f N/m" % k2)

energy_acc = 0.5 * k1 * ((theta_start ** 2) - ((theta_start - theta_acc) ** 2))
print("energy_acc is: %f J" % energy_acc)

energy_dec = 0.5 * k2 * (theta_dec ** 2)
print("energy_dec is: %f J" % energy_dec)

Energy_Saved = energy_dec / energy_acc * 100
print("The Energy_Saved is: %f %%" % Energy_Saved)

COT = (energy_acc - energy_dec) / (J * g * theta_goal)
print("The COT is: %f" % COT)
