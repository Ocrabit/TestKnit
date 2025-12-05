import platform
import tkinter as tk
from tkinter import ttk

# Tkinter Mac Error Handle
import platform

if platform.system() == 'Darwin':
    from tkmacosx import Button

    print('mac os')
else:
    from tkinter import Button

from PIL import Image, ImageTk

# Tools
from ..tool_functions import tool_functions as tf


class PatternPopups:
    # Class-level variables to track popups
    pattern_popup_window = None
    torso_popup_window = None
    sleeve_popup_window = None
    swatch_popup_window = None
    size_popup_window = None
    torso_child_popup_window = None
    sleeve_child_popup_window = None

    @staticmethod
    def pattern_popup(master, options, callback_function, autofill=None):
        # Check if the popup is already open
        if PatternPopups.pattern_popup_window is not None and tk.Toplevel.winfo_exists(
                PatternPopups.pattern_popup_window):
            PatternPopups.pattern_popup_window.focus_force()  # Refocus existing popup
            tf.center_on_parent_window(master, PatternPopups.pattern_popup_window)  # Recenter existing popup
            return  # Do nothing if the popup is already open

        # Create a Toplevel window (popup)
        popup = tk.Toplevel(master)
        popup.title("Select a Sweater Pattern")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        # Assign the popup window to the class-level variable
        PatternPopups.pattern_popup_window = popup

        # When the popup is closed, reset the variable
        def on_close():
            PatternPopups.pattern_popup_window = None
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        tk.Label(popup, text="Please select a sweater pattern:").pack(pady=10)

        # Listbox to display options
        listbox = tk.Listbox(popup, height=len(options))
        listbox.pack(pady=10)

        # Populate the Listbox with pattern options
        for pattern in options:
            listbox.insert(tk.END, pattern)

        # Select Autofill if applicable
        # print(f'autofill {autofill}')
        if autofill is not None:
            for index, pattern in enumerate(options):
                if pattern == autofill:
                    listbox.selection_set(index)

        def confirm_pattern_selection():
            # Get the selected pattern
            selected_index = listbox.curselection()

            if selected_index:
                pattern_selected = listbox.get(selected_index)

                callback_function(pattern_selected)

                # Close the popup
                popup.destroy()
            else:
                tk.Label(popup, text="Please select a pattern before confirming.").pack(pady=10)

        # Button to confirm selection
        confirm_button = Button(popup, text="Confirm", command=confirm_pattern_selection)
        confirm_button.pack(pady=10)

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: confirm_pattern_selection())

    @staticmethod
    def size_popup(master, callback_function, pattern, autofill=None):
        # Check if the popup is already open
        if PatternPopups.size_popup_window is not None and tk.Toplevel.winfo_exists(
                PatternPopups.size_popup_window):
            PatternPopups.size_popup_window.focus_force()  # Refocus existing popup
            tf.center_on_parent_window(master, PatternPopups.size_popup_window)  # Recenter existing popup
            return  # Do nothing if the popup is already open

        # Create a Toplevel window (popup)
        popup = tk.Toplevel(master)
        popup.title("Presets")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        # Assign the popup window to the class-level variable
        PatternPopups.size_popup_window = popup

        # When the popup is closed, reset the variable
        def on_close():
            PatternPopups.size_popup_window = None
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        # Sizes
        sizes = ['extra small (XS)', 'small (S)', 'medium (M)', 'large (L)', 'extra large (XL)']

        tk.Label(popup, text="Please select a preset size:").pack(pady=10)

        # Listbox to display options
        listbox = tk.Listbox(popup, height=len(sizes))
        listbox.pack(pady=10)

        # Populate the Listbox with pattern options
        for size in sizes:
            listbox.insert(tk.END, size)

        # Select Autofill if applicable
        if autofill is not None:
            for index, size in enumerate(sizes):
                if size == autofill:
                    listbox.selection_set(index)

        def confirm_selection():
            # Get the selected pattern
            selected_index = listbox.curselection()

            if selected_index:
                # Get the selected size from listbox
                size_selected = listbox.get(selected_index)

                # Pull json values for standard size selected
                swatch, torso, sleeve, needle_size = tf.standard_size_values(pattern, size_selected)

                print(needle_size)
                # Parse json to respective args
                swatch_args = [float(swatch['width']), float(swatch['height']), float(swatch['stitches']),
                               float(swatch['rows']), needle_size]
                torso_args = [float(torso['width']), float(torso['height']), torso['ribbing'],
                              [float(torso['taper_offset']), float(torso['taper_hem'])],
                              [float(torso['neck_offset_width']), float(torso['neck_offset_height']), float(torso['neck_depth'])]]
                sleeve_args = [float(sleeve['width']), float(sleeve['height']), sleeve['ribbing'],
                               [float(sleeve['taper_offset']), float(sleeve['taper_hem']), sleeve['taper_style']],
                               [float(sleeve['neck_offset_width']), float(sleeve['neck_offset_height']), float(sleeve['neck_depth'])]]

                # Send back args
                callback_function(swatch_args, torso_args, sleeve_args, size_selected)

                # Close the popup
                popup.destroy()
            else:
                # Close the popup
                popup.destroy()
                # Call Missing Popup Notifier
                PatternPopups.missing_popup(master, lambda: PatternPopups.size_popup(master, callback_function, pattern, autofill))

        # Button to confirm selection
        confirm_button = Button(popup, text="Confirm", command=confirm_selection)
        confirm_button.pack(pady=10)

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: confirm_selection())

    @staticmethod
    def swatch_popup(master, callback_function, autofill=None):
        # Check if the popup is already open
        if PatternPopups.swatch_popup_window is not None and tk.Toplevel.winfo_exists(
                PatternPopups.swatch_popup_window):
            PatternPopups.swatch_popup_window.focus_force()  # Refocus existing popup
            tf.center_on_parent_window(master, PatternPopups.swatch_popup_window)  # Recenter existing popup
            return  # Do nothing if the popup is already open

        # Toplevel for Torso dimensions
        popup = tk.Toplevel(master)
        popup.title("Swatch Dimensions")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        # Assign the popup window to the class-level variable
        PatternPopups.swatch_popup_window = popup

        # When the popup is closed, reset the variable
        def on_close():
            PatternPopups.swatch_popup_window = None
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        tk.Label(popup, text="Enter the swatch details:", justify='center').grid(row=0, column=0, columnspan=2, pady=10,
                                                                                 padx=10)

        # Width
        tk.Label(popup, text="Width:").grid(row=1, column=0)
        width_entry = tk.Entry(popup, justify="center", width=5)
        width_entry.grid(row=1, column=1)

        # Height
        tk.Label(popup, text="Height:").grid(row=2, column=0)
        height_entry = tk.Entry(popup, justify="center", width=5)
        height_entry.grid(row=2, column=1)

        # Stitches
        tk.Label(popup, text="Stitches:").grid(row=3, column=0)
        stitches_entry = tk.Entry(popup, justify="center", width=5)
        stitches_entry.grid(row=3, column=1)

        # Rows
        tk.Label(popup, text="Rows:").grid(row=4, column=0)
        rows_entry = tk.Entry(popup, justify="center", width=5)
        rows_entry.grid(row=4, column=1)

        # Needle Size
        tk.Label(popup, text="Needle Size: (mm)").grid(row=5, column=0)
        needle_size_entry = tk.Entry(popup, justify="center", width=5)
        needle_size_entry.grid(row=5, column=1)

        # Select Autofill if applicable
        if autofill is not None:
            width_entry.insert(0, float(autofill[0]))
            height_entry.insert(0, float(autofill[1]))
            stitches_entry.insert(0, float(autofill[2]))
            rows_entry.insert(0, float(autofill[3]))
            needle_size_entry.insert(0, float(autofill[4]))

        def confirm_dimensions():
            # Handle No Response
            if (not tf.is_number(width_entry.get()) or not tf.is_number(height_entry.get()) or
                    not tf.is_number(stitches_entry.get()) or not tf.is_number(rows_entry.get()) or not tf.is_number(needle_size_entry.get())):
                PatternPopups.missing_popup(master, lambda: PatternPopups.swatch_popup(master, callback_function, autofill))
                popup.destroy()
                return

            # Set Values
            width = float(width_entry.get())
            length = float(height_entry.get())
            stitches = float(stitches_entry.get())
            rows = float(rows_entry.get())
            needle_size = float(needle_size_entry.get())

            # Return information
            callback_function(width, length, stitches, rows, needle_size)

            # Close Popup
            popup.destroy()

        # Confirm button
        confirm_button = Button(popup, text="Confirm",
                                command=confirm_dimensions)
        confirm_button.grid(row=6, column=1)

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: confirm_dimensions())

    @staticmethod
    def torso_popup(master, callback_function, autofill=None):
        # Check if the popup is already open
        if PatternPopups.torso_popup_window is not None and tk.Toplevel.winfo_exists(PatternPopups.torso_popup_window):
            if PatternPopups.torso_child_popup_window is not None and tk.Toplevel.winfo_exists(
                    PatternPopups.torso_child_popup_window):
                PatternPopups.torso_child_popup_window.focus_force()
                tf.center_on_parent_window(master, PatternPopups.torso_child_popup_window)
                return
            PatternPopups.torso_popup_window.focus_force()  # Refocus existing popup
            tf.center_on_parent_window(master, PatternPopups.torso_popup_window)  # Recenter existing popup
            return  # Do nothing if the popup is already open

        # Toplevel for Torso dimensions
        popup = tk.Toplevel(master)
        popup.title("Torso Dimensions")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        # Assign the popup window to the class-level variable
        PatternPopups.torso_popup_window = popup

        # When the popup is closed, reset the variable
        def on_close():
            PatternPopups.torso_popup_window = None
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        # Width and Length
        tk.Label(popup, text="Torso Width (inches):").pack(pady=5)
        width_entry = tk.Entry(popup, justify='center', width=12)
        width_entry.pack(pady=5)

        tk.Label(popup, text="Torso Length (inches):").pack(pady=5)
        height_entry = tk.Entry(popup, justify='center', width=12)
        height_entry.pack(pady=5)

        # Ribbing
        ribbing_var = tk.IntVar()
        tk.Checkbutton(popup, text="Add Ribbing", variable=ribbing_var).pack(pady=5)

        # Taper
        taper_var = tk.IntVar()
        tk.Checkbutton(popup, text="Add Taper", variable=taper_var).pack(pady=5)

        # Neck
        neck_var = tk.IntVar()
        tk.Checkbutton(popup, text="Add Neck", variable=neck_var).pack(pady=5)

        # Select Autofill if applicable
        if autofill is not None:
            width_entry.insert(0, autofill[0])
            height_entry.insert(0, autofill[1])

        def confirm_dimensions():
            # Handle Open Child
            if PatternPopups.torso_child_popup_window is not None and tk.Toplevel.winfo_exists(
                    PatternPopups.torso_child_popup_window):
                PatternPopups.torso_child_popup_window.focus_force()
                tf.center_on_parent_window(master, PatternPopups.torso_child_popup_window)
                return

            # Handle No Response
            if not tf.is_number(width_entry.get()) or not tf.is_number(height_entry.get()):
                PatternPopups.missing_popup(master,
                                            lambda: PatternPopups.torso_popup(master, callback_function, autofill))
                popup.destroy()
                return

            # Set Vars
            width = float(width_entry.get())
            height = float(height_entry.get())
            if autofill is not None:
                ribbing = autofill[2]
                taper = autofill[3]
                neck = autofill[4]
            else:
                ribbing = None
                taper = None
                neck = None

            # Ask Details
            if ribbing_var.get():
                if autofill is not None:
                    ribbing = PatternPopups.ribbing_popup(popup, 'torso', autofill[2])
                else:
                    ribbing = PatternPopups.ribbing_popup(popup, 'torso')

            if taper_var.get():
                if autofill is not None:
                    taper = PatternPopups.taper_popup(popup, height, 'torso', autofill[3])
                    print(f'taper was {taper}')
                else:
                    taper = PatternPopups.taper_popup(popup, height, 'torso')

            if neck_var.get():
                if autofill is not None:
                    neck = PatternPopups.neck_popup(popup, autofill[4])
                    print(f'neck was {neck}')
                else:
                    neck = PatternPopups.neck_popup(popup)  ##### DO THISSSS  ######

            # Return Information
            callback_function(width, height, ribbing, taper, neck)

            popup.destroy()

        # Confirm button
        confirm_button = Button(popup, text="Confirm", command=confirm_dimensions)
        confirm_button.pack(pady=10)

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: confirm_dimensions())

    @staticmethod
    def sleeve_popup(master, callback_function, autofill=None):
        # Check if the popup is already open
        if PatternPopups.sleeve_popup_window is not None and tk.Toplevel.winfo_exists(
                PatternPopups.sleeve_popup_window):
            if PatternPopups.sleeve_child_popup_window is not None and tk.Toplevel.winfo_exists(
                    PatternPopups.sleeve_child_popup_window):
                PatternPopups.sleeve_child_popup_window.focus_force()
                tf.center_on_parent_window(master, PatternPopups.sleeve_popup_window)
                return
            PatternPopups.sleeve_popup_window.focus_force()  # Refocus existing popup
            tf.center_on_parent_window(master, PatternPopups.sleeve_popup_window)  # Recenter existing popup
            return  # Do nothing if the popup is already open

        # Toplevel for Torso dimensions
        popup = tk.Toplevel(master)
        popup.title("Sleeve Dimensions")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        # Assign the popup window to the class-level variable
        PatternPopups.sleeve_popup_window = popup

        # When the popup is closed, reset the variable
        def on_close():
            PatternPopups.torso_popup_window = None
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        # Width and Height
        tk.Label(popup, text="Sleeve Width (inches):").pack(pady=5)
        width_entry = tk.Entry(popup, justify='center', width=12)
        width_entry.pack(pady=5)

        tk.Label(popup, text="Sleeve Length (inches):").pack(pady=5)
        height_entry = tk.Entry(popup, justify='center', width=12)
        height_entry.pack(pady=5)

        # Ribbing
        ribbing_var = tk.IntVar()
        tk.Checkbutton(popup, text="Add Ribbing", variable=ribbing_var).pack(pady=5)

        # Taper
        taper_var = tk.IntVar()
        tk.Checkbutton(popup, text="Add Taper", variable=taper_var).pack(pady=5)

        # Neck
        neck_var = tk.IntVar()
        tk.Checkbutton(popup, text="Add Neck (to sleeve)", variable=neck_var).pack(pady=5)

        # Select Autofill if applicable
        if autofill is not None:
            width_entry.insert(0, autofill[0])
            height_entry.insert(0, autofill[1])

        def confirm_dimensions():
            # Handle Open Child
            if PatternPopups.sleeve_child_popup_window is not None and tk.Toplevel.winfo_exists(
                    PatternPopups.sleeve_child_popup_window):
                PatternPopups.sleeve_child_popup_window.focus_force()
                tf.center_on_parent_window(master, PatternPopups.sleeve_child_popup_window)
                return

            # Handle No Response
            if not tf.is_number(width_entry.get()) or not tf.is_number(height_entry.get()):
                PatternPopups.missing_popup(master,
                                            lambda: PatternPopups.sleeve_popup(master, callback_function, autofill))
                popup.destroy()
                return

            # Set Vars
            width = float(width_entry.get())
            height = float(height_entry.get())
            if autofill is not None:
                ribbing = autofill[2]
                taper = autofill[3]
                neck = autofill[4]
            else:
                ribbing = None
                taper = None
                neck = None

            # Ask Details
            if ribbing_var.get():
                if autofill is not None:
                    ribbing = PatternPopups.ribbing_popup(popup, 'sleeve', autofill[2])
                else:
                    ribbing = PatternPopups.ribbing_popup(popup, 'sleeve')

            if taper_var.get():
                if autofill is not None:
                    taper = PatternPopups.taper_popup(popup, height, 'sleeve', autofill[3])  # autofill has 2 values, popup returns 3
                    print(f'taper was {taper}')
                else:
                    taper = PatternPopups.taper_popup(popup, height, 'sleeve')

            if neck_var.get():
                if autofill is not None:
                    neck = PatternPopups.neck_popup(popup, autofill[4])
                    print(f'neck was {neck}')
                else:
                    neck = PatternPopups.neck_popup(popup)

            # Return Information
            callback_function(width, height, ribbing, taper, neck)

            popup.destroy()

        # Confirm button
        confirm_button = Button(popup, text="Confirm", command=confirm_dimensions)
        confirm_button.pack(pady=10)

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: confirm_dimensions())

    @staticmethod
    def ribbing_popup(master, window: str, autofill=None):
        #Initialize Window
        popup = tk.Toplevel(master)
        popup.title("Ribbing Options")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        if window == 'torso':
            # Assign popup
            PatternPopups.torso_child_popup_window = popup
        else:
            PatternPopups.sleeve_child_popup_window = popup

        # Set Close Function
        def on_close():
            if window == 'torso':
                PatternPopups.torso_child_popup_window = None
            else:
                PatternPopups.sleeve_child_popup_window = None
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        # Set UI
        tk.Label(popup, text="Select ribbing thickness:").pack(pady=5)
        ribbing_options = ["thick", "normal", "thin"]
        ribbing = tk.StringVar(value='normal')

        # Create array of btns in order to select preset val with autofill
        radio_btns = []
        for option in ribbing_options:
            btn = tk.Radiobutton(popup, text=option.capitalize(), variable=ribbing, value=option)
            radio_btns += [btn]
            btn.pack(pady=5)

        # Select autofill if applicable
        if autofill is not None:
            for index, thickness in enumerate(ribbing_options):
                if thickness == autofill:
                    radio_btns[index].invoke()

        # Confirm Button
        Button(popup, text="Confirm", command=lambda: popup.destroy()).pack(pady=10)

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: popup.destroy())

        # Wait for user to make choice
        popup.wait_window(popup)

        # Return value
        return ribbing.get()

    @staticmethod
    def taper_popup(master, length, window, autofill=None):
        # UI Position
        popup = tk.Toplevel(master)
        popup.title("Taper Options")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        if window == 'torso':
            # Assign popup
            PatternPopups.torso_child_popup_window = popup
        else:
            PatternPopups.sleeve_child_popup_window = popup

        # Set Close Function
        def on_close():
            if window == 'torso':
                # Assign popup
                PatternPopups.torso_child_popup_window = None
            else:
                PatternPopups.sleeve_child_popup_window = None
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        # Vars
        offset = tk.DoubleVar()
        hem_size = tk.DoubleVar()
        taper_style = tk.StringVar()
        _confirm = False

        help_popup: tk.Toplevel = None

        def press_help():
            if help_popup is None:
                h_popup()
            else:
                tf.center_on_parent_window(master, help_popup)
                help_popup.focus_force()

        def h_popup():
            nonlocal help_popup
            help_popup = tk.Toplevel(master)
            if window == 'torso':
                help_popup.title("Recommended Dimension For Torso")
                help_popup.resizable(False, False)

                reco_text = (
                    f'Adding a taper offset for the torso is a common practice depending on the desired fit for the upper arm.'
                    f'\nThe offset will determine how many rows into the torso you go without beginning the decrease to the desired hem size.'
                    f'\nregular fit usually around (2/3 offset): {round(length * 2 / 3, 2)} inches'
                    f'\ntailored fit usually around (1/2 offset): {round(length * 1 / 2, 2)} inches'
                    f'\nlooser fit usually around (1/4 offset): {round(length * 1 / 4, 2)} inches')

                tk.Label(help_popup, text='Tip', font=tk.font.Font(family="Arial", size=16, weight="bold")).pack(
                    padx=10)
                tk.Label(help_popup, text=reco_text, font=tk.font.Font(family="Arial", size=14, weight="normal")).pack(
                    padx=10)
            else:
                help_popup.title("Recommended Dimension For Sleeve")
                help_popup.resizable(False, False)

                reco_text = (
                    f'Adding a taper offset for the sleeve is a common practice depending on the desired fit for the upper arm.'
                    f'\nThe offset will determine how many rows into the sleeve you go without beginning the decrease to the desired hem size.'
                    f'\nregular fit usually around (2/3 offset): {round(length * 2 / 3, 2)} inches'
                    f'\ntailored fit usually around (1/2 offset): {round(length * 1 / 2, 2)} inches'
                    f'\nlooser fit usually around (1/4 offset): {round(length * 1 / 4, 2)} inches')

                tk.Label(help_popup, text='Tip', font=tk.font.Font(family="Arial", size=16, weight="bold")).pack(
                    padx=10)
                tk.Label(help_popup, text=reco_text, font=tk.font.Font(family="Arial", size=14, weight="normal")).pack(
                    padx=10)

            def on_press():
                nonlocal help_popup
                help_popup.destroy()
                help_popup = None

            ok_button = Button(help_popup, text="Okay", command=on_press)
            ok_button.pack(pady=10)
            tf.center_on_parent_window(master, help_popup)

            # Bind the Enter (Return) key
            help_popup.bind('<Return>', lambda event: on_press())

        # Help Button
        from pathlib import Path
        help_img_path = Path(__file__).parent.parent.parent / 'data/assets/icons/help_button.png'
        #print(help_img_path)  # LOGS
        help_img = ImageTk.PhotoImage(Image.open(help_img_path))
        help_btn = Button(popup, image=help_img, width=50, height=50, relief="flat",
                          foreground=master.cget('bg'), background=master.cget('bg'), takefocus=False, borderless=True,
                          command=press_help)
        help_btn.image = help_img
        help_btn.grid(row=0, column=3, sticky='e')

        # UI Label
        tk.Label(popup, text="Enter taper offset (in inches):").grid(row=1, column=0, columnspan=4)
        taper_offset_entry = tk.Entry(popup, width=8, justify='center', textvariable=offset)
        taper_offset_entry.grid(row=2, column=0, columnspan=4)

        tk.Label(popup, text="Enter hem size (in inches):").grid(row=3, column=0, columnspan=4)
        hem_size_entry = tk.Entry(popup, width=8, justify='center', textvariable=hem_size)
        hem_size_entry.grid(row=4, column=0, columnspan=4)

        # Section for SLEEVE
        taper_style_entry = None
        if window != 'torso':
            tk.Label(popup, text='Taper from both sides? Bottom side? Top side? \nEnter: "both" "bottom" or "side"').grid(row=5, column=0, columnspan=4)
            taper_style_entry = tk.Entry(popup, width=8, justify='center', textvariable=taper_style)
            taper_style_entry.grid(row=6, column=0, columnspan=4)

        # Select autofill if applicable
        if autofill is not None:
            # Taper Offset
            taper_offset_entry.delete(0, tk.END)
            taper_offset_entry.insert(0, (float(autofill[0])))
            # Hem_size
            hem_size_entry.delete(0, tk.END)
            hem_size_entry.insert(0, (float(autofill[1])))

        if window != 'torso':
            if autofill is not None:
                taper_style_entry.delete(0, tk.END)
                taper_style_entry.insert(0, (autofill[2]))
            else:
                taper_style_entry.delete(0, tk.END)
                taper_style_entry.insert(0, 'both')

        def confirm():
            if tf.is_number(taper_offset_entry.get()) and tf.is_number(hem_size_entry.get()):
                popup.destroy()
                nonlocal _confirm
                _confirm = True
            else:
                PatternPopups.fill_in_fields_popup(master)

        Button(popup, text="Confirm", command=confirm).grid(row=7, column=0, columnspan=4, sticky='ns')

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: confirm())

        popup.wait_window(popup)

        # Don't return values until they are valid int/float
        if _confirm:
            if window == 'torso':
                return [float(offset.get()), float(hem_size.get())]
            else:
                if taper_style is None or taper_style == '':
                    taper_style = 'both'
                return [float(offset.get()), float(hem_size.get()), taper_style.get().lower().strip()]

        # Handle if they close it early
        if autofill is not None:
            if window == 'torso':
                return [float(autofill[0]), float(autofill[1])]
            else:
                return [float(autofill[0]), float(autofill[1]), autofill[2]]

    @staticmethod
    def neck_popup(master, autofill=None):  #### Make sure this is done
        # UI Position
        popup = tk.Toplevel(master)
        popup.title("Neck Options")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        # Assign popup
        PatternPopups.torso_child_popup_window = popup

        # Set Close Function
        def on_close():
            PatternPopups.torso_child_popup_window = None
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        # Vars
        offset_width = tk.DoubleVar()
        offset_height = tk.DoubleVar()
        neck_depth = tk.DoubleVar()
        _confirm = False

        # UI Label
        tk.Label(popup, text="Enter offset width (in inches):").grid(row=0, column=0, columnspan=4)
        offset_width_entry = tk.Entry(popup, width=8, justify='center', textvariable=offset_width)
        offset_width_entry.grid(row=1, column=0, columnspan=4)

        tk.Label(popup, text="Enter offset height (in inches):").grid(row=2, column=0, columnspan=4)
        offset_height_entry = tk.Entry(popup, width=8, justify='center', textvariable=offset_height)
        offset_height_entry.grid(row=3, column=0, columnspan=4)

        tk.Label(popup, text="Enter neck depth (in inches):").grid(row=4, column=0, columnspan=4)
        neck_depth_entry = tk.Entry(popup, width=8, justify='center', textvariable=neck_depth)
        neck_depth_entry.grid(row=5, column=0, columnspan=4)

        # Select autofill if applicable
        if autofill is not None:
            # Offset Width
            offset_width_entry.delete(0, tk.END)
            offset_width_entry.insert(0, (float(autofill[0])))
            # Offset Height
            offset_height_entry.delete(0, tk.END)
            offset_height_entry.insert(0, (float(autofill[1])))
            # Neck Depth
            neck_depth_entry.delete(0, tk.END)
            neck_depth_entry.insert(0, (float(autofill[1])))

        def confirm():
            if tf.is_number(offset_width_entry.get()) and tf.is_number(offset_height_entry.get()) and tf.is_number(
                    neck_depth_entry.get()):
                popup.destroy()
                nonlocal _confirm
                _confirm = True
            else:
                PatternPopups.fill_in_fields_popup(master)

        Button(popup, text="Confirm", command=confirm).grid(row=6, column=0, columnspan=4, sticky='ns')

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: confirm())

        popup.wait_window(popup)

        # Don't return values until they are valid int/float
        if _confirm:
            return [float(offset_width.get()), float(offset_height.get()), float(neck_depth.get())]

        # Handle if they close it early
        if autofill is not None:
            return [float(autofill[0]), float(autofill[1]), float(autofill[2])]

    @staticmethod
    def missing_popup(master, call_function):
        popup = tk.Toplevel(master)
        popup.title("Missing Options")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        def on_press():
            popup.destroy()
            call_function()

        tk.Label(popup, text='Input Error', font=tk.font.Font(family="Arial", size=16, weight="bold")).pack(padx=10)
        tk.Label(popup, text="Please enter your dimensions again.",
                 font=tk.font.Font(family="Arial", size=14, weight="normal")).pack(padx=10)

        ok_button = Button(popup, text="Okay", command=on_press)
        ok_button.pack(pady=10)

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: on_press())

    @staticmethod
    def fill_in_fields_popup(master, call_function=None):
        popup = tk.Toplevel(master)
        popup.title("Missing Options")
        popup.resizable(False, False)
        tf.center_on_parent_window(master, popup)

        def on_press():
            popup.destroy()
            if call_function is not None:
                call_function()

        tk.Label(popup, text='Input Error', font=tk.font.Font(family="Arial", size=16, weight="bold")).pack(padx=10)
        tk.Label(popup, text="Please fill in all fields correctly.",
                 font=tk.font.Font(family="Arial", size=14, weight="normal")).pack(padx=10)

        ok_button = Button(popup, text="Okay", command=on_press)
        ok_button.pack(pady=10)

        # Bind the Enter (Return) key
        popup.bind('<Return>', lambda event: on_press())

