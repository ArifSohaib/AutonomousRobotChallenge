import RPi.GPIO as GPIO # always needed with RPi.GPIO  
from time import sleep

class MotorControls:
    def __init__(self, pin1=18, pin2=19):
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  
        
        GPIO.setup(pin1, GPIO.OUT)# set GPIO pin1 as an output. You can use any GPIO port  
        GPIO.setup(pin2, GPIO.OUT)# set GPIO pin1 as an output. You can use any GPIO port  
        
        self.motor1 = GPIO.PWM(pin1, 50)    # create an object p for PWM on port pin at 50 Hertz  
                                # you can have more than one of these, but they need  
                                # different names for each port   
                                # e.g. p1, p2, motor, servo1 etc.  
        self.motor2 = GPIO.PWM(pin2, 50)                        
        self.forwardStart()

    def forwardStart(self):
        # start the PWM on 90 percent duty cycle 
        self.motor1.start(80) 
        self.motor2.start(80)
        # duty cycle value can be 0.0 to 100.0%, floats are OK 
    def forward(self):
        self.motor1.ChangeDutyCycle(90)
        self.motor2.ChangeDutyCycle(90)
    def turn1(self):
        self.motor1.ChangeDutyCycle(50)
        self.motor2.ChangeDutyCycle(90)

    def turn2(self):
        self.motor1.ChangeDutyCycle(90)
        self.motor2.ChangeDutyCycle(50)
    
    def reverse(self):
        #TODO
        pass

    def stop(self):
        # stop the PWM output  
        self.motor2.stop()
        self.motor1.stop()                
        GPIO.cleanup()          # when your program exits, tidy up after yourself  

if __name__ == "__main__":
    pass
