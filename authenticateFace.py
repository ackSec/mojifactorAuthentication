import cv2
import boto3
import time
import os

BUCKET_NAME = 'faces-emojifactor'


def download_images_from_s3():
    s3 = boto3.client('s3')
    images = []
    result = s3.list_objects(Bucket=BUCKET_NAME)

    for content in result.get('Contents', []):
        file_key = content['Key']
        file_name = os.path.basename(file_key)
        if file_name.lower().endswith('.jpg'):
            local_path = os.path.join('/tmp', file_name)
            with open(local_path, 'wb') as f:
                s3.download_fileobj(BUCKET_NAME, file_key, f)
            with open(local_path, 'rb') as f:
                image_bytes = f.read()
            os.remove(local_path)
            images.append((file_name, image_bytes))

    return images


def compare_frame_to_images(frame, images):
    rekognition = boto3.client('rekognition')
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
        raise RuntimeError("Unable to open camera.")

    time.sleep(1)

    ret, frame = video_capture.read()
    video_capture.release()

    if not ret:
        raise RuntimeError("Failed to capture frame from camera.")

    return compare_frame_to_images(frame, target_images)
