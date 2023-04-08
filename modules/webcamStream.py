import cv2
from common.detectEmotions import detect_emotion
from common.emojiMap import emoji_map

# Initialize the video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a frame from the video stream
    ret, frame = video_capture.read()

    # Detect the emotion from the frame
    emotion = detect_emotion(cv2.imencode('.jpg', frame)[1].tobytes())

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Check if an emotion is detected
    if emotion is not None:
        # Print the detected emotion to the console
        print(f'Detected emotion: {emotion}')

    # Check if the user wants to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()
