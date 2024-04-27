import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageTk, ImageDraw
import tkmacosx as tkmac
from CreateGrid import GridTable


class ImageCanvas(tk.Canvas):

    def __init__(self, parent, grid: GridTable, grid_image: Image, grid_size: int):
        tk.Canvas.__init__(self, parent)

        self.image = None
        self.__grid = grid
        self.rows = grid.num_rows
        self.cols = grid.num_cols
        self.grid_size = grid_size
        self.grid_spacing = grid_size
        self._image = grid_image.convert("RGBA")
        self.color_grid = grid.color_grid
        self.current_color = '#eb6aff'
        #self.draw_image()

        self.grid(column=0, row=0)  #add canvas to frame

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose color")
        if (color[0] is not None):
            if (color[1][0] == '#'):
                self.current_color = color[1]
            else:
                self.current_color = '#FFFFFF'
                print('erased')

    def determine_grid_click(self, x: int, y: int):
        if (x < self.grid_spacing * (self.cols + 1) and y < self.grid_spacing * (self.rows + 1)):
            i = int(x / self.grid_spacing) - 1
            j = int(y / self.grid_spacing) - 1

            if (i > -1 and j > -1):
                print('i,j: (', i, ',', j, ')')
                return [i, j]

        print('clicked not in grid')
        return None

    def click(self, x, y):
        spot_clicked = self.determine_grid_click(x, y)
        if (spot_clicked is not None):
            self.color_grid[spot_clicked[0]][spot_clicked[1]] = str(self.current_color)
            #print(self.color_grid[spot_clicked[0]][spot_clicked[1]])
            #print(self.color_grid)
            print('(', x, ',', y, ')')
            self.drawNewSquare(spot_clicked[0], spot_clicked[1])

    def drawNewSquare(self, x: int, y: int):
        square = Image.new(self._image.mode, self._image.size, (0, 0, 0, 0))
        square_draw = ImageDraw.Draw(square)
        square_draw.rectangle(((self.grid_size) + self.grid_size * x,
                               (self.grid_size) + self.grid_size * y,
                               (self.grid_size * 2) + self.grid_size * x,
                               (self.grid_size * 2) + self.grid_size * y),
                              outline='black',
                              fill=self.current_color)
        self._image.alpha_composite(square)
        self.update()

    def return_image(self):
        return self._image
    def update(self):
        #Update childs
        pass

    def save_file(self):
        print("called save_file")
        filepath = filedialog.asksaveasfilename(
            initialfile="knitting_grid",
            defaultextension='.jpeg', filetypes=(("JPEG", ".jpeg"), ("PNG", ".png")))
        print(filepath)
        if not filepath:
            return
        save_image = self._image.convert("RGB")
        save_image.save(filepath)