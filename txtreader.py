


import os


class TxtReader:
    
    def __init__(self):
        self.maze = []
    
    def read_txt_maze(self,filename):
        path = os.getcwd()+"/maze/"
        with open(path+filename) as f:
            for line in f.readlines():
                tmp = []
                for val in line:
                    if val != '\n':
                        tmp.append(val)    
                self.maze.append(tmp)
        
        return self.maze
        
        
    