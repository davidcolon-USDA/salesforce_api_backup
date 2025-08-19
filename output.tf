output "glue_job_name" {
  description = "The name of the AWS Glue job"
  value       = aws_glue_job.docker_salesforce_glue_job.name
}

output "glue_job_script_location" {
  description = "The S3 location of the Glue script"
  value       = aws_glue_job.docker_salesforce_glue_job.command[0].script_location
}

output "salesforce_secret_arn" {
  description = "The ARN of the Salesforce Secrets Manager secret"
  value       = data.aws_secretsmanager_secret.salesforce_secret.arn
}

output "salesforce_data_bucket" {
  description = "S3 bucket where Salesforce data is written"
  value       = var.s3_bucket_name_salesforce
}

output "glue_temp_dir" {
  description = "Temporary directory used by Glue for intermediate files"
  value       = "s3://${var.s3_bucket_name_salesforce}/temp/"
}
