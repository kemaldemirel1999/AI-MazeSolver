import os

class TxtReader:
    
    def __init__(self):
        self.maze_folder_path = os.getcwd() + "/labirentler/"
    
    def read_from_txt_maze(self,filename):
        maze_path = self.maze_folder_path + filename
        maze = []
        with open(maze_path) as f:
            for line in f.readlines():
                tmp = []
                for val in line:
                    if val != '\n':
                        tmp.append(val)    
                maze.append(tmp)
        return maze

        
        
    