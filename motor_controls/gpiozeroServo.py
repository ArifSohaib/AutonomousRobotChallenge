from gpiozero import Servo
from time import sleep

#global definations
myGPIO = 18
myGPIO2 = 23
correction = 0.45
maxPW = (2.0+correction)/1000
minPW = (1.0-correction)/1000

myServo1 = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)
myServo2 = Servo(myGPIO2, min_pulse_width=minPW, max_pulse_width=maxPW)

def forward(myServo1=myServo1, myServo2=myServo2):
    myServo1.min()
    myServo2.max()
    sleep(0.5)



def backward(myServo1=myServo1, myServo2=myServo2):
    myServo1.max()
    myServo2.max()
    sleep(1)

def turn1(myServo1=myServo1, myServo2=myServo2):
    myServo1.max()
    myServo2.max()
    sleep(1)


if __name__ == "__main__":
    forward()