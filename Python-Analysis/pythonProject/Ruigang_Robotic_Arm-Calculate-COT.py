import numpy as np

# You should need to fill in this variable
theta_dec = 30 * np.pi / 180  # The deceleration angle
theta_acc = 10 * np.pi / 180  # The acceleration angle
theta = 137 * np.pi / 180  # The final theta the robotic arm rotates

print("acceleration angle is: %f degrees" % (theta_acc * 180 / np.pi))
print("deceleration angle is: %f degrees" % (theta_dec * 180 / np.pi))
g = 9.8
print("gravitational_acceleration is: %f m/s^2" % g)
J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
print("rotation inertia is: %f Kg·m²" % J)
w1 = 5.22
w2 = 5.72

print("omega1 is: %f rad/s" % w1)
print("omega2 is: %f rad/s" % w2)
k1 = J * (w1 ** 2)
k2 = J * (w2 ** 2)
print("stiffness1 is: %f N/m" % k1)
print("stiffness2 is: %f N/m" % k2)

energy_acc = 0.5 * k1 * (np.pi * theta_acc - (theta_acc ** 2))
energy_dec = 0.5 * k2 * (theta_dec ** 2)
print("energy_acc is: %f J" % energy_acc)
print("energy_dec is: %f J" % energy_dec)

COT = (energy_acc - energy_dec) / (J * g * theta)
print("The COT is: %f" % COT)
