import cv2
import pywhatkit
import os
from PIL import Image
from preprocess import Preprocess
from txtreader import TxtReader

class JpgReader:
    
    def __init__(self):
        self.maze = []
        self.none_symbols = ['.',':']
        self.maze_folder_path = os.getcwd()+"/labirentler/"
        
    '''
        İlgili JPG labirent dosyasi txt formatina çevrilir.
        İlgili labirent parse işlemlerinden sonra return edilir.
    '''
    def read_maze_from_jpg(self, filename):
        #İlgili resmin path'i
        input_image_path = self.maze_folder_path + filename
        
        # Resim üzerinde görüntü işleme uygulanır
        Preprocess(input_image_path)
        
        # İlgili resim txt formatına çevrilir.
        pywhatkit.image_to_ascii_art('processed_image.jpg','pyhwatkitMaze')
        os.remove('processed_image.jpg')
        
        # Parse işlemi uygulanmamis labirent array olarak Txt dosyasindan okunur
        unparsed_maze = TxtReader().read_from_txt_maze("pyhwatkitMaze.txt")
        os.remove('pyhwatkitMaze.txt')
        # İlgili parse işlemleri uygulanir.
        parsed_maze = self.parse_jpg_maze(unparsed_maze, filename)
        return parsed_maze
    
    
    '''
        Bir satir veya sütündaki '.' ve '#' sayilari karşilaştirilir.
        '.' fazla ise return 1
        '#' fazla ise return 0
    '''
    def compareNumOfSymbols(self, line):
        numOfDot = 0
        numOfArrow = 0
        for symbol in line:
            if(symbol == '.'):
                numOfDot = numOfDot + 1
            elif(symbol == '#'):
                numOfArrow = numOfArrow + 1
        if numOfDot>numOfArrow:
            return 1
        else:
            return 0
                
    '''
        Labirent hedef noktasi bulunur.
    '''
    def find_goal_point(self):
        first_row = 0
        last_row = len(self.maze)-1
        first_row_indexes = self.getGateIndexes(self.maze[first_row])
        last_row_indexes = self.getGateIndexes(self.maze[last_row])
        
        first_col = []
        for i in range(len(self.maze)):
            first_col.append(self.maze[i][0])
        
        last_col = []    
        for i in range(len(self.maze)):
            last_col.append(self.maze[i][len(self.maze[0])-1])
            
        first_col_indexes = self.getGateIndexes(first_col)
        last_col_indexes = self.getGateIndexes(last_col)
        
        
        if first_row_indexes != None:
            goal_set = False
            for i in first_row_indexes:
                if(goal_set == True):
                    self.maze[first_row][i] = '#'
                else:
                    self.maze[first_row][i] = 'G'  
                    goal_set = True 
        elif last_row_indexes != None:
            goal_set = False
            for i in last_row_indexes:
                if(goal_set == True):
                    self.maze[last_row][i] = '#'
                else:
                    self.maze[last_row][i] = 'G'  
                    goal_set = True
        elif first_col_indexes != None:
            goal_set = False
            for i in first_col_indexes:
                if(goal_set == True):
                    self.maze[i][0] = '#'
                else:
                    self.maze[i][0] = 'G'  
                    goal_set = True
        elif last_col_indexes != None:
            goal_set = False
            last_col_index = len(self.maze[0])-1
            for i in last_col_indexes:
                if(goal_set == True):
                    self.maze[i][last_col_index] = '#'
                else:
                    self.maze[i][last_col_index] = 'G'  
                    goal_set = True  
        return self.maze
        
    
    def getGateIndexes(self, line):
        indexes = []
        i = 0
        for i in range(len(line)):
            if line[i] == '.':
                indexes.append(i)
        if(len(indexes)>0):
            return indexes
        else:
            return None
    
                
        
    def find_start_point(self):
        firstRow, lastRow = self.compareFirstAndLastRow()
        firstCol, lastCol = self.compareFirstAndLastCol()
        # . fazla oluyorsa 1
        
        if firstRow == 1:
            found = False
            col_indexes = []
            for row in range(0,len(self.maze)):
                line = self.maze[row]
                if found == True:
                    break
                for i in range(0,len(line)):
                    if(line[i] == '#'):
                        col_indexes.append(i)
                        found = True
            wallRow = 0
            for row in range(0,len(self.maze)):
                if(self.compareNumOfSymbols(self.maze[row]) == 0):
                    wallRow = row    
                    break
            start_set = False
            while(wallRow > 0):
                if start_set == True:
                    break
                for index in col_indexes:
                    if(self.maze[wallRow][index] == '.'):
                        self.maze[wallRow][index] = 'S'
                        start_set = True
                        for i in range(len(self.maze[wallRow])):
                            if(self.maze[wallRow][i] == '.'):
                                self.maze[wallRow][i] = '#'
                        break
                wallRow = wallRow -1
            new_maze = []
            wallRow = wallRow + 1
            while(wallRow < len(self.maze)):
                new_maze.append(self.maze[wallRow])
                wallRow = wallRow + 1
            return new_maze
        ################
        elif lastRow == 1:
            found = False
            col_indexes = []
            row = len(self.maze)-1
            while(row >0):
                line = self.maze[row]
                if found == True:
                    break
                for i in range(0,len(line)):
                    if(line[i] == '#'):
                        col_indexes.append(i)
                        found = True
                row = row - 1
            wallRow = 0
            row = len(self.maze)-1
            while(row > 0):
                if(self.compareNumOfSymbols(self.maze[row]) == 0):
                    wallRow = row
                    break
                row = row -1
            start_set = False
            while(wallRow < len(self.maze)):
                if start_set == True:
                    break
                for index in col_indexes:
                    if(self.maze[wallRow][index] == '.'):
                        self.maze[wallRow][index] = 'S'
                        start_set = True
                        for i in range(len(self.maze[wallRow])):
                            if(self.maze[wallRow][i] == '.'):
                                self.maze[wallRow][i] = '#'
                        break
                wallRow = wallRow + 1
            new_maze = []
            i = 0
            while(i < wallRow):
                new_maze.append(self.maze[i])
                i = i + 1
            return new_maze
        ###########################
        elif firstCol == 1:
            found = False
            row_indexes = []
            for col_index in range(0, len(self.maze[0])):
                column = []
                for i in range(len(self.maze)):
                    column.append(self.maze[i][col_index])
                if(found == True):
                    break
                for i in range(len(column)):
                    if column[i] == '#':
                        row_indexes.append(i)
                        found = True
            wallCol = 0
            for col_index in range(0,len(self.maze[0])):
                whole_column = []
                for i in range(0,len(self.maze)):
                    whole_column.append(self.maze[i][col_index])
                if self.compareNumOfSymbols(whole_column) == 0:
                    wallCol = col_index
                    break
            start_set = False
            while(wallCol > 0):
                if start_set == True:
                    break
                for index in row_indexes:
                    if self.maze[index][wallCol] == '.':
                        self.maze[index][wallCol] = 'S'
                        start_set = True
                for i in range(len(self.maze)):
                    if self.maze[i][wallCol] == '.':
                        self.maze[i][wallCol] = '#'
                
                wallCol = wallCol - 1
            new_maze = []
            wallCol = wallCol + 1
            for i in range(len(self.maze)):
                new_maze.append(self.maze[i][wallCol:len(self.maze[0])])
            return new_maze
        elif lastCol == 1:
            found = False
            row_indexes = []
            col_index = len(self.maze[0]) -1
            while(col_index>0):
                column = []
                for i in range(len(self.maze)):
                    column.append(self.maze[i][col_index])
                if(found == True):
                    break
                for i in range(len(column)):
                    if column[i] == '#':
                        row_indexes.append(i)
                        found = True
                col_index = col_index - 1
            wallCol = 0
            col_index = len(self.maze[0]) -1
            while(col_index > 0):
                whole_column = []
                for i in range(0,len(self.maze)):
                    whole_column.append(self.maze[i][col_index])
                if self.compareNumOfSymbols(whole_column) == 0:
                    wallCol = col_index
                    break
                col_index = col_index - 1
            start_set = False
            while(wallCol<len(self.maze[0])):
                if(start_set == True):
                    break
                for index in row_indexes:
                    if self.maze[index][wallCol] == '.':
                        self.maze[index][wallCol] = 'S'
                        start_set = True
                for i in range(len(self.maze)):
                    if self.maze[i][wallCol] == '.':
                        self.maze[i][wallCol] = '#'
                wallCol = wallCol + 1
                
            new_maze = []
            for i in range(len(self.maze)):
                new_maze.append(self.maze[i][0:wallCol])
            return new_maze
    
    def compareFirstAndLastRow(self):
        lastRow = self.maze[len(self.maze)-1]
        firstRow = self.maze[0]
        numOfDot = 0
        numOfArrow = 0
        first = 0
        last = 0
        for symbol in lastRow:
            if(symbol == '.'):
                numOfDot = numOfDot + 1
            elif(symbol == '#'):
                numOfArrow = numOfArrow + 1
        if(numOfDot>numOfArrow):
            last = 1
        else:
            last = 0
        numOfDot = 0
        numOfArrow = 0
        for symbol in firstRow:
            if(symbol == '.'):
                numOfDot = numOfDot + 1
            elif(symbol == '#'):
                numOfArrow = numOfArrow + 1
        if(numOfDot>numOfArrow):
            first = 1
        else:
            first = 0
        return [first,last]
        
            
    def compareFirstAndLastCol(self):
        numOfDot = 0
        numOfArrow = 0
        firstCol = 0
        lastCol = 0
        for line in self.maze:
            symbol = line[0]
            if(symbol == '.'):
                numOfDot = numOfDot + 1
            elif(symbol == '#'):
                numOfArrow = numOfArrow + 1
        if(numOfDot>numOfArrow):
            #print("İlk column . fazla")
            firstCol = 1
        else:
            #print("İlk column # fazla")
            firstCol = 0
        numOfDot = 0
        numOfArrow = 0
        for line in self.maze:
            symbol = line[len(line)-1]
            if(symbol == '.'):
                numOfDot = numOfDot + 1
            elif(symbol == '#'):
                numOfArrow = numOfArrow + 1
        if(numOfDot>numOfArrow):
            #print("Son column . fazla")
            lastCol = 1
        else:
            #print("Son column # fazla")
            lastCol = 0
        return [firstCol,lastCol]
        
            
    
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
        self.maze = self.find_start_point()
        self.maze = self.find_goal_point()
        with open(os.getcwd()+"/labirentler/"+"final.txt", 'w') as f:
            i = 0
            for line in self.maze:
                for symbol in line:
                    f.write(symbol) 
                if(i < len(self.maze)-1):   
                    f.write("\n")
                i = i + 1
        return self.maze
         
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
    
        

        

