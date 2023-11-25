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

sys.path.insert(1, "../../job_search")
# ==============================================================================

BUCKET = "dataflow-jobsearch-bucket"
PROJECT_ID = "gcp-practice"


def test_gcs_client():
    # sys.path.append("../data/tools/io/GCSClient.py")
    from job_search.data._tools.io import GCSClient

    gcs_client = GCSClient(bucket_name=BUCKET, project_id=PROJECT_ID)

    assert gcs_client != None, "GCSClient is not valid"
    assert gcs_client.bucket_name == BUCKET, "GCSClient bucket name is not valid"
    assert gcs_client.project_id == PROJECT_ID, "GCSClient project id is not valid"
