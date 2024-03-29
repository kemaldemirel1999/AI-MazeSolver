import os
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt

class Visualize:
    
    def __init__(self):
        None

    # İlgili trace edilmiş labirent dosyasını visualize eder ve return eder.
    # Başlangıç : mavi
    # Bitiş: yeşil
    # trace edilen yol: kırmızı
    def visualize_traced_maze(self, maze):
        width = 1024
        height = 1024
        wall_color = (0, 0, 0)  # black
        path_color = (255, 255, 255)  # white
        traced_color = (255, 0, 0) #red
        start = (0, 255, 0) #green
        end = (0, 0, 255) #blue
        image = Image.new('RGB', (width, height), wall_color)
        draw = ImageDraw.Draw(image)
        cell_width = width // len(maze[0])
        cell_height = height // len(maze)
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == 'S':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=start)
                elif maze[row][col] == 'G':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=end)
                elif maze[row][col] == '#':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=wall_color)
                elif maze[row][col] == '.':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=path_color)
                else:
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=traced_color)
        return image

        
    