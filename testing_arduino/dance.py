import serial
ser = serial.Serial('/dev/ttyACM0','9600')
for i in range(30):
    if i % 3 == 0:
        ser.write('3')
    if i % 5 == 0:
        ser.write('5')
    if i % 2 == 0:
        ser.write('6')

