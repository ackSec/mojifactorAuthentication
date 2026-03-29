import cv2
import time
from common.detectEmotions import detect_emotion
from common.emojiMap import emoji_map


def display_countdown(countdown_seconds):
    for i in range(countdown_seconds, 0, -1):
        print(f"Capturing in {i} seconds...")
        time.sleep(1)


def runner():
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        raise RuntimeError("Unable to open camera.")

    time.sleep(2)

    ret, frame = video_capture.read()
    video_capture.release()
    cv2.destroyAllWindows()

    if not ret:
        raise RuntimeError("Failed to capture frame from camera.")

    emotion = detect_emotion(cv2.imencode('.jpg', frame)[1].tobytes())

    if emotion is not None:
        print(f'Detected emotion: {emotion}')
        print(f'Corresponding emoji: {emoji_map.get(emotion, "❓")}')
    else:
        print('No emotion detected')

    return emotion
