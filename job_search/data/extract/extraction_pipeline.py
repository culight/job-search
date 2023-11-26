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
from jobspy import scrape_jobs

VALID_SOURCES = ("indeed", "linkedin", "zip_recruiter", "glassdoor")

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# ==============================================================================


def extract_jobs_scrape(
    site_name: str,
    search_term: str,
    location: str,
    results_wanted: int,
    country_indeed: str = "USA",
    country_glassdoor: str = "USA",
) -> list:
    """Scrapes job postings from various job boards

    Args:
        site_name (str): Name of job board to scrape from
        search_term (str): Job title to search for
        location (str): Location to search for
        results_wanted (int): Number of results to scrape
        country_indeed (str, optional): Country to search for on Indeed. Defaults to "USA".
        country_glassdoor (str, optional): Country to search for on Glassdoor. Defaults to "USA".

    Returns:
        list: List of dictionaries containing job postings
    """

    if site_name not in VALID_SOURCES:
        raise ValueError(f"Invalid site_name: {site_name}")

    if site_name == "indeed":
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            country_indeed=country_indeed,
        )

    elif site_name == "linkedin":
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
        )

    elif site_name == "zip_recruiter":
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
        )

    elif site_name == "glassdoor":
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            country=country_glassdoor,
        )

    return jobs


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
