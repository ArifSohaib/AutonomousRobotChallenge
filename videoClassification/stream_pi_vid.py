import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
#import picamera
#import io

cap=cv2.VideoCapture(0)
#my_stream = io.BytesIO()
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('',8200)
clientsocket.bind(server_address)

while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame) ### new code
    clientsocket.sendall(struct.pack("H", len(data))+data) ### new code
