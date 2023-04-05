provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "rekognition_processor_role" {
  name = "rekognition-processor-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "rekognition.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rekognition_processor_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonRekognitionReadOnlyAccess"
  role       = aws_iam_role.rekognition_processor_role.name
}

resource "aws_kinesis_video_stream_processor" "example_processor" {
  name = "example-processor"
  kinesis_video_stream_arn = aws_kinesis_video_stream.example_stream.arn
  role_arn = aws_iam_role.rekognition_processor_role.arn
  input {
    kinesis_video_stream {
      arn = aws_kinesis_video_stream.example_stream.arn
    }
  }
  output {
    s3 {
      bucket_arn = "arn:aws:s3:::example-bucket"
      role_arn   = aws_iam_role.rekognition_processor_role.arn
    }
  }
  processing_configuration {
    face_detection {
      face_detection_model_version = "2.0"
      face_search_threshold        = 90
    }
    emotion_detection {
      model_name =
