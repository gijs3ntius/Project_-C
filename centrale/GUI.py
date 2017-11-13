from tkinter import *
from Project.enums import *
from Project.controlers import SerialController

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
        self.controller = SerialController()
        self.frame1 = Frame(master, bg='slategray2')
        self.frame1.grid(row=0, column=0)
        self.frame2 = Frame(master, bg='slategray2')
        self.frame2.grid(row=0, column=1, sticky=NW)
        self.frame3 = Frame(master, bg='slategray2')
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
    This function adds the buttons and entries for the min and max temp values.
    """

    def tempset(self):
        self.mintemp_entry = Entry(self.frame3, width=20)
        self.mintemp_entry.insert(0, 'Enter min temp')
        self.mintemp_entry.grid(row=4, column=1, sticky=E)

        self.maxtemp_entry = Entry(self.frame3, width=20)
        self.maxtemp_entry.insert(0, 'Enter max temp')
        self.maxtemp_entry.grid(row=5, column=1, sticky=E)

        submit_mintemp = Button(self.frame3, text='Submit', pady=20, padx=20, bg='gray75', command=self.grabmintemp)
        submit_mintemp.grid(row=4, column=2, columnspan=3, sticky=W)

        submit_maxtemp = Button(self.frame3, text='Submit', pady=20, padx=20, bg='gray75', command=self.grabmaxtemp)
        submit_maxtemp.grid(row=5, column=2, columnspan=3, sticky=W)

    """
    This function adds the buttons and entries for the min and max light values.
    """

    def lightset(self):
        self.minlight_entry = Entry(self.frame3, width=20)
        self.minlight_entry.insert(0, 'Enter min intensity')
        self.minlight_entry.grid(row=2, column=1, sticky=E)

        self.maxlight_entry = Entry(self.frame3, width=20)
        self.maxlight_entry.insert(0, 'Enter max intensity')
        self.maxlight_entry.grid(row=3, column=1, sticky=E)

        submit_minlight = Button(self.frame3, text='Submit', pady=20, padx=20, bg='gray75', command=self.grabminlight)
        submit_minlight.grid(row=2, column=2, columnspan=3, sticky=W)

        submit_maxlight = Button(self.frame3, text='Submit', pady=20, padx=20, bg='gray75', command=self.grabmaxlight)
        submit_maxlight.grid(row=3, column=2, columnspan=3, sticky=W)

    """
    This function adds the buttons and entries to determine the max and min values for roll in/roll out
    """

    def rollset(self):
        self.minroll_entry = Entry(self.frame2, width=20)
        self.minroll_entry.insert(0, 'Enter min roll distance')
        self.minroll_entry.grid(row=3, column=1, sticky=W)

        self.maxroll_entry = Entry(self.frame2, width=20)
        self.maxroll_entry.insert(0, 'Enter max roll distance')
        self.maxroll_entry.grid(row=4, column=1, sticky=W)

        submit_minroll = Button(self.frame2, text='Submit', pady=37, padx=20, bg='gray75', command=self.grabminroll)
        submit_minroll.grid(row=3, column=1, columnspan=3, sticky=S)

        submit_maxroll = Button(self.frame2, text='Submit', pady=33, padx=20, bg='gray75', command=self.grabmaxroll)
        submit_maxroll.grid(row=4, column=1, columnspan=3, sticky=S)

    """
    This function adds the buttons to roll in/roll out and refresh the connection.
    """

    def settings(self):
        self.roll_in = Button(self.frame2, text='Roll in', padx=35, pady=39, bg='gray75')
        self.roll_in.grid(row=3, column=1, sticky=E)

        self.roll_out = Button(self.frame2, text='Roll out', padx=31, pady=35, bg='gray75')
        self.roll_out.grid(row=4, column=1, sticky=E)

    """
    These functions grab the input and sends the input to the Arduino
    along with the corresponding command.
    """

    def grabmaxtemp(self):
        maxtemp = self.maxtemp_entry.get()
        self.controller.send_command('COM4', Command.TEMP_ROL_OUT, maxtemp)  # sends the maxtemp
        #print(maxtemp)

    def grabmintemp(self):
        mintemp = self.mintemp_entry.get()
        self.controller.send_command('COM4', Command.TEMP_ROL_IN, mintemp)  # sends the mintemp
        #print(mintemp)

    def grabmaxlight(self):
        maxlight = self.maxlight_entry.get()
        self.controller.send_command('COM4', Command.LIGHT_ROL_OUT, maxlight)  # sends the maxlight
        #print(maxlight)

    def grabminlight(self):
        minlight = self.minlight_entry.get()
        self.controller.send_command('COM4', Command.LIGHT_ROL_IN, minlight)  # sends the minlight
        #print(minlight)

    def grabmaxroll(self):
        maxroll = self.maxroll_entry.get()
        self.controller.send_command('COM4', Command.MAX_ROL_OUT, maxroll)  # sends the maxroll
        #print(maxroll)

    def grabminroll(self):
        minroll = self.minroll_entry.get()
        self.controller.send_command('COM4', Command.MIN_ROL_OUT, minroll)  # sends the minroll
        #print(minroll)

    """
    These functions will send the command to roll out/roll in to the Arduino when the button is pressed
    """

    #def rollout(self):
        #self.controller.send_command('COM4', Command.ROL_OUT)
        #print('test')

    #def rollin(self):
        #self.controller.send_command('COM4', Command.ROL_IN)
        #print('test')




"""
The main function which runs the application.
"""

if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    app.first_window()
    app.plotCelc()
    app.tempset()
    app.lightset()
    app.rollset()
    app.settings()
    root.mainloop()