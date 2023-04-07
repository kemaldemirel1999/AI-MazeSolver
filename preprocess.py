import os
import cv2

class Preprocess:
    def __init__(self):
        None

    # Labirent resmi üzerinde görüntü işleme uygulanır ve böylece daha kolay işlem yapmamız sağlanır.
    # Resim Grayscale olarak okunur ve threshold işlemi gerçekleştirilir.
    # Duvar ve boş noktalar böylelikle kolayca ayırt edilir.
    def preprocess_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, maze = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        return maze
