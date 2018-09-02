import serial

serLidar = serial.Serial("/dev/ttyACM0","115200")
serMotor = serial.Serial("/dev/ttyUSB0","9600")

while True:
    dist = serLidar.readline()
    try:
        dist = dist[:3]
        dist = int(dist)
    except ValueError:
        print("can not convert '{}' to int".format(dist))
        serMotor.write(b'5')
    if dist > 50:
        serMotor.write(b'1')
        print(dist)
        #print("moving forward")
    else:
        serMotor.write(b'1')
        print(dist)

