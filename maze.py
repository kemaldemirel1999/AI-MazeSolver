from queue import PriorityQueue
from txtreader import TxtReader
from jpgreader import JpgReader

class Maze:
    
    def __init__(self):
        self.maze_map = {}
        self.start_point = (5,4)
        self.goal_point = (1,0)
        filename = "txtmaze.txt"
        if(filename.endswith(".txt")):
            maze = TxtReader().read_txt_maze(filename)            
        elif(filename.endswith(".jpg")):
            maze = JpgReader(filename)
        #maze = [ ['0','0','0','0','0'], ['#','#','0','0','0'], ['#','0','0','0','#'], ['#','0','0','0','0']]
        self.make_maze_map(maze)
        path = self.a_star_algorithm(maze)
        print(path)
        
    def maze_grid(self,maze):
        grid = []
        for i in range(0,len(maze)):
            for j in range(0,len(maze[0])):
                grid.append((i,j))
        return grid
    
    def make_maze_map(self, maze):
        col_length = len(maze[0])
        row_length = len(maze)
        for col in range(0,len(maze[0])):
            for row in range(0,len(maze)):
                self.maze_map[row,col]={'E':0,'W':0,'N':0,'S':0}
                if col+1 < col_length:
                    if self.is_it_wall(maze[row][col+1]):
                        self.maze_map[row,col]['E'] = 0
                    else:
                        self.maze_map[row,col]['E'] = 1
                        
                if col-1 >= 0:                       
                    if self.is_it_wall(maze[row][col-1]):
                        self.maze_map[row,col]['W'] = 0
                    else:
                        self.maze_map[row,col]['W'] = 1  
                                        
                if row-1 >= 0:                        
                    if self.is_it_wall(maze[row-1][col]):
                        self.maze_map[row,col]['N'] = 0
                    else:
                        self.maze_map[row,col]['N'] = 1 
                        
                if row+1 < row_length:    
                    if self.is_it_wall(maze[row+1][col]):
                        self.maze_map[row,col]['S'] = 0
                    else:
                        self.maze_map[row,col]['S'] = 1  
                        
    
    def is_it_wall(self, symbol):
        if symbol == '#' or symbol == '$':
            return True
        elif symbol == '.' or symbol == '0':
            return False
        print("Unknown Cell")
        return False
    
    def h_diff(self,first_cell, second_cell):
        x1, y1 = first_cell
        x2, y2 = second_cell
        return abs(x1-x2) + abs(y1-y2)

    
        
    def a_star_algorithm(self,maze):
        start = self.start_point
        g_score = {cell:float('inf') for cell in self.maze_grid(maze)}
        g_score[start]=0
        goal = self.goal_point
        f_score = {cell:float('inf') for cell in self.maze_grid(maze)}
        f_score[start] = self.h_diff(start,goal)
        
        open=PriorityQueue()
        open.put( (self.h_diff(start, goal), self.h_diff(start, goal), start) )
        aPath = {}
        
        
        while not open.empty():
            currCell = open.get()[2]
            if currCell == goal:
                break
            for d in 'ESNW':
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
                    temp_f_score = temp_g_score + self.h_diff(childCell, goal)

                    if temp_f_score < f_score[childCell]:
                        g_score[childCell] = temp_g_score
                        f_score[childCell] = temp_f_score
                        open.put((temp_f_score, self.h_diff(childCell, goal), childCell))
                        aPath[childCell] = currCell

        fwdPath = {}
        cell = goal
        while cell != start:
            fwdPath[aPath[cell]] = cell
            cell = aPath[cell]
        return fwdPath

class Main:
    if __name__ == '__main__':
        Maze()
        

        
        
    
    
    
    




