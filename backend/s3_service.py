import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
)


def upload_resume(file_path: str, object_key: str) -> str:
    if not S3_BUCKET_NAME:
        raise RuntimeError("S3_BUCKET_NAME is not configured.")

    try:
        s3_client.upload_file(
            file_path,
            S3_BUCKET_NAME,
            object_key,
        )

        return object_key

    except (BotoCoreError, ClientError) as error:
        print(f"S3 upload failed: {error}")
        raise RuntimeError("Failed to upload resume to S3.") from error