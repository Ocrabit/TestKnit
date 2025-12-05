import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Tkinter Mac Error Handle
import platform

if platform.system() == 'Darwin':
    from tkmacosx import Button
else:
    from tkinter import Button

from ..tool_functions import tool_functions as tf


class PatternDisplay(ttk.Frame):
    def __init__(self, master, parent, sweater):
        super().__init__(master)
        self.master = master
        self.parent = parent
        self.sweater = sweater

        # Image index and zoom control variables
        self.image_index = 0
        self.zoom_level = 2.0
        self.max_zoom_level = 5.0
        self.min_zoom_level = 0.5

        # For panning
        self.drag_data = {"x": 0, "y": 0, "start_x": 0, "start_y": 0}

        # Load images from the sweater object (assuming they are PIL Image objects)
        self.original_images = [image for image in sweater.images]

        # Create Canvas for image display
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create image counter label
        self.image_counter_label = tk.Label(self, text="")
        self.image_counter_label.pack(side=tk.TOP)
        self.part_names = ['Front Torso', 'Back Torso', 'Left Sleeve', 'Right Sleeve']

        # Set the initial size of the window (larger)
        self.master.geometry("800x800")

        # Bind events for zooming and panning
        self.canvas.bind("<MouseWheel>", self.zoom_image)
        self.canvas.bind("<Configure>", self.update_image)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan_image)
        self.canvas.bind("<ButtonRelease-1>", self.end_pan)

        # Display the first image
        self.canvas_image = None  # Initialize self.canvas_image to None
        self.update_image()

        # Navigation buttons
        Button(self, text='Previous', command=self.show_previous_image).pack(side=tk.LEFT)
        Button(self, text='Next', command=self.show_next_image).pack(side=tk.RIGHT)
        Button(self, text='Back', command=lambda: self.parent.select_pattern()).pack(side=tk.BOTTOM)

        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Center the window
        self.update_idletasks()
        tf.center_window(self.master)

    def update_image(self, event=None):
        # Resize the image based on the current zoom level, applying limits
        image = self.original_images[self.image_index].resize(
            (int(self.original_images[self.image_index].width * self.zoom_level),
             int(self.original_images[self.image_index].height * self.zoom_level)),
            Image.LANCZOS
        )

        self.photo_image = ImageTk.PhotoImage(image)

        # Clear the canvas
        self.canvas.delete("all")

        # Calculate the coordinates to draw the image
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width = self.photo_image.width()
        image_height = self.photo_image.height()

        # Determine the new position for the image
        if self.canvas_image:
            # Get the current center position of the image if it exists
            coords = self.canvas.coords(self.canvas_image)
            if coords:
                x_center, y_center = coords[0], coords[1]
            else:
                # Set to center if coords are not available
                x_center = (canvas_width - image_width) / 2
                y_center = (canvas_height - image_height) / 2
        else:
            # Set to center if this is the first time displaying
            x_center = (canvas_width - image_width) / 2
            y_center = (canvas_height - image_height) / 2

        # Draw the image on the canvas
        self.canvas_image = self.canvas.create_image(x_center, y_center, anchor=tk.NW, image=self.photo_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))  # Update scroll region

        # Update the image counter label
        self.image_counter_label.config(
            text=f"{self.part_names[self.image_index]} \nImage {self.image_index + 1} of {len(self.original_images)}"
        )

    def show_next_image(self):
        # Move to the next image, wrap around if at the end
        self.image_index = (self.image_index + 1) % len(self.original_images)
        self.zoom_level = 3.0
        self.update_image()

    def show_previous_image(self):
        # Move to the previous image, wrap around if at the beginning
        self.image_index = (self.image_index - 1) % len(self.original_images)
        self.zoom_level = 3.0
        self.update_image()

    def zoom_image(self, event):
        # Get the current mouse position on the canvas
        mouse_x = self.canvas.canvasx(event.x)
        mouse_y = self.canvas.canvasy(event.y)

        # Get the position of the image on the canvas
        coords = self.canvas.coords(self.canvas_image)
        if not coords:
            return  # Prevent further execution if coordinates are not available
        image_x, image_y = coords[0], coords[1]

        # Calculate the offset of the mouse from the image's top-left corner
        offset_x = mouse_x - image_x
        offset_y = mouse_y - image_y

        # Store the current zoom level before updating
        old_zoom_level = self.zoom_level

        # Zoom in/out with mouse wheel, applying zoom limits
        if event.delta > 0 and self.zoom_level < self.max_zoom_level:
            self.zoom_level *= 1.1  # Zoom in
        elif event.delta < 0 and self.zoom_level > self.min_zoom_level:
            self.zoom_level /= 1.1  # Zoom out

        # Update the image
        self.update_image()

        # Calculate the scaling factor
        scaling_factor = self.zoom_level / old_zoom_level

        # Calculate new offsets
        new_offset_x = offset_x * scaling_factor
        new_offset_y = offset_y * scaling_factor

        # Calculate the new top-left corner position of the image
        new_image_x = mouse_x - new_offset_x
        new_image_y = mouse_y - new_offset_y

        # Move the image to the new position
        self.canvas.coords(self.canvas_image, new_image_x, new_image_y)

    def start_pan(self, event):
        # Save the starting point of the drag
        self.drag_data["start_x"] = event.x
        self.drag_data["start_y"] = event.y

    def pan_image(self, event):
        # Calculate the distance moved
        dx = event.x - self.drag_data["start_x"]
        dy = event.y - self.drag_data["start_y"]

        # Move the canvas image
        self.canvas.move(self.canvas_image, dx, dy)

        # Update the drag_data with new position
        self.drag_data["start_x"] = event.x
        self.drag_data["start_y"] = event.y

    def end_pan(self, event):
        # Reset drag data
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0