import cv2
from http import server
import time
import numpy as np


PAGE="""\
<html>
<head>
<title>Video Streaming Demonstration</title>
</head>
<body>
<center><h1>Video Streaming Demonstration</h1></center>
<center><img src="/video_feed"></center>
</body>
</html>
"""

video = cv2.VideoCapture(0)
video.set(3,640) # set Width
video.set(4,480) # set Height


def get_frame(v):
    success, image = v.read()

    image = cv2.rotate(image, cv2.ROTATE_180)

    ############## Computer vision part ##############
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) 
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) # image binaryzation

    newImg = np.zeros(image.shape, np.uint8)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    n = len(contours)
    contoursImg = []

    for i in range(n):
        temp = np.zeros(image.shape, np.uint8)
        contoursImg.append(temp)
        contoursImg[i] = cv2.drawContours(contoursImg[i], contours, i, (255, 0, 0), 2)
        if cv2.contourArea(contours[i]) > 1000:
            newImg = cv2.add(image, contoursImg[i])
            mom = cv2.moments(contours[i])
            pt = (int(mom['m10'] / mom['m00']), int(mom['m01'] / mom['m00']))
            cv2.circle(newImg, pt, 10, (255, 0, 255), -1)
            text = "(" + str(pt[0]) + ", " + str(pt[1]) + ")"
            cv2.putText(newImg, text, (pt[0] - 7, pt[1] + 45),cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, 8, 0)
    #################################################

    ret, jpeg = cv2.imencode('.jpg', newImg)
    return jpeg.tobytes()

def function_Camera(camera):
    while True:
        frame = get_frame(camera)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class HTTPHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()

        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        elif self.path == '/video_feed':
            self.send_response(200)
            self.send_header('Content-Type','multipart/x-mixed-replace; boundary=frame')
            self.end_headers()
            while True:
                self.wfile.write(next(cam))
                self.wfile.write(b'\r\n')

        else:
            self.send_error(404)
            self.end_headers()

cam = function_Camera(video)

try:
    print("http server start...")
    address = ('', 8080)
    server = server.HTTPServer(address, HTTPHandler)
    server.serve_forever()

finally:
    print('done')
