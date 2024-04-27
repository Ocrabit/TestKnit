import math
import tkinter as tk
from tkinter import ttk

import tkmacosx
from PIL import Image, ImageTk

import ImageClickCanvas as ICC
from CreateGrid import GridTable

import AppKit



class AutoScrollbar(ttk.Scrollbar):
    """ A scrollbar that hides itself if it's not needed. Works only for grid geometry manager """
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with the widget ' + self.__class__.__name__)

    def place(self, **kw):
        raise tk.TclError('Cannot use place with the widget ' + self.__class__.__name__)


class CanvasImage():
    """ Display and zoom image """

    def __init__(self, placeholder, rows: int, columns: int):
        """ Initialize the ImageFrame """
        self.imscale = 1.0  # scale for the canvas image zoom, public for outer classes
        self.__delta = 1.3  # zoom magnitude
        self.__filter = Image.Resampling.LANCZOS  # could be: NEAREST, BILINEAR, BICUBIC and ANTIALIAS
        #self.__previous_state = 0  # previous state of the keyboard
        # Create ImageFrame in placeholder widget
        self.__imframe = ttk.Frame(placeholder)  # placeholder of the ImageFrame object

        #Drawing mode
        self.drawing_mode = True

        #Pan mode
        self.panning_mode = False
        # Panning offsets
        self.pan_offset_x = 0
        self.pan_offset_y = 0

        # Vertical and horizontal scrollbars for canvas
        hbar = AutoScrollbar(self.__imframe, orient='horizontal')
        vbar = AutoScrollbar(self.__imframe, orient='vertical')
        hbar.grid(row=1, column=0, sticky='we')
        vbar.grid(row=0, column=1, sticky='ns')

        # Create canvas and bind it with scrollbars. Public for outer classes
        # Create my own canvas and put image on it
        grid_size = 96
        new_grid = GridTable(rows, columns)
        img = new_grid.gridImage(grid_size)
        self.canvas = ICC.ImageCanvas(self.__imframe, new_grid, img, grid_size)
        self.canvas.config(highlightthickness=0, xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        hbar.configure(command=self.__scroll_x)  # bind scrollbars to the canvas
        vbar.configure(command=self.__scroll_y)

        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda event: self.__show_image())  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.__move_from)  # remember canvas position
        self.canvas.bind('<B1-Motion>', self.__move_to)  # move canvas to the new position
        self.canvas.bind('<MouseWheel>', self.__wheel)  # zoom for Windows and MacOS, but not Linux

        '''# Handle keystrokes in idle mode, because program slows down on a weak computers,
        # when too many key stroke events in the same time
        #self.canvas.bind('<Key>', lambda event: self.canvas.after_idle(self.__keystroke, event))
        #removed'''
        self.__image = img # open image, but don't load it
        self.imwidth, self.imheight = self.__image.size  # public for outer classes

        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle((0, 0, self.imwidth, self.imheight), width=0)
        self.__show_image()  # show image on the canvas
        self.canvas.focus_set()  # set focus on the canvas

    def click(self, event):
        if (self.drawing_mode):
            # Get the coordinates of the click relative to the canvas
            canvas_x = event.x
            canvas_y = event.y

            # Subtract the accumulated panning offset from the click coordinates
            canvas_x -= self.pan_offset_x
            canvas_y -= self.pan_offset_y

            # Get the bounding box of the image on the canvas
            bbox = self.canvas.coords(self.container)
            image_width = bbox[2] - bbox[0]
            image_height = bbox[3] - bbox[1]
            #print(image_width, image_height)

            # Calculate the scale and offset due to zooming and panning
            scale = self.imscale
            offset_x = bbox[0] / scale
            offset_y = bbox[1] / scale

            # Calculate the coordinates of the click on the original image
            image_x = int((canvas_x / scale) - offset_x)
            image_y = int((canvas_y / scale) - offset_y)
            print("({}, {})".format(image_width, image_height))

            #Click original coordinates
            self.canvas.click(image_x, image_y)

            #Place Image
            self.__image = self.canvas.return_image()

            #Show Image
            self.__show_image()

            '''Remember to add in fixing the panning issue. Subtract panned movement'''

    def redraw_figures(self):
        """ Dummy function to redraw figures in the children classes """
        pass

    def __scroll_x(self, *args, **kwargs):
        """ Scroll canvas horizontally and redraw the image """
        self.canvas.xview(*args)  # scroll horizontally
        self.__show_image()  # redraw the image

    def __scroll_y(self, *args, **kwargs):
        """ Scroll canvas vertically and redraw the image """
        self.canvas.yview(*args)  # scroll vertically
        self.__show_image()  # redraw the image

    def __show_image(self):
        """ Show image on the Canvas. Implements correct image zoom almost like in Google Maps """
        box_image = self.canvas.coords(self.container)  # get image area
        box_canvas = (self.canvas.canvasx(0),  # get visible area of the canvas
                      self.canvas.canvasy(0),
                      self.canvas.canvasx(self.canvas.winfo_width()),
                      self.canvas.canvasy(self.canvas.winfo_height()))
        box_img_int = tuple(map(int, box_image))  # convert to integer or it will not work properly
        # Get scroll region box
        box_scroll = [min(box_img_int[0], box_canvas[0]), min(box_img_int[1], box_canvas[1]),
                      max(box_img_int[2], box_canvas[2]), max(box_img_int[3], box_canvas[3])]
        # Horizontal part of the image is in the visible area
        if box_scroll[0] == box_canvas[0] and box_scroll[2] == box_canvas[2]:
            box_scroll[0] = box_img_int[0]
            box_scroll[2] = box_img_int[2]
        # Vertical part of the image is in the visible area
        if box_scroll[1] == box_canvas[1] and box_scroll[3] == box_canvas[3]:
            box_scroll[1] = box_img_int[1]
            box_scroll[3] = box_img_int[3]
        # Convert scroll region to tuple and to integer
        self.canvas.configure(scrollregion=tuple(map(int, box_scroll)))  # set scroll region
        x1 = max(box_canvas[0] - box_image[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(box_canvas[1] - box_image[1], 0)
        x2 = min(box_canvas[2], box_image[2]) - box_image[0]
        y2 = min(box_canvas[3], box_image[3]) - box_image[1]

        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.imwidth)  # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.imheight)  # ...and sometimes not
            image = self.__image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(box_canvas[0], box_img_int[0]),
                                               max(box_canvas[1], box_img_int[1]),
                                               anchor='nw', image=imagetk)

            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def __move_from(self, event):
        if(self.panning_mode):
            """ Remember previous coordinates for scrolling with the mouse """
            self.canvas.scan_mark(event.x, event.y)

            #Store panning clicks
            self.prev_x = event.x
            self.prev_y = event.y

        self.click(event)  #call my function to get info

    def __move_to(self, event):
        if(self.panning_mode):
            #Panning store calculations
            delta_x = event.x - self.prev_x
            delta_y = event.y - self.prev_y
            self.prev_x = event.x
            self.prev_y = event.y

            # Update the accumulated panning offset
            self.pan_offset_x += delta_x
            self.pan_offset_y += delta_y

            """ Drag (move) canvas to the new position """
            self.canvas.scan_dragto(event.x, event.y, gain=1)
            self.__show_image()  # zoom tile and show it on the canvas

    def outside(self, x, y):
        """ Checks if the point (x,y) is outside the image area """
        bbox = self.canvas.coords(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            return False  # point (x,y) is inside the image area
        else:
            return True  # point (x,y) is outside the image area

    def __wheel(self, event):
        """ Zoom with mouse wheel """
        x = self.canvas.canvasx(event.x)  # get coordinates of the event on the canvas
        y = self.canvas.canvasy(event.y)
        if self.outside(x, y): return  # zoom only inside image area
        scale = 1.0
        # Respond to Mac wheel event
        if event.num == 5 or event.delta < 0:  # scroll down, smaller
            i = min(self.imwidth, self.imheight)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.__delta
            scale /= self.__delta
        if event.num == 4 or event.delta > 0:  # scroll up, bigger
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.__delta
            scale *= self.__delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all objects
        # Redraw some figures before showing image on the screen
        self.redraw_figures()  # method for child classes
        self.__show_image()

    '''def __keystroke(self, event):
        """ Scrolling with the keyboard.
            Independent from the language of the keyboard, CapsLock, <Ctrl>+<key>, etc. """
        if event.state - self.__previous_state == 4:  # means that the Control key is pressed
            pass  # do nothing if Control key is pressed
        else:
            self.__previous_state = event.state  # remember the last keystroke state
            # Up, Down, Left, Right keystrokes
            if event.keycode in [68, 39, 102]:  # scroll right: keys 'D', 'Right' or 'Numpad-6'
                self.__scroll_x('scroll',  1, 'unit', event=event)
            elif event.keycode in [65, 37, 100]:  # scroll left: keys 'A', 'Left' or 'Numpad-4'
                self.__scroll_x('scroll', -1, 'unit', event=event)
            elif event.keycode in [87, 38, 104]:  # scroll up: keys 'W', 'Up' or 'Numpad-8'
                self.__scroll_y('scroll', -1, 'unit', event=event)
            elif event.keycode in [83, 40, 98]:  # scroll down: keys 'S', 'Down' or 'Numpad-2'
                self.__scroll_y('scroll',  1, 'unit', event=event)'''

    def enable(self, input_string: str):
        if (input_string == 'draw'):
            self.panning_mode = False
            self.drawing_mode = True
        if (input_string == 'pan'):
            self.panning_mode = True
            self.drawing_mode = False
        print('Draw status: ', self.drawing_mode)
        print('Panning status: ', self.panning_mode)

    def grid(self, **kw):
        """ Put CanvasImage widget on the parent widget """
        self.__imframe.grid(**kw)  # place CanvasImage widget on the grid
        self.__imframe.grid(sticky='nswe')  # make frame container sticky
        self.__imframe.rowconfigure(0, weight=1)  # make canvas expandable
        self.__imframe.columnconfigure(0, weight=1)

    def destroy(self):
        """ ImageFrame destructor """
        self.__image.close()
        self.canvas.destroy()
        self.__imframe.destroy()
