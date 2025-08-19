resource "aws_iam_role" "glue_role" {
  name = var.glue_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "glue.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "glue_policy" {
  name = "glue-s3-access"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${var.s3_bucket_name_scripts}",
          "arn:aws:s3:::${var.s3_bucket_name_scripts}/*",
          "arn:aws:s3:::${var.s3_bucket_name_salesforce}",
          "arn:aws:s3:::${var.s3_bucket_name_salesforce}/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ],
        Resource = "*"
      }
    ]
  })
}

data "aws_secretsmanager_secret" "salesforce_secret" {
  name = var.salesforce_secret_name
}

resource "aws_iam_policy" "salesforce_secret_access" {
  name        = "glue-salesforce-secret-access"
  description = "Allow Glue job to access Salesforce credentials from Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = [
        "secretsmanager:GetSecretValue"
      ],
      Resource = data.aws_secretsmanager_secret.salesforce_secret.arn
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach_salesforce_secret_access" {
  role       = aws_iam_role.glue_role.name
  policy_arn = aws_iam_policy.salesforce_secret_access.arn
}
