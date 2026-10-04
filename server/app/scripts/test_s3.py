from app.core.storage.s3 import get_s3_client
from app.core.storage.config import storage_settings

s3 = get_s3_client()

response = s3.list_buckets()

for bucket in response["Buckets"]:
    print(bucket["Name"])

print("Configured bucket:", storage_settings.S3_BUCKET_NAME)
