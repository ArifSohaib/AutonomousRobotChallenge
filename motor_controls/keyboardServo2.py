# import curses and GPIO
import curses
from gpiozeroServo import MotorControls

motor = MotorControls()

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

try:
        while True:   
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                motor.forward()
            elif char == curses.KEY_DOWN:
                motor.backward()
            elif char == curses.KEY_RIGHT:
                motor.turn1()
            elif char == curses.KEY_LEFT:
                motor.turn1()
            # elif char == 10:
            #     GPIO.output(7,False)
            #     GPIO.output(11,False)
            #     GPIO.output(13,False)
            #     GPIO.output(15,False)
             
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    
    
