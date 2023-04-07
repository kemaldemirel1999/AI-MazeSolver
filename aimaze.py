from jpg_maze import JpgMaze
from txt_maze import TxtMaze

class AIMazeSolver:
    '''
        Artifical Intelligence Maze Solver uygulamasını yöneten kısımdır.
        İlgili dosyanın txt dosyası veya resim olup olmadığını ayırt eder ve gerekli işlemleri yapar.
        Resim için .jpg, .jpeg, .png formatları desteklenmektedir
    '''
    def __init__(self):
        None

    # filename: labirent dosya ismi
    # kaggle_dataset:   kaggle veriseti olup olmadığı belirtilir. initial olarak False alınır.
    # labirent dosya ismi belirtirken path vermemelisiniz.
    # labirentler maze_samples içerisine koyulmalıdır
    # Kaggle veriseti test ediyorsanız gerekli 'bool' değişkenini True yapın
    def solve_maze(self, filename, kaggle_dataset=False):
        if filename.endswith(".txt"):   # Txt dosyası ise
            maze_solver = TxtMaze()
            maze_solver.start_maze_solver(filename)
        elif filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"): # Resim ise
            maze_solver = JpgMaze()
            if kaggle_dataset:
                maze_solver.start_maze_solver(filename, True)
            else:
                maze_solver.start_maze_solver(filename)
        else:
            print("Lutfen Gecerli Bir Dosya Uzantisi Giriniz.")
        print(filename," is traced successfully.")
