import boto3

def detect_emotion(image_bytes):
    # Set up the AWS client
    rekognition = boto3.client('rekognition')

    # Detect the emotions in the image
    response = rekognition.detect_faces(
        Image={
            'Bytes': image_bytes
        },
        Attributes=['ALL']
    )

    # Check if any faces are detected
    if len(response['FaceDetails']) == 0:
        return None

    # Get the emotion with the highest confidence
    emotions = response['FaceDetails'][0]['Emotions']
    emotion = max(emotions, key=lambda e: e['Confidence'])

    return emotion['Type']
