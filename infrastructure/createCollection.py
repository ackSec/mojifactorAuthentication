# Training script: indexes faces from the FER2013 dataset into a Rekognition collection.
# FER2013 contains 48x48 grayscale pixel arrays, which must be converted to
# PNG before sending to Rekognition (it requires encoded image bytes, not raw pixels).

import boto3
import csv
import io
from PIL import Image

rekognition = boto3.client('rekognition')

COLLECTION_ID = 'my-collection'

with open('fer2013.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        pixels = [int(p) for p in row[1].split()]
        label = row[0]

        # Convert raw pixels to a 48x48 grayscale image, then encode as PNG
        img = Image.new('L', (48, 48))
        img.putdata(pixels)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()

        rekognition.index_faces(
            CollectionId=COLLECTION_ID,
            Image={'Bytes': image_bytes},
            ExternalImageId=label
        )
