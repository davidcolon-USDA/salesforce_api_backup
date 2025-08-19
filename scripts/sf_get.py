import os
import sys
import json
import logging
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from simple_salesforce import Salesforce
from awsglue.utils import getResolvedOptions
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Load Salesforce credentials from AWS Secrets Manager
def get_salesforce_credentials(secret_arn):
    client = boto3.client("secretsmanager")
    try:
        response = client.get_secret_value(SecretId=secret_arn)
        secret = json.loads(response["SecretString"])
        return {
            "username": secret["SF_USERNAME"],
            "password": secret["SF_PASSWORD"],
            "security_token": secret["SF_SECURITY_TOKEN"],
            "domain": secret["SF_DOMAIN"],
        }
    except ClientError as e:
        logger.error(f"Failed to retrieve secret: {e}")
        raise

# Read environment variables
args = getResolvedOptions(sys.argv, ["S3_DATA_BUCKET", "S3_SCRIPT_BUCKET", "SECRET_ARN", "QUERIES_FILE"])
SECRET_ARN = args["SECRET_ARN"]
S3_DATA_BUCKET = args["S3_DATA_BUCKET"]
S3_SCRIPT_BUCKET = args["S3_SCRIPT_BUCKET"]
QUERIES_FILE = args["QUERIES_FILE"]

# Init boto3 clients
s3 = boto3.client("s3")

# Retrieve Salesforce credentials
creds = get_salesforce_credentials(SECRET_ARN)
logger.info("Retrieved Salesforce credentials successfully")

# Connect to Salesforce
sf = Salesforce(
    username=creds["username"],
    password=creds["password"],
    security_token=creds["security_token"],
    domain=creds["domain"],
)

def sanitize_filename(name: str) -> str:
    """Make query names safe for use in S3 keys."""
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name)

def save_to_s3(records, query_name, chunk_number):
    safe_name = sanitize_filename(query_name)
    key = f"{safe_name}_chunk_{chunk_number:04d}.json"
    logger.info(f"Uploading {len(records)} records to s3://{S3_DATA_BUCKET}/{key}")
    s3.put_object(
        Bucket=S3_DATA_BUCKET, Key=key, Body=json.dumps(records, indent=2)
    )

def export_query_to_s3(query_name, query):
    logger.info(f"Running query '{query_name}': {query}")
    result = sf.query_all_iter(query)

    chunk = []
    chunk_size = 1000
    chunk_num = 1

    for record in result:
        chunk.append(record)
        if len(chunk) >= chunk_size:
            save_to_s3(chunk, query_name, chunk_num)
            chunk = []
            chunk_num += 1

    if chunk:
        save_to_s3(chunk, query_name, chunk_num)

    logger.info(f"Export complete for '{query_name}'. Total chunks: {chunk_num}")

def load_queries():
    # 1. Try local file first (works for local testing)
    if os.path.exists(QUERIES_FILE):
        logger.info(f"Loading queries from local file {QUERIES_FILE}")
        with open(QUERIES_FILE, "r") as f:
            return json.load(f)

    # 2. Otherwise assume it's an S3 key in the same bucket as scripts/config
    logger.info(f"Loading queries from s3://{S3_SCRIPT_BUCKET}/{QUERIES_FILE}")
    obj = s3.get_object(Bucket=S3_SCRIPT_BUCKET, Key=QUERIES_FILE)

    body = obj["Body"].read().decode("utf-8")
    # print(f"QUERIES_FILE: {QUERIES_FILE}")  # DEBUG
    # print("First 200 chars of queries.json:\n", body[:200])  # DEBUG

    # return json.loads(obj["Body"].read())
    return json.loads(body)

if __name__ == "__main__":
    logger.info(f"Started at {datetime.utcnow().isoformat()}")

    # print("Files in /tmp:", os.listdir("/tmp")) # DEBUG

    try:
        queries = load_queries()

        if not isinstance(queries, dict):
            raise ValueError("queries.json must be a JSON object with {query_name: query}")

        for name, query in queries.items():
            export_query_to_s3(name, query)

    except Exception as e:
        logger.exception("Unhandled exception during export.")

    logger.info(f"Finished at {datetime.utcnow().isoformat()}")
