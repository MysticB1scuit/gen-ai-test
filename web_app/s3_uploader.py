import boto3
import os

from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_to_s3(file_path, s3_key=None):
    """Uploads a local file to the configured S3 bucket."""
    try:
        if s3_key is None:
            s3_key = os.path.basename(file_path)

        s3.upload_file(file_path, AWS_BUCKET_NAME, s3_key)
        print(f"Uploaded {file_path} to S3://{AWS_BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {e}")
