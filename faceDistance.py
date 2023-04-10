# Takes a reference photo from S3 and measures the similarity between
# it and faces a user makes on the webcam.
#
#

import boto3
import cv2
import numpy as np
import time
import os

# Set up AWS Rekognition and S3 clients
rekognition = boto3.client("rekognition")
s3 = boto3.client("s3")

# Provide the S3 bucket and key for the resting face image
resting_face_bucket = "faces-emojifactor"
resting_face_key = "Jon.jpg"

def download_image_from_s3(bucket, key, local_path):
    s3.download_file(bucket, key, local_path)

def compare_faces(source_bucket, source_key, target_image):
    try:
        response = rekognition.compare_faces(
            SourceImage={"S3Object": {"Bucket": source_bucket, "Name": source_key}},
            TargetImage={"Bytes": target_image},
        )
        if len(response["FaceMatches"]) > 0:
            similarity = response["FaceMatches"][0]["Similarity"]
            return similarity
        else:
            return 0
    except Exception as e:
        print(f"Error in compare_faces: {e}")
        return 0

# Download the resting face image from S3 to verify it exists
local_resting_face_path = "resting_face_downloaded.jpg"
download_image_from_s3(resting_face_bucket, resting_face_key, local_resting_face_path)

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to open the webcam.")
    exit()

time.sleep(1)  # Wait for 1 second to allow the camera to adjust

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to bytes
    frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

    # Compare the current frame to the hardcoded resting face
    similarity = compare_faces(resting_face_bucket, resting_face_key, frame_bytes)
    print(f"Similarity: {similarity}")

    # Display the resulting frame
    cv2.putText(frame, f"Similarity: {similarity}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow("Frame", frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
