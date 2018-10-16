import curses
import serial
import numpy as np
# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

keyRec = open('key_strokes.txt','w+')
outRec = open('serialOuts.txt', 'w+')
ser = serial.Serial("/dev/ttyACM0", "9600")
serRead = ''

try:
    while True:   
        char = screen.getch()
        if char == ord(' '):
            ser.write(b'5')
            #one-hot format ['up', 'down', 'left', 'right','pause','speedup','slowdown']
            key = [0,0,0,0,1,0,0]
            
        elif char == ord('q'):
            ser.write(b'6')
            key = [0,0,0,0,0,1,0]

        elif char == ord('e'):
            ser.write(b'7')
            key = [0,0,0,0,0,0,1]

        elif char == ord('w'):
            ser.write(b'1')
            key = [1,0,0,0,0,0,0]

        elif char == ord('s'):
            ser.write(b'2')
            key = [0,1,0,0,0,0,0]

        elif char == ord('a'):
            ser.write(b'3')
            key = [0,0,1,0,0,0,0]
                
        elif char == ord('d'):
            ser.write(b'4')
            key = [0,0,0,1,0,0,0]
        elif char == ord('x'):
            break
        else:
            print("unknown command, pausing, key not recorded")
            ser.write(b'5')
        serRead += str(ser.readline())
        keyRec.write(str(key)+"\n")
        outRec.write(serRead + "\n")
finally:
    #Close down curses properly, inc turn echo back on!
    keyRec.close()
    outRec.close()
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
