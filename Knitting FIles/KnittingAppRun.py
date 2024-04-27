import tkinter as tk
from tkinter import ttk
from CanvasZP import CanvasImage
import tkmacosx
from CustomMenu import Menubar


class MainWindow(ttk.Frame):
    """ Main window class """

    def __init__(self, mainframe, rows, columns):
        """ Initialize the main Frame """
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('Knitting App')
        self.master.geometry('800x600')  # size of the main window
        self.master.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
        self.master.columnconfigure(0, weight=1)
        canvas = CanvasImage(self.master, rows, columns)  # create widget
        canvas.grid(row=0, column=0)  # show widget

        draw_btn = tkmacosx.Button(self.master, text='Draw', command=lambda: canvas.enable('draw'))
        pan_btn = tkmacosx.Button(self.master, text='Pan', command=lambda: canvas.enable('pan'))
        color_btn = tkmacosx.Button(self.master, text='Choose Color', command=canvas.canvas.choose_color)
        draw_btn.grid(row=1, column=0)
        pan_btn.grid(row=2, column=0)
        color_btn.grid(row=3, column=0)

        #add Menu
        menu = Menubar(root, canvas.canvas)


root = tk.Tk()
app = MainWindow(root, rows=8, columns=10)
app.mainloop()
