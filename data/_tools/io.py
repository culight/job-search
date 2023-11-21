"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Ingests job postings from various job boards using crawler
DEVELOPER NOTES: 
"""

import logging
import os

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
        LOGGER.info(f"File {source_file_name} uploaded to {destination_blob_name}.")

    def download_blob(self, source_blob_name, destination_file_name):
        bucket = self.get_bucket()
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        LOGGER.info(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

    def upload_dir(self, source_dir_name, destination_dir_name):
        bucket = self.get_bucket()
        for file in os.listdir(source_dir_name):
            blob = bucket.blob(destination_dir_name + "/" + file)
            blob.upload_from_filename(source_dir_name + "/" + file)
            LOGGER.info(f"File {file} uploaded to {destination_dir_name}.")
