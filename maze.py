from queue import PriorityQueue

class Maze:
    
    # Indexleme sistemi 1 den başlayarak ilerleyecek şekilde implement ettim.
    
    def __init__(self):
        self.grid = []
        self.maze_map = {}
        #maze = self.read_maze_from_text_file()
        maze = [ ['0','0','0','0','0'], ['#','#','#','#','0'], ['#','#','#','#','0'], ['#','#','#','#','0'], ['#','#','#','#','0'] ]
        self.make_maze_map(maze)
        for val in self.maze_map:
            print(val,", ",self.maze_map[val])
        path = self.a_star_algorithm(maze)
        print(path)
        None
        
    def read_maze_from_text_file(self):
        with open('maze.txt') as f:
            [print(line) for line in f.readlines()]
        
    def maze_grid(self,maze):
        for i in range(0,len(maze)):
            for j in range(0,len(maze[0])):
                self.grid.append((j,i))
        return self.grid
    
    def make_maze_map(self, maze):
        i_length = len(maze)
        j_length = len(maze[0])
        for i in range(0,len(maze)):
            for j in range(0,len(maze[0])):
                self.maze_map[j,i]={'E':0,'W':0,'N':0,'S':0}
                if i+1 <= i_length-1:
                    if self.is_it_wall(maze[j][i+1]):
                        self.maze_map[j,i]['E'] = 0
                    else:
                        self.maze_map[j,i]['E'] = 1
                        
                if i-1 >= 0:                       
                    if self.is_it_wall(maze[j][i-1]):
                        self.maze_map[j,i]['W'] = 0
                    else:
                        self.maze_map[j,i]['W'] = 1  
                                        
                if j-1 >= 0:                        
                    if self.is_it_wall(maze[j-1][i]):
                        self.maze_map[j,i]['N'] = 0
                    else:
                        self.maze_map[j,i]['N'] = 1 
                        
                if j+1 <= j_length-1:    
                    if self.is_it_wall(maze[j+1][i]):
                        self.maze_map[j,i]['S'] = 0
                    else:
                        self.maze_map[j,i]['S'] = 1  
                        
    
    def is_it_wall(self, symbol):
        if symbol == '#':
            return True
        return False
    
    def h_diff(self,first_cell, second_cell):
        x1, y1 = first_cell
        x2, y2 = second_cell
        return abs(x1-x2) + abs(y1-y2)

    
        
    def a_star_algorithm(self,maze):
        # Start point is given
        start = (4,4)
        
        # G score array is created and start point's g_score added as 0
        g_score = {cell:float('inf') for cell in self.maze_grid(maze)}
        g_score[start]=0
        
        # Goal cell is defined
        goal = (0,0)
        
        # F score array is created and start point's g_score added as 0
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
        

        
        
    
    
    
    




