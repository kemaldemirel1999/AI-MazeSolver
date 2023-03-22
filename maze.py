from queue import PriorityQueue
from txtreader import TxtReader
from jpgreader import JpgReader
from visualize import Visualize

import os

class Maze:
    
    def __init__(self):
        print("Hello to Kemal Demirel AI Maze Solver.")
        
    def start_maze_solver(self,filename):
        self.maze_map = {}
        isItJPGMaze = False
        givenImage = None
        
        if(filename.endswith(".txt")):
            maze = TxtReader().read_txt_maze(filename)            
        elif(filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg")):
            givenImage = filename
            filename = str(JpgReader().read_jpg_maze(filename))
            maze = TxtReader().read_txt_maze(filename)
            try:
                os.remove(os.getcwd()+"/labirentler/"+filename)    
            except:
                print("File not found")
            isItJPGMaze = True
        else:
            print("Yanlis Dosya Input Girildi. Lütfen .txt, .jpg, .png, .jpeg uzantili labirent dosyasi giriniz.")
            return
            
        self.start_point = self.find_start_point(maze)
        self.goal_point = self.find_goal_point(maze)
        self.make_maze_map(maze)
        
        path = self.a_star_algorithm(maze)
        self.tracePath(path,maze)
        self.visualize_maze(givenImage, maze, isItJPGMaze)
        self.write_maze_to_txt(filename, maze)
        
    def visualize_maze(self,givenImage, maze, isItJPGMaze):
        if(isItJPGMaze):
            Visualize().visualizeTracedMaze(givenImage, maze, isItJPGMaze)    
        else:
            Visualize().visualizeTracedMaze(None, maze, isItJPGMaze)
            
    def write_maze_to_txt(self, filename, maze):
        filename = "trace_"+filename
        print(os.getcwd()+filename)
        with open(os.getcwd()+"/cozumler/"+filename, 'w') as f:
            for line in maze:
                for symbol in line:
                    f.write(symbol)    
                f.write("\n")
        
    def tracePath(self, path, maze):
        for val in path:
            if(path[val] == self.goal_point):
                continue
            maze[path[val][0]][path[val][1]] = "x";
        
    def find_start_point(self, maze):
        for row in range(0,len(maze)):
            for col in range(0,len(maze[row])):
                if maze[row][col] == "s" or maze[row][col] == "S":
                    return (row,col)
    
    def find_goal_point(self, maze):
        for row in range(0,len(maze)):
            for col in range(0,len(maze[0])):
                if maze[row][col] == "g" or maze[row][col] == "G":
                    return (row,col)        
    
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
        ####
        
        
        if not open.empty():
            currCell = open.get()[2]
            if currCell == goal:
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
        
        ####
        fwdPath = {}
        cell = goal
        while cell != start:
            fwdPath[aPath[cell]] = cell
            cell = aPath[cell]
        return fwdPath
        

        
        
    
    
    
    




