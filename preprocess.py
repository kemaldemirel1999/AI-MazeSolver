
import cv2

# Load the maze image
maze = cv2.imread('/Users/kemaldemirel/Desktop/Lectures/Yap 441/Project_Code/AI-MazeSolver/labirentler/test.jpg')

# Convert the maze image to grayscale
gray = cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY)

# Apply binary thresholding with a threshold value of 127
thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

# Invert the binary image so that walls are black and background is white


# Save the preprocessed image
cv2.imwrite("preprocessed_maze.jpg", thresh)


import cv2
import numpy as np

# Load the preprocessed maze image
maze = cv2.imread("preprocessed_maze.jpg", 0)

# Detect contours in the image
contours, hierarchy = cv2.findContours(maze, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop through the contours to find the arrow
for i, contour in enumerate(contours):
    # Approximate the contour as a polygon
    polygon = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
    # Check if the polygon has 3 vertices (triangle)
    if len(polygon) == 3:
        # Get the coordinates of the vertices
        x1, y1 = polygon[0][0]
        x2, y2 = polygon[1][0]
        x3, y3 = polygon[2][0]
        # Calculate the centroid of the triangle
        cx = int((x1 + x2 + x3) / 3)
        cy = int((y1 + y2 + y3) / 3)
        # Draw a circle at the centroid
        cv2.circle(maze, (cx, cy), 5, (255, 0, 0), 2)
        # Print the coordinates of the centroid
        print("Start point found at ({}, {})".format(cx, cy))

# Save the image with the detected start point
cv2.imwrite("start_point.jpg", maze)
