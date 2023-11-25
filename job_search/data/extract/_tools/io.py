"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Ingests job postings from various job boards using crawler
DEVELOPER NOTES: 
"""

import logging
import os
import requests

# from google.cloud import bigquery
from google.cloud import storage

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# ==============================================================================


class RESTClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint: str, params: dict = None) -> dict:
        """
        Makes a GET request to the specified endpoint

        Args:
            endpoint (str): Endpoint to make GET request to
            params (dict, optional): Parameters to pass to GET request. Defaults to None.

        Returns:
            dict: JSON response from GET request
        """
        response = requests.get(self.base_url + endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict = None) -> dict:
        """
        Makes a POST request to the specified endpoint

        Args:
            endpoint (str): Endpoint to make POST request to
            data (dict, optional): Data to pass to POST request. Defaults to None.

        Returns:
            dict: JSON response from POST request
        """
        response = requests.post(self.base_url + endpoint, data=data)
        response.raise_for_status()
        return response.json()


class GCSClient:
    def __init__(self, bucket_name, project_id):
        self.bucket_name = bucket_name
        self.project_id = project_id
        self.client = storage.Client(project=self.project_id)

    def get_bucket(self) -> None:
        """
        Get bucket from GCS
        """
        return self.client.get_bucket(self.bucket_name)

    def upload_file(self, source_file_name: str, destination_file_name: str) -> None:
        """
        Upload local file to GCS

        Args:
            source_file_name (str): Local file path to upload.
            destination_file_name (str): Destination file path name.
        """
        bucket = self.get_bucket()
        blob = bucket.blob(destination_file_name)
        blob.upload_from_filename(source_file_name)
        LOGGER.info(f"File {source_file_name} uploaded to {destination_file_name}.")

    def download_file(self, source_file_name: str, destination_file_name: str) -> None:
        """
        Download file from GCS to local

        Args:
            source_file_name (str): GCS file path to download.
            destination_file_name (str): Local file path name.
        """
        bucket = self.get_bucket()
        blob = bucket.blob(source_file_name)
        blob.download_to_filename(destination_file_name)
        LOGGER.info(f"Blob {source_file_name} downloaded to {destination_file_name}.")

    def upload_dir(self, source_dir_name: str, destination_dir_name: str) -> None:
        """
        Upload local directory to GCS

        Args:
            source_dir_name (str): Local directory path to upload.
            destination_dir_name (str): Destination directory path name.
        """
        bucket = self.get_bucket()
        for file in os.listdir(source_dir_name):
            blob = bucket.blob(destination_dir_name + "/" + file)
            blob.upload_from_filename(source_dir_name + "/" + file)
            LOGGER.info(f"File {file} uploaded to {destination_dir_name}.")

    def download_dir(self, source_dir_name: str, destination_dir_name: str) -> None:
        """
        Download directory from GCS to local

        Args:
            source_dir_name (str): GCS directory path to download.
            destination_dir_name (str): Local directory path name.
        """
        bucket = self.get_bucket()
        blobs = bucket.list_blobs(prefix=source_dir_name)
        for blob in blobs:
            blob.download_to_filename(destination_dir_name + "/" + blob.name)
            LOGGER.info(f"Blob {blob.name} downloaded to {destination_dir_name}.")


# class BigQueryClient:
#     def __init__(self, project_id):
#         self.project_id = project_id
#         self.client = bigquery.Client(project=self.project_id)

#     def get_table(self, dataset_name, table_name):
#         return self.client.get_table(f"{self.project_id}.{dataset_name}.{table_name}")

#     def create_table(self, dataset_name, table_name, schema):
#         dataset = bigquery.Dataset(f"{self.project_id}.{dataset_name}")
#         table = bigquery.Table(dataset.table(table_name), schema=schema)
#         table = self.client.create_table(table)
#         LOGGER.info(
#             f"Created table {table.project}.{table.dataset_id}.{table.table_id}"
#         )

#     def insert_rows(self, dataset_name, table_name, rows):
#         table = self.get_table(dataset_name, table_name)
#         errors = self.client.insert_rows(table, rows)
#         if errors == []:
#             LOGGER.info(f"New rows have been added.")
#         else:
#             LOGGER.error(f"Encountered errors while inserting rows: {errors}")
