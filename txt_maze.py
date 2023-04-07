from queue import PriorityQueue
from visualize import Visualize
import os
import cv2

class TxtMaze:
    
    def __init__(self):
        self.maze_path = os.getcwd() + "/maze_samples/" # Labirentlerin bulunduğu path
        self.results_path = os.getcwd() + "/results/"   # Sonuçların bulunduğu path

    # Labirent ismini parametre olarak alır.
    # Gerekli işlemleri gerçekleştirir.
    def start_maze_solver(self,filename):
        self.maze_map = {}
        maze = self.read_txt_maze(filename) # labirent txt dosyasından okunur ve bir array'e kaydedilir.
        self.start_point = self.find_start_point(maze)  # başlangıç noktası bulunur ve kaydedilir.
        self.goal_point = self.find_goal_point(maze)    # bitiş noktası bulunur ve kaydedilir.
        self.make_maze_map(maze)    # Labirentin haritası çıkarılır. North, south, west, east şeklinde.
        path = self.a_star_algorithm(maze)  # a-star algoritması çalıştırılarak hedef noktaya gidilen en optimal yol bulunur.
        self.tracePath(path,maze)   # hedef noktaya gidilen path trace edilir.
        image = Visualize().visualize_traced_maze(maze) # trace edilmiş labirent görselleştirilir.
        filename = filename[0:len(filename)-4]+".jpg"
        image.save(self.results_path + filename) # trace edilmiş vegörselleştirilmiş labirent .jpg dosyası olarak kaydedilir.

    # Txt dosyasından labirent okunur ve array'e kaydedilir.
    def read_txt_maze(self, filename):
        maze = []
        with open(self.maze_path + filename) as f:
            for line in f.readlines():
                tmp = []
                for val in line:
                    if val != '\n':
                        tmp.append(val)
                maze.append(tmp)
        return maze

    # ilgili path trace edilir
    def tracePath(self, path, maze):
        for val in path:
            if(path[val] == self.goal_point):
                continue
            maze[path[val][0]][path[val][1]] = "x"

    # labirent içerisindeki başlangıç noktası bulunur.
    def find_start_point(self, maze):
        for row in range(0,len(maze)):
            for col in range(0,len(maze[row])):
                if maze[row][col] == "s" or maze[row][col] == "S":
                    return (row,col)

    # labirent içerisindeki bitiş noktası bulunur.
    def find_goal_point(self, maze):
        for row in range(0,len(maze)):
            for col in range(0,len(maze[0])):
                if maze[row][col] == "g" or maze[row][col] == "G":
                    return (row,col)        

    # labirent düz bir hale çevrilir.

    def maze_grid(self,maze):
        grid = []
        for i in range(0,len(maze)):
            for j in range(0,len(maze[0])):
                grid.append((i,j))
        return grid

    # Labirentin haritası çıkarılır ve hedef noktaya gitmek için kullanılır.
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

    # ilgili noktanın duvar olup olmadığını bulur.
    def is_it_wall(self, symbol):
        if symbol == '#' or symbol == '$':
            return True
        return False

    # heuristic fonksiyonudur.
    def h_diff(self,first_cell, second_cell):
        x1, y1 = first_cell
        x2, y2 = second_cell
        return abs(x1-x2) + abs(y1-y2)   

    # a-star algoritmasıdır ve hedef noktaya gitmek için en optimal yolu hesaplar.

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
        

        
        
    
    
    
    




