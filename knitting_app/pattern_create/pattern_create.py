import tkinter as tk
from tkinter import ttk
import platform

if platform.system() == 'Darwin':
    from tkmacosx import Button
    print('mac os')
else:
    from tkinter import Button

from ..tool_functions import tool_functions as tf
from .pattern_selection_ui import PatternSelectionUI
from .pattern_image_display import PatternDisplay


class MainWindow(ttk.Frame):
    def __init__(self, mainframe):
        super().__init__(mainframe)
        self.mainframe = mainframe

        # tab options
        self.basic_ui = ttk.Frame(mainframe)
        self.pattern_selection = PatternSelectionUI(mainframe, self)
        self.pattern_display = None
        self.new_pattern = None

        # Build UI
        self.build_ui()
        self.pack()

    def build_ui(self):
        # Using grid for layout
        tk.Label(self.basic_ui, text="Use existing pattern?").grid(row=0, column=0, sticky=tk.NSEW, padx=40)
        Button(self.basic_ui, text='Select Pattern', command=self.select_pattern).grid(row=1, column=0, sticky=tk.NS)

        tk.Label(self.basic_ui, text="Create New Pattern?").grid(row=2, column=0, sticky=tk.NSEW)
        Button(self.basic_ui, text='New Pattern').grid(row=3, column=0, sticky=tk.NS)

        self.basic_ui.pack()

    def select_pattern(self, sweater=None):
        self.basic_ui.pack_forget()
        if self.pattern_display is not None:
            self.pattern_display.pack_forget()
        self.pattern_selection.pack(fill='both', expand=True)

        self.master.update_idletasks()
        self.master.geometry('')
        tf.center_window(self.master)

    def display_pattern(self):
        self.basic_ui.pack_forget()
        self.pattern_selection.pack_forget()
        self.pattern_display.pack(fill='both', expand=True)
        tf.center_window(self.master)

    def back_to_main(self):
        self.pattern_selection.pack_forget()
        self.basic_ui.pack(fill='both', expand=True)

    def add_pattern_display(self, sweater):
        self.pattern_display = PatternDisplay(self.mainframe, self, sweater)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Sweater Maker')
        self.window_sweater_maker = MainWindow(self)

        # Center the window after it has been initialized
        self.update_idletasks()  # Ensure geometry is calculated
        tf.center_window(self)

        # Start Loop
        self.mainloop()
