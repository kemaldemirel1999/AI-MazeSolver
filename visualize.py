import os
from PIL import Image, ImageDraw

class Visualize:
    
    def __init__(self):
        None
    
    def visualizeTracedMaze(self, filename, maze):
        
        # Define the dimensions of your maze
        width = len(maze[0])
        height = len(maze)

        # Define the colors for the walls and the path
        wall_color = (0, 0, 0)  # black
        path_color = (255, 255, 255)  # white
        traced_color = (255, 0, 0) #red
        
        # Create a new image
        image = Image.new('RGB', (width, height), wall_color)

        # Draw the maze onto the image
        draw = ImageDraw.Draw(image)
        cell_width = width // len(maze[0])
        cell_height = height // len(maze)
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == '#':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=wall_color)
                elif maze[row][col] == '.':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=path_color)
                else:
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=traced_color)

        # Save the image as a JPG file
        image.save('coloredmaze.jpg', 'JPEG')

        
    