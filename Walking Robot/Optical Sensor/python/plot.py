import serial
import matplotlib.pyplot as plt
from drawnow import *
import atexit
import time

xs = []
ys = []
plt.ion()  # 打开交互模式

ser = serial.Serial('/dev/cu.usbserial-210', 9600)
line_as_list = [0,1]

def plotValues():
    line = ser.readline()
    line_as_list = line.split(b',')
    i = int(line_as_list[0])
    relProb = line_as_list[1]
    relProb_as_list = relProb.split(b'\n')
    relProb_float = float(relProb_as_list[0])
    xs.append(i)
    ys.append(relProb_float)
    plt.title('Serial from Arduino')
    plt.grid(True)
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.plot(xs, ys, 'rx-')


def doAtExit():
    ser.close()
    print("Close serial")
    print("ser.isOpen() = " + str(ser.isOpen()))


atexit.register(doAtExit)  # 程序退出时，回调函数
print("ser.isOpen() = " + str(ser.isOpen()))
while True:
    drawnow(plotValues)