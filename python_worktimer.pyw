from tkinter import Tk, Label, Button, Text, Frame, Entry
from tkinter import N, E, S, W, END
from tkinter.ttk import Notebook

from datetime import date

import os

from worktimer import *

'''
The WorkTimer is a tkinter application which allows the user to keep track of
worked time in order to accurately figure contract time billed.  The application
consists of two main elements - the timer notebook and the system.  
The system displays output and copyright information, and is only a small bar 
at the bottom of the window.
The timer notebook contains one instance of the actual work timer, which is 
defined in the create_timer function and added to the notebook via that
function.  Important elements are made accessible by adding them to the timer_dict.
The actual time functionality is contained in the Timer class, whose tick function
is called for every instance of the timer in the WorkTimer tick function, which 
uses tkinter await to call a tick every second.

'''

root = Tk()

# find current path and set the icon
ABSPATH = os.path.abspath(os.curdir)
icon_path = ABSPATH + r'/WorkTimerIcon.ico'

root.iconbitmap(icon_path)

gui = WorkTimer(root)
root.mainloop()