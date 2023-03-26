from aimaze_solver import AIMazeSolver


class Main:

    def __init__(self):
        print("Hello Kemal Demirel AI Maze Solver from images and txt files.")

    if __name__ == '__main__':
        maze = AIMazeSolver()
        maze.solve_maze("solsag.jpeg")

        maze.solve_maze("sagsol.png")
        maze.solve_maze("altust.png")
        maze.solve_maze("altust2.png")
        maze.solve_maze("ustalt.png")
        maze.solve_maze("ustalt2.png")
        ''''''