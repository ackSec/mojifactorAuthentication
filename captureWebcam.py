import cv2
import boto3
import os 
import sys
from emojiMap import emoji_map

# Create a Rekognition client
rekognition = boto3.client('rekognition')

# Initialize the OpenCV video capture object
cap = cv2.VideoCapture(0)

# Loop indefinitely
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to JPEG format
    ret, buffer = cv2.imencode('.jpg', frame)
    image_bytes = buffer.tobytes()

    # Call the Rekognition detect_faces API
    response = rekognition.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']
    )

    # Add the detected emotions to the emotions_list
    emotions_list = []
    for face_detail in response['FaceDetails']:
        for emotion in face_detail['Emotions']:
            emotions_list.append(emotion['Type'])

    # Display the detected emotions as emojis
    if len(emotions_list) > 0:
        emojis = [emoji_map.get(emotion, '') for emotion in emotions_list]
        print('Emotions:', ' '.join(emojis))

    # Display the video stream in a window
    cv2.imshow('Video Stream', frame)

    # Listen for keyboard events
    key = cv2.waitKey(1)
    if key == ord('q'):  # Quit the program on 'q' key press
        break

# Release the OpenCV video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
