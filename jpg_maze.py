import cv2
import heapq
import os
import numpy as np
from preprocess import Preprocess


class JpgMaze:
    def __init__(self):
        self.maze_path = os.getcwd() + "/maze_samples/"
        self.trials_path = os.getcwd() + "/trials/"
        self.kaggle_path = os.getcwd() + "/kaggle_maze_dataset/rectangular_mazes_10x10/"
        self.results_path = os.getcwd() + "/results/"
        self.kaggle_results_path = os.getcwd()+"kaggle_results/"

    def start_maze_solver(self, filename, kaggle_dataset=False):
        self.parse_image(filename, kaggle_dataset)

    def parse_image(self, filename, kaggle_dataset):
        maze = self.get_maze(filename, kaggle_dataset)
        if self.includes_arrow(maze, "red") and self.includes_arrow(maze, "green"):
            maze, start_x, start_y, direction_start, left, right, up, down = self.find_arrow_coordinates(maze, "red")
            maze = self.remove_arrow_from_image(maze, left, right, up, down)
            maze, end_x, end_y, direction_end, left, right, up, down = self.find_arrow_coordinates(maze, "green")
            maze = self.remove_arrow_from_image(maze, left, right, up, down)
            maze = Preprocess().preprocess_image(maze)

            maze, start_x, start_y, end_x, end_y = self.crop_maze(maze, start_x, start_y, end_x, end_y, direction_start,
                                                                  direction_end)
            start = (start_x, start_y)
            end = (end_x, end_y)
        else:
            maze = Preprocess().preprocess_image(maze)
            start_x, start_y, end_x, end_y = self.find_start_end_points(maze)
            start = (start_x, start_y)
            end = (end_x, end_y)

        traced_maze = self.a_star_algorithm(start, end, maze)

        if not kaggle_dataset:
            cv2.imwrite(self.results_path + filename, traced_maze)
        else:
            cv2.imwrite(self.kaggle_results_path + filename, traced_maze)



    def find_start_end_points(self, maze):
        up, down, left, right = self.get_least_coordinates(maze)
        first_col = maze[:, 0]
        last_col = maze[:, len(maze[0])-1]
        first_row = maze[0]
        last_row = maze[len(maze)-1]
        start_x = -1
        start_y = -1
        end_x = -1
        end_y = -1

        start_found = False
        end_found = False
        for i in range(len(first_row)):
            if first_row[i] == 255 and not start_found:
                start_x = i
                start_y = 0
                start_found = True
                break
        for i in range(len(last_row)):
            if last_row[i] == 255 and not start_found:
                end_y = len(maze)-1
                end_x = i
                start_found = True
                break
            elif last_row[i] == 255 and not end_found:
                end_y = len(maze)-1
                end_x = i
                end_found = True
                break
        for i in range(len(first_col)):
            if first_col[i] == 255 and not start_found:
                start_y = i
                start_x = 0
                start_found = True
                break
            elif first_col[i] == 255 and not end_found:
                end_y = i
                end_x = 0
                end_found = True
                break
        for i in range(len(last_col)):
            if last_col[i] == 255 and not start_found:
                start_y = i
                start_x = len(maze[0])-1
                start_found = True
                break
            elif last_col[i] == 255 and not end_found:
                end_y = i
                end_x = len(maze[0])-1
                end_found = True
                break
        if not start_found or not end_found:
            return None
        else:
            return start_x, start_y, end_x, end_y

    def includes_arrow(self, maze, arrow_color):
        hsv = cv2.cvtColor(maze, cv2.COLOR_BGR2HSV)
        if arrow_color == "red":
            lower_range = np.array([0, 100, 100])
            upper_range = np.array([10, 255, 255])
        elif arrow_color == "green":
            lower_range = np.array([40, 50, 50])
            upper_range = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_range, upper_range)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = None
        largest_contour_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_contour_area:
                largest_contour = contour
                largest_contour_area = area
        if largest_contour is not None:
            return True
        else:
            return False
    def crop_maze(self, maze, start_x, start_y, end_x, end_y, direction_start, direction_end):
        up, down, left, right = self.get_least_coordinates(maze)

        if (direction_start == "left" and direction_end == "right") \
                or (direction_end == "left" and direction_start == "right") \
                or (direction_end == "left" and direction_start == "left")\
                or (direction_end == "right" and direction_start == "right"):
            maze = maze[up:len(maze)]
            start_y = start_y - up
            end_y = end_y - up
            up, down, left, right = self.get_least_coordinates(maze)
            maze = maze[0:down + 1]
        elif (direction_start == "up" and direction_end == "down") \
                or (direction_end == "up" and direction_start == "down") \
                or (direction_end == "up" and direction_start == "up")\
                or (direction_end == "down" and direction_start == "down"):
            maze = maze[:, left:len(maze[0]) + 1]
            start_x = start_x - left
            end_x = end_x - left
            up, down, left, right = self.get_least_coordinates(maze)
            maze = maze[:, 0:right + 1]
        else:
            is_start_inside = self.is_it_inside_of_maze(maze, start_x, start_y)
            is_end_inside = self.is_it_inside_of_maze(maze, end_x, end_y)
            if is_start_inside and is_end_inside:
                print("both inside")
                maze = maze[:, left:right + 1]
                start_x = start_x - left
                end_x = end_x - left
                maze = maze[up:down + 1]
                start_y = start_y - up
                end_y = end_y - up
            elif is_start_inside:
                print("Start inside")
                maze = maze[:, left:right + 1]
                start_x = start_x - left
                end_x = end_x - left
            elif is_end_inside:
                print("End inside")
                maze = maze[up:down + 1]
                start_y = start_y - up
                end_y = end_y - up
            else:
                print("both outside")
                if direction_start == "left" and direction_end =="up":
                    maze, start_x, start_y, end_x, end_y = self.crop_south(maze, start_x, start_y, end_x, end_y, direction_start, direction_end, False)
                elif direction_start == "left" and direction_end == "down":
                    None
                elif direction_start == "right" and direction_end == "up":
                    maze, start_x, start_y, end_x, end_y = self.crop_south(maze, start_x, start_y, end_x, end_y, direction_start, direction_end, False)
                elif direction_start == "right" and direction_end == "down":
                    None
                elif direction_start == "up" and direction_end == "left":
                    maze, start_x, start_y, end_x, end_y = self.crop_south(maze, start_x, start_y, end_x, end_y, direction_start, direction_end, True)
                elif direction_start == "up" and direction_end == "right":
                    maze, start_x, start_y, end_x, end_y = self.crop_south(maze, start_x, start_y, end_x, end_y, direction_start, direction_end, True)
                elif direction_start == "down" and direction_end == "left":
                    None
                elif direction_start == "down" and direction_end == "right":
                    None

        return maze, start_x, start_y, end_x, end_y

    def crop_south(self, maze, start_x, start_y, end_x, end_y, direction_start, direction_end, isItStart):
        up, down, left, right = self.get_least_coordinates(maze)
        if direction_start == "up" and isItStart:
            maze = maze[0:down + 1]
            diff_y = len(maze) - down
            end_y = end_y - diff_y
            up, down, left, right = self.get_least_coordinates(maze)
            start_y = down - 1
        elif direction_end == "up" and not isItStart:
            maze = maze[0:down + 1]
            diff_y = len(maze) - down
            start_y = start_y - diff_y
            up, down, left, right = self.get_least_coordinates(maze)
            end_y = down - 1
        else:
            print("Wrong Crop South Input")
        return maze, start_x, start_y, end_x, end_y
    def is_it_inside_of_maze(self, maze, x_coord, y_coord):
        up = len(maze)
        left = len(maze[0])
        down = 0
        right = 0
        maze_row = maze[y_coord]
        maze_col = maze[:, x_coord]
        for col in range(len(maze_row)):
            if maze_row[col] == 0:
                if col < left:
                    left = col
                if col > right:
                    right = col
        for row in range(len(maze_col)):
            if maze_col[row] == 0:
                if row < up:
                    up = row
                if row > down:
                    down = row
        if left < x_coord < right and down > y_coord > up:
            return True
        else:
            return False

    def get_least_coordinates(self, maze):
        up = len(maze)
        left = len(maze[0])
        down = 0
        right = 0
        for row in range(len(maze)):
            for col in range(len(maze[0])):
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

    def get_maze(self, filename, kaggle_dataset):
        if kaggle_dataset:
            maze = cv2.imread(self.kaggle_path + filename)
        else:
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

    def find_arrow_coordinates(self, maze, arrow_color):
        hsv = cv2.cvtColor(maze, cv2.COLOR_BGR2HSV)
        if arrow_color == "red":
            lower_range = np.array([0, 100, 100])
            upper_range = np.array([10, 255, 255])
        elif arrow_color == "green":
            lower_range = np.array([40, 50, 50])
            upper_range = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_range, upper_range)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = None
        largest_contour_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_contour_area:
                largest_contour = contour
                largest_contour_area = area
        M = cv2.moments(largest_contour)

        center_x = int(M['m10'] / M['m00'])
        center_y = int(M['m01'] / M['m00'])
        [vx, vy, x, y] = cv2.fitLine(largest_contour, cv2.DIST_L2, 0, 0.01, 0.01)
        angle = np.arctan2(vy, vx) * 180 / np.pi
        if -45 <= angle < 45:
            direction = 'right' if center_x < maze.shape[1] // 2 else 'left'
        elif 45 <= angle < 135:
            direction = 'down' if center_y < maze.shape[0] // 2 else 'up'
        elif -135 <= angle < -45:
            direction = 'up' if center_y > maze.shape[0] // 2 else 'down'
        else:
            direction = 'left' if center_x < maze.shape[1] // 2 else 'right'
        up, left, down, right = self.get_least_val_in_largest_contour(maze, largest_contour)
        x_axis = 0
        y_axis = 0
        if direction == "left":
            x_axis = left
            y_axis = center_y
        elif direction == "right":
            x_axis = right
            y_axis = center_y
        elif direction == "down":
            x_axis = center_x
            y_axis = down
        else:
            x_axis = center_x
            y_axis = up
        # coordinates = (x_axis, y_axis)
        return maze, x_axis, y_axis, direction, left, right, up, down

    def remove_arrow_from_image(self, image, left, right, up, down):
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (left, up), (right, down), 255, -1)
        result = image.copy()
        result[np.where(mask == 255)] = [255, 255, 255]
        return result
