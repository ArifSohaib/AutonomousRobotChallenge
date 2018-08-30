# import curses and GPIO
import curses
import serial
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

ser = serial.Serial("/dev/ttyUSB0", "9600")
serLidar = serial.Serial("/dev/ttyACM0", "115200")
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
        distString = serLidar.readline()
        dist = 1000
        try:
            dist = int(distString[:3])
        except:
            print("can't convert dist")
        if piCam == True:
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image_np = np.array(frame.array)
                
                rawCapture.truncate(0)
                
                char = screen.getch()
                key = [0,0,0,0,1]
                if char == ord('x'):
                    np.save("train_data_wcc2.npy", train_data)
                    ser.write(b'5')
                    keyRec.close()
                    curses.nocbreak(); screen.keypad(0); curses.echo()
                    curses.endwin()
                    break
                elif char == ord('w') and dist > 100:
                    ser.write('1')
                    key = [1,0,0,0,0]

                elif char == ord('s') and dist > 100:
                    ser.write('2')
                    key = [0,1,0,0,0]
                    
                elif char == ord('a') and dist > 100:
                    ser.write('3')
                    key = [0,0,1,0,0]
                    
                elif char == ord('d') and dist > 100:
                    ser.write('4')
                    key = [0,0,0,1,0]
                elif char == ord('q'):
                    ser.write('5')
                    key = [0,0,0,0,1]
                
                val_dict = {"input":key, "image":image_np}
                train_data.append(val_dict)
                keyRec.write(str(key)+"\n")
                
                if len(train_data) % 100 == 0:
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
            elif char == ord('w') and dist > 100:
                ser.write(b'1')
                key = [1,0,0,0,0]

            elif char == ord('s') and dist > 100:
                ser.write(b'2')
                key = [0,1,0,0,0]
                    
            elif char == ord('a') and dist > 100:
                ser.write(b'3')
                key = [0,0,1,0,0]
                    
            elif char == ord('d') and dist > 100:
                ser.write(b'4')
                key = [0,0,0,1,0]
            elif char == ord('q'):
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
