
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.41.0" # Specify a version known to work with your configuration
    }
  }
}


provider "aws" {
  region = "ca-central-1" # Target the Canada (Central) region
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket where the XGBoost model is stored"
  type        = string
  default     = "bucket_name"
}

variable "model_path" {
  description = "The S3 path to the XGBoost model artifact"
  type        = string
  default     = "model.tar.gz"
}

# IAM role for SageMaker to access resources
resource "aws_iam_role" "sagemaker_role" {
  name = "SageMakerExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
        Effect = "Allow"
        Sid    = ""
      },
    ]
  })
}

# IAM policy to allow SageMaker access to S3
resource "aws_iam_policy" "sagemaker_s3_access" {
  name = "SageMakerS3AccessPolicy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket",
        ],
        Resource = [
          "arn:aws:s3:::${var.s3_bucket_name}",
          "arn:aws:s3:::${var.s3_bucket_name}/*",
        ],
        Effect = "Allow",
      },
    ]
  })
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "sagemaker_s3_access" {
  role       = aws_iam_role.sagemaker_role.name
  policy_arn = aws_iam_policy.sagemaker_s3_access.arn
}

# SageMaker model using an existing S3 bucket and model path
resource "aws_sagemaker_model" "xgb_model" {
  name = "xgb-model-${var.s3_bucket_name}"

  execution_role_arn = aws_iam_role.sagemaker_role.arn

  primary_container {
    image         = "341280168497.dkr.ecr.ca-central-1.amazonaws.com/sagemaker-xgboost:1.7-1" # SageMaker XGBoost built-in image
    model_data_url = "s3://${var.s3_bucket_name}/${var.model_path}"
    # environment = {
    #   SAGEMAKER_PROGRAM = "custom_inference_code.py" # Specify if using custom inference code
    # }
  }
}

# SageMaker endpoint configuration
resource "aws_sagemaker_endpoint_configuration" "xgb_endpoint_config" {
  name = "xgb-model-endpoint-config-${var.s3_bucket_name}"

  production_variants {
    variant_name          = "AllTraffic"
    model_name            = aws_sagemaker_model.xgb_model.name
    initial_instance_count = 1
    instance_type         = "ml.m4.xlarge"
  }
}

# SageMaker endpoint
resource "aws_sagemaker_endpoint" "xgb_endpoint" {
  name                 = "xgb-model-endpoint-${var.s3_bucket_name}"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.xgb_endpoint_config.name
}
