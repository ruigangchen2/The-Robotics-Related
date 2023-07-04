import cv2
import numpy as np
import matplotlib.pyplot as plt
height=600
width=600
color = (1,0,0)
color2 = (0,1,0)

img = np.zeros([600,600,2])
triangle1 = np.array([[20,20], [20, 100], [500, 600],[300,20],[200,10]])
cv2.fillConvexPoly(img, triangle1, color)

area1 = img.sum()
img = np.zeros([600,600,3])
triangle2 = np.array([[600,60], [500, 120], [300, 120],[500,60]])
cv2.fillConvexPoly(img, triangle2, color2)
area2 = img.sum()
cv2.fillConvexPoly(img, triangle1, color)
union_area = img.sum()
inter_area = area1 + area2 - union_area
IOU = inter_area / union_area
plt.imshow(img)
plt.show()
print (IOU * 100)