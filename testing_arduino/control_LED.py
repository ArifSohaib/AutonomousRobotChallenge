import curses
import time
import serial

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
ser = serial.Serial('/dev/ttyACM0', '9600')
while True:
    char = screen.getch()
    if char == ord('q'):
        break
    elif char == ord('b'):
        ser.write('6')
    elif char == ord('y'):
        ser.write('5')
    elif char == ord('g'):
        ser.write('3')
    else:
        print('unknown command')

curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()

