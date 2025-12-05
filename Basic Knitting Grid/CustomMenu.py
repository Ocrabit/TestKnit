import tkinter as tk
import ImageClickCanvas as ICC
class Menubar(tk.Menu):
    def __init__(self, parent, canvasImage: ICC.ImageCanvas):
        tk.Menu.__init__(self, parent)

        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label='Open')
        file_menu.add_command(label='New')
        file_menu.add_separator()
        file_menu.add_command(label='Save As...', command=canvasImage.save_file)
        self.add_cascade(label='File', menu=file_menu)

        view_menu = tk.Menu(self, tearoff=0)
        view_menu.add_command(label='Zoom In')
        view_menu.add_command(label='Zoom Out')
        view_menu.add_separator()
        self.add_cascade(label='View', menu=view_menu)


        parent.config(menu=self)