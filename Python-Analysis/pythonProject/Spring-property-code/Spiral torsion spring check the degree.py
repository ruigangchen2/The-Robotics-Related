import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy

data = pd.read_csv("./rotation_data3/-30degree_-16degree.csv")

time = np.array(data['Time'].ravel())
time = np.around(time,2)
degree = np.array(data['Degree'].ravel())
degree = np.around(degree,2)
velocity = np.array(data['Velocity'].ravel())
velocity = np.around(velocity,2)
Electromagnet_1_Clutch = np.array(data['Electromagnet_Clutch_1'].ravel())
Electromagnet_1_Clutch = np.around(Electromagnet_1_Clutch,2)
Electromagnet_2_Clutch = np.array(data['Electromagnet_Clutch_2'].ravel())
Electromagnet_2_Clutch = np.around(Electromagnet_2_Clutch,2)
Electromagnet_3_Clutch = np.array(data['Electromagnet_Clutch_3'].ravel())
Electromagnet_3_Clutch = np.around(Electromagnet_3_Clutch,2)
Electromagnet_4_Clutch = np.array(data['Electromagnet_Clutch_4'].ravel())
Electromagnet_4_Clutch = np.around(Electromagnet_4_Clutch,2)


startline = 2000
endline = None

time = time[startline:endline] - time[startline]
degree = degree[startline:endline]
velocity = velocity[startline:endline]
Electromagnet_1_Clutch = Electromagnet_1_Clutch[startline:endline]
Electromagnet_2_Clutch = Electromagnet_2_Clutch[startline:endline]
Electromagnet_3_Clutch = Electromagnet_3_Clutch[startline:endline]
Electromagnet_4_Clutch = Electromagnet_4_Clutch[startline:endline]



fig ,ax1 = plt.subplots(figsize=(8, 4), dpi=200)
ax1.plot(time, degree, 'k--', label='Angular Displacement [degree]')
ax1.set_xlabel('Time [ms]', fontweight ='bold')
ax1.set_ylabel('Angular Displacement [degree]',fontweight ='bold')
ax1.grid()
fig.legend()
ax1.set_ylim([-180, 180])
fig.savefig('The Angular Displacement.pdf')
print("The maximum is: %.2f" % degree.max())
print("The minimum is: %.2f" % degree.min())
plt.show()