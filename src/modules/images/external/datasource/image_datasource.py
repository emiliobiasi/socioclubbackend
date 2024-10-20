from google.cloud import storage
from datetime import timedelta


class ImageDatasource:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def generate_signed_url(self, file_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="PUT",
            content_type="application/octet-stream",
        )

        return url
