import time
from gpioServo import MotorControls
motor = MotorControls()

with open("key_strokes.txt",'r') as keys:
    key_strokes = keys.readlines()

key_strokes = [x.strip() for x in key_strokes]
print([x for x in key_strokes])
for x in key_strokes:
    if x == '1,0,0,0':
        print('moving forward')
        motor.forward()
        time.sleep(1)
    elif x == '0,1,0,0':
        print('stopping')
        motor.stop()
        time.sleep(1)
    elif x == '0,0,1,0':
        print('turning left')
        motor.turn1()
        time.sleep(1)
    elif x == '0,0,0,1':
        print('turning right')
        motor.turn2()
        time.sleep(1)
motor.end()
