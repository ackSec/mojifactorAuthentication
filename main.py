import authenticateFace
import captureWebcam
import cv2
import emojiAuthentication

# Authenticate the user
if authenticateFace.authenticate_user():
    # Start capturing webcam data and detecting emotions
    emojiAuthentication.show_random_emoji()
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'): # Exit the program on 'q' key press
            break
        captureWebcam.detect_emotions()
else:
    print('Authentication failed')

# Release the OpenCV video capture object and close all windows
cv2.destroyAllWindows()
