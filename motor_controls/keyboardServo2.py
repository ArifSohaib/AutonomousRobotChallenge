# import curses and GPIO
import curses
# from gpiozeroServo import MotorControls
from gpioServo import MotorControls

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
                motor.end()
                break
            elif char == curses.KEY_UP:
                motor.forward()
            elif char == curses.KEY_DOWN:
                motor.stop()
            elif char == curses.KEY_RIGHT:
                motor.turn1()
            elif char == curses.KEY_LEFT:
                motor.turn2()
            else:
                motor.stop()
            
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    
    
