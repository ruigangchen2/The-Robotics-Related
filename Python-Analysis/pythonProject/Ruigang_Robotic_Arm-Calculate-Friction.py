import numpy as np

J = 1 / 3 * (14.7 * 0.001) * ((123.6 * 0.001) ** 2)\
          + (5.5 * 0.001) * ((110 * 0.001) ** 2)  # 0.5 * M * R^2
print("rotation inertia is:%f" % J)
w1 = 5.28
w2 = 5.25
print("omega1 is:%f" % w1)
print("omega2 is:%f" % w2)
theta_goal = 110 * np.pi/ 180
print("theta goal is:%f" % theta_goal)
k1 = J * (w1 ** 2)
k2 = J * (w2 ** 2)
print("stiffness1 is:%f" % k1)
print("stiffness2 is:%f" % k2)
theta_acceleration = 10 * np.pi/ 180
print("theta acceleration is:%f" % theta_acceleration)
slope1 = 0.108
slope2 = 0.185
torque = slope1 * np.pi * k1 / 2 / w1
torque *= 1
print("moment of friction is:%f" % torque)

theta_clutch = ((k2*theta_goal - torque)/k2) - (2*((0.5*k1*(np.pi*theta_acceleration-(theta_acceleration**2))+torque*theta_acceleration-0.5*k2*(theta_goal**2))/k2) +((torque-k2*theta_goal)/k2)**2)**0.5
print("clutching theta is: %.2f degrees" % (theta_clutch * 180 / np.pi - 90))

