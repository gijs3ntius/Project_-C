from tkinter import *
from tkinter import ttk

"""
Version: 1.0.1
Author: Stephan Hilberts
Date: 01 Nov 2017
"""

msg = "Please insert an Arduino"  # The message used in the GUI.


class Window(Frame):  # FRAMES INDELEN VOORDAT JE DE WIDGETS ADD ANDERS AIDS

    """
    Init the constructor of the Window class.
    @:param master as in masterwidget.
    Saves the masterwidget in a variable master.
    """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.listener = None

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

        button1 = Button(text=msg, height=10, width=60, state=DISABLED)
        button1.grid(row=0, column=0)
        button2 = Button(text=msg, height=10, width=60, state=DISABLED)
        button2.grid(row=1, column=0)
        button3 = Button(text=msg, height=10, width=60, state=DISABLED)
        button3.grid(row=2, column=0)
        button4 = Button(text=msg, height=10, width=60, state=DISABLED)
        button4.grid(row=3, column=0)
        button5 = Button(text=msg, height=10, width=60, state=DISABLED)
        button5.grid(row=4, column=0)

        """
        The checkbuttons to select a connected Arduino.
        Functionality has yet to be added.
        """

        button1.checked = IntVar()
        Checkbutton(variable=button1.checked).grid(row=0, sticky=E, padx=10)
        button2.checked = IntVar()
        Checkbutton(variable=button2.checked).grid(row=1, sticky=E, padx=10)
        button3.checked = IntVar()
        Checkbutton(variable=button3.checked).grid(row=2, sticky=E, padx=10)
        button4.checked = IntVar()
        Checkbutton(variable=button4.checked).grid(row=3, sticky=E, padx=10)
        button5.checked = IntVar()
        Checkbutton(variable=button5.checked).grid(row=4, sticky=E, padx=10)

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
class Graph(Canvas):
    def __init__(self):
        self.start = 1

    def make_canvas(self):
        canvas = Canvas(root, width=400, height=400, bg='white')
        canvas.grid(row=0, column=1)








    def tab(self):
        nb = ttk.Notebook(root)
        page1 = ttk.Frame(nb)
        page2 = ttk.Frame(nb)

        nb.add(page1, text='One')
        nb.add(page2, text='Two')

        #nb.grid(row=0)

"""

if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    app.first_window()
    app.make_canvas()
    root.mainloop()