import os
import cv2

class Preprocess:
    def __init__(self):
        None
    
    # İlgili resme görüntü işleme teknikleri uygulanır ve resim çözüm için daha uygun bir görsek hale getirilir
    def preprocess_image(self, image):
        path = os.getcwd() + "/labirentler/"+image
        maze = cv2.imread(path)
        gray = cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("preprocessed_maze.jpg", thresh)
