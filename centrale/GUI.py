from tkinter import *

"""
Version: 1.0.2
Author: Stephan Hilberts
Date: 9 Nov 2017
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
        self.graphType = True
        self.frame1 = Frame(master)
        self.frame1.grid(row=0, column=0)
        self.frame2 = Frame(master)
        self.frame2.grid(row=0, column=1, sticky=NW)
        self.frame3 = Frame(master)
        self.frame3.grid(row=0, column=6, sticky=NW)

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
        These are put in frame1
        Functionality has yet to be added.
        """

        button1 = Button(self.frame1, text=msg, font='Arial 9', height=10, width=35, bg='slategray2')
        button1.grid(row=0, column=0)
        button2 = Button(self.frame1, text=msg, font='Arial 9', height=10, width=35, bg='slategray3')
        button2.grid(row=1, column=0)
        button3 = Button(self.frame1, text=msg, font='Arial 9', height=10, width=35, bg='slategray2')
        button3.grid(row=2, column=0)
        button4 = Button(self.frame1, text=msg, font='Arial 9', height=10, width=35, bg='slategray3')
        button4.grid(row=3, column=0)
        button5 = Button(self.frame1, text=msg, font='Arial 9', height=10, width=35, bg='slategray2')
        button5.grid(row=4, column=0)


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
    This graph will show the temperature over time.
    Temperature will be showed in celsius from 0 - 100.
    """

    def plotCelc(self,):
        self.canvas = Canvas(self.frame2, width=1050, height=600, bg='white')  # 0,0 is top left corner
        self.canvas.grid(row=0, column=1, sticky=NW)

        self.canvas.create_line(50, 550, 1150, 550, width=2)  # x-axis
        self.canvas.create_text(550, 580, text='Time in minutes')  # x-axis text

        self.canvas.create_line(50, 550, 50, 50, width=2)  # y-axis
        self.canvas.create_text(10, 300, text='Temperature in Celsius', angle=90)  # y-axis text

        self.canvas.create_text(200, 20, text='Temperature over time', font='Arial 25')

        switch_graph = Button(self.frame2, text='Switch graph', pady=10, bg='seashell3', command=self.change_graph)  # button to switch graph types
        switch_graph.grid(row=0, column=1, sticky=N)  # position of the button on the canvas

        """
        This block of code adds the vertical dotted lines in the graph, forming the squares.
        """

        for i in range(23):
            x = 50 + (i * 50)
            self.canvas.create_line(x, 550, x, 50, width=1, dash=(2, 5))
            self.canvas.create_text(x, 550, text='%d' % (1 * i), anchor=NE)  # temp in Celsius

        """
        This block of code adds the horizontal dotted lines in the graph, forming the squares.
        """

        for i in range(11):
            y = 550 - (i * 50)
            self.canvas.create_line(50, y, 1150, y, width=1, dash=(2, 5))
            self.canvas.create_text(40, y, text='%d' % (5 * i-10), anchor=NE)

    """
    Function to make a canvas with lines which can be used to show a graph.
    This graph will show the light intensity over time.
    Light intensity will be shown in percent from 0 - 100.
    """

    def plotLight(self):
        self.canvas = Canvas(self.frame2, width=1050, height=600, bg='white')  # 0,0 is top left corner
        self.canvas.grid(row=0, column=1, sticky=NW)

        self.canvas.create_line(50, 550, 1150, 550, width=2)  # x-axis
        self.canvas.create_text(550, 580, text='Time in minutes')  # x-axis text

        self.canvas.create_line(50, 550, 50, 50, width=2)  # y-axis
        self.canvas.create_text(10, 300, text='Light intensity in %', angle=90)  # y-axis text

        switch_graph = Button(text='Switch graph', pady=10, bg='seashell3', command=self.change_graph)  # button to switch graph types
        switch_graph.grid(row=0, column=1, sticky=N)  # position of the button on the canvas

        self.canvas.create_text(200, 20, text='Light intensity over time', font='Arial 25')

        """
        This block of code adds the vertical dotted lines in the graph, forming the squares.
        """

        for i in range(23):
            x = 50 + (i * 50)
            self.canvas.create_line(x, 550, x, 50, width=1, dash=(2, 5))
            self.canvas.create_text(x, 550, text='%d' % (1 * i), anchor=NE)  # light intensity in %

        """
        This block of code adds the horizontal dotted lines in the graph, forming the squares.
        """

        for i in range(11):
            y = 550 - (i * 50)
            self.canvas.create_line(50, y, 1150, y, width=1, dash=(2, 5))
            self.canvas.create_text(40, y, text='%d' % (10 * i), anchor=NE)

    """
    Function used as a command for the buttons to switch between the light and the temperature graph.
    Should be changed and tested when data is being shown.
    """

    def change_graph(self):
        if self.graphType:
            self.graphType = False
            app.plotLight()
        else:
            self.graphType = True
            app.plotCelc()

    """
    This function adds the buttons to reset the connection,
    set the program to roll out/roll in when a value is met (automatic),
    set the program to only roll out/ roll in when a button is pushed manually
    """

    def modes(self):
        fixer1 = Button(self.frame2, text='Manual', pady=37, padx=40, bg='gray75', state=DISABLED)  # to fix the layout of GUI zzz
        fixer1.grid(row=2, column=1, sticky=W)

        fixer2 = Button(self.frame2, text='Automatic', pady=37, padx=32, bg='gray75', state=DISABLED)  # to fix the layout of the GUI zzz
        fixer2.grid(row=3, column=1, sticky=W)
        # roll_out.grid(row=0, column=1, sticky=SW) used to position bottomleft

        mintemp_entry = Entry(self.frame2, width=20)
        mintemp_entry.insert(0, 'Enter min temperature')
        mintemp_entry.grid(row=2, column=1, sticky=W)

        maxtemp_entry = Entry(self.frame2, width=20)
        maxtemp_entry.insert(0, 'Enter max temperature')
        maxtemp_entry.grid(row=3, column=1, sticky=W)

        submit_mintemp = Button(self.frame2, text='Submit max temp', pady=37, padx=20, bg='gray75')
        submit_mintemp.grid(row=2, column=1, sticky=S)

        submit_maxtemp = Button(self.frame2, text='Submit min temp', pady=37, padx=22, bg='gray75')
        submit_maxtemp.grid(row=3, column=1, sticky=S)



    def settings(self):
        roll_in = Button(self.frame3, text='Roll in', padx=35, pady=30 ,bg='gray75')
        roll_in.grid(row=0, column=3, sticky=NW)

        roll_out = Button(self.frame3, text='Roll out', padx=31, pady=30 ,bg='gray75')
        roll_out.grid(row=0, column=4, sticky=NW)

        refresh = Button(self.frame3, text='Refresh', padx=88, pady=10, bg='gray75')
        refresh.grid(row=1, column=3, columnspan=2, sticky=NW)










"""
The main function which runs the application.
"""

if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    app.first_window()
    app.plotCelc()
    app.modes()
    app.settings()
    root.mainloop()