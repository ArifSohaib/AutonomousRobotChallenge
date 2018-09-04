import serial

serLidar = serial.Serial("/dev/ttyACM0","115200")
serMotor = serial.Serial("/dev/ttyUSB0","9600")
distArr = []
while True:
    dist = serLidar.readline()
    try:
        dist = dist[:3]
        dist = int(dist)
        distArr.append(dist)
        if len(distArr) == 100:
            del distArr[0]
    except ValueError:
        print("can not convert '{}' to int stopping".format(dist))
        serMotor.write(b'5')
        exit()
    distArrMore = [dist > 50 for dist in distArr]
    if len(distArrMore) > 5:
        serMotor.write(b'1')
        print(dist)
        #print("moving forward")
    else:
        serMotor.write(b'1')
        print(dist)

