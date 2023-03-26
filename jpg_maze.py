import cv2
import heapq
import os
import numpy as np
from preprocess import Preprocess

class JpgMaze:
    def __init__(self):
        self.maze_path = os.getcwd() + "/maze_samples/"
        self.trials_path = os.getcwd() + "/trials/"

    def start_maze_solver(self, filename):
        self.parse_image(filename)

    def parse_image(self, filename):
        maze_image = self.get_maze(filename)
        maze_image, start_x, start_y, orientation_start, direction_start = self.find_arrow_center(maze_image, "red")
        maze_image, end_x, end_y, orientation_end, direction_end = self.find_arrow_center(maze_image, "green")
        self.remove_arrow_from_image(maze_image, "red")
        self.remove_arrow_from_image(maze_image, "green")
        maze_image = Preprocess().preprocess_image(maze_image)
        maze_image, start_x, start_y, end_x, end_y = self.crop_maze(
            maze_image, start_x, start_y, end_x, end_y, orientation_start, direction_start, orientation_end,
            direction_end
        )
        start = (start_x, start_y)
        end = (end_x, end_y)
        ## START KONTROL ET HATALI

        traced_maze = self.a_star_algorithm(start, end, maze_image)
        cv2.circle(traced_maze, start, 10, (0, 0, 255), thickness=-1)
        cv2.circle(traced_maze, end, 10, (0, 255, 0), thickness=-1)
        cv2.imshow("Result", traced_maze)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #cv2.imwrite(self.trials_path + 'result.jpg', traced_maze)

    def get_least_coordinates(self, maze):
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
                    if col > right:
                        right = col
        return up, down, left, right

    def crop_maze(self, maze, start_x, start_y, end_x, end_y, orientation_start, direction_start, orientation_end,
                  direction_end):
        up, down, left, right = self.get_least_coordinates(maze)
        print("up:", up)
        print("down:", down)
        print("left:", left)
        print("right:", right)
        if orientation_start == "vertical" and orientation_end == "vertical":
            start_x = start_x - left
            end_x = end_x - left
            maze = maze[:, left:right + 1]
        elif orientation_start == "horizontal" and orientation_end == "horizontal":
            start_y = start_y - up
            end_y = end_y - up
            maze = maze[up:down + 1]
        else:
            if (direction_start == "left" and direction_end == "up") or (
                    direction_start == "up" and direction_end == "left"):
                maze = maze[up:down + 1]
                maze = maze[:, left:right + 1]
                start_x = start_x - left
                start_y = start_y - up
                end_x = end_x - left
                end_y = end_y - up
                up, down, left, right = self.get_least_coordinates(maze)
                if direction_start == "up":
                    start_y = down - 1
                    end_x = right - 1
                else:
                    end_y = down - 1
                    start_x = right - 1
            elif (direction_start == "left" and direction_end == "down") or (
                    direction_start == "down" and direction_end == "left"):
                maze = maze[0:down + 1]
                maze = maze[:, left:len(maze)]
                start_x = start_x - left
                end_x = end_x - left
                up, down, left, right = self.get_least_coordinates(maze)
            elif (direction_start == "right" and direction_end == "up") or (
                    direction_start == "up" and direction_end == "right"):
                maze = maze[0:down + 1]
                maze = maze[:, 0:right + 1]
                start_y = start_y - up
                end_y = end_y - up
            elif (direction_start == "right" and direction_end == "down") or (
                    direction_start == "down" and direction_end == "right"):
                maze = maze[up:down + 1]
                maze = maze[:, left:right + 1]
                start_y = start_y - up
                end_y = end_y - up
                start_x = start_x - left
                end_x = end_x - left
                up, down, left, right = self.get_least_coordinates(maze)
                if direction_start == "right":
                    start_x = left + 1
                    end_y = up + 1
                else:
                    end_x = left + 1
                    start_y = up + 1

            up, down, left, right = self.get_least_coordinates(maze)
            print("After color: red x:", start_x, " y:", start_y)
            print("After color: green x:", end_x, " y:", end_y)
            print("up:", up)
            print("down:", down)
            print("left:", left)
            print("right:", right)
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

        rgb_img = cv2.cvtColor(maze_gray, cv2.COLOR_GRAY2RGB)
        cv2.polylines(rgb_img, [np.array(path)], False, (0, 0, 255), thickness=5)
        return rgb_img

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, cell, maze):
        x, y = cell
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(nx, ny) for nx, ny in candidates if
                0 <= nx < maze.shape[1] and 0 <= ny < maze.shape[0] and maze[ny, nx] == 255]



    def get_maze(self, filename):
        maze = cv2.imread(self.maze_path + filename)
        return maze

    def get_least_val_in_largest_contour(self, maze, largest_contour):
        up = len(maze)
        left = len(maze[0])
        down = 0
        right = 0
        for val in largest_contour:
            col = val[0][0]
            row = val[0][1]
            if row < up:
                up = row
            if row > down:
                down = row
            if col < left:
                left = col
            if col > right:
                right = col
        return up, left, down, right

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
        center = (center_x, center_y)

        [vx, vy, x, y] = cv2.fitLine(largest_contour, cv2.DIST_L2, 0, 0.01, 0.01)
        angle = np.arctan2(vy, vx) * 180 / np.pi
        if -45 <= angle < 45:
            orientation = 'horizontal'
            direction = 'right' if center_x < maze.shape[1] // 2 else 'left'
        elif 45 <= angle < 135:
            orientation = 'vertical'
            direction = 'down' if center_y < maze.shape[0] // 2 else 'up'
        elif -135 <= angle < -45:
            orientation = 'vertical'
            direction = 'up' if center_y > maze.shape[0] // 2 else 'down'
        else:
            orientation = 'horizontal'
            direction = 'left' if center_x < maze.shape[1] // 2 else 'right'

        up, left, down, right = self.get_least_val_in_largest_contour(maze, largest_contour)

        if direction == "left":  # WORKS FINE
            center_x = left
            maze = maze[:, 0:left + 1]

        elif direction == "right":  # WORKS FINE
            center_x = 1
            maze = maze[:, right:len(maze[center_x])]

        elif direction == "up":  # WORKS FINE
            center_y = up
            maze = maze[0:up + 1]

        elif direction == "down":  # WORKS FINE
            center_y = 1
            maze = maze[down:len(maze)]

        print("Before Color:", arrow_color, " x:", center_x, " y:", center_y)
        return maze, center_x, center_y, orientation, direction

    def remove_arrow_from_image(self, image, arrow_color):
        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        if arrow_color == "red":
            lower_range = np.array([0, 100, 100])
            upper_range = np.array([10, 255, 255])
        elif arrow_color == "green":
            lower_range = np.array([40, 50, 50])
            upper_range = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_range, upper_range)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (255, 255, 255), -1)
        return image
