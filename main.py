from aimaze_solver import AIMazeSolver


class Main:

    def __init__(self):
        None

    if __name__ == '__main__':
        print("Hello Kemal Demirel AI Maze Solver from images and txt files.")
        maze = AIMazeSolver()

        '''Horizantal or Vertical Mazes'''
        # maze.solve_maze("solsag.jpeg")
        # maze.solve_maze("sagsol.png")
        # maze.solve_maze("altust.png")
        # maze.solve_maze("ustalt.png")
        # maze.solve_maze("ustalt2.png")
        # maze.solve_maze("altust2.png")
        # maze.solve_maze("ustalt3.png")
        # maze.solve_maze("yuvarlak.png")
        # maze.solve_maze("yuvarlak2.png")
        # maze.solve_maze("ucgen.png")
        # maze.solve_maze("altigen.png")
        # maze.solve_maze("solsag2.jpeg")
        # maze.solve_maze("altigen2.png")
        # maze.solve_maze("altust4.png")
        # maze.solve_maze("altust3.png")

        '''Mixed Mazes'''
        # maze.solve_maze("leftdown.png")
        # maze.solve_maze("inside_downleft.png")
        # maze.solve_maze("mixed_leftup.png")
        maze.solve_maze("outside_leftup.png")

