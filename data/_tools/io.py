"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Ingests job postings from various job boards using crawler
DEVELOPER NOTES: 
"""

import logging

from google.cloud import storage

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# ==============================================================================


class GCSClient:
    def __init__(self, bucket_name, project_id):
        self.bucket_name = bucket_name
        self.project_id = project_id
        self.client = storage.Client(project=self.project_id)

    def get_bucket(self):
        return self.client.get_bucket(self.bucket_name)

    def upload_blob(self, source_file_name, destination_blob_name):
        bucket = self.get_bucket()
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(f"File {source_file_name} uploaded to {destination_blob_name}.")

    def download_blob(self, source_blob_name, destination_file_name):
        bucket = self.get_bucket()
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")
