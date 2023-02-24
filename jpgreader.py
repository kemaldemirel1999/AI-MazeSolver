import pywhatkit
import os
from PIL import Image

class JpgReader:
    
    def __init__(self):
        self.maze = []
        self.none_symbols = ['.']

    def read_jpg_maze(self, filename):
        path = os.getcwd()+"/maze/"
        pywhatkit.image_to_ascii_art(path+filename,path+'jpgmaze')
        unparsed_maze = self.read_jpg_text_file("jpgmaze.txt")
        self.parse_jpg_maze(unparsed_maze, filename)
        filename = filename[0:len(filename)-4] + ".txt"
        return filename
    
    def parse_jpg_maze(self, unparsed_maze, filename):
        maze_indexes = []
        for line in unparsed_maze:
            left = -1
            right = len(line)
            wall_found = False
            for i in range(len(line)):
                left = left + 1
                if not( self.none_symbols.__contains__(line[left]) ):
                    wall_found = True
                    break
            for i in range(len(line)):
                right = right - 1                
                if not( self.none_symbols.__contains__(line[right]) ):
                    wall_found = True
                    break
            if wall_found:
                start = left
                end = right+1
                maze_indexes.append([start,end])
                #self.maze.append(line[start:end])
                
        west = maze_indexes[0][0]
        east = maze_indexes[0][1]
        for val in maze_indexes:
            if val[0] < west:
                west = val[0]
            if val[1] > east:
                east = val[1]
         
        maze_indexes = []       
        for col in range(len(unparsed_maze[0])): 
            up = -1
            down = len(unparsed_maze)
            wall_found = False
            for i in range(len(unparsed_maze)):
                up = up + 1
                if not( self.none_symbols.__contains__(unparsed_maze[up][col])):
                    wall_found = True
                    break
            for i in range(len(unparsed_maze)):
                down = down - 1
                if not( self.none_symbols.__contains__(unparsed_maze[down][col])):
                    wall_found = True
                    break
            if wall_found:
                maze_indexes.append([up,down+1])

        north = maze_indexes[0][0]
        south = maze_indexes[0][1]
        for val in maze_indexes:
            if val[0] < north:
                north = val[0]
            if val[1] > south:
                south = val[1]    
        self.get_maze_part(unparsed_maze, east, west, north, south)
        self.clear_maze()
        self.write_maze_to_txt(filename)
         
    def get_maze_part(self, unparsed_maze, east, west, north, south):
        curr_row = north
        row = []
        while curr_row < south:
            self.maze.append(unparsed_maze[curr_row][west:east])
            curr_row = curr_row + 1
        
        
               
    def clear_maze(self):
        
        for i in range(0,len(self.maze)):
            for j in range(0,len(self.maze[i])):
                if not(self.none_symbols.__contains__(self.maze[i][j])):
                    self.maze[i][j] = '#'
                else:
                    self.maze[i][j] = '.'
                    
    def write_maze_to_txt(self,filename):
        filename = filename[0:len(filename)-4] + ".txt"
        with open(os.getcwd()+"/maze/"+filename, 'w') as f:
            for line in self.maze:
                for symbol in line:
                    f.write(symbol)    
                f.write("\n")
        
        
    def read_jpg_text_file(self, filename):
        path = os.getcwd()+"/maze/"
        unparsed_maze = []
        with open(path+filename) as f:
            for line in f.readlines():
                tmp = []
                for val in line:
                    if val != '\n':
                        tmp.append(val)    
                unparsed_maze.append(tmp)
        try:
            os.remove(path+filename)    
            None
        except:
            print("File not found")
        return unparsed_maze
            
        

        

