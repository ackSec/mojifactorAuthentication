import boto3
import csv

# Create a Rekognition client
rekognition = boto3.client('rekognition')

# Read the FER2013 dataset CSV file
with open('fer2013.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row
    for row in reader:
        # Parse the image data and label from the row
        pixels = [int(p) for p in row[1].split()]
        label = row[0]

        # Convert the pixel values to bytes
        bytes_data = bytearray(pixels)

        # Add the face to the Rekognition collection with the label as the external ID
        rekognition.index_faces(
            CollectionId='my-collection',
            Image={
                'Bytes': bytes_data
            },
            ExternalImageId=label
        )
