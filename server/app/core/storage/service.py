from app.core.storage.config import storage_settings
from app.core.storage.s3 import get_s3_client


class StorageService:
    def __init__(self):
        self.client = get_s3_client()
        self.bucket = storage_settings.S3_BUCKET_NAME

    def upload_file(
        self, file_path: str, object_key: str, content_type: str | None = None
    ) -> None:
        extra_args = {}

        if content_type:
            extra_args["ContentType"] = content_type

        self.client.upload_file(
            Filename=file_path,
            Bucket=self.bucket,
            Key=object_key,
            ExtraArgs=extra_args or None,
        )

    def download_file(
        self,
        object_key: str,
        destination_path: str,
    ) -> None:
        self.client.download_file(
            Bucket=self.bucket, Key=object_key, Filename=destination_path
        )

    def delete_file(self, object_key: str):

        self.client.delete_object(Bucket=self.bucket, Key=object_key)
