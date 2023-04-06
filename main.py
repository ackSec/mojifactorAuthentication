#import authenticateFace
import cv2
import emojiAuthentication
from authenticateFace import authenticate_face

# Call the authenticate_face function
authenticate_face()


# Authenticate the user
if authenticateFace.authenticated:
    # Show random emojis
    #emojiAuthentication.show_random_emoji()

    # Start capturing webcam data and detecting emotions
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'): # Exit the program on 'q' key press
            break
        captureWebcam.detect_emotions_from_webcam()
#else:
    print('Authentication failed')

# Release the OpenCV video capture object and close all windows
cv2.destroyAllWindows()
