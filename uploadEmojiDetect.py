import boto3
from emojiMap import emoji_map

# Create a Rekognition client
rekognition = boto3.client('rekognition')

# Specify the name of the file to upload
filename = 'upload.jpg'

# Open the file
with open(filename, 'rb') as image_file:
    # Call the Rekognition detect_faces API
    response = rekognition.detect_faces(
        Image={'Bytes': image_file.read()},
        Attributes=['ALL']
    )

    # Add the detected emotions to the emotions_list
    emotions_list = []
    for face_detail in response['FaceDetails']:
        for emotion in face_detail['Emotions']:
            emotions_list.append(emotion['Type'])

    # Display the detected emotions as emojis
    if len(emotions_list) > 0:
        emojis = [emoji_map.get(max(set(emotions_list), key = emotions_list.count), '')]
        print('Emotion:', emojis[0])
    else:
        print('No emotions detected')
