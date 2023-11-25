"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Extracts job postings from various job boards using crawler
DEVELOPER NOTES: 
"""

import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.dataframe.convert import to_pcollection

from extract_raw_jobs import extract_jobs_scrape

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# ==============================================================================


def run(argv=None):
    """Main entry point"""

    pipeline_options = PipelineOptions(argv)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "Extract Jobs"
            >> beam.Map(
                extract_jobs_scrape,
                site_name="linkedin",
                search_term="data engineer",
                location="united states",
                results_wanted=10,
            )
            | "Write to CSV"
            >> beam.io.WriteToText("gs://dataflow-jobsearch-bucket/job_results.output")
        )
