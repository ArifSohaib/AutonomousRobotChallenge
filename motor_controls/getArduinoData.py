# import curses and GPIO
import curses
import serial
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import datetime

ser = serial.Serial("/dev/ttyUSB0", "9600")
cap = cv2.VideoCapture(0)
piCam = False
#check if picamera exists
try:
    camera = PiCamera()
    camera.resolution = (224,224)
    camera.framerate = 20
    rawCapture = PiRGBArray(camera, size=(224,224))
    piCam = True
except:
    print("Pi camera does not exist, using USB camera")
# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

keyRec = open('key_strokes.txt','w+')

train_data = []

try:
    while True:
        if piCam == True:
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image_np = np.array(frame.array)
                
                rawCapture.truncate(0)
                
                char = screen.getch()
                key = [0,0,0,0,1]
                if char == ord('x'):
                    np.save("train_data_{}.npy".format(str(datetime.datetime.now()), train_data)
                    ser.write(b'5')
                    keyRec.close()
                    curses.nocbreak(); screen.keypad(0); curses.echo()
                    curses.endwin()
                    break
                elif char == ord('w'):
                    ser.write(b'1')
                    key = [1,0,0,0,0,0,0]

                elif char == ord('s'):
                    ser.write(b'2')
                    key = [0,1,0,0,0,0,0]
                    
                elif char == ord('a'):
                    ser.write(b'3')
                    key = [0,0,1,0,0,0,0]
                    
                elif char == ord('d'):
                    ser.write(b'4')
                    key = [0,0,0,1,0,0,0]

                elif char == ord(' '):
                    ser.write(b'5')
                    key = [0,0,0,0,1,0,0]

                elif char == ord('q'):
                    ser.write(b'6')
                    key = [0,0,0,0,0,1,0]

                elif char == ord('e'):
                    ser.write(b'7')
                    key = [0,0,0,0,0,0,1]

                val_dict = {"input":key, "image":image_np}
                train_data.append(val_dict)
                keyRec.write(str(key)+"\n")
                
                if len(train_data) % 50 == 0:
                    np.save("train_data.npy", train_data)
        #no pi camera, using USB
        else:
            ret, image_np = cap.read()
                
            char = screen.getch()
            key = [0,0,0,0,1]
            if char == ord('x'):
                np.save("train_data.npy", train_data)
                ser.write(b'5')
                keyRec.close()
                curses.nocbreak(); screen.keypad(0); curses.echo()
                curses.endwin()
                break
            elif char == ord('w'):
                ser.write(b'1')
                key = [1,0,0,0,0]
                
            elif char == ord('s'):
                ser.write(b'2')
                key = [0,1,0,0,0]
                
            elif char == ord('a'):
                ser.write(b'3')
                key = [0,0,1,0,0]
                
            elif char == ord('d'):
                ser.write(b'4')
                key = [0,0,0,1,0]
            elif char == ord(' '):
                ser.write(b'5')
                key = [0,0,0,0,1]
                
            val_dict = {"input":key, "image":image_np}
            train_data.append(val_dict)
            keyRec.write(str(key)+"\n")
                
            if len(train_data) % 100 == 0:
                np.save("train_data.npy", train_data)
finally:
    #Close down curses properly, inc turn echo back on!
    keyRec.close()
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
