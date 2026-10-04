import boto3

from app.core.storage.config import storage_settings


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=storage_settings.S3_ENDPOINT_URL,
        region_name=storage_settings.S3_REGION,
        aws_access_key_id=storage_settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=storage_settings.AWS_SECRET_ACCESS_KEY,
    )
