
from aimaze import AIMazeSolver
import os

class Main:

    # İşlem uzun süreceği için yoruma alıp test edebilirsiniz.
    # Kaggle dataset 1000 labirent içerdiği için çok yavaş sürmektedir.
    def __init__(self):
        None

    if __name__ == '__main__':
        print("Hello Kemal Demirel AI Maze Solver from images and txt files.")
        maze = AIMazeSolver()

        # İlgili labirentin çözümü bulunduğu zaman "[dosya ismi] is traced successfully." mesajı konsola yazdırılır.
        ''' Txt Mazes '''
        maze.solve_maze("txtmaze.txt")
        maze.solve_maze("labirentdosya.txt")
        maze.solve_maze("maze20_20.txt")
        maze.solve_maze("test.txt")

        ''' Labirentler '''
        maze.solve_maze("solsag.jpeg")
        maze.solve_maze("sagsol.png")
        maze.solve_maze("altust.png")
        maze.solve_maze("ustalt.png")
        maze.solve_maze("ustalt2.png")
        maze.solve_maze("altust2.png")
        maze.solve_maze("ustalt3.png")
        maze.solve_maze("yuvarlak.png")
        maze.solve_maze("yuvarlak2.png")
        maze.solve_maze("ucgen.png")
        maze.solve_maze("altigen.png")
        maze.solve_maze("solsag2.jpeg")
        maze.solve_maze("altigen2.png")
        maze.solve_maze("altust4.png")
        maze.solve_maze("altust3.png")
        maze.solve_maze("leftdown.png")
        maze.solve_maze("inside_downleft.png")
        maze.solve_maze("mixed_leftup.png")

        # Kaggle Dataset Labirentleri
        # Kaggle veritesi üzerinde çalışırken 1000 tane labirent olduğu için uzun sürmektedir.
        # Kaçıncı labirent çözüldüğü takibi kolay olması için print ile ekrana yazdırılmaktadır.
        kaggle_path = os.getcwd() + "/kaggle_maze_dataset/rectangular_mazes_10x10"
        files = os.listdir(kaggle_path)
        i = 0
        for val in files:
            maze.solve_maze(val, True)
            print(i)
            i = i + 1

