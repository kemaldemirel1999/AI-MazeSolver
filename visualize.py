import os
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt

class Visualize:
    
    def __init__(self):
        None
    
    '''
     Labirentin çözümünü görselleştirir.
     Duvarlar: Siyah
     Boş yerler: Beyaz
     Başlangiç noktasi: Yeşil
     Bitiş noktasi: Mavi
     Çözüm yolu: Kirmizi
    '''
    def visualizeTracedMaze(self, givenMaze, traced_maze, isItJPGMaze):
        if(isItJPGMaze):
            givenImage = cv2.imread(os.getcwd()+"/labirentler/"+givenMaze, 0)
        width = 1024
        height = 1024
        wall_color = (0, 0, 0)  # black
        path_color = (255, 255, 255)  # white
        traced_color = (255, 0, 0) #red
        start = (0, 255, 0) #green
        end = (0, 0, 255) #blue
        image = Image.new('RGB', (width, height), wall_color)
        draw = ImageDraw.Draw(image)
        cell_width = width // len(traced_maze[0])
        cell_height = height // len(traced_maze)
        for row in range(len(traced_maze)):
            for col in range(len(traced_maze[0])):
                if traced_maze[row][col] == 'S':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=start)
                elif traced_maze[row][col] == 'G':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=end)
                elif traced_maze[row][col] == '#':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=wall_color)
                elif traced_maze[row][col] == '.':
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=path_color)
                else:
                    draw.rectangle((col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height), fill=traced_color)
                    
        # Labirent eğer JPG dosyası ise input maze ve traced maze gösterilir.
        if(isItJPGMaze):
            fig, axs = plt.subplots(1, 2, figsize=(12, 8))
            axs[0].imshow(givenImage, cmap='gray')
            axs[0].set_title('Given Maze')
            axs[1].imshow(image, cmap='gray')
            axs[1].set_title('(Start:Green, Goal:Blue) Maze with traced to goal point')
            plt.show()
        # Labirent eğer TXT dosyası ise traced maze gösterilir.
        else:
            plt.imshow(image, cmap='gray')
            plt.show()

        
    