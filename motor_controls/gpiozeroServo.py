from gpiozero import Servo
from time import sleep

class MotorControls:
    def __init__(self, pin1=18, pin2=23, correction=0.45):
        self.myGPIO1 = pin1
        self.myGPIO2 = pin2
        self.correction = correction
        self.maxPW = (2.0+correction)/1000
        self.minPW = (1.0-correction)/1000

        self.myServo1 = Servo(self.myGPIO1, min_pulse_width=self.minPW, max_pulse_width=self.maxPW)
        self.myServo2 = Servo(self.myGPIO2, min_pulse_width=self.minPW, max_pulse_width=self.maxPW)

    def forward(self):
        self.myServo1.min()
        self.myServo2.max()
        sleep(0.5)



    def backward(self):
        self.myServo1.max()
        self.myServo2.max()
        sleep(1)

    def turn1(self):
        self.myServo1.max()
        self.myServo2.max()
        sleep(1)


if __name__ == "__main__":
    motor = MotorControls()
    motor.forward()