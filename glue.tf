resource "aws_cloudwatch_log_group" "glue_job_logs" {
  name              = "/aws-glue/jobs/${var.glue_job_name}"
  retention_in_days = 14
}

resource "aws_glue_job" "docker_salesforce_glue_job" {
  name              = var.glue_job_name
  role_arn = aws_iam_role.glue_role.arn
# glue_version      = "5.0"
  max_capacity      = 1
  timeout           = 2880

  command {
    name            = "pythonshell"
    python_version  = "3.9"
    script_location = "s3://${aws_s3_bucket.glue_scripts.bucket}/${var.glue_script_name}"
  }

  execution_property {
    max_concurrent_runs = 1
  }

  default_arguments = {
    "--additional-python-modules"             = "simple-salesforce"
    "--enable-glue-datacatalog"               = "true"
    "--enable-continuous-cloudwatch-log"      = "true"
    "--TempDir"                               = "s3://${aws_s3_bucket.salesforce_data.bucket}/temp/"
    "--SECRET_ARN"                            = data.aws_secretsmanager_secret.salesforce_secret.arn
    "--S3_DATA_BUCKET"                        = aws_s3_bucket.salesforce_data.id
    "--S3_SCRIPT_BUCKET"                      = aws_s3_bucket.glue_scripts.id
    "--QUERIES_FILE"                          = var.glue_script_config_name
  }

  connections     = []
  execution_class = "STANDARD"
  depends_on      = [aws_s3_object.glue_script]
}
