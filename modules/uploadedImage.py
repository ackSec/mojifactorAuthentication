import os
import boto3
from common.emojiMap import emoji_map

# Initialize the Amazon Rekognition client
rekognition = boto3.client('rekognition')

# Find the upload file in the root directory
upload_file = None
for filename in os.listdir('.'):
    if filename.startswith('upload.'):
        upload_file = filename
        break

if upload_file is None:
    print('Could not find an upload file')
    exit(1)

# Load the target image
with open(upload_file, 'rb') as f:
    target_bytes = f.read()

# Call the Rekognition detect_faces API
response = rekognition.detect_faces(
    Image={'Bytes': target_bytes},
    Attributes=['ALL']
)

# Extract the emotions with their confidence percentages
emotions_list = []
for face_detail in response['FaceDetails']:
    for emotion in face_detail['Emotions']:
        emotions_list.append((emotion['Type'], emotion['Confidence']))

# Sort the emotions by confidence (highest to lowest)
emotions_list.sort(key=lambda x: x[1], reverse=True)

# Display the emoji and percentage of the most prominent emotion
emoji = emoji_map.get(emotions_list[0][0], '')
percentage = emotions_list[0][1]
print(f'{emoji} ({percentage:.2f}%)\n')

# Display the percentages of the other emotions
for emotion, percentage in emotions_list[1:]:
    print(f'{emotion}: {percentage:.2f}%')
