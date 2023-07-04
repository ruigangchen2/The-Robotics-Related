import cv2
import numpy as np
import matplotlib.pyplot as plt
img = cv2.imread("test4.png", 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

newImg = np.zeros(img.shape, np.uint8)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
n = len(contours)
contoursImg = []
for i in range(n):
    temp = np.zeros(img.shape, np.uint8)
    contoursImg.append(temp)
    contoursImg[i] = cv2.drawContours(contoursImg[i], contours, i, (255, 255, 0), 10)
    if cv2.contourArea(contours[i]) > 1000:
        newImg = cv2.add(img, contoursImg[i])
        mom = cv2.moments(contours[i])
        pt = (int(mom['m10'] / mom['m00']), int(mom['m01'] / mom['m00']))
        cv2.circle(newImg, pt, 20, (0, 0, 255), -1)
        text = "(" + str(pt[0]) + ", " + str(pt[1]) + ")"
        cv2.putText(newImg, text, (pt[0] - 7, pt[1] + 20),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5, 8, 0)

                    
plt.subplot(122)
img2 = newImg[:, :, ::-1]
plt.imshow(img2)
plt.xticks([]), plt.yticks([])
plt.subplot(121)
img2 = img[:, :, ::-1]
plt.imshow(img2)
plt.xticks([]), plt.yticks([])
plt.savefig('test.pdf')
plt.show()