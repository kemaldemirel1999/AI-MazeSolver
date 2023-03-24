import cv2
import heapq
import os
import numpy as np
class JpgMaze:
    def __init__(self):
        self.maze_path = os.getcwd() + "/maze_samples/"
        self.trials_path = os.getcwd() + "/trials/"
    def parse_image(self, filename):
        maze_image = self.get_maze(filename)
        start_x, start_y, orientation = self.find_arrow_center(maze_image, "red")
        end_x, end_y, orientation = self.find_arrow_center(maze_image, "green")

        self.remove_arrow_from_image(maze_image, "red")
        self.remove_arrow_from_image(maze_image, "green")
        maze_gray = self.preprocess_image(maze_image)
        start = (start_x, start_y)
        end = (end_x, end_y)
        maze_gray, start_x, start_y, end_x, end_y = self.crop_maze(maze_gray, start_x, start_y, end_x, end_y)
        start = (start_x, start_y)
        end = (end_x, end_y)
        self.a_star_algorithm(start, end, maze_gray)
        cv2.imwrite(self.trials_path + 'processed_image.jpg', maze_gray)

    def crop_maze(self, maze, start_x, start_y, end_x, end_y):
        up = len(maze)
        left = len(maze[0])
        down = 0
        right = 0
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if maze[row][col] == 0:
                    if row < up:
                        up = row
                    if row > down:
                        down = row
                    if col < left:
                        left = col
                        start_x = start_x - left
                        end_x = end_x - left
                    if col > right:
                        right = col
        maze = maze[:, left:right+1]
        return maze, start_x, start_y, end_x, end_y

    def a_star_algorithm(self, start, end, maze_gray):

        visited = set()
        queue = [(self.heuristic(start, end), 0, start, [])]
        while queue:
            _, cost, cell, path = heapq.heappop(queue)
            if cell in visited:
                continue
            visited.add(cell)
            path = path + [cell]
            if cell == end:
                break
            for neighbor in self.neighbors(cell, maze_gray):
                if neighbor not in visited:
                    neighbor_cost = cost + 1
                    neighbor_priority = neighbor_cost + self.heuristic(neighbor, end)
                    heapq.heappush(queue, (neighbor_priority, neighbor_cost, neighbor, path))


        for i in range(len(path) - 1):
            cv2.line(maze_gray, path[i], path[i + 1], (0, 0, 255), 20)

    def heuristic(self,a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Define neighbors function
    def neighbors(self,cell, maze):
        x, y = cell
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(nx, ny) for nx, ny in candidates if
                0 <= nx < maze.shape[1] and 0 <= ny < maze.shape[0] and maze[ny, nx] == 255]


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

        return center_x, center_y, orientation

    def remove_arrow_from_image(self, image, arrow_color):
        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        if arrow_color == "red":
            lower_range = np.array([0, 100, 100])
            upper_range = np.array([10, 255, 255])
        elif arrow_color == "green":
            lower_range = np.array([40, 50, 50])
            upper_range = np.array([80, 255, 255])

        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower_range, upper_range)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Draw white filled contours over the red arrow to remove it
        cv2.drawContours(image, contours, -1, (255, 255, 255), -1)

        # Save the image
        return image

if __name__ == '__main__':
    jpg_maze = JpgMaze()
    # jpg_maze.parse_image("test2.png")
    # jpg_maze.parse_image("maze_20_20.png")
    # jpg_maze.parse_image("test.jpg")
    jpg_maze.parse_image("new_maze.png")
    #jpg_maze.parse_image("new_maze2.png")



