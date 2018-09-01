import os

import tensorflow as tf
from tensorflow import keras
from drive_model import default_linear
import numpy as np

model = default_linear()
checkpoint_path = "training_1/cp.ckpt"
model.load_weights()

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
            dist = int(distString.decode("utf-8"))
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
                elif np.argmax(model.predict(image_np)) == 0 and dist > 100:
                    ser.write(b'1')
                    key = [1,0,0,0,0]

                elif np.argmax(model.predict(image_np)) == 1 and dist > 100:
                    ser.write(b'2')
                    key = [0,1,0,0,0]
                    
                elif np.argmax(model.predict(image_np)) == 2 and dist > 100:
                    ser.write(b'3')
                    key = [0,0,1,0,0]
                    
                elif np.argmax(model.predict(image_np)) == 3 and dist > 100:
                    ser.write(b'4')
                    key = [0,0,0,1,0]
                elif np.argmax(model.predict(image_np)) == 1:
                    ser.write(b'5')
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
