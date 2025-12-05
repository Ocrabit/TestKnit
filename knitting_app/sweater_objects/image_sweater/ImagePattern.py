import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ...tool_functions import tool_functions as tf


class ImagePattern:
    def __init__(self, width, height):  # Stitches and Rows only no inches
        self.image = Image.new('RGB', (width, height), color='white')

    def addNeck(self, starting_point, stitches_decrease, rows_decrease):
        draw = ImageDraw.Draw(self.image)  # create draw to draw on image

        x = starting_point  # set start x
        y = 0  # set start y

        # Create Vertices for left side
        left_line_vertices = [(x, y)]
        for i in range(len(rows_decrease)):
            print(f'left i: {i}')
            y += rows_decrease[i]
            left_line_vertices.append((x, y))
            x += stitches_decrease[i]
            left_line_vertices.append((x, y))
        print(left_line_vertices)

        # Draw Line From Left
        draw.line(left_line_vertices, fill=0)

        # Create Vertices for right side
        right_line_vertices = [(x, y)]
        for i in range(len(rows_decrease)-1, -1, -1):
            print(f'right i: {i}')
            x += stitches_decrease[i]
            right_line_vertices.append((x, y))
            y -= rows_decrease[i]
            right_line_vertices.append((x, y))
        print(right_line_vertices)

        # Draw Line From Left
        draw.line(right_line_vertices, fill=0)

        del draw
        # Show Image
        self.image.show()