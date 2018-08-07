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

keyRec = file('key_strokes.txt','w+')


try:
        while True:   
            char = screen.getch()
            if char == ord('q'):
                motor.end()
                break
            elif char == curses.KEY_UP:
                motor.forward()
                keyRec.write('1,0,0,0\n')
            elif char == curses.KEY_DOWN:
                motor.stop()
                keyRec.write('0,1,0,0\n')
            elif char == curses.KEY_RIGHT:
                motor.turn1()
                keyRec.write('0,0,1,0\n')
            elif char == curses.KEY_LEFT:
                motor.turn2()
                keyRec.write('0,0,0,1\n')
           
            
finally:
    #Close down curses properly, inc turn echo back on!
    keyRec.close()
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    
    
