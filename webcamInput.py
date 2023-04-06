import cv2

def webcam_input():
    # Initialize the OpenCV video capture object
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()

        # Display the video stream in a window
        cv2.imshow('Video Stream', frame)

        # Listen for keyboard events
        key = cv2.waitKey(1)
        if key == ord('q'):  # Quit the program on 'q' key press
            break

    # Release the OpenCV video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    webcam_input()
