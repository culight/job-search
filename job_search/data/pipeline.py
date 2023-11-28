"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Master pipeline which will combine relevant jobs
DEVELOPER NOTES: 
"""

import logging

# from .extract import extraction_pipeline
import apache_beam as beam
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import PipelineOptions

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# ==============================================================================


def build_pipeline(argv):
    # extraction_pipeline.run(argv)
    with beam.Pipeline(options=PipelineOptions(argv)) as pipeline:
        pass
        # # Read in the data
        # df = pipeline | "Read CSV" >> beam.io.ReadFromText("data/extract/extracted_jobs.csv")

        # # Convert to a PCollection
        # pcoll = to_pcollection(df)

        # # Write the PCollection to a file
        # pcoll | "Write CSV" >> beam.io.WriteToText("data/transform/transformed_jobs.csv")


if __name__ == "__main__":
    import sys

    build_pipeline(sys.argv[1:])
