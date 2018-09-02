import os
import cv2
import tensorflow as tf
from tensorflow import keras
from drive_model import default_linear
import numpy as np
import serial
from picamera.array import PiRGBArray
from picamera import PiCamera

model = default_linear()
checkpoint_path = "./training_1/model.h5"
model.load_weights(checkpoint_path)

ser = serial.Serial("/dev/ttyUSB0", "9600")
#serLidar = serial.Serial("/dev/ttyACM0", "115200")
cap = cv2.VideoCapture(0)
piCam = False
#check if picamera exists
try:
    camera = PiCamera()
    camera.resolution = (224,224)
    camera.framerate = 20
    rawCapture = PiRGBArray(camera, size=(224,224))
    piCam = True
    print("starting pi camera")
except:
    print("Pi camera does not exist")

while True:
    #distString = serLidar.readline()
    #dist = 1000
    #try:
        #dist = int(distString.decode("utf-8"))
    #except:
    #    print("can't convert dist")
    if piCam == True:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image_np = np.array(frame.array).reshape(-1,224,224,3)
                
            rawCapture.truncate(0)
            result = model.predict([image_np])
            print(np.argmax(result))        
