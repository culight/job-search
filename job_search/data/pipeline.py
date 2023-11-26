"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Master pipeline which will combine relevant jobs
DEVELOPER NOTES: 
"""

import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.dataframe.convert import to_pcollection

from .extract import extraction_pipeline

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# ==============================================================================


def build_pipeline(argv):
    extraction_pipeline.run(argv)


if __name__ == "__main__":
    import sys
    build_pipeline(sys.argv[1:])
