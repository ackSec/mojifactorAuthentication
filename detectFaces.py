import boto3

# Define a dictionary of emoji for each emotion type
EMOJI_MAP = {
    'HAPPY': '😀',
    'SAD': '😢',
    'ANGRY': '😠',
    'CONFUSED': '😕',
    'DISGUSTED': '🤢',
    'SURPRISED': '😲',
    'CALM': '😌',
    'FEAR': '😨'
}

# Create a Rekognition client
rekognition = boto3.client('rekognition')

# List all objects in the S3 bucket
s3 = boto3.resource('s3')
bucket = s3.Bucket('faces-emojifactor')
objects = bucket.objects.all()

# Loop through all objects in the bucket
for obj in objects:
    # Detect faces in the image and get the emotion data
    response = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': 'faces-emojifactor',
                'Name': obj.key
            }
        },
        Attributes=['ALL']
    )

    # Print the highest confidence result for each emotion
    print('Emotions in {}:'.format(obj.key))
    emotions = {}
    for face_detail in response['FaceDetails']:
        for emotion in face_detail['Emotions']:
            if emotion['Type'] not in emotions or emotion['Confidence'] > emotions[emotion['Type']]:
                emotions[emotion['Type']] = emotion['Confidence']
    for emotion, confidence in emotions.items():
        if confidence == max(emotions.values()):
            emoji = EMOJI_MAP.get(emotion, '❓')
            print('{} {}: {}'.format(emoji, emotion, confidence))
