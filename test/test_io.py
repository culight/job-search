"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Test Input/Output components
DEVELOPER NOTES: 
"""

import logging

import pytest

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# bring io files into workig directory
import sys


# ==============================================================================


def test_gcs_client():
    # sys.path.append("../data/tools/io/GCSClient.py")
    from job_search.data._tools.io import GCSClient

    gcs_client = GCSClient(bucket_name="test", project_id="test")
    # assert gcs_client.bucket_name == "test"
    # assert gcs_client.project_id == "test"
    # assert gcs_client.client.project == "test"
    # assert gcs_client.get_bucket().name == "test"
    # assert gcs_client.get_bucket().exists() == True

    # with pytest.raises(Exception):
    #     gcs_client.upload_blob("test", "test")
    #     gcs_client.download_blob("test", "test")
    #     gcs_client.upload_dir("test", "test")
