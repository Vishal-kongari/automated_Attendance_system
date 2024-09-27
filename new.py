
import cv2
import numpy as np

# Step 1: Load the image
image = cv2.imread('C:/Users/Rammohan/projects/face_attendance_system/data/23241a0533.png')

# Step 2: Convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Step 3: Define the lower and upper bounds for the blue color
lower_blue = np.array([100, 150, 0])
upper_blue = np.array([140, 255, 255])

# Step 4: Create a mask
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Step 5: Mask the original image using bitwise_and
result = cv2.bitwise_and(image, image, mask=mask)

# Step 6: Show the result
cv2.imshow('Original Image', image)
cv2.imshow('Mask', mask)
cv2.imshow('Result', result)

cv2.waitKey(0)
cv2.destroyAllWindows()
