import cv2
import boto3
import time
import os

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

bucket_name = 'faces-emojifactor'

def download_images_from_s3():
    images = []
    result = s3.list_objects(Bucket=bucket_name)

    for content in result.get('Contents', []):
        file_key = content['Key']
        file_name = os.path.basename(file_key)
        if file_name.lower().endswith('.jpg'):
            with open(file_name, 'wb') as f:
                s3.download_fileobj(bucket_name, file_key, f)
            with open(file_name, 'rb') as f:
                image_bytes = f.read()
            images.append((file_name, image_bytes))

    return images

def compare_frame_to_images(frame, images):
    for image_name, image_bytes in images:
        compare_response = rekognition.compare_faces(
            SourceImage={
                'Bytes': image_bytes
            },
            TargetImage={
                'Bytes': cv2.imencode('.jpg', frame)[1].tobytes()
            }
        )

        if len(compare_response['FaceMatches']) > 0:
            return os.path.splitext(image_name)[0]

    return None

def runner():
    target_images = download_images_from_s3()
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Unable to open camera.")
        exit()

    time.sleep(1)  # Wait for 1 second to allow the camera to adjust

    ret, frame = video_capture.read()

    recognized_name = compare_frame_to_images(frame, target_images)

    if recognized_name:
        print(f"Welcome, {recognized_name}")
    else:
        print("Sorry, I don't know you")

    video_capture.release()
