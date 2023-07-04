import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    newImg = np.zeros(frame.shape, np.uint8)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    n = len(contours)
    contoursImg = []

    for i in range(n):
        temp = np.zeros(frame.shape, np.uint8)
        contoursImg.append(temp)
        contoursImg[i] = cv2.drawContours(contoursImg[i], contours, i, (255, 0, 0), 2)
        if cv2.contourArea(contours[i]) > 1000:
            newImg = cv2.add(frame, contoursImg[i])
            mom = cv2.moments(contours[i])
            pt = (int(mom['m10'] / mom['m00']), int(mom['m01'] / mom['m00']))
            cv2.circle(newImg, pt, 10, (255, 0, 255), -1)
            text = "(" + str(pt[0]) + ", " + str(pt[1]) + ")"
            cv2.putText(newImg, text, (pt[0] - 7, pt[1] + 45),cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, 8, 0)
                    
    cv2.imshow('newImg', newImg)
    # cv2.imshow('thresh', thresh)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()