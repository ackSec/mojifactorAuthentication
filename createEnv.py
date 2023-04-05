import boto3

# Create a Kinesis Video Streams client
kinesis_video = boto3.client('kinesisvideo')

# Create a new Kinesis Video Streams stream
response = kinesis_video.create_stream(
    StreamName='emojifactor-auth',
    MediaType='video/h264',
    DataRetentionInHours=24
)

# Get the stream ARN
stream_arn = response['StreamARN']

# Create an Amazon Rekognition client
rekognition = boto3.client('rekognition')

# Create a new Amazon Rekognition collection
collection_name = 'emojifactor_collection'
rekognition.create_collection(CollectionId=collection_name)
