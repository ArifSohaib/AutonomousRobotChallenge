import gpiozeroServo

import curses
import os



def detect(win):
    win.nodelay(True)
    key=""
    win.clear()                
    win.addstr("Detected key:")
    while 1:          
        try:                 
           key = win.getkey()         
           win.clear()                
           win.addstr("Detected key:")
           
           win.addstr(str(key)) 
           if str(key) == "KEY_UP:
               gpiozeroServo.forward()
           if key == os.linesep:
              break           
        except Exception as e:
           # No input   
           pass
def main():
    curses.wrapper(detect)

if __name__ == "__main__":
    main()