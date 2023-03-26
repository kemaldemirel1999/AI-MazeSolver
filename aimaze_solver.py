from jpg_maze import JpgMaze
class AIMazeSolver:

    def __init__(self):
        None
    def solve_maze(self, filename):
        if filename.endswith(".txt"):
            None
        elif filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            maze_solver = JpgMaze()
            maze_solver.start_maze_solver(filename)
        else:
            print("Lutfen Gecerli Bir Dosya Uzantisi Giriniz.")
