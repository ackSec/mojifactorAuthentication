# This takes an image from an S3 bucket and authenticates it to the person on the webcam
#
#

import cv2
import boto3

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

bucket_name = 'faces-emojifactor'
object_key = 'target.jpg'


with open('target.jpg', 'wb') as f:
    s3.download_fileobj(bucket_name, object_key, f)


with open('target.jpg', 'rb') as f:
    target_image_bytes = f.read()


video_capture = cv2.VideoCapture(0)

while True:
    # Capture a frame from the video stream
    ret, frame = video_capture.read()

    # Detect faces in the frame using Rekognition
    response = rekognition.detect_faces(
        Image={
            'Bytes': cv2.imencode('.jpg', frame)[1].tobytes()
        }
    )

    # Check if any face is detected
    if len(response['FaceDetails']) > 0:
        # Compare the detected face with the target image using Rekognition
        compare_response = rekognition.compare_faces(
            SourceImage={
                'Bytes': target_image_bytes
            },
            TargetImage={
                'Bytes': cv2.imencode('.jpg', frame)[1].tobytes()
            }
        )

        # Check if the detected face matches the target image
        if len(compare_response['FaceMatches']) > 0:
            print('Match found!')
            # TODO: Add shtuff here 
        else:
            print('No match found')

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Check if the user wants to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()
