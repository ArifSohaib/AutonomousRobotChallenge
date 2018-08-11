# import curses and GPIO
import curses
from gpioServo import MotorControls
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2

motor = MotorControls()
camera = PiCamera()
camera.resolution = (224,224)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(224,224))
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
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image_np = np.array(frame.array)
            # image_np = cv2.resize(image_np,(244,244),interpolation=cv2.INTER_LINEAR)
            rawCapture.truncate(0)
            
            char = screen.getch()
            key = [1,0,0,0]
            if char == ord('q'):
                np.save("train_data.npy", train_data)
                motor.end()
                keyRec.close()
                curses.nocbreak(); screen.keypad(0); curses.echo()
                curses.endwin()
                break
            elif char == curses.KEY_UP:
                motor.forward()
                key = [1,0,0,0]

            elif char == curses.KEY_DOWN:
                motor.stop()
                key = [0,1,0,0]
                
            elif char == curses.KEY_RIGHT:
                motor.turn1()
                key = [0,0,1,0]
                
            elif char == curses.KEY_LEFT:
                motor.turn2()
                key = [0,0,0,1]
            
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
    
    