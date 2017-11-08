from tkinter import *

"""
Version: 1.0.1
Author: Stephan Hilberts
Date: 01 Nov 2017
"""

msg = "Please insert an Arduino"  # The message used in the GUI.


class Window(Frame):

    """
    Init the constructor of the Window class.
    @:param master as in masterwidget.
    Saves the masterwidget in a variable master.
    """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.listener = None
        self.frame1 = Frame(master)
        self.frame1.grid(row=0)
        self.frame2 = Frame(master)
        self.frame2.grid(row=1, rowspan=3, column=1, columnspan=3)

    """
    The function to create the first buttons and place them on the master window.
    These buttons are used to show what Arduino is connected and give the option to select an Arduino.
    """

    def first_window(self):

        """
        The title of the application.
        """

        self.master.title("!C Application")

        """
        The buttons which show the actual Arduinos on the left side of the Application.
        Functionality has yet to be added.
        """

        button1 = Button(self.frame1, text=msg, height=10, width=30, state=DISABLED)
        button1.grid(row=0, column=0)
        button2 = Button(self.frame1, text=msg, height=10, width=30, state=DISABLED)
        button2.grid(row=1, column=0)
        button3 = Button(self.frame1, text=msg, height=10, width=30, state=DISABLED)
        button3.grid(row=2, column=0)
        button4 = Button(self.frame1, text=msg, height=10, width=30, state=DISABLED)
        button4.grid(row=3, column=0)
        button5 = Button(self.frame1, text=msg, height=10, width=30, state=DISABLED)
        button5.grid(row=4, column=0)

        """
        The checkbuttons to select a connected Arduino.
        Functionality has yet to be added.
        """

        button1.checked = IntVar()
        Checkbutton(self.frame1, variable=button1.checked).grid(row=0, sticky=E, padx=10)
        button2.checked = IntVar()
        Checkbutton(self.frame1, variable=button2.checked).grid(row=1, sticky=E, padx=10)
        button3.checked = IntVar()
        Checkbutton(self.frame1, variable=button3.checked).grid(row=2, sticky=E, padx=10)
        button4.checked = IntVar()
        Checkbutton(self.frame1, variable=button4.checked).grid(row=3, sticky=E, padx=10)
        button5.checked = IntVar()
        Checkbutton(self.frame1, variable=button5.checked).grid(row=4, sticky=E, padx=10)

    """
    The function to read and receive the data coming from the Arduino.
    @:param listener it will receive data from the listener.
    """

    def register(self, listener):
        self.listener = listener

    """
    This function will keep the data for the Application updated.
    @:param this function uses data and makes sure it is updated on the GUI in a set interval.
    """

    def notify(self, data):
        pass

    """
    Function to make a canvas with lines which can be used to show a graph.
    """

    def plot(self,):
        canvas = Canvas(width=1000, height=600, bg='white')  # 0,0 is top left corner
        canvas.grid(row=0, column=2)

        canvas.create_line(50, 550, 1150, 550, width=2)  # x-axis
        canvas.create_line(50, 550, 50, 50, width=2)  # y-axis

        # x-axis
        for i in range(23):
            x = 50 + (i * 50)
            canvas.create_line(x, 550, x, 50, width=1, dash=(2, 5))
            canvas.create_text(x, 550, text='%d' % (10 * i), anchor=N)

        # y-axis
        for i in range(11):
            y = 550 - (i * 50)
            canvas.create_line(50, y, 1150, y, width=1, dash=(2, 5))
            canvas.create_text(40, y, text='%d' % (10 * i), anchor=E)



if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    app.first_window()
    app.plot()
    root.mainloop()