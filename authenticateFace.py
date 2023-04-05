import boto3
import cv2
import numpy as np
import os

# Set up the Amazon Rekognition client
client = boto3.client('rekognition')

# Load the image of the target face for authentication
target_image = cv2.imread('target.jpg')

# Convert the target image to grayscale
target_image_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

# Initialize the OpenCV video capture object
cap = cv2.VideoCapture(0)

# Loop indefinitely
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use OpenCV's face detection algorithm to find the faces in the frame
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw a rectangle around each face and authenticate it
    for (x, y, w, h) in faces:
        # Extract the face from the frame
        face = frame[y:y+h, x:x+w]

        # Resize the face to match the size of the target image
        face_resized = cv2.resize(face, (target_image.shape[1], target_image.shape[0]))

        # Convert the face to grayscale
        face_resized_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)

        # Calculate the similarity between the target image and the face in the frame
        similarity = cv2.matchTemplate(face_resized_gray, target_image_gray, cv2.TM_CCOEFF_NORMED)

        # Check if the similarity is above a certain threshold
        if similarity > 0.8:
            # Authenticate the face with Amazon Rekognition
            ret, buffer = cv2.imencode('.jpg', face)
            image_bytes = buffer.tobytes()
            response = client.search_faces_by_image(
                CollectionId='my-collection-id',
                Image={'Bytes': image_bytes},
                FaceMatchThreshold=90
            )

            # Check if the face was authenticated
            if len(response['FaceMatches']) > 0:
                print('Authenticated')
            else:
                print('Not authenticated')

        # Draw a rectangle around the face in the frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the video stream in a window
    cv2.imshow('Video Stream', frame)

    # Listen for keyboard events
    key = cv2.waitKey(1)
    if key == ord('q'):  # Quit the program on 'q' key press
        break

# Release the OpenCV video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
