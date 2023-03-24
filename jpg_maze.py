import cv2
import heapq
import os
import numpy as np
class JpgMaze:
    def __init__(self):
        self.maze_path = os.getcwd() + "/maze_samples/"
    def parse_image(self, filename):
        maze = self.get_maze(filename)
        start_x, start_y, orientation = self.find_arrow_center(maze, "red")
        goal_x, goal_y, orientation = self.find_arrow_center(maze, "green")
    def preprocess_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, maze = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        return maze
    def get_maze(self, filename):
        maze = cv2.imread(self.maze_path + filename)
        return maze
    def find_arrow_center(self, maze, arrow_color):
        # Convert image to HSV color space
        hsv = cv2.cvtColor(maze, cv2.COLOR_BGR2HSV)

        if arrow_color == "red":
            lower_range = np.array([0, 100, 100])
            upper_range = np.array([10, 255, 255])
        elif arrow_color == "green":
            lower_range = np.array([40, 50, 50])
            upper_range = np.array([80, 255, 255])

        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower_range, upper_range)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop over contours and find the largest red contour
        largest_contour = None
        largest_contour_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_contour_area:
                largest_contour = contour
                largest_contour_area = area

        # Find the center of the largest red contour (i.e. the center of the arrow)
        M = cv2.moments(largest_contour)
        center_x = int(M['m10'] / M['m00'])
        center_y = int(M['m01'] / M['m00'])

        # Set the start point variable to the center of the arrow
        center = (center_x, center_y)

        # Calculate the bounding rectangle of the largest red contour
        rect = cv2.minAreaRect(largest_contour)
        aspect_ratio = rect[1][0] / rect[1][1]  # width / height
        if aspect_ratio > 1:
            orientation = 'horizontal'
        else:
            orientation = 'vertical'

        # Draw a circle at the center of the arrow on the maze image
        cv2.circle(maze, center, 30, (0, 0, 0), -1)

        # Display the image with the arrow highlighted
        cv2.imshow('Maze', maze)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return center_x, center_y, orientation

if __name__ == '__main__':
    jpg_maze = JpgMaze()
    # jpg_maze.parse_image("test2.png")
    # jpg_maze.parse_image("maze_20_20.png")
    # jpg_maze.parse_image("test.jpg")
    jpg_maze.parse_image("new_maze.png")
    jpg_maze.parse_image("new_maze2.png")



