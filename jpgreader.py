import pywhatkit
import os
from PIL import Image

class JpgReader:
    
    def __init__(self):
        self.maze = []
        self.none_symbols = ['.', '*']

    def read_jpg_maze(self, filename):
        path = os.getcwd()+"/maze/"
        pywhatkit.image_to_ascii_art(path+filename,path+'jpgmaze')
        unparsed_maze = self.read_jpg_text_file("jpgmaze.txt")
        self.parse_jpg_maze(unparsed_maze)
        return self.maze
    
    def parse_jpg_maze(self, unparsed_maze):
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
                self.maze.append(line[start:end])
                #print(line[start : end])
                
        with open('trial.txt', 'w') as f:
            for line in self.maze:
                for symbol in line:
                    f.write(symbol)    
                f.write("\n")
             
                
            
            
            
        None
        
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
            #os.remove(path+filename)    
            None
        except:
            print("File not found")
        return unparsed_maze
            
        

        

