import os
import cv2

class Preprocess:
    def __init__(self):
        None
    def preprocess_image(self, filename):
        path = os.getcwd()+"/labirentler/"
        # Resim grayscale hale getirilir.
        img = cv2.imread(path+filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
        gray = thresh
        if gray.shape[0] < 1200 and gray.shape[1] < 1200:
            upscaled_img = cv2.resize(img, (2000, 2000), interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(path+'processed_image.jpg', upscaled_img)
        else:
            cv2.imwrite(path+'processed_image.jpg', gray)
