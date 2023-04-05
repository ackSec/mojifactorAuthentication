import boto3
import cv2
import numpy as np

# Initialize the Amazon Rekognition client
rekognition = boto3.client('rekognition')

# Initialize the OpenCV video capture object
cap = cv2.VideoCapture(0)

# Take the user's name as input
name = input('Please enter your name: ')

# Load the target image for authentication
target_image = cv2.imread('target.jpg')

# Convert the target image to grayscale
target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

# Detect the keypoints and descriptors in the target image using ORB
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(target_gray, None)

# Initialize the flag for authentication
authenticated = False

# Loop indefinitely
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the keypoints and descriptors in the current frame using ORB
    kp2, des2 = orb.detectAndCompute(gray, None)

    # Initialize the BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match the descriptors of the target image and the current frame
    matches = bf.match(des1, des2)

    # Sort the matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw the top 10 matches on the current frame
    img_matches = cv2.drawMatches(target_gray, kp1, gray, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Display the video stream in a window
    cv2.imshow('Video Stream', img_matches)

    # Authenticate if there is a match
    if len(matches) > 0 and matches[0].distance < 50:
        authenticated = True
        
        # Capture the frame upon authentication and save it to the running directory
        cv2.imwrite('authenticated.jpg', frame)
        
        break

    # Listen for keyboard events
    key = cv2.waitKey(1)
    if key == ord('q'):  # Quit the program on 'q' key press
        break

# Release the OpenCV video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

# Print authentication result
if authenticated:
    print('Authenticated as', name)
else:
    print('Authentication failed')
