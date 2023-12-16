"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Master pipeline which will combine relevant jobs
DEVELOPER NOTES: 
"""

import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# ==============================================================================

jobs_schema = {
    "fields": [
        {"name": "job_url", "type": "STRING", "mode": "NULLABLE"},
        {"name": "site", "type": "STRING", "mode": "NULLABLE"},
        {"name": "title", "type": "STRING", "mode": "NULLABLE"},
        {"name": "company", "type": "STRING", "mode": "NULLABLE"},
        {"name": "company_url", "type": "STRING", "mode": "NULLABLE"},
        {"name": "location", "type": "STRING", "mode": "NULLABLE"},
        {"name": "job_type", "type": "STRING", "mode": "NULLABLE"},
        {"name": "date_posted", "type": "STRING", "mode": "NULLABLE"},
        {"name": "interval", "type": "STRING", "mode": "NULLABLE"},
        {"name": "min_amount", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "max_amount", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "currency", "type": "STRING", "mode": "NULLABLE"},
        {"name": "is_remote", "type": "BOOL", "mode": "NULLABLE"},
        {"name": "num_urgent_words", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "benefits", "type": "STRING", "mode": "NULLABLE"},
        {"name": "emails", "type": "STRING", "mode": "NULLABLE"},
        {"name": "description", "type": "STRING", "mode": "NULLABLE"},
    ]
}


def build_pipeline(argv):
    with beam.Pipeline(options=PipelineOptions(argv)) as pipeline:
        # Read in the data
        jobs_raw = pipeline | "Read CSV" >> beam.io.ReadFromText(
            "gs://dataflow-jobsearch-bucket/jobs/gcp/glassdoor_0-100.csv"
        )

        LOGGER.debug(f"jobs_raw: {jobs_raw}")

        jobs_raw | "Write to BQ" >> beam.io.WriteToBigQuery(
            dataset="job_search",
            table="raw_jobs",
            project="gcp-practice-325719",
            schema=jobs_schema,
        )


if __name__ == "__main__":
    import sys

    build_pipeline(sys.argv[1:])
