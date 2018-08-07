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
        
    elif x == '0,1,0,0':
        print('stopping')
        motor.stop()
        
    elif x == '0,0,1,0':
        print('turning left')
        motor.turn1()
        
    elif x == '0,0,0,1':
        print('turning right')
    time.sleep(0.05)
    
motor.end()
