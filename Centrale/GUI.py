from tkinter import *

"""" 
Version: 1.0.0
Author: Stephan Hilberts
Date: 01 Nov 2017
 """

msg = "Please insert an Arduino" #The message used in the Arduino status windows.

class AppGUI(Frame): #using Frame from the tkinter library
    #init global vars
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        #creating the 5 status windows for the 5 different Arduinos.
        #The way this is done will most likely change as this is only a 1st version.
        button1 = Button(text=msg, height=10, width=60, state=DISABLED)
        button1.grid(row=0)
        button2 = Button(text=msg, height=10, width=60, state=DISABLED)
        button2.grid(row=1)
        button3 = Button(text=msg, height=10, width=60, state=DISABLED)
        button3.grid(row=2)
        button4 = Button(text=msg, height=10, width=60, state=DISABLED)
        button4.grid(row=3)
        button5 = Button(text=msg, height=10, width=60, state=DISABLED)
        button5.grid(row=4)

#Making a new class to setup the canvas to write the graphs to.
class Graph(Frame):
    #init global vars
    def __init__(self):
        self.s = 1
        self.x2 = 50

#The mainloop below to run the code.
if __name__ == "__main__":
    root = Tk()
    root.title('!C Application')
    AppGUI(root)
    root.mainloop()
