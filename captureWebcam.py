import cv2
import boto3
from emojiMap import emoji_map

# Create a Rekognition client
rekognition = boto3.client('rekognition')

def detect_emotions_from_image(image_path):
    # Load the image file
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    # Call the Rekognition detect_faces API
    response = rekognition.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']
    )

    # Get the strongest emotion
    emotions = []
    for face_detail in response['FaceDetails']:
        for emotion in face_detail['Emotions']:
            emotions.append((emotion['Type'], emotion['Confidence']))
    emotions.sort(key=lambda x: x[1], reverse=True)
    strongest_emotion = emotions[0][0] if len(emotions) > 0 else None

    return strongest_emotion

def detect_emotions_from_webcam():
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

        # Get the strongest emotion
        emotions = []
        for face_detail in response['FaceDetails']:
            for emotion in face_detail['Emotions']:
                emotions.append((emotion['Type'], emotion['Confidence']))
        emotions.sort(key=lambda x: x[1], reverse=True)
        strongest_emotion = emotions[0][0] if len(emotions) > 0 else None

        # Display the detected emotion as an emoji
        if strongest_emotion is not None:
            emoji = emoji_map.get(strongest_emotion, '')
            print('Emotion:', emoji)

        # Display the video stream in a window
        cv2.imshow('Video Stream', frame)

        # Listen for keyboard events
        key = cv2.waitKey(1)
        if key == ord('q'):  # Quit the program on 'q' key press
            break

    # Release the OpenCV video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
