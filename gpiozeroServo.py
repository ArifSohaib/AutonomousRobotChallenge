from gpiozero import Servo
from time import sleep

myGPIO = 18
myGPIO2 = 23
correction = 0.45
maxPW = (2.0+correction)/1000
minPW = (1.0-correction)/1000

myServo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)
myServo2 = Servo(myGPIO2, min_pulse_width=minPW, max_pulse_width=maxPW)
while True:
    myServo.mid()
    myServo2.mid()
    sleep(1)
    myServo.min()
    myServo2.min()
    sleep(1)
    myServo.mid()
    myServo2.mid()
    sleep(1)
    myServo.max()
    myServo2.max()
    sleep(1)


