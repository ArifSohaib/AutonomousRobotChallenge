import numpy as np
import serial
# key_strokes = np.load('train_data.npy',encoding='latin1')
key_strokes = open("key_strokes.txt", 'r')
ser = serial.Serial("/dev/ttyUSB0", "9600")
key_strokes = [x['input'] for x in key_strokes]
print([x for x in key_strokes])
for x in key_strokes:
    if x == [1,0,0,0,0]:
        print('moving forward')
        ser.write('1')

    elif x == [0,1,0,0,0]:
        print('reverse')
        ser.write('2')

    elif x == [0,0,0,0,1]:
        print('pausing')
        ser.write('5')
        
    elif x == [0,0,1,0,0]:
        print('turning left')
        ser.write('3')
        
    elif x == [0,0,0,1,0]:
        print('turning right')
        ser.write('4')
    