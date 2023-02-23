

class TxtReader:
    
    def __init__(self, filename):
        self.maze = []
        self.read_txt_maze(filename)
    
    def read_txt_maze(self,filename):
        with open(filename) as f:
            [print(line) for line in f.readlines()]
        
        
    