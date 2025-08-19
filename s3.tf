resource "aws_s3_bucket" "salesforce_data" {
  bucket = var.s3_bucket_name_salesforce
}

resource "aws_s3_bucket" "glue_scripts" {
  bucket = var.s3_bucket_name_scripts
}

resource "aws_s3_object" "glue_script" {
  bucket = aws_s3_bucket.glue_scripts.id
  key    = basename(var.glue_script_key)
  source = var.glue_script_key
  etag   = filemd5(var.glue_script_key)
}

resource "aws_s3_object" "glue_script_config" {
  bucket = aws_s3_bucket.glue_scripts.id
  key    = basename(var.glue_script_config_key)
  source = var.glue_script_config_key
  etag   = filemd5(var.glue_script_config_key)
}
