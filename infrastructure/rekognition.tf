provider "aws" {
  region = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS account ID"
  type        = string
}

variable "s3_bucket_arn" {
  description = "ARN of the S3 bucket for Rekognition output"
  type        = string
}

variable "kinesis_video_stream_arn" {
  description = "ARN of the Kinesis Video Stream"
  type        = string
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
  policy_arn = "arn:aws:iam::${var.aws_account_id}:policy/AmazonRekognitionReadOnlyAccess"
  role       = aws_iam_role.rekognition_processor_role.name
}
