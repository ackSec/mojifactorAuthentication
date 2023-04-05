import authenticateFace
import captureWebcam

# Authenticate the user
if authenticateFace.authenticate_user():
    # Start capturing webcam data and detecting emotions
    captureWebcam.detect_emotions()
else:
    print('Authentication failed')
