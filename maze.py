from queue import PriorityQueue

class Maze:
    
    def __init__(self):
        self.grid = []
        self.maze_map = {}
        maze = self.read_maze_from_text_file()
        maze = [[1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1],[1,1,1,1,1]]
        path = self.a_star_algorithm(maze)
        
    def read_maze_from_text_file(self):
        return None

    def read_maze_from_jpg(self):
        None

    def maze_grid(self,maze):
        for i in range(1,len(maze)+1):
            for j in range(1,len(maze[0])+1):
                self.grid.append((j,i))
                self.maze_map[j,i]={'E':0,'W':0,'N':0,'S':0}
        return self.grid 
    
    def diff(self,first_cell, second_cell):
        x1, y1 = first_cell
        x2, y2 = second_cell
        return abs(x1-x2) + abs(y1-y2)

    def print_path(self):
        None
        
    def trace_path(self):
        None
        
    def a_star_algorithm(self,maze):
        start = (5, 5)
        g_score = {cell:float('inf') for cell in self.maze_grid(maze)}
        g_score[start]=0
        f_score = {cell:float('inf') for cell in self.maze_grid(maze)}
        f_score[start] = self.diff(start,(1,1))
        
        open=PriorityQueue()
        open.put( (self.diff(start, (1,1)), self.diff(start, (1,1)), start) )
        aPath = {}
        while not open.empty():
            currCell = open.get()[2]
            if currCell == (1,1):
                break
            for d in 'ESNW':
                print(currCell,"  ", d)
                if self.maze_map[currCell][d] == True:
                    if d=='E':
                        childCell = (currCell[0], currCell[1]+1)
                    if d=='W':
                        childCell = (currCell[0], currCell[1]-1)
                    if d=='N':
                        childCell = (currCell[0]-1, currCell[1])
                    if d=='S':
                        childCell = (currCell[0]+1, currCell[1])
                    temp_g_score = g_score[currCell]+1
                    temp_f_score = temp_g_score + self.diff(childCell,(1,1))

                    if temp_f_score < f_score[childCell]:
                        g_score[childCell] = temp_g_score
                        f_score[childCell] = temp_f_score
                        open.put((temp_f_score, self.diff(childCell, (1,1)), childCell))
                        aPath[childCell] = currCell
                        
        fwdPath = {}
        cell=(1,1)
        while cell != start:
            fwdPath[aPath[cell]] = cell
            cell = aPath[cell]
        return fwdPath

class Main:
    if __name__ == '__main__':
        Maze()
        

        
        
    
    
    
    




