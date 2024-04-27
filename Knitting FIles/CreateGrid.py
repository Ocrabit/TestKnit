from PIL import Image, ImageDraw, ImageFont


class GridTable:
    grid = None
    num_rows = None
    num_cols = None

    def __init__(self, rows: int, cols: int):
        self.num_rows = rows
        self.num_cols = cols
        self.grid = [['0' for i in range(rows)] for j in range(cols)]
        self.color_grid = [['#FFFFFF' for i in range(rows)] for j in range(cols)]

    def gridImage(self, gridSize: int):
        grid_size = gridSize

        fnt = ImageFont.truetype("fonts/arial.ttf", int(grid_size*0.18))

        row_size = self.num_rows * grid_size
        col_size = self.num_cols * grid_size

        width = col_size + (grid_size * 2)
        height = row_size + (grid_size * 2)
        image = Image.new(mode='L', size=(width, height), color=255)

        # Draw some lines
        draw = ImageDraw.Draw(image)

        # Create col steps
        x_step = int((image.width - (grid_size * 2)) / self.num_cols)
        y_step = int((image.height - (grid_size * 2)) / self.num_rows)

        # Y locations
        y_start = grid_size
        y_end = image.height - grid_size

        # X locations
        x_start = grid_size
        x_end = image.width - grid_size

        for x in range(grid_size, image.width, x_step):
            line = ((x, y_start), (x, y_end))
            draw.line(line, fill=128)

        for y in range(grid_size, image.height, y_step):
            line = ((x_start, y), (x_end, y))
            draw.line(line, fill=128)

        # draw numbers
        for x in range(1, self.num_cols + 1, 1):
            draw.text(((grid_size/2 - grid_size/13.5) + x * grid_size, grid_size / 2), str((self.num_cols + 1) - x), fill="black", align="center", font=fnt)
            draw.text(((grid_size/2 - grid_size/13.5) + x * grid_size, ((3 * grid_size) / 8) + y_end), str((self.num_cols + 1) - x), fill="black",
                      align="center", font=fnt)

        for y in range(1, self.num_rows + 1, 1):
            draw.text((grid_size / 2, (grid_size/2 - grid_size/13.5) + y * grid_size), str((self.num_rows + 1) - y), fill="black", align="center", font=fnt)
            draw.text((((3 * grid_size) / 8) + x_end, (grid_size/2 - grid_size/13.5) + y * grid_size), str((self.num_rows + 1) - y), fill="black",
                      align="center", font=fnt)
        del draw

        return image

    def writeToTxtFile(self):
        with open('../grid.txt', 'w') as f:
            for line in self.grid:
                for element in line:
                    f.write(str(element) + " ")
                f.write("\n")
            f.close()

if __name__ == '__main__':
    new_grid = GridTable(8, 10)
    img = new_grid.gridImage(gridSize=96)
    img.show()

    '''for row in new_grid.grid:
        print(row)
    new_grid.writeToTxtFile()

    new_grid.runColorUI()'''