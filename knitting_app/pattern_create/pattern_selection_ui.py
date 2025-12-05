import asyncio
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import tkinter.messagebox as messagebox

from PIL import ImageTk

# Tkinter Mac Error Handle
import platform

from .pattern_image_display import PatternDisplay

if platform.system() == 'Darwin':
    from tkmacosx import Button

    print('mac os')
else:
    from tkinter import Button

# Tools
from ..tool_functions import tool_functions as tf

# Sweater Imports
from ..sweater_objects.pattern_objects import Swatch
from ..sweater_objects.sweater_pieces import FrontTorso, BackTorso, LeftSleeve, RightSleeve
from ..sweater_objects import Sweater

# Popup Imports
from .pattern_popups import PatternPopups


class PatternSelectionUI(ttk.Frame):
    def __init__(self, master, parent):
        super().__init__(master)
        self.master = master
        self.parent = parent

        # Sweater Objects
        self.sweater = None
        self.front_torso = None
        self.back_torso = None
        self.left_sleeve = None
        self.right_sleeve = None
        self.swatch = None
        self.needle_size = None  # Units: (mm)

        # Image Sweater
        self.sweater_image = None

        # List of available patterns
        self.options = {'basic', 'dipper', 'mable'}

        # Selections Vars
        self.pattern_selected = None
        self.size_selected = None
        self.swatch_selected = None
        self.torso_selected = None
        self.sleeve_selected = None

        # Replacement Buttons
        self.sweater_type_btn = None
        self.torso_btn = None
        self.sleeve_btn = None
        self.swatch_btn = None

        # Edit Buttons
        self.edit_pattern = None
        self.edit_torso = None
        self.edit_sleeve = None
        self.edit_swatch = None

        # Font
        self.input_font = tkfont.Font(family="Arial", size=15, slant="italic", weight="normal")
        self.subheader = tkfont.Font(family="Arial", size=14, slant="italic", weight="bold")

        # Unit used
        self.unit = 'in'  # Future add options page

        # Frames
        self.selection_frame = ttk.Frame(self)
        self.torso_frame = ttk.Frame(self)
        self.sleeve_frame = ttk.Frame(self)
        self.swatch_frame = ttk.Frame(self)

        # Build
        self.build_ui()

    def build_ui(self):
        # Select Pattern
        self.select_pattern()

        # add standard size filler
        self.select_standard_size()

        # Ask Swatch
        self.swatch_dimensions()

        # Ask Torso
        self.torso_dimensions()

        # Ask Sleeve
        self.sleeve_dimensions()

        # Compile
        self.compile_button()

    def select_pattern(self):
        tk.Label(self.selection_frame, text='Pattern Selection:', font=self.subheader).grid(row=0, column=0,
                                                                                            sticky='nsew')
        tk.Label(self.selection_frame, text='Sweater Type:').grid(row=1, column=0, sticky='nsew')
        self.sweater_type_btn = Button(self.selection_frame, text='Select', height=22, width=55,
                                       command=lambda: PatternPopups.pattern_popup(self.master, self.options,
                                                                                   self.on_select_pattern))
        self.sweater_type_btn.grid(row=1, column=1, sticky='nse')

        # Pack Selection Frame
        self.selection_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')

        # Edit Button
        self.edit_pattern = Button(self, text='Edit', width=50,
                                   command=lambda: PatternPopups.pattern_popup(self.master, self.options,
                                                                               self.on_select_pattern,
                                                                               self.pattern_selected))
        self.edit_pattern.grid(row=1, column=3, sticky='nse')

    def on_select_pattern(self, pattern: str):
        # Save selected pattern to var
        self.pattern_selected = pattern
        #print(self.pattern_selected)

        # Update UI with information
        self.sweater_type_btn.grid_forget()
        tk.Label(self.selection_frame, text=self.pattern_selected, font=self.input_font).grid(row=1, column=1,
                                                                                              sticky='nsew')

    def select_standard_size(self):
        def on_press():
            if self.pattern_selected is None:
                messagebox.showwarning("Pattern Not Selected", "Please select a pattern before choosing a size.")
            else:
                PatternPopups.size_popup(self.master, self.on_size_confirm, self.pattern_selected, self.size_selected)

        btn = tk.Button(self, text='Standard Sizes', command=on_press)
        btn.grid(row=2, column=0, sticky='nsew')

    def on_size_confirm(self, swatch_args, torso_args, sleeve_args, size):
        # Save selected size to var
        self.size_selected = size

        self.on_swatch_confirm(*swatch_args)
        self.on_torso_confirm(*torso_args)
        self.on_sleeve_confirm(*sleeve_args)

    def swatch_dimensions(self):
        tk.Label(self.swatch_frame, text='Swatch Info: ', font=self.subheader).grid(row=0, column=0,
                                                                                    sticky='nsew')
        self.swatch_btn = Button(self.swatch_frame, text='Select', height=22, width=55,
                                 command=lambda: PatternPopups.swatch_popup(self.master, self.on_swatch_confirm))
        self.swatch_btn.grid(row=3, column=2, sticky='e')
        tk.Label(self.swatch_frame, text='Width:').grid(row=1, column=0, sticky='nsew')
        tk.Label(self.swatch_frame, text='Height:').grid(row=2, column=0, sticky='nsew')
        tk.Label(self.swatch_frame, text='Stitches:').grid(row=3, column=0, sticky='nsew')
        tk.Label(self.swatch_frame, text='Rows:').grid(row=4, column=0, sticky='nsew')
        tk.Label(self.swatch_frame, text='Needle Size:').grid(row=5, column=0, sticky='nsew')

        # Pack Swatch Frame
        self.swatch_frame.grid(row=3, column=0, columnspan=3, sticky='nsew')

        # Edit Button
        self.edit_swatch = Button(self, text='Edit', width=50,
                                  command=lambda: PatternPopups.swatch_popup(self.master, self.on_swatch_confirm,
                                                                             self.swatch_selected))
        self.edit_swatch.grid(row=4, column=3, sticky='nse')

    def on_swatch_confirm(self, width, height, stitches, rows, needle_size):
        # Save selected values to var
        self.swatch_selected = [width, height, stitches, rows, needle_size]

        # Logs
        print('swatch: ', width, height, stitches, rows, needle_size)

        # Create Swatch Object
        self.swatch = Swatch(width, height, stitches, rows)

        # Set Needle_Size
        self.needle_size = needle_size

        # Clear Select Button
        self.swatch_btn.grid_forget()

        # Fill Values
        tk.Label(self.swatch_frame, text=f'{width} {self.unit}', font=self.input_font).grid(row=1, column=1,
                                                                                            sticky='nsew')
        tk.Label(self.swatch_frame, text=f'{height} {self.unit}', font=self.input_font).grid(row=2, column=1,
                                                                                             sticky='nsew')
        tk.Label(self.swatch_frame, text=f'{stitches} {self.unit}', font=self.input_font).grid(row=3, column=1,
                                                                                               sticky='nsew')
        tk.Label(self.swatch_frame, text=f'{rows} {self.unit}', font=self.input_font).grid(row=4, column=1,
                                                                                           sticky='nsew')
        tk.Label(self.swatch_frame, text=f'{needle_size} {'mm'}', font=self.input_font).grid(row=5, column=1,
                                                                                             sticky='nsew')

    def torso_dimensions(self):
        tk.Label(self.torso_frame, text='Torso Dimensions:', font=self.subheader).grid(row=0, column=0, sticky='nsew')
        self.torso_btn = Button(self.torso_frame, text='Select', height=22, width=55,
                                command=lambda: PatternPopups.torso_popup(self.master,
                                                                          self.on_torso_confirm))
        self.torso_btn.grid(row=4, column=2, sticky='nse')
        tk.Label(self.torso_frame, text='Width:').grid(row=1, column=0, sticky='nsew')
        tk.Label(self.torso_frame, text='Height:').grid(row=2, column=0, sticky='nsew')
        tk.Label(self.torso_frame, text='Ribbing:').grid(row=3, column=0, sticky='nsew')
        tk.Label(self.torso_frame, text='Taper Offset:').grid(row=4, column=0, sticky='nsew')
        tk.Label(self.torso_frame, text='Taper Hem:').grid(row=5, column=0, sticky='nsew')
        tk.Label(self.torso_frame, text='Neck Offset Width:').grid(row=6, column=0, sticky='nsew')
        tk.Label(self.torso_frame, text='Neck Offset Height:').grid(row=7, column=0, sticky='nsew')
        tk.Label(self.torso_frame, text='Neck Depth:').grid(row=8, column=0, sticky='nsew')

        # Pack Torso Frame
        self.torso_frame.grid(row=5, column=0, columnspan=3, sticky='nsew')

        # Edit Button
        self.edit_torso = Button(self, text='Edit', width=50,
                                 command=lambda: PatternPopups.torso_popup(self.master, self.on_torso_confirm,
                                                                           self.torso_selected))
        self.edit_torso.grid(row=6, column=3, sticky='nse')

    def on_torso_confirm(self, width, height, ribbing, taper, neck):
        # Save selected values to var
        _ribbing = ribbing
        _taper = taper
        _neck = neck
        print(f'inside on_torso taper is {_taper}')
        # Deal with trying to parse None later, now
        if taper is not None:
            _taper = taper.copy()
        if _neck is not None:
            _neck = neck.copy()

        self.torso_selected = [width, height, _ribbing, _taper, _neck]

        # Logs
        print('torso: ', width, height, _ribbing, _taper, _neck)

        # Torso Class Dealings
        self.front_torso = FrontTorso(width, height, ribbing, taper, neck)  # For this pattern it is the same
        self.back_torso = BackTorso(width, height, ribbing, taper, neck)  # ^^^

        # Formating
        if ribbing is None:
            ribbing = 'N/A'

        if taper is not None:
            print('_taper passed as not None ', taper)
            taper[0] = f'{taper[0]} {self.unit}'
            taper[1] = f'{taper[1]} {self.unit}'
        else:
            print('_taper changing as is None ', taper)
            taper = ['N/A', 'N/A']
            print('changed taper', taper)

        if neck is not None:
            neck[0] = f'{neck[0]} {self.unit}'
            neck[1] = f'{neck[1]} {self.unit}'
            neck[2] = f'{neck[2]} {self.unit}'
        else:
            neck = ['N/A', 'N/A', 'N/A']

        # Clear Select Button
        self.torso_btn.grid_forget()

        # Fill Values
        tk.Label(self.torso_frame, text=f'{width} {self.unit}', font=self.input_font).grid(row=1, column=1,
                                                                                           sticky='nsew')
        tk.Label(self.torso_frame, text=f'{height} {self.unit}', font=self.input_font).grid(row=2, column=1,
                                                                                            sticky='nsew')
        tk.Label(self.torso_frame, text=ribbing, font=self.input_font).grid(row=3, column=1, sticky='nsew')

        tk.Label(self.torso_frame, text=taper[0], font=self.input_font).grid(row=4, column=1, sticky='nsew')
        tk.Label(self.torso_frame, text=taper[1], font=self.input_font).grid(row=5, column=1, sticky='nsew')

        tk.Label(self.torso_frame, text=neck[0], font=self.input_font).grid(row=6, column=1, sticky='nsew')
        tk.Label(self.torso_frame, text=neck[1], font=self.input_font).grid(row=7, column=1, sticky='nsew')
        tk.Label(self.torso_frame, text=neck[2], font=self.input_font).grid(row=8, column=1, sticky='nsew')

    def sleeve_dimensions(self):
        tk.Label(self.sleeve_frame, text='Sleeve Dimensions:', font=self.subheader).grid(row=0, column=0, sticky='nsew')
        self.sleeve_btn = Button(self.sleeve_frame, text='Select', height=22, width=55,
                                 command=lambda: PatternPopups.sleeve_popup(self.master,
                                                                            self.on_sleeve_confirm))
        self.sleeve_btn.grid(row=4, column=2, sticky='nse')
        tk.Label(self.sleeve_frame, text='Width:').grid(row=1, column=0, sticky='nsew')
        tk.Label(self.sleeve_frame, text='Height:').grid(row=2, column=0, sticky='nsew')
        tk.Label(self.sleeve_frame, text='Ribbing:').grid(row=3, column=0, sticky='nsew')
        tk.Label(self.sleeve_frame, text='Taper Offset:').grid(row=4, column=0, sticky='nsew')
        tk.Label(self.sleeve_frame, text='Taper Hem:').grid(row=5, column=0, sticky='nsew')
        tk.Label(self.sleeve_frame, text='Taper Style:').grid(row=6, column=0, sticky='nsew')
        tk.Label(self.sleeve_frame, text='Neck Offset Width:').grid(row=7, column=0, sticky='nsew')
        tk.Label(self.sleeve_frame, text='Neck Offset Height:').grid(row=8, column=0, sticky='nsew')
        tk.Label(self.sleeve_frame, text='Neck Depth:').grid(row=9, column=0, sticky='nsew')

        # Pack Sleeve Frame
        self.sleeve_frame.grid(row=7, column=0, columnspan=3, sticky='nsew')

        # Edit Button
        self.edit_sleeve = Button(self, text='Edit', width=50,
                                  command=lambda: PatternPopups.sleeve_popup(self.master, self.on_sleeve_confirm,
                                                                             self.sleeve_selected))
        self.edit_sleeve.grid(row=8, column=3, sticky='nse')

    def on_sleeve_confirm(self, width, height, ribbing, taper, neck):
        # Save selected values to var
        _ribbing = ribbing
        _taper = taper
        _neck = neck

        # Deal with trying to parse None later, now
        if taper is not None:
            #Default taper_style if input was typed incorrectly
            if taper[2] != 'both' or taper[2] != 'bottom' or taper[2] != 'top':
                taper[2] = 'both'
            _taper = taper.copy()
        if _neck is not None:
            _neck = neck.copy()

        self.sleeve_selected = [width, height, _ribbing, _taper, _neck]

        # Logs
        print('sleeve: ', width, height, _ribbing, _taper, _neck)

        # Torso Class Dealings
        self.left_sleeve = LeftSleeve(width, height, ribbing, taper, neck)  # For this pattern it is the same
        self.right_sleeve = RightSleeve(width, height, ribbing, taper, neck)  # ^^^

        # Formating
        if ribbing is None:
            ribbing = 'N/A'

        if taper is not None:
            taper[0] = f'{taper[0]} {self.unit}'
            taper[1] = f'{taper[1]} {self.unit}'
        else:
            taper = ['N/A', 'N/A', 'both']

        if neck is not None:
            neck[0] = f'{neck[0]} {self.unit}'
            neck[1] = f'{neck[1]} {self.unit}'
            neck[2] = f'{neck[2]} {self.unit}'
        else:
            neck = ['N/A', 'N/A', 'N/A']

        # Clear Select Button
        self.sleeve_btn.grid_forget()

        # Fill Values
        tk.Label(self.sleeve_frame, text=f'{width} {self.unit}', font=self.input_font).grid(row=1, column=1,
                                                                                            sticky='nsew')
        tk.Label(self.sleeve_frame, text=f'{height} {self.unit}', font=self.input_font).grid(row=2, column=1,
                                                                                             sticky='nsew')
        tk.Label(self.sleeve_frame, text=ribbing, font=self.input_font).grid(row=3, column=1, sticky='nsew')

        tk.Label(self.sleeve_frame, text=taper[0], font=self.input_font).grid(row=4, column=1, sticky='nsew')
        tk.Label(self.sleeve_frame, text=taper[1], font=self.input_font).grid(row=5, column=1, sticky='nsew')
        tk.Label(self.sleeve_frame, text=taper[2], font=self.input_font).grid(row=6, column=1, sticky='nsew')

        tk.Label(self.sleeve_frame, text=neck[0], font=self.input_font).grid(row=7, column=1, sticky='nsew')
        tk.Label(self.sleeve_frame, text=neck[1], font=self.input_font).grid(row=8, column=1, sticky='nsew')
        tk.Label(self.sleeve_frame, text=neck[2], font=self.input_font).grid(row=9, column=1, sticky='nsew')

    def compile_button(self):
        def on_press():
            async def run_calculations():
                if (self.front_torso is not None and self.back_torso is not None and
                        self.left_sleeve is not None and self.right_sleeve is not None and
                        self.pattern_selected is not None):

                    self.sweater = Sweater(
                        front_torso=self.front_torso,
                        back_torso=self.back_torso,
                        left_sleeve=self.left_sleeve,
                        right_sleeve=self.right_sleeve,
                        swatch=self.swatch,
                        needle_size=self.needle_size
                    )

                    await self.sweater.do_calculations()

                    self.parent.add_pattern_display(self.sweater)
                    self.parent.display_pattern()
                    # self.sweater_image = self.sweater.printSweater()

                    # self.pattern_guide()
                else:
                    PatternPopups.fill_in_fields_popup(self.master)

            # Run the async function using asyncio
            asyncio.run(run_calculations())

        Button(self, text='Compile', command=on_press).grid(row=9, column=0, columnspan=4, pady=5)

    def pattern_guide(self):
        popup = tk.Toplevel(self)
        popup.title("Pattern Guide")
        popup.resizable(False, False)

        def on_press():
            popup.destroy()

        result_text = (
            f'You will be making a {self.pattern_selected} sweater!\n'
            f'Each side of the torso has {round(self.torso.stitches)} stitches and {round(self.torso.rows)} rows.\n'
            f'Each side of the sleeve has {round(self.sleeve.stitches)} stitches and {round(self.sleeve.rows)} rows.\n'
            'To make this sweater, you will need to create 2 of the torso pattern and 4 of the sleeve pattern.'
        )
        tk.Label(popup, text='Pattern Guide', font=tk.font.Font(family="Arial", size=16, weight="bold")).pack(padx=10)
        tk.Label(popup, text=result_text,
                 font=tk.font.Font(family="Arial", size=14, weight="normal")).pack(padx=10)
        img = ImageTk.PhotoImage(self.sweater_image)
        image_label = tk.Label(popup, image=img)
        image_label.image = img
        image_label.pack(padx=10)

        ok_button = Button(popup, text="Okay", command=on_press)
        ok_button.pack(pady=10)

        tf.center_window(popup)
